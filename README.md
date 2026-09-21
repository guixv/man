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
name, and refreshes every 60 seconds. It also has an `Oldest to latest` view
backed by `logs/period_changes.csv`.

The daily PowerShell job rebuilds `period_changes.csv` after removing snapshots
older than 30 days. This keeps the comparison aligned with the oldest snapshot
that is still retained.

Start it from the project root:

```powershell
python -m http.server 8765
```

Then open `http://localhost:8765/web/` in a browser. The daily
`run_tracker.ps1` job keeps updating `logs/changes.csv`; refreshes will pick up
new data automatically. The CSV files are intentionally ignored by Git.

## Deploy to the scheduled Windows machine

After pushing these code changes, update the machine that runs the scheduled
job:

```powershell
Set-Location "path\to\man"
git pull origin main
python -m pip install -r requirements.txt
```

Keep the real `.env` on that machine. Also keep the dated files in
`snapshots\`, for example `members_20260727.csv`; the comparison cannot be
calculated from `members_latest.csv` alone.

To rebuild the all-period comparison immediately, run:

```powershell
python tracker.py --refresh-period
```

This writes `logs\period_changes.csv`, comparing the oldest retained dated
snapshot with the newest one. The daily `run_tracker.ps1` task runs the same
refresh after deleting snapshots older than 30 days, so the result stays
current automatically.
