import pandas as pd

from common import DATA, DOCS_DATA, log

CLEAN = DATA / "clean.csv"

df = pd.read_csv(CLEAN)

# Keep only rows with a valid song submission
tracks = df[
    ["participant_id", "song_title", "song_artist"]
].copy()

# Create the fields expected elsewhere in the site
tracks["matched_title"] = tracks["song_title"]
tracks["matched_artist"] = tracks["song_artist"]
tracks["album"] = ""

# Save the file used by the Playlist page
tracks.to_csv(
    DOCS_DATA / "playlist_tracks.csv",
    index=False
)

# Save the import file
tracks[
    ["matched_title", "matched_artist", "album"]
].rename(
    columns={
        "matched_title": "Title",
        "matched_artist": "Artist",
        "album": "Album",
    }
).to_csv(
    DOCS_DATA / "playlist_import.csv",
    index=False
)

log(f"wrote {len(tracks)} playlist entries")
