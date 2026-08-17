import pandas as pd
from common import DATA, DOCS_DATA

df = pd.read_csv(DATA / "clean.csv")

if {
    "song_title",
    "song_artist"
}.issubset(df.columns):

    playlist = pd.DataFrame({
        "Title": df["song_title"],
        "Artist": df["song_artist"]
    })

else:

    playlist = pd.DataFrame(
        columns=["Title", "Artist"]
    )

playlist.to_csv(
    DOCS_DATA / "playlist_import.csv",
    index=False
)
