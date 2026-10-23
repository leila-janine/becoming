"""Browser-only Python/SQLite execution. Submitted code is never executed here."""
from pathlib import Path
from streamlit.components.v1 import declare_component

COMPONENT_PATH=Path(__file__).parent/'components'/'coding_runner'
# Register the static frontend on startup; it contains no account data.
declare_component('browser_runner',path=COMPONENT_PATH)

def runner_config(challenge, draft=None):
    if challenge['extension'] not in ['py','sql']:
        return None
    return {'challengeId':challenge['id'],'language':'sql' if challenge['extension']=='sql' else 'python',
            'starter':challenge['starter'],'code':draft if isinstance(draft,str) else challenge['starter'],
            'checks':challenge.get('checks',''),'setup':challenge.get('setup',''),
            'expected':[[1,'Aya',3500],[2,'Mika',0],[3,'Lea',500]] if challenge['id']=='sql-zero' else None}


def editor(challenge,draft=None):
    config=runner_config(challenge,draft)
    if config is None: return None
    # Register inside the script context, including when AppTest reruns the app.
    component=declare_component('browser_runner',path=COMPONENT_PATH)
    return component(**config,key='browser_editor_'+challenge['id'],default=None)


def validate_editor_result(result):
    if not isinstance(result,dict): return None
    if not isinstance(result.get('code'),str) or len(result['code'])>30000: return None
    if not isinstance(result.get('revision'),str) or len(result['revision'])>100: return None
    if result.get('status') not in ['draft','ran','passed','failed','stopped']: return None
    return {k:result[k] for k in ['code','revision','status']}
