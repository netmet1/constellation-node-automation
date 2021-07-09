from datetime import datetime, timedelta
import os
import yaml

class Config():

    def __init__(self,dag_args):

        self.dag_args = dag_args
        self.path = os.path.dirname(__file__)
        
        self.config = {}
        
        self.config = self.pull_configuration()
        self.setup_variables()
        self.setup_flags()
        self.config_default_check()
        self.setup_dates_times()

    def reload_needed(self):
        new_config = self.pull_configuration()
        if new_config == self.config:
            # nothing changed
            return False
        else:
            # something changed
            return True


    def pull_configuration(self):
        # uses return in order to be able to check for changes
        config_file = self.path.replace("classes","configs/config.yaml")
        with open(config_file,'r') as stream:
            try:
                config = yaml.safe_load(stream)
                config = config["configuration"]
            except yaml.YAMLError as exc:
                print(exc)

        return config


    def setup_dates_times(self):
        self.current_date = datetime.now().strftime("%Y-%m-%d")

        try:
            start = datetime.strptime(self.config['intervals']['start_time'], "%H:%M")
        except:
            start = datetime.strptime("07:00", "%H:%M")
        try:
            end = datetime.strptime(self.config['intervals']['end_time'], "%H:%M")
        except:
            end = datetime.strptime("20:00","%H:%M")

        if start > end:
            start = datetime.strptime("07:00", "%H:%M")
            end = datetime.strptime("20:00","%H:%M")
        elif start == end:
            start = datetime.strptime("00:00", "%H:%M")
            end = datetime.strptime("23:50", "%H:%M") # leave time for report feature

        self.start_time = start - timedelta(minutes=start.minute % 15)
        self.end_time = end - timedelta(minutes=end.minute % 15)
        self.report_time = self.end_time + timedelta(minutes=5)

        self.day_time_frame = f"{end.hour - start.hour} Hours {end.minute - start.minute} Minutes"
        self.day_run_hours = end.hour - start.hour

        # All calculations are done, remove date from times
        self.start_time = self.start_time.time()
        self.end_time = self.end_time.time()
        self.report_time = self.report_time.time()


    def setup_variables(self):
        self.action = self.dag_args.Action
        self.last_run = "never"
        self.dag_log_file = self.path.replace("classes","logs/dag_count.log")
        self.mms_email_recipients = self.config['email']['mms_recipients']
        self.email = self.config['email']['gmail_acct']
        self.token = self.config['email']['gmail_token']
        self.error_max = self.config['constraints']['error_max']
        self.mem_swap_min = self.config['constraints']['memory_swap_min']
        self.uptime = self.config['constraints']['uptime_threshold']
        self.load = self.config['constraints']['load_threshold']        
        self.username = self.config['email']['node_username']
        self.split1 = self.config['splits']['split1']
        self.split2 = self.config['splits']['split2']
        self.collateral_nodes = self.config['collateral']['node_count']
        self.report_estimates = self.config['report']['estimates']
        self.alert_interval = self.config['intervals']['int_minutes']
        self.silence_email = False
        self.silence_writelog = False
        self.local = False
        self.create_report = False

    def setup_flags(self):
        if self.action == "silent":
            self.silence_email = True
            self.silence_writelog = False
            self.local = False
            self.create_report = False
        elif self.action == "report":
            if self.dag_args.print is True:
                self.silence_email = True
                self.local = True
            else:
                self.silence_email = False
                self.local = False
            self.create_report = True
            self.silence_writelog = True
        elif self.action == "alert":
            if self.dag_args.print is True:
                self.silence_email = True
                self.local = True
            else:
                self.silence_email = False
                self.local = False
            self.create_report = False
            self.silence_writelog = False
        else: 
            # self.action is auto
            self.silence_email = False
            self.local = False
            self.create_report = False
            self.silence_writelog = False

        self.security_enabled= self.config['constraints']['security_check']
        self.splits_enabled = self.config['splits']['enabled']
        self.report_enabled = self.config['report']['enabled']
        self.collateral_enabled = self.config['collateral']['enabled']


    def config_default_check(self):
        try:
            int(self.error_max)
        except:
            self.error_max = 20
        else:
            if self.error_max == -1:
                self.error_max = 20

        try:
            int(self.mem_swap_min)
        except:
            self.mem_swap_min = 1000000
        else:
            if self.mem_swap_min == -1:
                self.mem_swap_min = 1000000
 
        try:
            int(self.alert_interval)
        except:
            self.alert_interval = 30  # default
        else:
            self.alert_interval = 5 * round(self.alert_interval/5) # round to nearest 5
            if self.alert_interval > 1440:
                self.alert_interval = 1440
            elif self.alert_interval < 10:
                self.alert_interval = 10

        try:
            int(self.uptime)
        except:
            self.uptime = 30
        else:
            if self.uptime == -1:
                self.uptime = 30
        finally:
            self.uptime = int(self.uptime)
 
        try:
            float(self.load)
        except:
            self.load = 40
        else:
            if self.load == -1 or self.load > 1:
                self.load = 40
        finally:
            self.load = float(self.load)
 
        try:
            float(self.split1)
        except:
            self.splits_enabled = False

        try:
            float(self.split2)
        except:
            self.splits_enabled = False

        try: 
            int(self.collateral_nodes)
        except:
            self.collateral_enabled = False

        if not isinstance(self.mms_email_recipients,list): 
            print("no recipients have been specified, or error in config.yaml.  Please see README.md")
            exit(1)

        if self.email == "" or self.email == None or not isinstance(self.email,str):
            print("no source sender email allocated in config.yaml. Please see README.md")
            exit(1)

        if self.token == "" or self.token == None or not isinstance(self.token,str):
            print("no source sender email token (password) allocated in config.yaml. Please see README.md")
            exit(1)

        if not isinstance(self.security_enabled,bool): 
            self.security_enabled = False

        if not isinstance(self.splits_enabled,bool): 
            self.splits_enabled = False

        if not isinstance(self.report_enabled,bool): 
            self.report_enabled = False

        if not isinstance(self.report_estimates,list): 
            if self.report_enabled:
                self.report_estimates = [.5,1,5,10,100]


if __name__ == "__main__":
    print("This class module is not designed to be run independently, please refer to the documentation")



