import pandas as pd,urllib.parse,json
from common import DATA,DOCS_DATA,log
CLEAN=DATA/'clean.csv'; COORDS=DOCS_DATA/'taste_coords.csv'
def sp(t,a): return 'https://open.spotify.com/search/'+urllib.parse.quote(f'{t} {a}')
def yt(t,a): return 'https://www.youtube.com/results?search_query='+urllib.parse.quote(f'{t} {a}')
df=pd.read_csv(CLEAN)
if COORDS.exists():
    try: df=df.merge(pd.read_csv(COORDS)[['participant_id','pc1','neighborhood']],on='participant_id',how='left').sort_values(['neighborhood','pc1'],na_position='last')
    except Exception: pass
rows=[]
for pos,r in enumerate(df.itertuples(),1):
    t=getattr(r,'song_title',''); a=getattr(r,'song_artist',''); rows.append({'position':pos,'participant_id':r.participant_id,'requested_title':t,'requested_artist':a,'matched_title':t,'matched_artist':a,'album':'','apple_url':'','preview_url':'','artwork':'','spotify_search_url':sp(t,a),'youtube_search_url':yt(t,a)})
tracks=pd.DataFrame(rows); tracks.to_csv(DOCS_DATA/'playlist_tracks.csv',index=False); tracks[['matched_title','matched_artist','album']].rename(columns={'matched_title':'Title','matched_artist':'Artist','album':'Album'}).to_csv(DOCS_DATA/'playlist_import.csv',index=False); (DOCS_DATA/'playlist.txt').write_text('\n'.join(f'{x.matched_title} - {x.matched_artist}' for x in tracks.itertuples())); (DOCS_DATA/'match_summary.json').write_text(json.dumps({'total':len(tracks),'matched':0,'unmatched':len(tracks)},indent=2)); log(f'wrote {len(tracks)} playlist entries')
