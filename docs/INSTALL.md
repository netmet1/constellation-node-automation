# CONSTELLATION INSTALLATION<a name="top">

## Node Operator Datapreneuer Alerting Automation Program

---

1. [Installation](#installation)
    1. [Setup Gmail](#gmail)
        1. [2FA](#2fa)
        1. [Create API password/token](#password)
        1. [Prepare SMS Emails](#prepare_email)
    1. [Node Automation Installation](#nodeinstall)
        1. [Manual Node Automation Installation](MANUAL_INSTALL.md)
    1. [Node Upgrade](#nodeupgrade)
    1. [Post configuration Testing](#tests)


## INSTALLATION <a name="installation"></a>

### GMAIL SETUP <a name="gmail"></a>

In order for this program to work properly, you will need to setup your Gmail account to allow incoming pushes from your Node.  

>You will need to setup 2-factor authentication in order to allow push notifications.  If you do not want to alter your Gmail, you can setup a dedicated new Gmail.   

Navigate to Gmail, and setup your account *or* login to your existing account.

**TWO STEP VERIFICATION** <a name="2fa">

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
1. Copy and **save** the password for later (**do not lose**).

**PREPARE MMS EMAIL ADDRESSES** <a name="prepare_email">

Figure out the proper email addresses that correlate to your phone providers MMS and SMS gateways.  You will find a nice cheat sheet in the following link below. Navigate to `step 3` on the website.  

> This speaks to United States carriers, please refer to your countries carrier to complete this step.

https://www.digitaltrends.com/mobile/how-to-send-a-text-from-your-email-account/

In order to properly display the text messages, it is highly recommended to use the MMS gateway verses the SMS. 

>Standard Data Rates Will Apply

## NODE AUTOMATION INSTALLATION <a name="nodeinstall"></a>

**This will `ONLY` work with the Ubuntu Distro, as required by the Constellation Network's Node installation documentation.**
> If you are running on another Linux distro, please refer to the [MANUAL_INSTALL.md](MANUAL_INSTALL.md) file.

1. Log into your node  
1. Download the `adminauto` installation script.
    1. copy and paste command below
    ```
    cd ~
    ```
    ```
    wget https://github.com/netmet1/constellation-node-automation/releases/download/v2.0.2/adminauto -O /usr/local/bin/adminauto; chmod +x /usr/local/bin/adminauto
    ```

1. Issue the following command and follow the prompts
    ```
    adminauto -i
    ```

## NODE AUTOMATION UPGRADE <a name="nodeupgrade"></a>
1. Log into your node
1. Issue the following command and follow the prompts
    ```
    adminauto -i
    ```

## POST INSTALLATION TESTING

> The following test will work regardless whether you started the automation program to run under your preferred schedule, at the end of the installation.

1. test alerts to console
    ```
    adminauto -a -p
    ```
1. test alerts to sms and/or email (depending on how you set up the program)
    ```
    adminauto -a
    ```
1. test health check to console
    ```
    adminauto -l -p
    ```
1. Test health check to sms and/or email (depending on how you set up the program)
    ```
    adminauto -l -p
    ```

---
DAG $DAG it! If you node you node.

[back to beginning of document](#top)

!enod

---

hgtp://netmet
