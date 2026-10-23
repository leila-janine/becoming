"""Wall-clock focus intervals; breaks never count as worked minutes."""
import math
import time
from domain import uid


def start_timer(title, minutes=25, short_break=5, long_break=15, every=4, pomodoro=True, stamp=None):
    stamp=time.time() if stamp is None else stamp
    return {'id':uid(),'title':title,'minutes':minutes,'short_break':short_break,
            'long_break':long_break,'every':every,'pomodoro':pomodoro,'phase':'Focus',
            'round':1,'duration':minutes*60,'end':stamp+minutes*60,'paused':False}


def remaining(timer, stamp=None):
    stamp=time.time() if stamp is None else stamp
    return max(0,math.ceil(timer.get('remaining',0) if timer.get('paused') else timer['end']-stamp))


def pause(timer, stamp=None):
    return {**timer,'remaining':remaining(timer,stamp),'paused':True}


def resume(timer, stamp=None):
    stamp=time.time() if stamp is None else stamp
    return {**timer,'end':stamp+remaining(timer,stamp),'paused':False}


def advance(timer, stamp=None):
    stamp=time.time() if stamp is None else stamp
    if timer['phase']=='Focus':
        is_long=timer['round']%timer['every']==0
        phase='Long break' if is_long else 'Short break'
        duration=60*timer['long_break' if is_long else 'short_break']
        round_number=timer['round']
    else:
        phase,duration,round_number='Focus',timer['minutes']*60,timer['round']+1
    return {**timer,'phase':phase,'round':round_number,'duration':duration,
            'end':stamp+duration,'remaining':duration,'paused':False}
