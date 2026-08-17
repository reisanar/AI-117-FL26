import json,re,random,pandas as pd,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter
from common import DATA,DOCS_ASSETS,DOCS_DATA,log
CLEAN=DATA/'clean.csv'; ACCENT='#4B9CD3'; NAVY='#13294B'; built={}
def ser(df,k):
    if k not in df: return None
    s=df[k].dropna().astype(str).str.strip(); s=s[s!='']; return s if len(s)>=3 else None
def loc(v):
    s=str(v).split(',')[-1].strip() if ',' in str(v) else str(v).strip(); return s.upper() if len(s)==2 else s.title()
def bg(v):
    s=str(v).lower();
    for n,p in [('Computer/Data/Information','computer|data|information|informatics|software'),('Math/Statistics','math|stat'),('Life/Health Sciences','bio|health|medicine|nursing|public health'),('Social Sciences','psych|soci|polit|policy|econom'),('Business','business|finance|account|marketing'),('Humanities/Arts','english|history|art|music|philos')]:
        if re.search(p,s): return n
    return 'Other'
def cloud(words,title,fname,cap):
    fig,ax=plt.subplots(figsize=(8,4.5)); ax.axis('off'); ax.set_title(title,color=NAVY); random.seed(7)
    for word,count in words.most_common(45): ax.text(random.random(),random.random(),word,fontsize=8+count*2.2,alpha=.76,color=NAVY if count%2 else ACCENT,transform=ax.transAxes)
    fig.tight_layout(); fig.savefig(DOCS_ASSETS/fname,bbox_inches='tight'); plt.close(fig); built[fname]=cap; log(f'chart -> {fname}')
def bar(counts,title,fname,cap):
    items=counts.most_common(15)[::-1]; labels=[x for x,y in items]; vals=[y for x,y in items]; fig,ax=plt.subplots(figsize=(7.5,max(2.5,.42*len(items)+1))); ax.barh(labels,vals,color=ACCENT); ax.set_xlabel('respondents'); ax.set_title(title,color=NAVY); fig.tight_layout(); fig.savefig(DOCS_ASSETS/fname,bbox_inches='tight'); plt.close(fig); built[fname]=cap; log(f'chart -> {fname}')
def freq(s):
    stop=set('the and for with this that about right now from into most want learn thing hope data ai artificial intelligence intelligence is are was were be being been a an to of in on by as or it its their they them we our us human humans machine machines computer computers system systems technology tool tools use uses using people person can could would should usually'.split()); c=Counter()
    for txt in s:
        for w in re.findall(r'[A-Za-z][A-Za-z-]{2,}', txt.lower()):
            if w not in stop: c[w.title()]+=1
    return c
df=pd.read_csv(CLEAN); summary={'n_participants':int(len(df))}
s=ser(df,'hometown')
if s is not None:
    c=Counter(loc(x) for x in s); cloud(c,'Places we call home','family_location_cloud.png','Places the cohort calls home'); summary['top_locations']=c.most_common(8)
s=ser(df,'background')
if s is not None:
    c=Counter(bg(x) for x in s); bar(c,'Undergraduate background grouped','background.png','Undergraduate background, grouped')
s=ser(df,'ai_definition')
if s is not None: cloud(freq(s),'How DATA 117 defines AI','ai_definition_cloud.png','Words from one-sentence AI definitions')
s=ser(df,'ai_interest')
if s is not None: cloud(freq(s),'What excites us about AI','ai_interest_cloud.png','AI interests in students own words')
if 'song_title' in df: summary['n_unique_songs']=int(df.song_title.astype(str).str.lower().nunique())
(DOCS_DATA/'summary.json').write_text(json.dumps(summary,indent=2)); (DOCS_DATA/'charts.json').write_text(json.dumps(built,indent=2)); log(f'built {len(built)} figures for {len(df)} participants')
