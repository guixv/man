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
