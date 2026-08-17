import re,sys,pandas as pd,requests
from io import StringIO
from pathlib import Path
from common import DATA,env,log
RAW=DATA/'raw_responses.csv'
def sid(s):
    m=re.search(r'/d/([A-Za-z0-9_-]+)',s or ''); return m.group(1) if m else (s or '')
def fetch_public_sheet():
    id=sid(env('GOOGLE_SHEET_ID','') or ''); gid=env('GOOGLE_SHEET_GID','') or '0'
    if not id: return None
    r=requests.get(f'https://docs.google.com/spreadsheets/d/{id}/export?format=csv&gid={gid}',timeout=30)
    if not r.ok or 'Sign in' in r.text[:500]: raise RuntimeError('Could not read sheet. Share as Anyone with the link = Viewer.')
    return pd.read_csv(StringIO(r.text))
def fetch_csv():
    u=env('FORM_CSV_URL',''); return pd.read_csv(u) if u else None
def fetch_local():
    p=Path(env('LOCAL_CSV','data/raw_responses.csv') or 'data/raw_responses.csv'); return pd.read_csv(p) if p.exists() else None
for label,fn in [('link-shared sheet',fetch_public_sheet),('published CSV',fetch_csv),('local file',fetch_local)]:
    try: df=fn()
    except Exception as e: log(f'{label} unavailable: {str(e).splitlines()[0]}'); continue
    if df is not None: df.to_csv(RAW,index=False); log(f'fetched {len(df)} rows from {label}'); sys.exit(0)
log('no response source configured'); sys.exit(1)
