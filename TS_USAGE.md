# COMMON COMMANDS AND TROUBLESHOOTING <a name="top">

## TABLE OF CONTENTS

1. [How Do We Know If The Program is Running?](#running)
1. [Find the Error We Might Be Having](#start)
1. [Common Error Log File Issue]("log_issue)
1. [Common Error Configuration Missing]("config_missing)
1. [Most Common Error Reasons](#other)
1. [My Date/Time is Wrong on my Alerts?](#timezone)
1. [How do I STOP the program?](#stop)
1. [What if error is not on this page?](#all_other_issues)
1. [Using the adminauto.sh script](#adminauto)

---

### HOW DO I KNOW IF MY PROGRAM IS RUNNING? <a name="running">

```
pgrep -f "python3.*automation.py.*auto"
```
If the program is running properly, this will come back with a number that represents the process ID number for the automation.py program.
or
```
ps -aux | grep automation
```
If the program is running properly, this command should show you 2 lines of results

```
nodeuser@constellation-node:~/# ps -aux | grep automation
root     18920  0.0  0.0  14864   988 pts/1    S+   09:01   0:00 grep --color=auto automation
root     30878  0.3  2.1 248172 177804 ?       S    Jul22  03:58 python3 automation.py auto
```
 - The first line says that the `ps -aux` command was running when you issued the command.  This will show up every time because you ran the command and it was then running to get these results in the first place.
 - The second line says that it sees that a `python version 3` program was started on `Jul22` and is running.

 **IF WE DO NOT SEE** the second line.  Something is wrong.

### TROUBLESHOOTING START <a name="start">
 If you followed the instructions based on the [INSTALL.md](installation instructions) in this repository. 

 Let's find out why (common mistakes)  **v1.0b** used as example, change this for your particular version.

If you ran the program from the command line with the `nohup` prefix...
 ```
 cd ~/constellation=node-automation-1.0b
 cat nohup.out
 ```

If your program ran from the CRON either because your system rebooted since last run, or because you are using the alertnative CRON method from the [INSTALL.md](INSTALL.md)

```
cd ~
cat cron.log
```

At the end of the file...  You will see a grouping of code errors.

#### COMMON ERROR #1 LOGGING <a name="log_issue">

File contents look like such

```
Traceback (most recent call last):
  File "automation.py", line 55, in <module>
    core.node_checkup()
  File "/root/constellation-node-automation-1.0b/classes/core.py", line 27, in node_checkup
    buildReport = CheckDagStatus(self.config)
  File "/root/constellation-node-automation-1.0b/classes/check_dag_status.py", line 55, in init
    self.create_alert_report()
  File "/root/constellation-node-automation-1.0b/classes/check_dag_status.py", line 125, in create_alert_report
    self.get_calc_stats_variables("alert")
  File "/root/constellation-node-automation-1.0b/classes/check_dag_status.py", line 162, in get_calc_stats_variables
    last_line = last_line[len(last_line)-1]
IndexError: list index out of range
```

This means that your log file contents are empty.  Something bad happened.  When you upgraded (or other)... 

#### FIX

```
cd ~/constellation=node-automation-1.0b/logs
cat dag_count.log
```

If the file is empty (this should be the case), you need to add an entry to get it started.

```
cd ~/constellation=node-automation-1.0b/logs
nano dag_count.log
```

Add this line (replace the date with the current date and time)
```
2021-07-25 11:15:02|0|0|0.0
```

`Ctrl-X`, and `Y`

#### COMMON ERROR #2 - Configuration File Missing <a name="config_missing">

If you `nohup.out` or `cron.log` file has the following (or close to)

```
Traceback (most recent call last):
  File "automation.py", line 43, in <module>
    config = Config(dag_args)
  File "/root/constellation-node-automation-1.0b/classes/config_obj.py", line 14, in __init__
    self.config = self.pull_configuration()
  File "/root/constellation-node-automation-1.0b/classes/config_obj.py", line 34, in pull_configuration
    with open(config_file,'r') as stream:
FileNotFoundError: [Errno 2] No such file or directory: '/root/constellation-node-automation-1.0b/configs/config.yaml'
```

Please refer to the [INSTALL.md](/INSTALL.md#configuration) section to add your `config.yaml` and configure it properly.

#### OTHER COMMON ERRORS <a name="other">

All other errors will be consistent with incorrect `config.yaml` settings.  You **MUST** have these settings correct in order to allow the program to function properly.

1. Make sure your GMAIL account is setup to receive requests from your node.  
    - This requires 2-factor authentication
    - This requires you have the **correct** token (password) entered.
1. Make sure that **even if you are using the same account to receive messages** that your gmail account email address is in the `email_recipients` list.
1. Make sure your `lb` line has been updated to the correct fully qualified domain name (FQDN) of the constellation's LB.  **Not recommended to use an IP address here because the IP address can change and then you will receive false alerts**.  If you do not know this address, ask someone in the Constellation community (Discord or Telegram).
1. Make sure you have your `node_ip` correct.
1. Make sure that all sections that have an option of being `enabled: true` are set to `true` if you want to use those features.

#### IF YOUR TIMEZONE IS WRONG <a name="timezone">

This is an issue with your `node` not the program.  See the [INSTALL.md clock setup](INSTALL.md#clocksetup) section to fix this issue.

Testing if this is the case

```
nodeuser@constellation-node:~# date
```
results
```
nodeuser@constellation-node:~# date
Sun Jul 25 11:26:05 EDT 2021
```
We are in the Eastern Time Zone
or
```
nodeuser@constellation-node:~# date
Sun Jul 25 13:04:15 UTC 2021
```
We are setup to use UTC, and this is *probably* not good.  See the [INSTALL.md clock setup](INSTALL.md#clocksetup) section to fix.

#### HOW DO I STOP THIS PROGRAM  <a name="stop">

What if you want to stop the program because you don't want it running?

```
pgrep -f "python3.*automation.py.*auto"
```
results
```
30878
```
or 

```
ps -aux | grep automation
```
results
```
root     18920  0.0  0.0  14864   988 pts/1    S+   09:01   0:00 grep --color=auto automation
root     30878  0.3  2.1 248172 177804 ?       S    Jul22  03:58 python3 automation.py auto
```
##### CAREFULLY

You now know that process # `30878` is your automation program's process.  We need to `kill` it.

```
kill 30878
```
```
ps -aux | grep automation
```
results
```
root     18920  0.0  0.0  14864   988 pts/1    S+   09:01   0:00 grep --color=auto automation
```

## IF THESE DIDN'T HELP AND YOU STILL HAVE ISSUES. <a name="all_other_issues">

Please open an issue on this repo and supply your `nohup.out` file or `cron.log`.  (Or both).

[back to beginning of document](#top)

## ADMINAUTO.SH <a name="adminauto">
Please see the [README.md](README.md) to details on using this helpful script.  You will find a link in the Table of Contents.

[back to beginning of document](#top)
---
Thank you!
hgtp://netmet
