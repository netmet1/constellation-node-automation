# CONSTELLATION MANUAL INSTALLATION <a name="top">

## Node Operator Datapreneuer Alerting Automation Program

1. [Installation](#installation)
    1. [Preparation](#prep)
    1. [Prerequisites](#prereq)
    1. [Automation Node Software Installation](#doinstall)
    1. [Configuration](README.md)
        1. [Manual Configuration](#manual_config)
    1. [Post configuration Testing](#tests)
1. [CRON setup](#cron)
1. [Upgrade](#upgrade)

# WARNING !!! MANUAL INSTALLATION DISCOURAGED.

> **As of `version 2.0` of this program, manual installation is discouraged.  The [INSTALL.md](INSTALL.md) has been updated to reflect this update, and the detailed manual instructions have been moved to this file.  To keep everything standardized and assist in more seamless upgrades in future releases, a installation script has been created.  This also eases the extra work necessary to start, restart and stop the program.  Configuration is offered as a quick step-by-step process.**

Version 2.0 is the first non-beta release of this software.

#### PREPARATION <a name="prep">
Before continuing you will need to have a Gmail account setup to receive emails from this program through Gmails API and push those notifications to other email address or SMS/MMS destinations.

Please follow the procedure in the [INSTALL.md](INSTALL.md), then you can return to this page.

>**NOTE**: The username of the box will be either `root` or whatever username you setup on the Node.  This was done when you set yourself up to join the constellation network.  These instructions will use a user called `nodeuser`.

> If you decide to do a `git clone`, please pick a location to install your clone, at your own discretion.  

**These instructions are designed to run on `Ubuntu 18.04` (*> 18.04 should work as well*) which was the set requirement when setting up the Node via the Constellation Networks requirement documentation.  If you are running this on another distribution, please change the commands to match your specific distro.**

---

#### Prerequisites <a name="prereq"></a>

> If you get a insufficient privileges error, you may need to include `sudo` at the beginning of some of your commands.  Visa-Versa, if you get an error using the `sudo` prefex, you might need to remove the `sudo` from the beginning of the command.

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
If you get an error. (*bash: python3: command not found*)
```
sudo apt-get install -y python3
```
*Note: `-y` will avoid confirming if you want to install the program*. If your node has a version **less than** 3.6.9, it is unknown what will and will not work?  Any other version 3 patch level above 3.6.9, should work.

You will need `pip3` installed. *Python 3's Preferred Installer Packages*.
```
root@constellation-node:~# pip3 --version
pip 9.0.1 from /usr/lib/python3/dist-packages (python 3.6)
```
If you get an error.
```
sudo apt-get install -y python3-pip
```

Check that the proper Python packages are installed
```
pip3 freeze | grep -i pytz
```
If this command results in empty output
```
pip3 install pytz
```
Next...
```
pip3 freeze | grep -i requests
```
If this command results in empty output
```
pip3 install requests
```
Next...
```
pip3 freeze | grep -i yaml
```
If this command results in empty output
```
pip3 install pyyaml
```

### IMPORTANT
**The constellation node validator software/installation is expected to be in the root of your node's user's home directory.**

> Note: The size of some of the directories, permission structure, etc. may not match exactly.  You just need to make sure the basic elements in each command check are there.  *Example) For the next command, you only need to make sure `constellation` is listed as a directory.  The size, dates, etc. do not matter.*

1. Check to make sure your **constellation** program is installed on your node.
```
nodeuser@constellation-node:~# cd ~
nodeuser@constellation-node:~/# ls -l
total 64
drwxr-xr-x 3 root root  4096 Jul 20 19:08 ./
drwxr-xr-x 6 root root  4096 Jul 20 19:00 ../
-rwxr-xr-x 1 root root  2498 Mar  2 10:59 config-security
drwxr-xr-x 4 root root  4096 Jul 19 12:45 constellation
nodeuser@constellation-node:/#
```

2. Return to the root of your home directory. <a name="install_step2">
```
nodeuser@constellation-node:/# cd ~
nodeuser@constellation-node:~/# pwd
/nodeuser
nodeuser@constellation-node:~/#
```

## READY TO INSTALL THE PROGRAM <a name="doinstall">

> In this section, if you see multiple lines of `commands` they are meant to be run separately, one at a time.

4. Grab the latest release of the program from the github (here) repository: `releases` section

**MAKE SURE YOU DOWNLOAD THE CORRECT VERSION (LATEST).** (example shows v2.0)
**THIS MAY NOT BE THE CURRENT VERSION: This document will only be updated when the procedure changes.**
```
wget https://github.com/netmet1/constellation-node-automation/archive/refs/tags/v2.0.tar.gz
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
-rw-r--r-- 1 root root 20196 Jul 20 19:08 v2.0.tar.gz
nodeuser@constellation-node:~#
```
> **You will see `v2.0.tar.gz` as a new file**

6. Extract the contents, which will create a dedicated directory
```
tar -xvf v2.0.tar.gz
```

7. Verify the extraction.  
    - The content results might not (probably won't) match up perfectly with below, important part is to make sure the **`constellation-node-automation-2.0`** where the `2.0` matches the current version no. is there.
```
nodeuser@constellation-node:~# ll
total 64
drwxr-xr-x 3 root root  4096 Jul 20 19:08 ./
drwxr-xr-x 6 root root  4096 Jul 20 19:00 ../
-rwxr-xr-x 1 root root  2498 Mar  2 10:59 config-security
drwxr-xr-x 4 root root  4096 Jul 19 12:45 constellation
drwxrwxr-x 5 root root  4096 Jul 16 13:11 constellation-node-automation-2.0/
-rw-r--r-- 1 root root 20196 Jul 20 19:08 v2.0.tar.gz
nodeuser@constellation-node:~#
```

8. *Optional*: Verify the contents
```
cd constellation-node-automation-2.0
ll
```

File structure should appear as follows:  

> Note: *You will not see it this way, but you can navigate around to check that it is correct*

```
automation
├── dag_count.log
├── __init__.py
├── adminauto
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
├── docs
│   │   ├── INSTALL.md
│   │   ├── MANUAL_INSTALL.md
│   │   ├── TS_USAGE.md
├── functions
│   │   ├── search_timezones.py
├── logs
│   │   ├── __init__.py
│   │   ├── dag_count.log
├── templates
│   │   ├── template.yaml
```

9. Copy the `adminauto` script to your user's bin directory.
```
cp adminauto /usr/local/bin
```

## MANUAL CONFIGURATION <a name="manual_config">

10. Copy the `config.example.yaml` file to `config.yaml`.  *This will allow you to keep the example handy.*
```
cd ~/constellation-node-automation-2.0/configs/
cp config.example.yaml config.yaml
```

### IMPORTANT: REFER TO THE [README.md](README.md) and follow the link to the CONFIGURATION section. 

Open the README.md in a separate window for ease of use!

11. Update the `config.yaml` with the correct settings from the configuration section of the [README](README.md).

    1. For ease of use, we will use `nano` for the next steps.  If you are savvy already, make the necessary changes using our favorite Linux editor.
        1. Open the configuration file for editing
            ```
            nano config.yaml
            ```
        1. Like a normal text editor add, update, modify the configuration.  
        1. This will require the [password you created from the GMAIL app section](INSTALL.md#password)
        1. **BE CAREFUL NOT TO MESS UP THE INDENTATION AND ADD EVERYTHING CORRECTLY (go slow)**
        1. Hit control and x  (`clt-x`)
        1. Choose `Y` to save
        1. Return to the root of your home directory.
            ```
            cd ~
            ```

12. Learn the usage and all necessary details from the [README](README.md).

13. ***Optional***: Clean up your file original install tar package file, to preserve space.
```
cd ~
rm v2.0.tar.gz
```

### QUICK TESTS <a name="tests">

14. Give the script a quick spin... 

```
cd ~/constellation-node-automation-2.0/
python3 automation.py alert -p
```
After a few seconds to waiting... alert message will appear on the screen!

```
cd ~/constellation-node-automation-2.0/
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

Add the following to the bottom of the file.  see [usage section](README.md#usage) for details.  

> Leave the `[...]` **out**, it is just an indication that other code is probably seen above (or below) the line you need to enter.

## Change `nodeuser` to whatever your username is!

```
[...]
@reboot /usr/bin/python3 /nodeuser/constellation-node-automation-2.0/automation.py auto >> ~/cron.log 2>&1
```

Now we have to start the program manually, because you don't want to have to actually reboot.  The first alert will not appear until the designated interval:

> **Warning**: If you decide to use the `adminauto` script after manual installations, the directory setup will change.  Important that you review your system installation before going between `manual` and `adminauto` configurations and setups.

start the program manually... 
```
nodeuser@constellation-node:~# nohup python3 automation.py auto &
```

### Alternative CRON Method <a name="alt_cron">

**WHY?** Because if you can alter the times in a staggered fashion, instead of just a single `start_time` and `end_time`.  

> **EXAMPLE**: Run the program between the hours of X and X, then stop, then run it again between X and X, then stop, then run only once at this time, report here and there... etc.  You can also setup health-checks to run at specific times as well manually.  Simply disable health-checks in the configuration, and setup a manual health-check in the CRON.

```
nodeuser@constellation-node:/# crontab -e
```

You can run crontab code as follows:

> **note**: You are using `alert`, `health`, and `report` verses `auto`.

```
[...]
*/15    07-19   *       * *     /usr/bin/python3 /nodeuser/constellation-node-automation-2.0/automation.py alert >> ~/cron.log 2>&1
0          20   *       * *     /usr/bin/python3 /nodeuser/constellation-node-automation-2.0/automation.py alert >> ~/cron.log 2>&1
5          20   *       * *     /usr/bin/python3 /nodeuser/constellation-node-automation-2.0/automation.py report >> ~/cron.log 2>&1
```

**line 1**:  Every 15 minutes between 07:00 and 19:45 of every day, every month, every year, run the program with the `alert` argument.

**line 2**: Start of the hour at 20:00 run the program once, every day, every month, every year... with the `alert` argument.

**line 3**: Five minutes past the 20:00 hour, run the program with the `report` argument.

[back to beginning of document](#top)

---

## UPGRADE EXISTING INSTALLATION <a name="upgrade"></a>

When a new version of the software is released...

### IMPORTANT IF YOU DID NOT FOLLOW THE INSTRUCTIONS FOR INSTALLATION ABOVE (ORIGINALLY) YOU NEED TO MODIFY THE FOLLOWING INSTRUCTIONS TO MEET YOUR CUSTOM INSTALLATION...  

1. Follow steps **`2`** through **`9`** from the [installation](#install_step2) section above.  Do **NOT** do step #10 from above!

2. Do a directory listing to remind yourself what the last version of the program installed was, and mark it down.
```
nodeuser@constellation-node:~# ll
total 64
drwxr-xr-x 3 root root  4096 Jul 20 19:08 ./
drwxr-xr-x 6 root root  4096 Jul 20 19:00 ../
-rwxr-xr-x 1 root root  2498 Mar  2 10:59 config-security
drwxr-xr-x 4 root root  4096 Jul 19 12:45 constellation
drwxrwxr-x 5 root root  4096 Jul 16 13:11 constellation-node-automation-1.2b/
drwxrwxr-x 5 root root  4096 Jul 21 08:22 constellation-node-automation-2.0/
nodeuser@constellation-node:~#
```
In this case, the last version was `v1.2b`

3. Read the `release notes` in the [README](README.md) to determine if anything has changed in the `config.yaml` file.  **It may be common for the configuration to change from version to version.**  This allows for new features, that may or may not need user intervention to work for each particular case. 

4. If there are **NO** changes to the `config.yaml` needed:  *Using the example that **v1.2b** was the last version.*  

### Version 2.0 has configuration file changes, so if you moving from `1.2` to `2.0`, please be aware this is JUST AN EXAMPLE!

```
cd ~
cp constellation-node-automation-1.2b/configs/config.yaml constellation-node-automation-2.0/configs/config.yaml
nodeuser@constellation-node:~#
```
Otherwise **skip to #5**.

If you needed step #4, **Skip to #6**.

5. **If changes to the `config.yaml` file were discovered in the [README](README.md).**

    1. Copy over the config example file to the new version config file in the new installation.
        ```
        cp constellation-node-automation-2.0/configs/config.example.yaml constellation-node-automation-2.0/configs/config.yaml
        ```
    1. Print the contents of your original (old version) config file to the terminal.
        ```
        cat constellation-node-automation-1.2b/configs/config.yaml
        ```
    1. Copy the contents to your home computer into NotePad or whatever text editor you use.  *Alternatively, you can open another terminal window side-by-side, navigate back to the correct directory, and continue.*
    1. Change directory to the configuration DIR of your new version.
        ```
        cd constellation-node-automation-2.0/configs/
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
cp constellation-node-automation-1.2b/logs/* constellation-node-automation-2.0/logs/
```

!enod

---
DAG $DAG it! If you node you node.

[back to beginning of document](#top)

---

hgtp://netmet