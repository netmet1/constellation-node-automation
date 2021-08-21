# CONSTELLATION

## Node Operator Datapreneuer Alerting Automation Program

## TABLE OF CONTENTS <a name="top"></a>
1. [About Program](#what)
1. [Changes](#changes)
1. [Features](#features)
1. [Usage](#usage)
    - [Understanding the `adminauto.sh` Helper Script](#adminauto)
    - [Start Scheduled Alert/Report](#schedule_alert)
    - [Send Out a manual Alert](#send_alert)
    - [Print alert to CLI](#send_alert)
    - [Alert Results Table](#alert_readout_key)
    - [Send Out a manual Report](#send_report)
    - [Send report to CLI](#send_report)
    - [Send Out a manual health check](#send_health)
    - [Send health check to CLI](#send_health)
    - [Example Log Reports](#logs_report)
        - Includes CSV attachments
    - [Print Log Reports to CLI](#logs_report)
1. [How to Configure](#config)
    1. [Parameter Description Table](#parms)
1. [Understanding the Log File](#logs)
1. [Sending Log Reports for Taxes or Documentation](#logs_report)
1. [Installation](INSTALL.md)
    1. [Setup Gmail](INSTALL.md#gmail)
    1. [Node Installation](INSTALL.md#nodeinstall)
    1. [Prerequisites](INSTALL.md#prereq)
        1. [Node TimeZone Setup](/INSTALL.md#clocksetup)
1. [Common Commands and Troubleshooting](TS_USAGE.md)

---

### ABOUT THIS PROGRAM <a name="what"></a>

A Python automation and status program to run on your node.  It will send you alerts so you can keep up to date on the progress of your node, DAGs, rewards, and basic **system engineering** statistics, to help keep you in the know.

**IT TAKES NO RESPONSIBILITY FOR RESULTS, OUTCOMES, AND ANYTHING ELSE THAT MIGHT CAUSE ISSUES.  USE AT YOUR OWN RISK**

#### This is a dynamic program that runs directly on your node to update you with your node's progress via:
    1. Text Message (mms or sms)
    2. Email
    3. Other
    
#### This program will monitor your node's state and how it is running.  

> The following code is free to use as you would like, and you are welcome to contribute to it to make it better and more feature rich, as necessary.

---

##### Version: v1.3b

---
### CHANGES <a name="changes"></a>

- Added version information to the `--help, -h` option.
- Some code refactoring


---
### FEATURES <a name="features"></a>

- Log Error Rate Alerting
- Node Reward Accumulation
    - Possible reset detection
- Node Reward/Collateral Accumulation
- $DAG to USD
- Current $DAG price v. USD
- Node Status
- Web Status
- Node State
- Data Usage
- Memory and Swap Warning
- Uptime Warning
- Load Warning
- Health Checks
    - Load Balancer
    - Load Balancer's view or your Endpoint
- Security Checks
    - Unauthorized login attempts
    - Login attempt port ranges
    - Brute Force Login Failures
- Network Node List Size
- Reinvestment to Income Splits
- Earned Node Counter
- End of Day Summary with passive earnings and estimations
- Local Print Feature
- Log DAG accumulation and pricing history
    - Print or email details for date or date range
    - CSV attachment via email


## USAGE <a name="usage"></a>

| command | Parameters | Optional |
| ------- | :-------: | :------- | 
| python3 automation.py | `alert` `report` `auto` `health` `silent` | -p, & |

> `&` will run the system in the background until `ctl-c` performed.

| CLI Parameter | Description |
| :-------------: | :--------- | 
| **auto** | This will start the program and continue running until `ctl-c` is executed, or the job is `killed`.  It will run in the foreground, unless you use `&`. The system will use the information from the [configuration](#config) parameters.  `start_time`, `end_time`, and `int_minutes`. |
| **alert** | This will run the a system alert report once.  This allows you to run a one-time instance of the program, at the time of your choice (current moment in time when executed). |
| **report** | This will run the system and send the `end of the day` report once.  This allows you to run a one-time instance of the program, at the time of your choice. *Note: This may produce unexpected statistical results, if not run at the end of the day.* |
| **silent** | This will run the program and update log files, but will **not** alert to the user via MMS, SMS or email. |
| **health** | This will perform a health check against the load balancer (LB) configured in the `config.yaml` file and your node's connection to the LB. Add the `-p` option to print to the console (CLI) instead of email. |

#### Help Usage

```
usage: automation.py [-h] [-p] [-c EMAIL] [-ss START_DATE] [-se END_DATE]
                     ACTION

dag alerting script

positional arguments:
  ACTION                Type of action the script will run: (auto, alert,
                        report, health, silent, or log). Search dates (currently) only
                        work with the "log" action.

optional arguments:
  -h, --help            show this help message and exit
  -p, --print           print to the console instead of mms/sms, does not work
                        with 'auto'.
  -c EMAIL, --csv EMAIL
                        For use with the 'log' action only. Program will send
                        a csv formated file with search results to the
                        specified email.
  -ss START_DATE, --search_start START_DATE
                        For use with 'log' action. The start date search log
                        files for DAG balance at a certain date in time.
                        Format: YYYY-MM-DD. This will supply the last entry
                        recorded for the specified date. If search_end is not
                        specified a single date will be searched.
  -se END_DATE, --search_end END_DATE
                        For use with 'log' action. The end date to search log
                        files. Format: YYYY-MM-DD
```

#### Start the program to run on a schedule via the [configuration](#config) parameters (start/stop/interval) <a name="schedule_alert">

```
python3 automation.py auto 
```

or run it in the background

```
python3 automation.py auto &
```
> **The `auto` command will execute the `alert` command every [n](#config) `int_minutes`, between the times configured in the [interval](#config) section of the configuration
file.  At 5 minutes past the `end_time`, the `report` command will be issued.  No alerts will be sent outside of the `start_time` and `end_time`.**

#### Send out a manual alert <a name="send_alert">


```
python3 automation.py alert
```

MMS (SMS) message on the phone or email will be received, upon execution completion. 

#### Print to the CLI

```
python3 automation.py alert -p
```

The system will log the entry and print the results to the console.  It will **not** send an email, mss, or alert.

Example Output:

```
MAINNET
=========================
2021-06-30 12:30:00
Rewards: 300,000 +12
USD: $17,411.40 +$0.70
$12,187.98/$5,223.42
DAG @ $0.058038
+0.0000446
Collateral Nodes: 2.200000
Collateral DAGs: 550,000
Collateral USD$: $31,920.90
Next Node: 200,000
=========================
Node Status : online
Web Status : online
Node State : Ready
Data usage: 12% of 18G
Memory: LOW@368,348
Swap: OK@7,713,020
Days up: OK@12
15M CPU: OK@2.00
Health ChecK: Healthy
Ready Nodes: 81
=========================
Inv Login Attempts: 683
Port Range: 1034-65428
Max Login Exceeded: 15
```

> Results above are fictitious. `node_count` parameter set to `2` (details here: [node_count](#node_count)).

<a name="alert_readout_key"></a>
| KEY | Result Description |
| ---: | :------ |
| rewards | How many rewards you have earned so far. How much your collateral has increased since the last time the program ran (incremental). |
| USD | What are your rewards worth in $USD.  How much has it changed `+` for increases, `()` for decreases. |
| Splits | Based on the [splits](#config) setup in the configuration, it will show you `split1`/`split2` |
| DAG Price | What is the current price, based on an API call in real time. (coingecko). **In the event an API call is unsuccessful after three attempts, a triple asterisk(*) will appear after the price to indicate the price is reflected from the last known log entry with a valid price.** |
| DAG Price Change | What was the change since the last lookup `+` for increases, `()` for decreases. |
| Collateral Nodes | Based on the number of nodes you added to the [configuration](#config) file prior to running the program.  It will compute the number of Nodes you could possibly have. |
| Collateral DAGs | Based on the number of nodes you added to the [configuration](#config) file prior to running the program.  It will compute the number of DAGs you should accumulated. | 
| Collateral USD | Based on the number of nodes you added to the [configuration](#config) file prior to running the program.  It will compute the USD value of all DAGs both reward and collateral. | 
| Next Node | How many DAGs you have to earn before you earn another Node based on collateral and rewards earned. |
| Node Status | What is the status of your node, based on a `dag metrics`. |
| Web Status | What is the status of your node's web interface, based on a `dag metrics`. |
| Data Usage | How much space is available on your HD based on a systems command results. |
| Memory | Will show memory allocation of `OK` or `LOW` based on the [configuration](#config) file setup. |
| Swap | Will show swap allocation of `OK` or `LOW` based on the [configuration](#config) file setup. |
| Days Up | Will show uptime in `days`  for the server with `OK` or `WARN` based on the [configuration](#config) file setup. |
| 15M CPU | Will show the current 15 minute average CPU load statistics with `OK` or `WARN` based on the [configuration](#config) file setup. |
| Health Check | Every N minutes based on the `healthcheck: int_minutes` the system will do a GET to the constellation LB and a GET against your specific endpoint, and return `healthy` or `error` based on the `status return codes`. |
| Ready Nodes | How many nodes are currently on your state channel and in `Ready`, based on `dag nodes`. |
| Inv Login Attempts | For the entire `auth.log` file, how many times has a user auth attempt begin denied. |
| Port Range | What was the lowest port and highest port where invalid login attempts were logged.  **If this shows below `1024`, this may be cause for concern.** |
| Max Login Exceeded | How many times has the system noticed and created an error log message, due to a possible brut force password authentication attempts. (`auth.log`) |

During the execution of an alert, if an error in the output of `Rewards` is non-integer. 

```
MAINNET
=========================
Error Detected
Possible Reset Required?
Rewards: 0 (-300000)
[...]
```

When the constellation log file goes over the [error threshold](#error_threshold).

```
Log Size: 157893
Errors:: 48
Percentage:: 0.0304%

MAINNET
=========================
2021-06-29 08:30:35
[...]
```

#### Send out manual end of day report. <a name="send_report">

```
python3 automation.py report
```

MMS message on the phone or email will be received

```
python3 automation.py report -p
```

The system will print the report results to the console.  It will **not** send an email, mss, or alert.

Example of End of Day Report.

```
END OF DAY REPORT
=================
8 Hours 30 Minutes
START: 2021-06-26 07:00:00
END: 2021-06-26 15:30:00
---
REWARDS: 841
AVE/15Min: 26
AVE/30Min: 53
AVE/1Hour: 105
---
$DAG DAY START: 0.057189
$DAG DAY END  : 0.058153
$DAG CHANGE   : 0.00096400
$DAG HIGH     : 0.065948
$DAG LOW      : 0.056524
---
$DAG ESTIMATES
Daily  : 2,520
Monthly: 75,600
Yearly : 919,800
========
USD @ $0.058153
DAILY   : $146.55
MONTHLY : $4,396.37
YEARLY  : $52,756.4
========
USD @ $0.1
DAILY   : $252.0
MONTHLY : $7,560.0
YEARLY  : $90,720.0
========
USD @ $0.5
DAILY   : $1,260.0
MONTHLY : $37,800.0
YEARLY  : $453,600.0
========
USD @ $1
DAILY   : $2,520
MONTHLY : $75,600
YEARLY  : $907,200
========
USD @ $3
DAILY   : $7,560
MONTHLY : $226,800
YEARLY  : $2,721,600
========
USD @ $5
DAILY   : $12,600
MONTHLY : $378,000
YEARLY  : $4,536,000
========
USD @ $10
DAILY   : $25,200
MONTHLY : $756,000
YEARLY  : $9,072,000
========
USD @ $50
DAILY   : $126,000
MONTHLY : $3,780,000
YEARLY  : $45,360,000
========
USD @ $100
DAILY   : $252,000
MONTHLY : $7,560,000
YEARLY  : $90,720,000
```

> Based on [config](#config) file that is set to $0.1, $0.5, $3, $5, $0 ,$50, $100

> **NOTE: If the program doesn't run for the day, the results will (obviously) be incorrect or screwed.  It works off the `dag_count.log` file located in the root of the automation program folder.** *Log rolling is not enabled, so you will need to keep an eye on the file, until a new release adds the log rolling feature.*

#### Do a health check <a name="send_health">
```
python3 automation.py health
```

Do a health check and print to the console (CLI)
```
python3 automation.py health -p
```

Results via the MMS, email, or CLI
```
<your_node_here>
=======================
HEALTH STATUS REPORT
--------------------
lb.constellationnetwork.io: Healthy
Endpoint <your_iop_here>: Healthy
Codes: (200, 204)
```

```
<your_node_here>
=======================
HEALTH STATUS REPORT
--------------------
lb.constellationnetwork.io: Healthy
Endpoint <your_ip_here>: Error
Codes: (200, 502)
```

## ADMINAUTO.SH HELPER SCRIPT <a name="adminauto">
The program now includes a script called `adminauto.sh` to help make it easier to `start`, `restart` and `stop` the program from running quickly and easily.
**THIS IS ONLY FOR USAGE WITH THE `auto` option.**

| command | Parameters | 
| ------- | :-------: | 
| . adminauto.sh | `-h` `-s` `-r` `-k` | 

> The command should always start with the `.` in the front of the command

```
Node Operator Automation Helper Script
--------------------------------------
usage: . admin_auto.sh [-h] [-s] [-r] [-k]

THIS IS FOR USE WITH THE "AUTO" ARGUMENT (auto run)
This does not deal with single alerts, reports, or logs

This does not deal with the program running locally in the current user session
without the "nohup" command.  See README.md

positional arguments:
  -h        show this help message
  -s        start the automation program if not running
            this will start the program in the background
  -r        stop the program, then restart it
  -k        stop the program from running in the background
            this will find and kill the automation program process

example usage:
~# . admin_auto.sh -s
This command will start the node operator automation program in the background with the "auto" variable.

~#: . admin_auto.sh -r
This command will find the process that is running and "kill" it (stop it).
then it will restart it with the auto command in the background (-s).
```

---

## CONFIGURATION <a name="config"></a>

Rename `config.example.yaml` to `config.yaml`. Navigate to your `config.yaml` file and open with your favorite editor.  
You **MUST** update this file in order for the program to function properly.

>This is the **ONLY** file that you should be manipulating.  All other files in this program should be left alone.

```
configuration:
  email:
    node_username: root
    gmail_acct: gmail_source_email@gmail.com
    gmail_token: gmail_app_password
    email_recipients:
      enabled: false
      - whoever1@whoever.com      
      - whoever2@whoever.com
    mms_recipients:
      enabled: true
      add_subject: false
      - 111111111@provider.gateway.net
      - 222222222@provider.gateway.net
    node_name: My_Node
  constraints:
    error_max: 20
    memory_swap_min: 200000
    security_check: true
    uptime_threshold: 30
    load_threshold: .7
  healthcheck:
    enabled: true
    lb: <constellation_lb_fqdn>
    lb_port: 9000
    node_ip: your_nodes_ext_ip_here
    node_port: 9001
    int_minutes: 5
  intervals:
    start_time: '07:00'
    end_time: '20:00'
    int_minutes: 15
  splits:
    enabled: true
    split1: .7
    split2: .3
  collateral:
    enabled: true
    node_count: 2
  report:
    enabled: true
    estimates:
      - .10
      - .50
      - 1
      - 3
      - 5
      - 10
      - 50
      - 100
      - 34000
```

The following pieces of the `config.yaml` must be changed to match your **specific** configuration.
- node_username
- gmail_acct
- gmail_token
- mms_recipients
- email_recipients
    - *If you are planning on using the same email address to accept the incoming push requests from your node and also as your recipient email, you **must** put it in the recipients list here as well; otherwise the program will exit with a failure.*
    - **aka**: `bob@bob.com` sends alerts to `bob@bob.com`.
- node_name
- lb
    - *If you don't know the LB fully qualified domain name (FQDN), you may need to ask in the community for this FQDN.  It isn't listed here for privacy reasons.*
- node_ip

The following elements you might want to change from `false` to `true`
- under the `healthcheck:` section `enabled: true`
- under the `collateral:` section `enabled: true`
- under the `report:` section `enabled: true`
- same for `splits` but this is only if you need/want the functionality (see below)

##### If you do not have email addresses to send notifications to...
- Make sure to set the `enabled` to false
- Leave the `list` parameters with the default `whoever` addresses (as placeholders)

##### If you do not have sms/mms addresses to send notifications to...
- Make sure to set the `enabled` to false
- Leave the `list` parameters with the default `1111111111` addresses (as placeholders)

#### Configuration file parameter details <a name="parms"></a>

| Section | Parameter | Sub Param | Description | Value type/Format | Default | Required |
| ------- | :-------: | :----------  | :---------- | :-----: | :-----: | :---: |
| **notifications** | | | Email parameters needed for program to function properly.
|  | `gmail_acct` | | Gmail account you created or used in the [Setup Gmail](#gmail) section. | - | - | yes
|  | `gmail_token` | | Password you saved in the [App Password](#gmail) section. | - | - | yes
|  | `email_recipients` | | Parameters necessary for emails to be sent out as notifications | - | - | yes
|  | | `enabled` | Enable ability to send notifications as email. You will want to change this to `false` (default) if you do not want to send notifications to any email addresses | boolean | `false` | yes
|  | | `list` | Making sure you leave the `-` and indentation unchanged, add in your email addresses where you want to send the reports.  If you only have `1` email, you can remove the extra list item(s).  If you have more than `2`, you can add in as many list entries (starting with a dash) as you like.  **NOTE**: *It is unknown how many requests will be accepted/allowed by Gmail or your mobile provider, so you may need to be cognizant of this when setting up complex lists of email recipients.* | - | - | yes
|  | `mms_recipients` | | Parameters necessary for sms/mms notifications to be sent outbound. | - | - | yes
|  | | `enabled` | Enable ability to send notifications as sms/mms messages. You will want to change this to `false` if you do not want to send notifications to any sms/mms addresses | boolean | `true` | yes
|  | | `add_subject` | Enable subject header when sending sms/mms notification alerts. **Some email providers (tmobile for example) seem to block or black-hole messages when a subject line is attached?** If you are **not** receiving sms/mms messages, you may want to remove the subject to see if this helps. | boolean | `true` | yes
|  | | `list` | Making sure you leave the `-` and indentation unchanged, add in your mms/sms email addresses where you want to send the reports.  If you only have `1` sms/mms email, you can remove the extra list item(s).  If you have more than `2`, you can add in as many list entries (starting with a dash) as you like.  **NOTE**: *It is unknown how many requests will be accepted/allowed by Gmail or your mobile provider, so you may need to be cognizant of this when setting up complex lists of email recipients.* | - | - | yes
| **constraints** |  | | This section should only be modified by more advanced users.  It allows you to manipulate several program thresholds.|
|  | `error_max` | | <a name="error_threshold"> How many errors should accumulate in the constellation log file before notifying in an alert.  **Note**: *The constellation log file is configured to roll, so the low error count is justified and only pertains to the current log.* | decimal | `20` | no
|  | `memory_swap_min` | | Low end threshold before alerting that memory or swap is low.  The same decimal is used to check both.  Memory and Swap are independently checked. | decimal | `100000` | no
|  | `security_check` | | Do you want the system to count unauthorized access requests and ports. | boolean | `false` | no
|  | `uptime_threshold` | | Number of days of uptime the server/node/instance has been running.  *Recommendation is to reboot after monthly patches* | int | `30` | no
|  | `load_threshold` |  | Percentage of CPU load you want to warn against when threshold is exceeded. *float represented as a percentage* | float | `.7` | no
| **healthcheck** |  | | Features that help setup the health check against the Load Balancer (LB) and End Node (Your Node) |
|  | `enabled` |  | Enable this feature. | boolean | `false` | yes
|  | `lb` | | The fully qualified domain name of the constellation LB. | string |  | yes
|  | `lb_port` | | Which TCP port is your health check using to do a GET for a response code? | int | `9000` | yes
|  | `node_ip` | | The external IP address of your node | string | `X.X.X.X` | yes
|  | `node_port` | | Which TCP port is your health check using to do a GET for a response code from the LB for your IP? | int | `9001` | yes| 
|  | `int_minutes` | | How often do you want to do a health check against the LB?  **no less than 5 or greater than 60**. Must be increments of 5. | int | `30` | no | 
|  | `alarm_once` | |If your End Point or the LB has an issue, only alarm once.  You will get alerted again, when the LB or EndPoint node is reachable again. If `false` as long as the LB or End Point is down, you will receive an alert every X minutes, based on the `int_minutes` setting. Because this is a critical function, it does not adhere to the `start_time` and `end_time` that might be setup for the normal `alert` feature. | boolean | `true` | yes | 
| **intervals** |  | | Setup when you want the alerts to start/stop being pushed to your `mms_recipients`. |
|  | `start_time` | | 24 hour clock notation - currently adheres to the systems local time zone.  When do you want the alerting to start each day? If you want the program to run 24/7, make your start time and end time '00:00'  **IMPORTANT**: The time needs to be surrounded by quotes. *Note: Stat calculations are rounded to the lowest hour.* | 'HH:MM' | `'07:00'` | no
|  | `end_time` | | 24 hour clock notation - local time zone.  When do you want the alerting to stop each day? **IMPORTANT**: The time needs to be surrounded by quotes. *Note: Stat calculations are rounded to the lowest hour.* | 'HH:MM' | `'20:00'` | no
|  | `int_minutes` | | How often do you want text messages to be pushed out to your recipients? Must be in 5 minute increments (10,15,1440).  Can not be over 1440. If you need something more specific, utilize the CRON (see [Alternative Cron](INSTALL.md#alt_cron)). Please be aware that a shorter interval could cause your provider to block your source account.  *Recommendation*: no less than every 15 minutes, system restriction to 10 minutes. | MM | `30` | no
| **splits** | | | This section is an optional configuration. When enabled, this feature will break out rewards/income into percentages between `split1` and `split2`.  When added together this should equal 1 (100%), otherwise calculations will not be accurate.  `Example`: You want to calculate how much of your income will be used for reinvestment (split1) verses taking profits (split2). |
|  | `enabled` | |Enable this feature. | boolean | `false` | yes
|  | `split1` | | Float number less than 1. Split1 and Split2 must equal 1 in order for accurate calculations. | float | - | if enabled
|  | `split2` | | Float number less than 1. Split1 and Split2 must equal 1 in order for accurate calculations. | float | - | if enabled
| **collateral** | | | This section is an optional configuration. When enabled, this feature will calculate your current collateral as it relates to the 250K USD requirement for obtaining a new node. |
|  | `enabled` | | Enable this feature. | boolean | `false` | yes 
|  | `node_count` | | ***INCLUDING THIS NODE***. <a name="node_count"></a> How many nodes do you own that you want to include in the collateral calculations?  Note: Until the program couples with other node reward/income statistics, this will not include the reward/income from the other nodes, only the node's collateral itself. AKA: `enabled` with `node_count: 2` means you have 2 nodes all together including this node, that you want to count in your collateral calculations. | int | `1` | if enabled  
| **reports** | | | This section is an optional configuration. When enabled, this feature will calculate your estimated earnings for the node, based on the prices allocated in the `estimates` list provided. |
|  | `enabled` | | Enable this feature. | boolean | `false` |  yes
|  | `estimates` | | $USD that you want to have the $DAG count translated into for the `end of day` report. *Note*: Make sure to leave the `-` in front of each list item.  You can have as many as you deem necessary, or you can remove list items that aren't wanted/needed. *The program will automatically remove estimates that are lower than the @report time USD/DAG price.* | float | `.50`, `1`, `5`, `10`, `100` |  no 

> **Warning**: When entering in the `start_time` and `end_time` parameters, if `start_time` is after the `end_time` the system will revert to defaults (see above), instead of erroring out.

> The program will check if the `config.yaml` has been updated by the user every `int_minutes`.  Therefore, any changes will **not** take affect until the next `int_minutes` interval is reached.

---

### Understanding the Log File <a name="logs">

During program execution of an `alert` (`auto`)

```
nodeuser@constellation-node:~/automation## python3 automation alert
```

The system will log the results of the `alert` call into a file called `dag_count.log`. This file is located in the `/logs/` directory off the program's root.

Clip of log file
```
[...]
2021-07-01 09:45:00|300000|22314.9|0.074383
2021-07-01 10:00:02|300121|22412.736159|0.074679
[...]
```

---

This file is **imperative** to the proper functionality of the automation program.  The end of the day report will review the daily activity that has been written to this file.  The program uses the start and stop times; configured in the `config.yaml` file, to calculate averages and predictive/assumptions.  

The log file does not roll (future update to the code).

The log file is only updated on an `alert`.

| Column | Description |
| :----: | :---------- |
|   1    | The date/time the last `alert` was run. |
|   2    | The number of rewards scrapped from a `dag metric`. |
|   3    | The timestamped reward value in USD | 
|   4    | The timestamped current $DAG price in USD |

---

### Creating Log Reports <a name="logs_report">

From the command line of the node, you can request $DAG `log` reports, by issuing the `log` action followed by date or date range.

The report offers a few options

Print a report for a single day based on a start time only, send to MMS alerting group.

```
python3 automation.py log -ss 2021-07-11
```

Print a report for a date range based on a start time and end time, send to MMS alerting group.

```
python3 automation.py log -ss 2021-07-01 --se 2021-07-11
```

Print a report and CSV attachment for a date range based on a start time, send to **specific email**.

```
python3 automation.py log -c someone@somewhere.com -ss 2021-07-01 
```

Print a report and CSV attachment for a date range based on a start time and end time, send to **specific email**.

```
python3 automation.py log -c someone@somewhere.com -ss 2021-07-01 --se 2021-07-11
```

Print a report for a single day based on a start time only, send to CLI (console).

```
python3 automation.py log -ss 2021-07-11 -p
```

Print a report for a date range based on a start time and end time, send to CLI (console).

```
python3 automation.py log -ss 2021-07-01 --se 2021-07-11 -p
```
---

[back to beginning of document](#top)

---

hgtp://netmet
