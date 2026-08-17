import sys
from common import resolve_columns,log
from importlib.machinery import SourceFileLoader
fetch=SourceFileLoader('fetch','scripts/00_fetch_responses.py').load_module()
df=None
try: df=fetch.fetch_public_sheet()
except Exception as e: log(f'live sheet unavailable: {e}')
if df is None: df=fetch.fetch_local()
if df is None: sys.exit(1)
m,u=resolve_columns(list(df.columns)); print(f'{len(df)} rows, {len(df.columns)} columns'); print('='*78); print(f"{'INTERNAL KEY':<20} FORM QUESTION"); print('-'*78)
for c,k in m.items(): print(f'{k:<20} {c}')
if u: print('\nUnmapped columns:'); [print(f'- {x}') for x in u]
