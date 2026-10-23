import unittest
from unittest.mock import patch, Mock
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from storage import CloudStore, StorageError, validate_backup, MemoryStore, export_records, RunStore
from domain import default_profile, seed_tasks
import requests


class CloudContractTests(unittest.TestCase):
    def setUp(self):
        self.store=CloudStore('https://project.supabase.co','publishable',{'access_token':'test-token','user':{'id':'user-a'}})
    @patch('storage.requests.get')
    def test_reads_paginate_and_scope_by_user(self,get):
        first=Mock(ok=True); first.json.return_value=[{'payload':{'id':str(i)}} for i in range(500)]
        last=Mock(ok=True); last.json.return_value=[{'payload':{'id':'last'}}]
        get.side_effect=[first,last]
        result=self.store.all('tasks')
        self.assertEqual(len(result),501)
        self.assertEqual(get.call_args.kwargs['params']['user_id'],'eq.user-a')
        self.assertEqual(get.call_args.kwargs['params']['offset'],500)
        self.assertEqual(get.call_args.kwargs['headers']['Authorization'],'Bearer test-token')
    @patch('storage.requests.request')
    def test_writes_scope_by_user_and_record(self,request):
        response=Mock(ok=True,content=b'[]'); response.json.return_value=[]; request.return_value=response
        self.store.put('tasks',{'id':'task-a','title':'Test'})
        self.assertEqual(request.call_args.kwargs['json']['user_id'],'user-a')
        self.assertEqual(request.call_args.kwargs['json']['id'],'task-a')
        self.store.delete('tasks','task-a')
        self.assertEqual(request.call_args.kwargs['params']['id'],'eq.task-a')
    @patch('storage.requests.get',side_effect=requests.ConnectionError())
    def test_network_failure_is_explicit(self,get):
        with self.assertRaises(StorageError): self.store.all('tasks')
    def test_backup_round_trip_and_validation(self):
        store=MemoryStore({})
        store.put('profile',default_profile())
        for t in seed_tasks(): store.put('tasks',t)
        data=export_records(store)
        self.assertEqual(validate_backup(data),4)
        data['collections']['tasks'][0]['minutes']=-1
        with self.assertRaises(ValueError): validate_backup(data)
    def test_cache_is_per_instance_and_invalidated(self):
        source=Mock(mode='cloud'); source.all.return_value=[]
        run=RunStore(source)
        run.all('tasks'); run.all('tasks'); self.assertEqual(source.all.call_count,1)
        run.put('tasks',{'id':'one'}); run.all('tasks'); self.assertEqual(source.all.call_count,2)
        RunStore(source).all('tasks'); self.assertEqual(source.all.call_count,3)

if __name__=='__main__': unittest.main()
