# CONSTELLATION

## Node Operator Datapreneuer Alerting Automation Program/Script

## TABLE OF CONTENTS <a name="top"></a>
1. [About Program](#what)
1. [Features](#features)
1. [Usage](#usage)
    1. [Alert Results Table](#alert_readout_key)
1. [Installation](#installation)
    1. [Setup Gmail](#gmail)
    1. [Node Installation](#nodeinstall)
    1. [Prerequisites](#prereq)
1. [How to Configure](#config)
    1. [Parameter Description Table](#parms)
1. [CRON setup](#cron)
1. [Understanding the Log File](#logs)

---
### ABOUT THIS PROGRAM <a name="what"></a>

A fun program to run on your node.  It will send you alerts so you can keep up to date on the progress of your node, DAGs, rewards, and basic **system engineering** statistics, to help keep you in the know.

**IT TAKES NO RESPONSIBILITY FOR RESULTS, OUTCOMES, AND ANYTHING ELSE THAT MIGHT CAUSE ISSUES.  USE AT YOUR OWN RISK**

#### This is a dynamic program that runs directly on your node to update you with your node's progress via:
    1. Text Message (mms or sms)
    2. Email
    3. Other
    
#### This program will monitor your node's state and how it is running.  

> The following code is free to use as you would like, and you are welcome to contribute to it to make it better and more feature rich, as necessary.

---

##### Version: 0.2b

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
- Security Checks
    - Unauthorized login attempts
    - Login attempt port ranges
    - Brute Force Login Failures
- Network Node List Size
- Reinvestment to Income Splits
- Earned Node Counter
- End of Day Summary with passive earnings and estimations
- Local Print Feature

## USAGE <a name="usage"></a>

| command | Parameter | Optional |
| ------- | :-------: | :------- | 
| python3 automation.py | `alert` `report` `auto` | -p, & |

> `&` will run the system in the background until `ctl-c` performed.

| CLI Parameter | Description |
| :-------------: | :--------- | 
| **auto** | This will start the program and continue running until `ctl-c` is executed, or the job is `killed`.  It will run in the foreground, unless you use `&`. The system will use the information from the [configuration](#config) parameters.  `start_time`, `end_time`, and `int_minutes`. |
| **alert** | This will run the a system alert report once.  This allows you to run a one-time instance of the program, at the time of your choice (current moment in time when executed). |
| **report** | This will run the system and send the `end of the day` report once.  This allows you to run a one-time instance of the program, at the time of your choice. *Note: This may produce unexpected statistical results, if not run at the end of the day.* |
| **silent** | This will run the program and update log files, but will **not** alert to the user via MMS, SMS or email. |

#### Help Usage

```
usage: automation.py [-h] [-p] action

dag alerting script

positional arguments:
  action       Type of action the script will run: (auto, alert, report, or
               silent)

optional arguments:
  -h, --help   show this help message and exit
  -p, --print  print to the console instead of mms/sms, does not work with
               'auto'.
```

#### Start the program to run on a schedule via the [configuration](#config) parameters (start/stop/interval)

```
python3 automation.py auto 
```

or run it in the background

```
python3 automation.py auto &
```
> **The `auto` command will execute the `alert` command every [n](#config) `int_minutes`, between the times configured in the [interval](#config) section of the configuration
file.  At 5 minutes past the `end_time`, the `report` command will be issued.  No alerts will be sent outside of the `start_time` and `end_time`.**

#### Send out a manual alert

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
15M Load: OK@2.00
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
| DAG Price | What is the current price, based on an API call in real time. (coingecko) |
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
| 15M Load | Will show the current 15M CPU load statistics with `OK` or `WARN` based on the [configuration](#config) file setup. |
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

#### Send out manual end of day report.

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

## INSTALLATION <a name="installation"></a>

### GMAIL SETUP <a name="gmail"></a>

In order for this program to work properly, you will need to setup your Gmail account to allow incoming pushes from your Node.  

>This can also be done via Twilio; however, I will show how to do it via Gmail for the purposes of this README.   *A lot of us are still 9-5'ers and need a free avenue*.

>You will need to setup 2-factor authentication in order to allow push notifications.  If you do not want to alter your Gmail, you can either sign up for a Twilio account and use their services, or (**used for this tutorial**) you can setup a dedicated new Gmail.   

Navigate to Gmail, and setup your account *or* login to your existing account.

**TWO STEP VERIFICATION**

1. https://myaccount.google.com (*navigate here after logging in*)
1. Click on `security` from the LEFT side menu
1. Enable `2-Step Verification`
   - Go through the step-by-step to set this up (*out of scope, for this document*)

**APP PASSWORD**

1. Follow steps above to return back to the `security` page.
1. `App passwords` option should appear.
1. Click `App passwords`.
1. From the `Select App` dropdown select `other`
1. Give it a name:  *example)* **DAGemailAlerts**
1. Click `GENERATE`
1. Copy and **save** the password for later.

**PREPARE MMS EMAIL ADDRESSES**

Figure out the proper email addresses that correlate to your phone providers MMS and SMS gateways.  You will find a nice cheat sheet in the following link below. Navigate to `step 3` on the website.  

> This speaks to United States carriers, please refer to your countries carrier to complete this step.

https://www.digitaltrends.com/mobile/how-to-send-a-text-from-your-email-account/

In order to properly display the text messages, it is highly recommended to use the MMS gateway verses the SMS. 

>Standard Data Rates Will Apply

### NODE INSTALLATION <a name="nodeinstall"></a>

Log into your node  

>**NOTE**: The username of the box will be either `root` or whatever username you setup on the Node.  This was done when you set yourself up to join the constellation network.  These instructions will use a user called `nodeuser`.

Create a dedicated directory for your automation program.

If you decide to do a `git clone`, you may **not** want or need to create the `automation` folder, as git will create a new directory `constellation-node-automation` which would suffice.

Without Git Clone, create the following:
```
nodeuser@constellation-node:/# cd ~
nodeuser@constellation-node:~# mkdir automation
nodeuser@constellation-node:~# cd automation
nodeuser@constellation-node:~/automation# pwd
/nodeuser/automation
nodeuser@constellation-node:~/automation#
```

#### prerequisites <a name="prereq"></a>

You will need python3 installed.
*This program was tested on `python 3.6.9`.*
```
nodeuser@constellation-node:~# python3 --version
Python 3.6.9
```
If you get an error.
```
sudo apt-get install python3
```

You will need `pip3` installed.
```
root@constellation-node:~# pip3 --version
pip 9.0.1 from /usr/lib/python3/dist-packages (python 3.6)
```
If you get an error.
```
sudo apt-get install python3-pip
```
> Note: As of the current time, this program uses default Python libraries, so *pip* may not be needed, as of this version of the automation program.  Future releases may require *pip*, so installation is recommended. 

### IMPORTANT
**The constellation installation is expected to be in the root of your node's user's home directory.**

```
nodeuser@constellation-node:~/constellation# pwd
/nodeuser/constellation
nodeuser@constellation-node:~/constellation#
```

> You cannot run a `report` until an `alert` has been run.

**Ready to install program**

**`git clone`** this project onto your node (recommended) **or**, copy the necessary files over to your `/nodeuser/automation` directory. (*how to clone the git repo is out of scope of this documentation.*)

File structure should appear as follows:
```
automation
├── dag_count.log
├── __init__.py
├── automation.py
├── classes
│   │   ├── __init__.py
│   │   ├── check_dag_status.py
│   │   ├── config_obj.py
│   │   ├── core.py
│   │   ├── error_log_check.py
│   │   ├── reports.py
│   │   └── send_sms_email.py
├── configs
│   │   ├── config.example.yaml
├── logs
│   │   ├── __init__.py
│   │   ├── dag_count.log
```

> You will need to rename the `config.example.yaml` file to `config.yaml` and update with correct [settings](#config). Configuration setup is discussed in the next section.

## CONFIGURATION <a name="config"></a>

Rename `config.example.yaml` to `config.yaml`. Navigate to your `config.yaml` file and open with your favorite editor.  
You **MUST** update this file in order for the program to function properly.

>This is the **ONLY** file that you should be manipulating.  All other files in this program should be left alone.

```
configuration:
  email:
    gmail_acct: gmail_source_email@gmail.com
    gmail_token: gmail_app_password
    mms_recipients:
        - 111111111@provider.gateway.net
        - 222222222@provider.gateway.net
        - whoever@whoever.com
  constraints:
    error_max: 20
    memory_swap_min: 200000
    security_check: true
    uptime_threshold: 30
    load_threshold: 40
  intervals:
    start_time: '07:00'
    end_time: '20:00'
    int_minutes: 15
  splits:
    enabled: true
    split1: 0.7
    split2: 0.3
  collateral:
    enabled: true
    node_count: 2
  report_estimates:
    - .1
    - .5
    - 1
    - 3
    - 5
    - 10
    - 50
    - 100
```

#### Configuration file parameter details <a name="parms"></a>

| Section | Parameter | Description | Value type/Format | Default | Required |
| ------- | :-------: | :---------- | :-----: | :-----: | :---: |
| **email** | | email parameters needed for program to function properly.
| - | `gmail_acct` | Gmail account you created or used in the [Setup Gmail](#gmail) section. | - | - | yes
| - | `gmail_token` | Password you saved in the [App Password](#gmail) section. | - | - | yes
| - | `mms_recipients` | Making sure you leave the `-` and indentation unchanged, add in your mobile number and/or email addresses where you want to send the reports.  If you only have `1` email, you can remove the extra list item(s).  If you have more than `2`, you can add in as many list entries (starting with a dash) as you like.  **NOTE**: *It is unknown how many requests will be accepted/allowed by Gmail or your mobile provider, so you may need to be cognizant of this when setting up complex lists of email recipients.* | - | - | yes
| **constraints** |  | This section should only be modified by more advanced users.  It allows you to manipulate several program thresholds.|
| - | `error_max` | <a name="error_threshold"> How many errors should accumulate in the constellation log file before notifying in an alert.  **Note**: *The constellation log file is configured to roll, so the low error count is justified and only pertains to the current log.* | decimal | `20` | no
| - | `memory_swap_min` | Low end threshold before alerting that memory or swap is low.  The same decimal is used to check both.  Memory and Swap are independently checked. | decimal | `100000` | no
| - | `security_check` | Do you want the system to count unauthorized access requests and ports. | boolean | `false` | no
| - | `uptime_threshold` | Number of days of uptime the server/node/instance has been running.  *Recommendation is to reboot after monthly patches* | int | `30` | no
| - | `load_threshold` | Percentage of CPU load you want to warn against when threshold is exceeded. *interger represented as a percentage* | int | `40` | no
| **intervals** |  | Setup when you want the alerts to start/stop being pushed to your `mms_email_recipients`. |
| - | `start_time` | 24 hour clock notation - currently adheres to the systems local time zone.  When do you want the alerting to start each day? If you want the program to run 24/7, make your start time and end time '00:00'  **IMPORTANT**: The time needs to be surrounded by quotes. *Note: Stat calculations are rounded to the lowest hour.* | 'HH:MM' | `'07:00'` | no
| - | `end_time` | 24 hour clock notation - local time zone.  When do you want the alerting to stop each day? **IMPORTANT**: The time needs to be surrounded by quotes. *Note: Stat calculations are rounded to the lowest hour.* | 'HH:MM' | `'20:00'` | no
| - | `int_minutes` | How often do you want text messages to be pushed out to your recipients? Must be in 5 minute increments (10,15,1440).  Can not be over 1440. If you need something more specific, utilize the CRON (see [Alternative Cron](#alt_cron)). Please be aware that a shorter interval could cause your provider to block your source account.  *Recommendation*: no less than every 15 minutes, system restriction to 10 minutes. | MM | `30` | no
| **splits** | | This section is an optional configuration. When enabled, this feature will break out rewards/income into percentages between `split1` and `split2`.  When added together this should equal 1 (100%), otherwise calculations will not be accurate.  `Example`: You want to calculate how much of your income will be used for reinvestment (split1) verses taking profits (split2). |
| - | `enabled` | Enable this feature. | boolean | `false` | yes
| - | `split1` | Float number less than 1. Split1 and Split2 must equal 1 in order for accurate calculations. | float | - | if enabled
| - | `split2` | Float number less than 1. Split1 and Split2 must equal 1 in order for accurate calculations. | float | - | if enabled
| **collateral** | | This section is an optional configuration. When enabled, this feature will calculate your current collateral as it relates to the 250K USD requirement for obtaining a new node. |
| - | `enabled` | Enable this feature. | boolean | `false` | yes 
| - | `node_count` | ***INCLUDING THIS NODE***. <a name="node_count"></a> How many nodes do you own that you want to include in the collateral calculations?  Note: Until the program couples with other node reward/income statistics, this will not include the reward/income from the other nodes, only the node's collateral itself. AKA: `enabled` with `node_count: 2` means you have 2 nodes all together including this node, that you want to count in your collateral calculations. | int | `1` | if enabled  
| **reports** | | This section is an optional configuration. When enabled, this feature will calculate your estimated earnings for the node, based on the prices allocated in the `estimates` list provided. |
| - | `enabled` | Enable this feature. | boolean | `false` |  yes
| - | `estimates` | $USD that you want to have the $DAG count translated into for the `end of day` report. *Note*: Make sure to leave the `-` in front of each list item.  You can have as many as you deem necessary, or you can remove list items that aren't wanted/needed. *The program will automatically remove estimates that are lower than the @report time USD/DAG price.* | float | `.50`, `1`, `5`, `10`, `100` |  no 

> **Warning**: When entering in the `start_time` and `end_time` parameters, if `start_time` is after the `end_time` the system will revert to defaults (see above), instead of erroring out.

> The program will check if the `config.yaml` has been updated by the user every `int_minutes`.  Therefore, any changes will **not** take affect until the next `int_minutes` interval is reached.

#### SETUP CRON JOB <a name="cron"></a>

*BASED ON A DIGITAL OCEAN NODE - UBUNTU 18.04*

Setup the crontab on your system to start the program at reboot.

> **NOTE**: This is if you want the program to run on startup and alert; based on the settings in the configuration file.  If you do not want to do it this way, you can see the [alternative option](#alt_cron) to run via the crontab iteratively, verses running the program in the background.

```
nodeuser@constellation-node:/# crontab -e
```

Add the following to the bottom of the file.  see [usage section](#usage) for details.  

> Leave the `[...]` out, it is just an indication that other code is probably seen above (or below) the line you need to enter.

```
[...]
@reboot /usr/bin/python3 /nodeuser/automation/automation.py auto >> ~/cron.log 2>&1
```

Start the program manually, because you don't want to reboot.  The first alert will not appear until the designated interval:

```
nodeuser@constellation-node:~# nohup python3 automation.py auto &
```

##### Alternative CRON Method <a name="alt_cron">

```
nodeuser@constellation-node:/# crontab -e
```

You can run crontab code as follows:

> **note**: You are using `alert` and `report` verses `auto`.

```
[...]
*/15    07-19   *       * *     /usr/bin/python3 /nodeuser/automation/automation.py alert >> ~/cron.log 2>&1
0          20   *       * *     /usr/bin/python3 /nodeuser/automation/automation.py alert >> ~/cron.log 2>&1
5          20   *       * *     /usr/bin/python3 /nodeuser/automation/automation.py report >> ~/cron.log 2>&1
```

**line 1**:  Every 15 minutes between 07:00 and 19:45 of every day, every month, every year, run the program with the `alert` argument.

**line 2**: Start of the hour at 20:00 run the program once, every day, every month, every year... with the `alert` argument.

**line 3**: Five minutes past the 20:00 hour, run the program with the `report` argument.

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

[back to beginning of document](#top)

---

hgtp://netmet
