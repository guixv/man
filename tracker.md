
run tracker daily:
1. 打开任务计划程序

按：

Win + R

输入：

taskschd.msc

回车。

2. 创建任务

右侧点击：

Create Task...

不要选：

Create Basic Task
General（常规）

填写：

Name

例如：

GitHub Member Tracker Daily

Description：

Fetch GitHub organization members daily

选择：

Run whether user is logged on or not

勾选：

Run with highest privileges
Triggers（触发器）

点击：

New...

设置：

Begin the task:
On a schedule

选择：

Daily

时间建议：

例如：

04:00:00

因为你的 VRA 是服务器，凌晨执行比较合适。

保持：

Enabled

点击 OK。

Actions（操作）

点击：

New...

Action:

Start a program
Program/script

填写：

powershell.exe
Add arguments

填写：

-ExecutionPolicy Bypass -File "E:\Programs\code\man\run_tracker.ps1"
Start in（非常重要）

填写：

E:\Programs\code\man

不要留空。

否则：

tracker.py

可能找不到。

Conditions（条件）

如果这是 VRA 服务器：

建议取消：

Start the task only if the computer is on AC power

取消：

Start the task only if the computer is idle
Settings（设置）

建议：

勾选：

Allow task to be run on demand

勾选：

If the task fails, restart every:

设置：

10 minutes

次数：

3

勾选：

Run task as soon as possible after a scheduled start is missed
3. 保存

点击：

OK

如果提示密码：

输入当前 Windows 用户密码。

4. 手动测试

在任务列表找到：

GitHub Member Tracker Daily

右键：

Run

等待几十秒。

检查：

snapshot

PowerShell：

ls E:\Programs\code\man\snapshots

应该看到：

members_20260727.csv
members_latest.csv
