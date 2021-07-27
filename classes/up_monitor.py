import requests
from datetime import datetime, timedelta, time

class UpMonitor():

    def __init__(self,config):
        self.config = config

        # done here instead of config obj to maintain status consistency
        # for the session
        self.health_node = 0
        self.health_lb = 0
        self.health_failure = False # local copy to maintain off-hours status
        self.alarm_triggered = False
        self.first_run = True

        if self.config.last_run == "never":
            self.next_health_check = self.config.build_time(self.config.health_int,"closest_backward")


    def perform_healthchecks(self):
        try:
            lb_status = requests.get(self.config.lb_url, timeout=10)
        except requests.exceptions.ConnectionError:
            self.health_lb = 502
        except requests.exceptions.ReadTimeout:
            self.health_lb = 408
        except:
            self.health_lb = 90000
        else:
             self.health_lb = lb_status.status_code
        finally:
             pass

        try:
            node_status = requests.get(self.config.node_url, timeout=10)
        except requests.exceptions.ConnectionError:
            self.health_node = 502
        except requests.exceptions.ReadTimeout:
            self.health_node = 408
        except:
            self.health_lb = 90000
        else:
            self.health_node = node_status.status_code
        finally:
            pass


    def build_health_msg(self):
        msg = (f"{self.config.node_name}\n"
               "=======================\n"
               "HEALTH STATUS REPORT\n"
               "--------------------\n"
               f"{self.config.lb}: ")

        results = [self.health_lb,self.health_node]

        for n in range(0,2):
            if n == 1:
                msg += f"\nEndpoint {self.config.node}: "
            if results[n] < 200 or results[n] > 299:
                msg += "Error"
            else:
                msg += "Healthy"
            if results[n] == 90000:
                results[n] = "unknown"

        msg += f"\nCodes: {results}\n"

        if results[0] > 199 and results[1] > 199 and results[0] < 300 and results[1] < 300:
            # everything is healthy
            self.health_failure = False
        else:
            self.health_failure = True
     
        if self.config.local:
            print(f"\n{msg}")
            
        return msg


if __name__ == "__main__":
    print("This class module is not designed to be run independently, please refer to the documentation")