from pathlib import Path
import os,re,hashlib,yaml
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'; DOCS_DATA=ROOT/'docs_data'; DOCS_ASSETS=ROOT/'docs_assets'
for p in (DATA,DOCS_DATA,DOCS_ASSETS): p.mkdir(exist_ok=True)
def env(n,d=None):
    if os.environ.get(n): return os.environ[n]
    for fn in ['.env','env.example']:
        p=ROOT/fn
        if p.exists():
            for line in p.read_text().splitlines():
                if '=' in line and not line.strip().startswith('#'):
                    k,v=line.split('=',1)
                    if k.strip()==n: return v.strip()
    return d
def log(m): print(f'[ai117] {m}')
def norm(s): return re.sub(r'[^a-z0-9]+',' ',str(s).lower()).strip()
def anon_id(v): return hashlib.sha256(f"{env('ANON_SALT','data117-fall-2026')}:{v}".encode()).hexdigest()[:8]
def resolve_columns(cols):
    spec=yaml.safe_load((ROOT/'schemas'/'columns.yml').read_text()); used={}; unm=[]
    for col in cols:
        cn=norm(col); found=None
        for key,cfg in spec.items():
            if any(norm(e)==cn for e in cfg.get('exact',[]) or []): found=key
            if not found:
                for pat in cfg.get('patterns',[]) or []:
                    if re.search(pat, cn): found=key; break
            if found: break
        if found and found not in used.values(): used[col]=found
        else: unm.append(col)
    return used,unm
