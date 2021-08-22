import os
import re
import requests
import json
import math
import pytz
from datetime import datetime
from time import sleep


class CheckDagStatus():

    def __init__(self,config):

        self.current_constellation_collateral = 250000
        self.action = config.action
        self.error_flag = False

        self.config = config
        self.now = datetime.now(self.config.tz)

        self.command_list = [
            "addline_/usr/local/bin/dag metrics | grep 'Rewards'",
            "addline_/usr/local/bin/dag | grep 'Node Status'",
            "/usr/local/bin/dag | grep 'Web Status'",
            "/usr/local/bin/dag metrics | grep 'State'",
            "df -h | grep 'vda1 ' | awk '{print \"Data usage: \"$5\" of \"$3}'",
            "free | awk '{print $4}'",
            "uptime",
            "/usr/local/bin/dag nodes --mainnet | grep 'Ready' | wc -l | awk '{print \"Ready Nodes: \"$0}'",
            "addline_security"
        ]

        self.report_body = ""
        self.usd_str = ""
        self.col_str = ""
        self.current_result = ""
        self.results = []

        self.current_dag_count = 0
        self.last_dag_count = 0
        self.delta_dags = 0
        self.delta_usd = 0
        self.current_price_usd = 0
        self.last_price_usd = 0
        self.usd_dag_price = 0

        self.today = datetime.now(self.config.tz)
        self.date_only = self.today.strftime("%Y-%m-%d")
        self.simple_time = self.today.strftime("%H:%M")
        self.today = self.today.strftime("%Y-%m-%d %H:%M:%S")
        
        self.create_alert_report()
        self.prepare_results()

        if not self.error_flag:
            self.calculate_dag_to_usd()
            self.calculate_collateral()

        self.create_alert_msg()

        if self.config.silence_writelog is False and self.error_flag is False:
            self.writeout_stats_logs()


    def security_check(self):
        result_stream = os.popen("cat /var/log/auth.log | grep \"]: Invalid user\" | awk '{print $8 \" \" $12}'")
        result_stream_max = os.popen("cat /var/log/auth.log | grep \"error: maximum authentication attempts exceeded\" | wc -l")

        results = result_stream.read()
        max_auth_attempt = result_stream_max.read()

        results = results.split("\n")
        # clean out empty lines
        results = [n for n in results if n]

        invalid_count = len(results)

        lower_port = 65535
        higher_port = 0

        # print(json.dumps(results,indent=4))

        for user_port in results:
            parts = user_port.split(" ")
            try: 
                int(parts[1])
            except:
                pass
            else:
                if int(parts[1]) < lower_port:
                    lower_port = int(parts[1])
                if int(parts[1]) > higher_port:
                    higher_port = int(parts[1])

        self.results.append(f"Inv Login Attempts: {invalid_count}")
        self.results.append(f"Port Range: {lower_port}-{higher_port}")
        self.results.append(f"Max Login Exceeded: {max_auth_attempt}")


    def create_alert_report(self):
        for command in self.command_list:
            if "addline" in command:
                self.results.append("=========================")
                command = command.split("_")
                command = command[1]
            if "security" in command and self.config.security_enabled is True:
                self.security_check()
            else:
                if "uptime" in command:
                    # fix problem with uptime less than 1 day
                    result_stream = os.popen("uptime")
                    result_test = result_stream.read()
                    if "day" in result_test:
                        command = "uptime | awk '{print $3\" \"$12}'"
                    elif "min" in result_test:
                        command = "uptime | awk '{print $3\" \"$11}'"
                    else:
                        command = "uptime | awk '{print $3\" \"$10}'"
                result_stream = os.popen(command)
                self.current_result = result_stream.read()
                if "Rewards" in command:
                    self.get_calc_stats_variables("alert")
                    self.current_result = self.cleaner(self.current_result,"spaces")
                    format_update = self.current_result.split(":")
                    try:
                        format_update = int(self.cleaner(format_update[-1],"ansi_escape"))
                    except:
                        format_update = 0 # There was an error in the rewards (reset necessary?)
                        self.current_result = f"Error Detected\n"
                        self.current_result += f"Possible Reset Required?\n"
                        self.error_flag = True
                    else:
                        self.results.append(f"{datetime.strftime(self.now,'%Y-%m-%d %H:%M:%S')}\n")
                        self.current_result = ""
                    format_update =  "{:,}".format(format_update)
                    if int(self.delta_dags) < 0:
                        self.delta_dags = f"({self.delta_dags})"
                    else:
                        self.delta_dags = f"+{self.delta_dags}"
                    self.current_result += f"Rewards: {format_update} {self.delta_dags}"
                if "free" in command:
                    self.parse_memory()
                if "uptime" in command:
                    self.parse_uptime_load()
                    # add healthcheck status (up_monitor)
                    if self.config.health_failure:
                        self.current_result += f"Health Check: Error"
                    else:
                        self.current_result += f"Health Check: Healthy"
                if self.current_result is not "":
                    self.results.append(self.current_result)


    def get_calc_stats_variables(self,action):
        f = open(self.config.dag_log_file)
        last_line = f.readlines()
        f.close()


        try:
            last_line = last_line[len(last_line)-1]
        except:
            # dag_log is empty... first run?
            last_line = f"{self.now}|0|0|{self.usd_dag_price}"
        finally:
            last_line = last_line.split("|")

            self.last_dag_usd = float(last_line[3])
            if action == "alert":
                self.last_dag_count = float(last_line[1])
                self.last_price_usd = float(last_line[2])

                self.current_dag_count = self.cleaner(self.current_result,"dag_count")

                self.delta_dags = int(self.current_dag_count) - int(self.last_dag_count)
                self.delta_dags = str(self.delta_dags)


    def cleaner(self, line, action):
        if action == "dag_count":
            cleaned_line = re.sub('\D', '', line)
            return cleaned_line[6:]
        elif action == "ansi_escape":
            ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
            return ansi_escape.sub('', line)  
        elif action == "spaces":
            return re.sub('\n', '', line)                 
        elif action == "commas":
            return re.sub(',', '', line) 
        elif action == "float_only":
            return re.sub('[^0-9,.]', '', line)                


    def parse_memory(self):
        details = self.current_result.split("\n")
        current_result = ""
        details.pop(0)
        details.pop()

        for n, useage in enumerate(details):
            if int(useage) < self.config.mem_swap_min:
                if n == 0:
                    current_result = f"Memory: LOW@{'{:,}'.format(int(useage))}"
                else:
                    if "Memory" in current_result:
                        current_result += "\n"
                    current_result += f"Swap: LOW@{'{:,}'.format(int(useage))}"
            else:
                if n == 0:
                    current_result = f"Memory: OK@{'{:,}'.format(int(useage))}"
                else:
                    current_result += f"\nSwap: OK@{'{:,}'.format(int(useage))}\n"

        self.current_result = current_result


    def parse_uptime_load(self):
        details = self.current_result.split(" ")
        details[0] = self.cleaner(details[0],"spaces")
        details[0] = self.cleaner(details[0],"commas")
        details[1] = self.cleaner(details[1],"spaces")
        details[1] = self.cleaner(details[1],"commas")

        try: 
            int(details[0])
        except:
            details[0] = 1

        if int(details[0]) > self.config.uptime:
            usage_line = f"Days Up: WARN@{details[0]}"
        else:
            usage_line = f"Days up: OK@{details[0]}"

        if float(details[1]) > float(self.config.load):
            usage_line2 = f"15M CPU: WARN@{details[1]}"
        else:
            usage_line2 = f"15M CPU: OK@{details[1]}"

        self.current_result = f"{usage_line}\n{usage_line2}\n"


    def prepare_results(self):
        new_results = []
        for result in self.results:
            result = self.cleaner(result,"ansi_escape")
            result = result.strip().rstrip()
            result = re.sub(' +', ' ', result)
            result = re.sub('^ +', '', result)
            new_results.append(result)
        self.results = new_results


    def create_alert_msg(self):
        self.report_body = "MAINNET\n"
        for line in self.results:
            self.report_body = self.report_body+line+"\n"
            if line.find("Rewards") > -1:
                self.report_body = f"{self.report_body}{self.usd_str}{self.col_str}\n"

        if self.config.local is True:
            print(f"\n{self.report_body}\n")


    def calculate_dag_to_usd(self):
        error_flag = False

        for n in range(0,4):
            # allow four attempts to retrieve new price before using last known price
            resp = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=constellation-labs&vs_currencies=usd')
            if resp.status_code == 200:
                api_results = resp.json()
                self.usd_dag_price = api_results['constellation-labs']['usd']
                break
            else:
                # This means something went wrong.
                # raise ApiError('GET /tasks/ {}'.format(resp.status_code))
                if n > 2:
                    self.get_calc_stats_variables("api_error")
                    self.usd_dag_price = self.last_dag_usd
                    error_flag = True
                    break
                sleep(2)
                        
        for line in self.results:
            if line.find("Rewards") > -1:
                parts = line.split(":")
                if "+" in parts[1]:
                    parts = parts[1].split("+")
                else:
                    parts[1] = parts[1].replace("(","").replace(")","")
                    parts = parts[1].split("-")
                price = float(self.cleaner(parts[0],"commas"))
                self.current_price_usd = price*self.usd_dag_price
                if self.config.splits_enabled:
                    split1 = "${:,.2f}".format(self.current_price_usd*self.config.split1)
                    split2 = "${:,.2f}".format(self.current_price_usd*self.config.split2)
                main_price = "${:,.2f}".format(self.current_price_usd)

        self.delta_usd = self.current_price_usd - self.last_price_usd
        if self.delta_usd < 0:
            self.delta_usd = abs(self.delta_usd)
            self.delta_usd = "(${:,.2f})".format(self.delta_usd)
        else:
            self.delta_usd = "+${:,.2f}".format(self.delta_usd)

        self.usd_str = f"USD: {main_price} {self.delta_usd}"
        if self.config.splits_enabled:
            self.usd_str += f"\n{split1}/{split2}"
        self.usd_str += f"\nDAG @ ${self.usd_dag_price}"

        if error_flag:
            self.usd_str += "***"
        self.usd_str += "\n"

        self.usd_dag_delta = "{:,.7f}".format(abs(self.last_dag_usd-self.usd_dag_price))
        if self.last_dag_usd-self.usd_dag_price < 0:
            self.usd_str += f"+{self.usd_dag_delta}"
        elif self.last_dag_usd-self.usd_dag_price == 0:
            self.usd_str += f"EVEN {self.usd_dag_delta}"            
        else:
            self.usd_str += f"({self.usd_dag_delta})"
 
        # self.usd_str += "{:,.7f}".format(abs(self.last_dag_usd-self.usd_dag_price)) # delta       


    def calculate_collateral(self):
        if self.config.collateral_enabled:
            collateral = self.config.collateral_nodes*self.current_constellation_collateral
            collateral += int(self.current_dag_count)
            collateral += int(self.config.free_dag)

            possible_nodes = collateral/self.current_constellation_collateral
            this_possible_nodes = math.floor((self.current_constellation_collateral+int(self.current_dag_count))/self.current_constellation_collateral)

            dag_b4_next = (self.current_constellation_collateral*this_possible_nodes)-int(self.current_dag_count)

            if dag_b4_next == 0:
                dag_b4_next = self.current_constellation_collateral

            usd_collateral_value = collateral * self.usd_dag_price

            self.col_str = f"\nCollateral Nodes: {'{:,}'.format(possible_nodes)}\n"
            self.col_str += f"Collateral DAGs: {'{:,}'.format(collateral)}\n"
            self.col_str += f"Collateral USD: {'${:,.2f}'.format(usd_collateral_value)}\n"
            self.col_str += f"Next Node: {'{:,}'.format(dag_b4_next)}"


    def writeout_stats_logs(self):
        result = f"{self.today}|{self.current_dag_count}|{self.current_price_usd}|{self.usd_dag_price}\n"

        f = open(self.config.dag_log_file, "a")
        f.write(result)
        f.close()


if __name__ == "__main__":
    print("This class module is not designed to be run independently, please refer to the documentation")
