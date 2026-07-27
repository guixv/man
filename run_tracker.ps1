# =========================
# GitHub Member Tracker Job
# =========================


$PROJECT_DIR = "E:\Programs\code\man"


# 修改成你的真实 Python 路径
$PYTHON = "C:\Users\Administrator\AppData\Local\Programs\Python\Python36\python.exe"


$LOG_DIR = "$PROJECT_DIR\logs"

$SNAPSHOT_DIR = "$PROJECT_DIR\snapshots"



# =========================
# Prepare directories
# =========================

if (!(Test-Path $LOG_DIR)) {
    New-Item -ItemType Directory $LOG_DIR | Out-Null
}

if (!(Test-Path $SNAPSHOT_DIR)) {
    New-Item -ItemType Directory $SNAPSHOT_DIR | Out-Null
}



# =========================
# Create log file
# =========================

$DATE = Get-Date -Format "yyyyMMdd_HHmmss"

$RUN_LOG = "$LOG_DIR\tracker_$DATE.log"


$START_TIME = Get-Date -Format "yyyy-MM-dd HH:mm:ss"


"[$START_TIME] Start tracker..." > $RUN_LOG



# =========================
# Run tracker.py
# =========================

Set-Location $PROJECT_DIR


"Running tracker.py..." >> $RUN_LOG


& $PYTHON tracker.py >> $RUN_LOG 2>&1


$PYTHON_EXIT = $LASTEXITCODE



# =========================
# Check tracker result
# =========================

if ($PYTHON_EXIT -ne 0) {

    "Tracker failed with exit code $PYTHON_EXIT" >> $RUN_LOG

    exit $PYTHON_EXIT
}



"tracker.py finished successfully." >> $RUN_LOG



# =========================
# Cleanup snapshots older than 30 days
# =========================

"Cleaning old snapshots..." >> $RUN_LOG


if (Test-Path $SNAPSHOT_DIR) {

    Get-ChildItem `
        -Path $SNAPSHOT_DIR `
        -Filter "members_*.csv" |
    Where-Object {

        $_.Name -ne "members_latest.csv" -and
        $_.LastWriteTime -lt (Get-Date).AddDays(-30)

    } |
    ForEach-Object {

        "Delete snapshot: $($_.FullName)" >> $RUN_LOG

        Remove-Item $_.FullName -Force

    }

}



# =========================
# Cleanup logs older than 30 days
# =========================

"Cleaning old logs..." >> $RUN_LOG


if (Test-Path $LOG_DIR) {

    Get-ChildItem `
        -Path $LOG_DIR `
        -Filter "tracker_*.log" |
    Where-Object {

        $_.LastWriteTime -lt (Get-Date).AddDays(-30)

    } |
    ForEach-Object {

        # avoid deleting current running log
        if ($_.FullName -ne $RUN_LOG) {

            Remove-Item $_.FullName -Force

        }

    }

}



# =========================
# Finish
# =========================

$END_TIME = Get-Date -Format "yyyy-MM-dd HH:mm:ss"


"[$END_TIME] Done." >> $RUN_LOG


exit 0
