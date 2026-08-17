import json,pandas as pd
from common import ROOT,DOCS_DATA,log
def img(f,c): return f'![{c}](docs_assets/{f})\n\n'
summary=json.loads((DOCS_DATA/'summary.json').read_text()) if (DOCS_DATA/'summary.json').exists() else {}; charts=json.loads((DOCS_DATA/'charts.json').read_text()) if (DOCS_DATA/'charts.json').exists() else {}
lines=[f"::: {{.hero-note}}\n**{summary.get('n_participants',0)} participants** represented so far, with **{summary.get('n_unique_songs',0)} unique songs** in the playlist.\n:::\n",'### Generated views\n']
for f,c in charts.items(): lines.append(img(f,c))
(ROOT/'_generated.md').write_text('\n'.join(lines))
t=json.loads((DOCS_DATA/'taste_terms.json').read_text()) if (DOCS_DATA/'taste_terms.json').exists() else {}; lines=[]
for pc,v in t.items(): lines.append(f"- **{pc}** explains approximately **{v.get('variance',0):.1%}** of the variance. Positive terms include: {', '.join(v.get('positive',[])[:6])}.")
(ROOT/'_tastemap.md').write_text('\n'.join(lines) if lines else 'The axis summary will appear after enough responses are available.')
tracks=pd.read_csv(DOCS_DATA/'playlist_import.csv') if (DOCS_DATA/'playlist_import.csv').exists() else pd.DataFrame(); lines=['| # | Song | Artist | Links |\n|---:|---|---|---|']
tracks = (
    pd.read_csv(DOCS_DATA / "playlist_import.csv")
    if (DOCS_DATA / "playlist_import.csv").exists()
    else pd.DataFrame(columns=["Title", "Artist"])
)

lines = []

lines.append("| # | Song | Artist |")
lines.append("|---:|---|---|")

for i, r in enumerate(
    tracks.itertuples(index=False),
    start=1
):

    lines.append(
        f"| {i} | {r.Title} | {r.Artist} |"
    )

lines.append("")
lines.append(
    "Download: [playlist_import.csv](docscsv"
)

(ROOT / "_playlist.md").write_text(
    "\n".join(lines)
)

log(
    f"rendered playlist with {len(tracks)} entries"
)
