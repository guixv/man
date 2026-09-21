# man
manba

set info in config.py
than use tracker.py to get info

example:
python tracker.py --compare 20260701
or simply compare to latest:
python tracker.py

compare.py can be used to compare changes between two logs

example:
python compare.py \
snapshots/members_20260701.csv \
snapshots/members_20260727.csv

## Web dashboard

The dashboard reads `logs/changes.csv`, groups changes by date, hides an
Added record when the same day also contains a Removed record with the same
name, and refreshes every 60 seconds.

Start it from the project root:

```powershell
python -m http.server 8765
```

Then open `http://localhost:8765/web/` in a browser. The daily
`run_tracker.ps1` job keeps updating `logs/changes.csv`; refreshes will pick up
new data automatically. The CSV files are intentionally ignored by Git.
