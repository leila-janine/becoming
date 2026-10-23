"""Local SQLite for a private local session; authenticated PostgREST for cloud."""
import json
import sqlite3
import time
import math
from datetime import date, datetime, time as daytime
from pathlib import Path
import requests

COLLECTIONS = {'profile','tasks','events','checkins','reflections','learning','evidence','transactions','budgets','sessions','practice','reviews','coding','jobs'}


class StorageError(Exception):
    pass


def valid(collection):
    if collection not in COLLECTIONS:
        raise StorageError('Unknown record collection.')


class RunStore:
    """Cache reads within one script run only, never across users or interactions."""
    def __init__(self, inner):
        self.inner, self.mode, self.cache = inner, inner.mode, {}

    def all(self, collection):
        if collection not in self.cache:
            self.cache[collection]=self.inner.all(collection)
        return self.cache[collection]

    def put(self, collection, row):
        self.inner.put(collection,row)
        self.cache.pop(collection,None)

    def delete(self, collection, record_id):
        self.inner.delete(collection,record_id)
        self.cache.pop(collection,None)


def validate_backup(data):
    """Validate an entire import before changing any records."""
    if not isinstance(data,dict) or data.get('format')!='becoming-v1' or not isinstance(data.get('collections'),dict):
        raise ValueError('Unrecognized backup format.')
    required={
        'profile':{'name':str,'role':str,'target_role':str,'workdays':list,'work_start':str,'work_end':str,'wake':str,'sleep':str,'buffer':int},
        'tasks':{'title':str,'next':str,'area':str,'minutes':int,'priority':int,'done':bool},
        'events':{'title':str,'date':str,'start':str,'end':str},
        'checkins':{'energy':int,'minutes':int},
        'reflections':{'date':str,'win':str,'obstacle':str,'kindness':str,'tomorrow':str},
        'learning':{'kind':str,'title':str},
        'evidence':{'date':str,'title':str,'situation':str,'action':str,'result':str,'url':str},
        'transactions':{'date':str,'title':str,'type':str,'category':str,'amount':(int,float)},
        'budgets':{k:(int,float) for k in ['income','needs','joy','buffer','learning','emergency','investing']},
        'sessions':{'date':str,'minutes':int,'title':str},
        'practice':{'date':str,'exercise':str,'draft':str,'level':str,'participated':bool,'clarity':int,'takeaway':str},
        'reviews':{'date':str,'answers':list},
        'coding':{'date':str,'kind':str},
        'jobs':{'title':str,'employer':str,'role':str,'location':str,'url':str,'experience':str,'requirements':list,'checked_on':str,'status':str},
    }
    count=0
    for collection,rows in data['collections'].items():
        valid(collection)
        if not isinstance(rows,list): raise ValueError('Invalid collection list.')
        ids=set()
        for row in rows:
            if not isinstance(row,dict) or not isinstance(row.get('id'),str) or not row['id'] or len(row['id'])>200:
                raise ValueError('Each record needs a nonempty text ID.')
            if row['id'] in ids: raise ValueError('Duplicate record ID.')
            ids.add(row['id'])
            for key,kind in required[collection].items():
                if key not in row or not isinstance(row[key],kind): raise ValueError(f'Invalid {collection} field: {key}.')
                if isinstance(row[key],(int,float)) and not math.isfinite(row[key]): raise ValueError('Non-finite number in backup.')
            for key in ['date','due','not_before']:
                if row.get(key): date.fromisoformat(row[key])
            for key in ['start','end','work_start','work_end','wake','sleep']:
                if row.get(key): daytime.fromisoformat(row[key])
            if collection=='tasks':
                if 'status' in row and row['status'] not in ['New','Ongoing','Completed']: raise ValueError('Invalid task status.')
                if row['area'] not in ['Life admin','Graduation','Career','Learning','Voice & confidence','Wellbeing'] or not 5<=row['minutes']<=480 or row['priority'] not in [1,2,3]: raise ValueError('Invalid task values.')
                if row.get('window'):
                    if not isinstance(row['window'],list) or len(row['window'])!=2: raise ValueError('Invalid time window.')
                    a,b=[daytime.fromisoformat(v) for v in row['window']]
                    if a>=b: raise ValueError('Invalid time window order.')
            if collection=='profile':
                if 'routine' in row:
                    from domain import validate_schedule
                    validate_schedule(row['routine'])
                if row['id']!='main' or not set(row['workdays']) <= {'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'} or not 0<=row['buffer']<=30: raise ValueError('Invalid profile.')
                if daytime.fromisoformat(row['work_start'])>=daytime.fromisoformat(row['work_end']) or daytime.fromisoformat(row['wake'])>=daytime.fromisoformat(row['sleep']): raise ValueError('Invalid daily rhythm.')
            if collection=='checkins' and (not 1<=row['energy']<=5 or not 0<=row['minutes']<=240): raise ValueError('Invalid daily capacity.')
            if collection=='checkins' and 'schedule' in row:
                from domain import validate_schedule
                validate_schedule(row['schedule'])
            if collection=='learning':
                if row['kind']=='goal':
                    if row.get('status') not in ['Considering','Studying','Scheduled','Earned / completed']: raise ValueError('Invalid learning status.')
                elif row['kind']=='card':
                    if not isinstance(row.get('answer'),str) or not isinstance(row.get('interval'),int) or not row.get('due'): raise ValueError('Invalid recall card.')
                else: raise ValueError('Invalid learning kind.')
            if collection=='jobs':
                date.fromisoformat(row['checked_on'])
                if row['role'] not in ['AI Engineer','Data Engineer','Data Analytics','Software Engineering'] or not all(isinstance(x,str) for x in row['requirements']): raise ValueError('Invalid opportunity fields.')
                if not isinstance(row.get('evidence_map',{}),dict): raise ValueError('Invalid evidence mapping.')
                if any(not isinstance(v,dict) or not isinstance(v.get('kind'),str) or not isinstance(v.get('detail'),str) for v in row.get('evidence_map',{}).values()): raise ValueError('Invalid evidence mapping entries.')
            if collection=='coding':
                if row['kind']=='attempt':
                    fields={'challenge_id':str,'title':str,'track':str,'minutes':int,'approach':str,'code':str,'assistance':str,'test_status':str,'lesson':str,'review_on':str,'logged_at':str}
                    if any(not isinstance(row.get(k),typ) for k,typ in fields.items()): raise ValueError('Invalid coding attempt.')
                    date.fromisoformat(row['review_on'])
                    if not 1<=row['minutes']<=240: raise ValueError('Invalid coding duration.')
                elif row['kind']=='debug':
                    if any(not isinstance(row.get(k),str) for k in ['title','expected','actual','cause','fix','regression']): raise ValueError('Invalid debugging entry.')
                else: raise ValueError('Invalid coding record kind.')
            if collection=='reviews' and (len(row['answers'])!=5 or not all(isinstance(a,str) for a in row['answers'])): raise ValueError('Invalid weekly answers.')
            if collection=='budgets':
                datetime.strptime(row['id'],'%Y-%m')
                if any(row[k]<0 for k in required['budgets']): raise ValueError('Budget amounts cannot be negative.')
                for k in ['current_emergency','emergency_target']:
                    if k in row and (not isinstance(row[k],(int,float)) or not math.isfinite(row[k]) or row[k]<0): raise ValueError('Invalid emergency reserve.')
                if row.get('emergency_target',1)<=0: raise ValueError('Savings milestone must be positive.')
            if collection in ['checkins','reflections','reviews']: date.fromisoformat(row['id'])
            if collection=='transactions' and (row['amount']<=0 or row['type'] not in ['Expense','Income','Savings transfer','Investment transfer']): raise ValueError('Invalid transaction.')
            if collection=='sessions' and not 1<=row['minutes']<=480: raise ValueError('Invalid focus duration.')
            if collection=='practice' and not 1<=row['clarity']<=5: raise ValueError('Invalid clarity rating.')
            if collection=='events' and daytime.fromisoformat(row['start'])>=daytime.fromisoformat(row['end']): raise ValueError('Invalid commitment times.')
            count+=1
    if count>10000: raise ValueError('Backup is too large.')
    return count


class LocalStore:
    mode = 'local'
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.execute('CREATE TABLE IF NOT EXISTS records (collection TEXT, id TEXT, payload TEXT NOT NULL, PRIMARY KEY(collection,id))')

    def connect(self):
        return sqlite3.connect(self.path, timeout=15)

    def all(self, collection):
        valid(collection)
        with self.connect() as db:
            return [json.loads(row[0]) for row in db.execute('SELECT payload FROM records WHERE collection=? ORDER BY id', (collection,))]

    def put(self, collection, row):
        valid(collection)
        with self.connect() as db:
            db.execute('INSERT INTO records VALUES (?,?,?) ON CONFLICT(collection,id) DO UPDATE SET payload=excluded.payload', (collection, row['id'], json.dumps(row)))

    def delete(self, collection, record_id):
        valid(collection)
        with self.connect() as db:
            db.execute('DELETE FROM records WHERE collection=? AND id=?', (collection, record_id))


class MemoryStore:
    mode = 'demo'
    def __init__(self, records):
        self.records = records

    def all(self, collection):
        valid(collection)
        return list(self.records.get(collection, {}).values())

    def put(self, collection, row):
        valid(collection)
        self.records.setdefault(collection, {})[row['id']] = dict(row)

    def delete(self, collection, record_id):
        valid(collection)
        self.records.get(collection, {}).pop(record_id, None)


def auth_request(url, key, payload, grant='password'):
    try:
        response = requests.post(url.rstrip('/') + '/auth/v1/token', params={'grant_type': grant}, headers={'apikey':key}, json=payload, timeout=15)
        if response.status_code != 200:
            raise StorageError('Sign-in failed. Check your email and password or try again later.')
        data = response.json()
        data['expires_at'] = time.time() + data.get('expires_in', 3600)
        return data
    except (requests.RequestException, ValueError) as exc:
        raise StorageError('Unable to reach sign-in. Your saved data has not been changed.') from exc


class CloudStore:
    mode = 'cloud'
    def __init__(self, url, key, session):
        self.url, self.key, self.session = url.rstrip('/'), key, session
        self.user_id = session['user']['id']

    def call(self, method, collection, record_id=None, row=None):
        valid(collection)
        headers = {'apikey': self.key, 'Authorization': 'Bearer '+self.session['access_token'], 'Prefer':'return=representation'}
        params = {'user_id': 'eq.'+self.user_id, 'collection':'eq.'+collection}
        body = None
        if record_id:
            params['id'] = 'eq.' + record_id
        if row is not None:
            body = {'user_id':self.user_id, 'collection':collection, 'id':row['id'], 'payload':row}
            params['on_conflict'] = 'user_id,collection,id'
            headers['Prefer'] = 'resolution=merge-duplicates,return=representation'
        try:
            response = requests.request(method, self.url+'/rest/v1/becoming_records', headers=headers, params=params, json=body, timeout=15)
            if not response.ok:
                raise StorageError('Could not sync. Check your connection, sign-in, and database setup. No local fallback was used.')
            return response.json() if response.content else []
        except (requests.RequestException, ValueError) as exc:
            raise StorageError('Sync is unavailable. Try again when connected.') from exc

    def all(self, collection):
        # PostgREST defaults to 1000 rows; paginate so historical records are not silently lost.
        valid(collection)
        rows, offset = [], 0
        while True:
            try:
                response = requests.get(self.url+'/rest/v1/becoming_records', headers={'apikey':self.key,'Authorization':'Bearer '+self.session['access_token']}, params={'user_id':'eq.'+self.user_id,'collection':'eq.'+collection,'select':'payload','order':'id.asc','offset':offset,'limit':500}, timeout=15)
                if not response.ok:
                    raise StorageError('Could not load your records. Check your connection and database setup.')
                batch = response.json()
                rows.extend(r['payload'] for r in batch)
                if len(batch) < 500:
                    return rows
                offset += 500
            except (requests.RequestException, ValueError, KeyError) as exc:
                raise StorageError('Could not load your records. Please retry.') from exc

    def put(self, collection, row):
        self.call('POST', collection, row=row)

    def delete(self, collection, record_id):
        self.call('DELETE', collection, record_id=record_id)


def get_record(store, collection, record_id, fallback=None):
    return next((x for x in store.all(collection) if x['id'] == record_id), fallback)


def export_records(store):
    return {'format':'becoming-v1', 'collections':{k:store.all(k) for k in sorted(COLLECTIONS)}}
