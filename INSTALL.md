# CONSTELLATION <a name="top">

## Node Operator Datapreneuer Alerting Automation Program

---

1. [Installation](#installation)
    1. [Setup Gmail](#gmail)
    1. [Node Installation](#nodeinstall)
    1. [Prerequisites](#prereq)
    1. [Setup correct Timezone](#clocksetup)
    1. [Operator Node Software Installation](#doinstall)
    1. [Post configuration Testing](#tests)
1. [CRON setup](#cron)
1. [Upgrade](#upgrade)

## INSTALLATION <a name="installation"></a>

### GMAIL SETUP <a name="gmail"></a>

In order for this program to work properly, you will need to setup your Gmail account to allow incoming pushes from your Node.  

>You will need to setup 2-factor authentication in order to allow push notifications.  If you do not want to alter your Gmail, you can setup a dedicated new Gmail.   

Navigate to Gmail, and setup your account *or* login to your existing account.

**TWO STEP VERIFICATION**

1. https://myaccount.google.com (*navigate here after logging in*)
1. Click on `security` from the LEFT side menu
1. Enable `2-Step Verification`
   - Go through the step-by-step to set this up (*out of scope, for this document*)

**APP PASSWORD** <a name="password">

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

## NODE INSTALLATION <a name="nodeinstall"></a>

Log into your node  

>**NOTE**: The username of the box will be either `root` or whatever username you setup on the Node.  This was done when you set yourself up to join the constellation network.  These instructions will use a user called `nodeuser`.

> If you decide to do a `git clone`, you are probably a more advanced user, please pick a location to install your clone, at your own discretion.  


#### Prerequisites <a name="prereq"></a>

1. Verify you are in the root of your home directory.
```
nodeuser@constellation-node:/# cd ~
nodeuser@constellation-node:~/# pwd
/nodeuser
nodeuser@constellation-node:~/#
```

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
If your node has a version **less than** 3.6.9, it is unknown what will and will not work?  Any other version 3 patch level above 3.6.9, should work.

You will need `pip3` installed. *Python 3's Preferred Installer Packages*.
```
root@constellation-node:~# pip3 --version
pip 9.0.1 from /usr/lib/python3/dist-packages (python 3.6)
```
If you get an error.
```
sudo apt-get install python3-pip
```
> Note: As of the current time, this program uses default Python libraries, so *pip* may not be needed.  Future releases may require *pip*, so installation is recommended. 

### IMPORTANT
**The constellation node validator software/installation is expected to be in the root of your node's user's home directory.**
### DO NOT CHANGE ANYTHING IN THIS DIRECTORY - BE CAREFUL
```
nodeuser@constellation-node:~# cd constellation/
nodeuser@constellation-node:~/constellation# pwd
/nodeuser/constellation
nodeuser@constellation-node:~/constellation#
```

2. Return to the root of your home directory. <a name="install_step2">
```
nodeuser@constellation-node:/# cd ~
nodeuser@constellation-node:~/# pwd
/nodeuser
nodeuser@constellation-node:~/#
```

### TIMEZONE <a name="clocksetup">

#### RUNNING YOUR NODE IN `UTC` IS BEST PRACTICE, SO NOTE OF CAUTION IF YOU WANT TO CHANGE THE NODE'S TIMEZONE.

> New future version will add the option to setup your specific timezone in the `config.yaml` file.

If this concerns you, skip to step #4.

3. Make sure our node *date/time* is setup properly within our own timezone 
```
date
```
This example will fix to EST verses UTC
```
nodeuser@constellation-node:/# date
Sun Jul 25 13:04:15 UTC 2021
```
First get the correct timezone long name...
```
timedatectl list-timezones
```
results
```
nodeuser@constellation-node:/# timedatectl list-timezones
Africa/Abidjan
Africa/Accra
Africa/Addis_Ababa
Africa/Algiers
Africa/Asmara
Africa/Bamako
Africa/Bangui
Africa/Banjul
Africa/Bissau
Africa/Blantyre
Africa/Brazzaville
Africa/Bujumbura
Africa/Cairo
Africa/Casablanca
Africa/Ceuta
Africa/Conakry
Africa/Dakar
Africa/Dar_es_Salaam
[...]
```
This will be a pain to sift through, so if you are in `America` or `Europe` (as an example)... You can narrow down your search this way...
```
nodeuser@constellation-node:/# timedatectl list-timezones | grep America
```
or
```
nodeuser@constellation-node:/# timedatectl list-timezones | grep Europe
```
Mark down the closest match to your location...

Now we can change our time (our example case we want EST.  Probably different for you?)

> If you are not already `root` this may require you prefix the command with `sudo`.

```
timedatectl set-timezone America/New_York
```
Check again
```
nodeuser@constellation-node:/# date
```

## READY TO INSTALL THE PROGRAM <a name="doinstall">

> In this section, if you see multiple lines of `commands` they are meant to be run separately, one at a time

4. Grab the latest release of the program from the github (here) repository: `releases` section

**MAKE SURE YOU DOWNLOAD THE CORRECT VERSION (LATEST).** (example shows v1.0b)
```
wget https://github.com/netmet1/constellation-node-automation/archive/refs/tags/v1.0b.tar.gz
```

5. Verify that you have the file `vX.X.tar.gz` (where X.X is the version)
    - *ll is letter `L` not number `1`*
```
nodeuser@constellation-node:~# ll
total 64
drwxr-xr-x 3 root root  4096 Jul 20 19:08 ./
drwxr-xr-x 6 root root  4096 Jul 20 19:00 ../
-rwxr-xr-x 1 root root  2498 Mar  2 10:59 config-security
drwxr-xr-x 4 root root  4096 Jul 19 12:45 constellation
-rw-r--r-- 1 root root 20196 Jul 20 19:08 v1.0b.tar.gz
nodeuser@constellation-node:~#
```
> **You will see `v1.0b.tar.gz` as a new file**

6. Extract the contents, which will create a dedicated directory
```
tar -xvf v1.0b.tar.gz
```

7. Verify the extraction.  
    - The content results might not (probably won't) match up perfectly with below, important part is to make sure the **`constellation-node-automation-1.0b`** where the `1.0b` matches the current version no. is there.
```
nodeuser@constellation-node:~# ll
total 64
drwxr-xr-x 3 root root  4096 Jul 20 19:08 ./
drwxr-xr-x 6 root root  4096 Jul 20 19:00 ../
-rwxr-xr-x 1 root root  2498 Mar  2 10:59 config-security
drwxr-xr-x 4 root root  4096 Jul 19 12:45 constellation
drwxrwxr-x 5 root root  4096 Jul 16 13:11 constellation-node-automation-1.0b/
-rw-r--r-- 1 root root 20196 Jul 20 19:08 v1.0b.tar.gz
nodeuser@constellation-node:~#
```

8. *Optional*: Verify the contents
```
cd constellation-node-automation-1.0b
ll
```

File structure should appear as follows:  

> Note: *You will not see it this way, but you can navigate around to check that it is correct*

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
│   │   ├── up_monitor.py
│   │   ├── reports.py
│   │   └── send_sms_email.py
├── configs
│   │   ├── config.example.yaml
├── logs
│   │   ├── __init__.py
│   │   ├── dag_count.log
```

9. Copy the `config.example.yaml` file to `config.yaml`.  *This will allow you to keep the example handy.*
```
cd ~/constellation-node-automation-1.0b/configs/
cp config.example.yaml config.yaml
```

### IMPORTANT: REFER TO THE [README.md](README.md) and follow the link to the CONFIGURATION section. 

Open the README.md in a separate window for ease of use!

10. Update the `config.yaml` with the correct settings from the configuration section of the [README](README.md).  *Recommendation: Open the README at the same time in a different browser window.*

    1. For ease of use, we will use `nano` for the next steps.  If you are savvy already, make the necessary changes using our favorite Linux editor.
        1. Open the configuration file for editing
            ```
            nano config.yaml
            ```
        1. Like a normal text editor add, update, modify (CRUD) the configuration.  
        1. This will require the [password you created from the GMAIL app section](#password)
        1. **BE CAREFUL NOT TO MESS UP THE INDENTATION AND ADD EVERYTHING CORRECTLY (go slow)**
        1. Hit control and x  (`clt-x`)
        1. Choose `Y` to save
        1. Return to the root of your home directory.
            ```
            cd ~
            ```

11. Learn the usage and all necessary details from the [README](README.md).

12. ***Optional***: Clean up your file original install tar package file, to preserve space.
```
cd ~
rm v1.0b.tar.gz
```

### QUICK TESTS <a name="tests">

13. Give the script a quick spin... 

```
cd ~/constellation-node-automation-1.0b/
python3 automation.py alert -p
```
After a few seconds to waiting... alert message will appear on the screen!

```
cd ~/constellation-node-automation-1.0b/
python3 automation.py alert 
```
After a few seconds to waiting... the prompt should return and an MMS should finally appear on your phone (and/or email)!

[back to beginning of document](#top)

---

## SETUP CRON JOB <a name="cron"></a>

*BASED ON A DIGITAL OCEAN NODE - UBUNTU 18.04*

Now that everything is in place.  You are able to use the program from the command line to issue alerts, reports, log searches and health checks manually, at any given time.  You can also manually start the program to run continuously via the `auto` parameter (see [README](README.md)).

However, if you want the program to run on its own even after a reboot, we need to setup the crontab on your system to start the program at reboot.

> **NOTE**: This is if you want the program to run on startup and alert; based on the settings in the configuration file.  If you do not want to do it this way, you can see the [alternative option](#alt_cron) to run via the crontab iteratively, verses running the program in the background.  

```
nodeuser@constellation-node:/# crontab -e
```

Add the following to the bottom of the file.  see [usage section](#usage) for details.  

> Leave the `[...]` out, it is just an indication that other code is probably seen above (or below) the line you need to enter.

## Change `nodeuser` to whatever your username is!

```
[...]
@reboot /usr/bin/python3 /nodeuser/constellation-node-automation-1.0b/automation.py auto >> ~/cron.log 2>&1
```

Now we have to start the program manually, because you don't want to have to actually reboot.  The first alert will not appear until the designated interval:

### OPTION 1
use the adminauto.sh script included with this program
```
nodeuser@constellation-node:~# . adminauto.sh -s
```

#### OPTION 2 
start the program manually...
```
nodeuser@constellation-node:~# nohup python3 automation.py auto &
```

### Alternative CRON Method <a name="alt_cron">

**WHY?** Because if you can alter the times in a staggered fashion, instead of just a single `start_time` and `end_time`.  

*AKA:* Run the program between the hours of X and X, then stop, then run it again between X and X, then stop, then run only once at this time, report here and there... etc.  You can also setup health-checks to run at specific times as well manually.  Simply disable health-checks in the configuration, and setup a manual health-check in the CRON.

```
nodeuser@constellation-node:/# crontab -e
```

You can run crontab code as follows:

> **note**: You are using `alert`, `health`, and `report` verses `auto`.

```
[...]
*/15    07-19   *       * *     /usr/bin/python3 /nodeuser/constellation-node-automation-1.0b/automation.py alert >> ~/cron.log 2>&1
0          20   *       * *     /usr/bin/python3 /nodeuser/constellation-node-automation-1.0b/automation.py alert >> ~/cron.log 2>&1
5          20   *       * *     /usr/bin/python3 /nodeuser/constellation-node-automation-1.0b/automation.py report >> ~/cron.log 2>&1
```

**line 1**:  Every 15 minutes between 07:00 and 19:45 of every day, every month, every year, run the program with the `alert` argument.

**line 2**: Start of the hour at 20:00 run the program once, every day, every month, every year... with the `alert` argument.

**line 3**: Five minutes past the 20:00 hour, run the program with the `report` argument.

[back to beginning of document](#top)

---

## UPGRADE EXISTING INSTALLATION <a name="upgrade"></a>

When a new version of the software is released...

### IMPORTANT IF YOU DID NOT FOLLOW THE INSTRUCTIONS FOR INSTALLATION ABOVE (ORIGINALLY) YOU NEED TO MODIFY THE FOLLOWING INSTRUCTIONS TO MEET YOUR CUSTOM INSTALLATION...  

1. Follow steps **`2`** through **`7`** from the [installation](#install_step2) section above.  Do **NOT** do step #8 from above!

2. Do a directory listing to remind yourself what the last version of the program installed was, and mark it down.
```
nodeuser@constellation-node:~# ll
total 64
drwxr-xr-x 3 root root  4096 Jul 20 19:08 ./
drwxr-xr-x 6 root root  4096 Jul 20 19:00 ../
-rwxr-xr-x 1 root root  2498 Mar  2 10:59 config-security
drwxr-xr-x 4 root root  4096 Jul 19 12:45 constellation
drwxrwxr-x 5 root root  4096 Jul 16 13:11 constellation-node-automation-0.5b/
drwxrwxr-x 5 root root  4096 Jul 21 08:22 constellation-node-automation-1.0b/
nodeuser@constellation-node:~#
```
In this case, the last version was `v0.5b`

3. Read the `release notes` in the [README](README.md) to determine if anything has changed in the `config.yaml` file.  **It may be common for the configuration to change from version to version.**  This allows for new features, that may or may not need user intervention to work for each particular case.

4. If there are **NO** changes to the `config.yaml` needed:  *Using the example that **v0.5b** was the last version.*  

```
cd ~
cp constellation-node-automation-0.5b/configs/config.yaml constellation-node-automation-1.0b/configs/config.yaml
nodeuser@constellation-node:~#
```
Otherwise **skip to #5**.

If you needed step #4, **Skip to #6**.

5. If changes to the `config.yaml` file were discovered in the [README](README.md).
    1. Copy over the config example file to the new version config file in the new installation.
        ```
        cp constellation-node-automation-1.0b/configs/config.example.yaml constellation-node-automation-1.0b/configs/config.yaml
        ```
    1. Print the contents of your original (old version) config file to the terminal.
        ```
        cat constellation-node-automation-0.5b/configs/config.yaml
        ```
    1. Copy the contents to your home computer into NotePad or whatever text editor you use.  *Alternatively, you can open another terminal window side-by-side, navigate back to the correct directory, and continue.*
    1. Change directory to the configuration DIR of your new version.
        ```
        cd constellation-node-automation-1.0b/configs/
        ```
    1. For ease of use, we will use `nano` for the next steps.  If you are savvy already, make the necessary changes using our favorite Linux editor.
        1. Open the configuration file for editing
            ```
            nano config.yaml
            ```
        1. Like a normal text editor add, update, modify (CRUD) the configuration from your old config that you copied to a local computer.  **Also verify and update any necessary new configuration details.**
        1. **BE CAREFUL NOT TO MESS UP THE INDENTATION AND ADD EVERYTHING CORRECTLY (go slow)**
        1. Hit control and x  (CLT-X)
        1. Choose `Y` to save
        1. Return to the root of your home directory.
            ```
            cd ~
            ```

---

6. **IMPORTANT STEP** move over your log file.  **In a future release, logging will be added and moved to a directory that will (hopefully) obfuscate this step.**
```
cp constellation-node-automation-0.5b/logs/* constellation-node-automation-1.0b/logs/
```

[back to beginning of document](#top)

---

hgtp://netmet
