from __future__ import annotations
import json, sys
from collections import Counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np, pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from common import DATA, DOCS_ASSETS, DOCS_DATA, log
CLEAN=DATA/'clean.csv'; NAVY='#13294B'; ACCENT='#4B9CD3'
STOP=list(set('music song songs listen listening like love feel feels feeling makes make making really kind stuff lot bit just pretty track sound sounds always every time way thing things me my the a an and or but to of in on for with from it is this that'.split()))

def placeholder(msg):
    fig, ax=plt.subplots(figsize=(7,4)); ax.axis('off'); ax.text(.5,.5,msg,ha='center',va='center',fontsize=14,color=NAVY); fig.savefig(DOCS_ASSETS/'taste_map.png',bbox_inches='tight'); plt.close(fig)
    (DOCS_ASSETS/'taste_map.html').write_text(f'<html><body><p>{msg}</p></body></html>')
    (DOCS_DATA/'taste_coords.csv').write_text('participant_id,pc1,pc2,neighborhood,neighborhood_label\n')
    (DOCS_DATA/'neighbors.csv').write_text('participant_id,neighbor_id,similarity\n')
    (DOCS_DATA/'taste_terms.json').write_text('{}')
    (DOCS_ASSETS/'pc_loadings.png').write_text('')

def main():
    if not CLEAN.exists(): placeholder('No data yet.'); return 1
    df=pd.read_csv(CLEAN)
    if 'taste_text' not in df or len(df)<4:
        placeholder(f'Only {len(df)} responses so far; need at least 4 for a map.'); return 0
    docs=df['taste_text'].fillna('').astype(str).str.lower()
    docs=docs[docs.str.strip()!='']; df=df.loc[docs.index].copy()
    if len(docs)<4: placeholder('Need at least 4 text responses for a map.'); return 0
    X=None; vec=None
    for md in (2,1):
        try:
            vec=TfidfVectorizer(stop_words=STOP, ngram_range=(1,2), min_df=md, max_df=.95, sublinear_tf=True)
            X=vec.fit_transform(docs)
            if X.shape[1]>=2: break
        except ValueError:
            X=None
    if X is None or X.shape[1]<2: placeholder('Not enough shared vocabulary yet.'); return 0
    dense=X.toarray(); n_comp=min(5, dense.shape[0]-1, dense.shape[1])
    if n_comp<2: placeholder('Need at least two components.'); return 0
    pca=PCA(n_components=n_comp, random_state=0); coords=pca.fit_transform(dense)
    k=min(4, max(2, len(df)//8))
    labels=KMeans(n_clusters=k, random_state=0, n_init=10).fit_predict(coords[:,:min(3,n_comp)]) if len(df)>=k else np.zeros(len(df), dtype=int)
    terms=np.array(vec.get_feature_names_out())
    cluster_names={}
    for lab in sorted(set(labels)):
        idx=np.where(labels==lab)[0]; weights=np.asarray(X[idx].sum(axis=0)).ravel(); top=terms[np.argsort(weights)[-3:]][::-1]
        cluster_names[int(lab)]=' / '.join([t.title() for t in top])
    out=pd.DataFrame({'participant_id':df['participant_id'].values, 'pc1':coords[:,0], 'pc2':coords[:,1], 'neighborhood':labels, 'neighborhood_label':[cluster_names[int(x)] for x in labels]})
    for c in ['program','song_title','song_artist']:
        if c in df: out[c]=df[c].values
    out.to_csv(DOCS_DATA/'taste_coords.csv', index=False)
    sim=cosine_similarity(X); rows=[]
    ids=list(df['participant_id'])
    for i,pid in enumerate(ids):
        order=np.argsort(sim[i])[::-1]
        for j in order[1:4]: rows.append({'participant_id':pid, 'neighbor_id':ids[j], 'similarity':round(float(sim[i,j]),3)})
    pd.DataFrame(rows).to_csv(DOCS_DATA/'neighbors.csv', index=False)
    comps={}
    for i in range(min(2, len(pca.components_))):
        comp=pca.components_[i]
        comps[f'PC{i+1}']={'positive':terms[np.argsort(comp)[-10:]][::-1].tolist(), 'negative':terms[np.argsort(comp)[:10]].tolist(), 'variance':float(pca.explained_variance_ratio_[i])}
    (DOCS_DATA/'taste_terms.json').write_text(json.dumps(comps, indent=2))
    fig, ax=plt.subplots(figsize=(7,5))
    for lab in sorted(set(labels)):
        mask=labels==lab; ax.scatter(coords[mask,0], coords[mask,1], s=65, alpha=.85, label=cluster_names[int(lab)])
    ax.axhline(0,color='#ddd',lw=.8); ax.axvline(0,color='#ddd',lw=.8)
    ax.set_xlabel(f'PC1 - {pca.explained_variance_ratio_[0]:.1%}'); ax.set_ylabel(f'PC2 - {pca.explained_variance_ratio_[1]:.1%}')
    ax.set_title('DATA 117 music-text map', color=NAVY); ax.legend(fontsize=8, loc='best'); fig.tight_layout(); fig.savefig(DOCS_ASSETS/'taste_map.png',bbox_inches='tight'); plt.close(fig)
    try:
        import plotly.express as px
        plotdf=out.copy(); plotdf['song']=plotdf.get('song_title','') + ' — ' + plotdf.get('song_artist','')
        fig=px.scatter(plotdf, x='pc1', y='pc2', color='neighborhood_label', hover_data=['participant_id','song'], title='DATA 117 music-text map')
        fig.write_html(DOCS_ASSETS/'taste_map.html', include_plotlyjs='cdn')
    except Exception:
        (DOCS_ASSETS/'taste_map.html').write_text('<html><body><p>Interactive map unavailable; see static image.</p></body></html>')
    # loadings chart
    fig, axes=plt.subplots(1,2, figsize=(10,4))
    for i, ax in enumerate(axes):
        comp=pca.components_[i]; top=np.argsort(np.abs(comp))[-10:]
        ax.barh(terms[top], comp[top], color=ACCENT); ax.set_title(f'PC{i+1} loadings', color=NAVY)
    fig.tight_layout(); fig.savefig(DOCS_ASSETS/'pc_loadings.png',bbox_inches='tight'); plt.close(fig)
    log(f'tf-idf matrix: {X.shape[0]} participants x {X.shape[1]} terms')
    return 0
if __name__=='__main__': sys.exit(main())
