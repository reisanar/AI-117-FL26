import sys,pandas as pd
from common import DATA,DOCS_DATA,anon_id,log,resolve_columns
RAW=DATA/'raw_responses.csv'; CLEAN=DATA/'clean.csv'; PUB=DOCS_DATA/'responses_anon.csv'
if not RAW.exists(): sys.exit(1)
df=pd.read_csv(RAW); m,u=resolve_columns(list(df.columns)); df=df.rename(columns=m); log(f"mapped {len(m)} columns: {sorted(set(m.values()))}")
key='email' if 'email' in df else ('timestamp' if 'timestamp' in df else df.columns[0]); df['participant_id']=[anon_id(v) for v in df[key]]
for k in ('ai_definition','ai_interest','goals','taste_text','song_title','song_artist','background','hometown'):
    if k in df: df[k]=df[k].fillna('').astype(str).str.strip()
if {'song_title','song_artist'}<=set(df.columns): df=df[(df.song_title!='')&(df.song_artist!='')]
df.to_csv(CLEAN,index=False); df.drop(columns=[c for c in ['email','display_name'] if c in df.columns]).to_csv(PUB,index=False); log(f'wrote {CLEAN} and {PUB} ({len(df)} participants)')
