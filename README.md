# DATA 117 Fall 2026 Cohort Snapshot

GitHub Pages-ready Quarto site with AI-definition word cloud, location word cloud, music map, and playlist.

- Survey form: [DATA 117 survey](https://forms.gle/xYPbUmVaRbAJpqSh9)
- Google Sheet ID: `1stguPJIK8VrrxXKbWyKb3Gz7OUTuL4icATUjgq8_B6Y`
- GID: `710329544`

## Test

```bash
pip install -r requirements.txt
python3 scripts/make_sample_data.py --n 42
python3 scripts/run_all.py --no-fetch
quarto preview
```

## GitHub Pages

Add secrets `GOOGLE_SHEET_ID`, `GOOGLE_SHEET_GID`, and `ANON_SALT`, then publish from branch `main`, folder `/docs`.
