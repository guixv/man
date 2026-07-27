# =========================
# GitHub Member Tracker Job
# =========================


$PROJECT_DIR = "E:\Programs\code\man"


# 修改成你的实际 Python 路径
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
# Create execution log
# =========================

$DATE = Get-Date -Format "yyyyMMdd_HHmmss"

$RUN_LOG = "$LOG_DIR\tracker_$DATE.log"



$START_TIME = Get-Date -Format "yyyy-MM-dd HH:mm:ss"


"[$START_TIME] Start tracker..." |
    Tee-Object -FilePath $RUN_LOG



# =========================
# Run tracker.py
# =========================

Set-Location $PROJECT_DIR



"Running tracker.py..." |
    Tee-Object -FilePath $RUN_LOG -Append



& $PYTHON tracker.py 2>&1 |
    Tee-Object -FilePath $RUN_LOG -Append

if ($LASTEXITCODE -ne 0) {

    "Tracker failed with exit code $LASTEXITCODE" |
        Tee-Object -FilePath $RUN_LOG -Append

    exit $LASTEXITCODE
}



# Check python result

if ($LASTEXITCODE -ne 0) {

    "Tracker failed with exit code $LASTEXITCODE" |
        Tee-Object -FilePath $RUN_LOG -Append

    exit $LASTEXITCODE
}



"tracker.py finished successfully." |
    Tee-Object -FilePath $RUN_LOG -Append



# =========================
# Cleanup old snapshots
# =========================

"Cleaning old snapshots..." |
    Tee-Object -FilePath $RUN_LOG -Append



if (Test-Path $SNAPSHOT_DIR) {

    Get-ChildItem `
        -Path $SNAPSHOT_DIR `
        -Filter "members_*.csv" |
    Where-Object {

        $_.Name -ne "members_latest.csv" -and
        $_.LastWriteTime -lt (Get-Date).AddDays(-30)

    } |
    ForEach-Object {

        "Delete snapshot: $($_.FullName)" |
            Tee-Object -FilePath $RUN_LOG -Append

        Remove-Item $_.FullName -Force

    }

}



# =========================
# Cleanup old logs
# =========================

"Cleaning old logs..." |
    Tee-Object -FilePath $RUN_LOG -Append



if (Test-Path $LOG_DIR) {

    Get-ChildItem `
        -Path $LOG_DIR `
        -Filter "tracker_*.log" |
    Where-Object {

        $_.LastWriteTime -lt (Get-Date).AddDays(-30)

    } |
    ForEach-Object {

        "Delete log: $($_.FullName)" |
            Tee-Object -FilePath $RUN_LOG -Append

        Remove-Item $_.FullName -Force

    }

}



# =========================
# Finish
# =========================

$END_TIME = Get-Date -Format "yyyy-MM-dd HH:mm:ss"


"[$END_TIME] Done." |
    Tee-Object -FilePath $RUN_LOG -Append
