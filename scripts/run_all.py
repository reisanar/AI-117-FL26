import argparse,subprocess,sys
from common import ROOT,log
def run(s): log(f'run {s}'); return subprocess.call([sys.executable,str(ROOT/'scripts'/s)],cwd=ROOT)
ap=argparse.ArgumentParser(); ap.add_argument('--no-fetch',action='store_true'); args=ap.parse_args(); run('bootstrap_placeholders.py')
if not args.no_fetch:
    rc=run('00_fetch_responses.py')
    if rc: sys.exit(rc)
for s in ['01_preprocess.py','02_demographics.py','03_taste_map.py','04_match_tracks.py','05_render_snippets.py']:
    rc=run(s)
    if rc and s!='03_taste_map.py': sys.exit(rc)
