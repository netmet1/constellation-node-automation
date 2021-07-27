#!/bin/bash

case "$1" in
    -s) action="start";;
    -r) action="restart";;
    -k) action="kill";;
    -h) action="help";;
    *) action="none";;
esac

if [[ $action = "help" ]]; then
    echo
    echo "Node Operator Automation Helper Script"
    echo "--------------------------------------"
    echo "usage: . admin_auto.sh [-h] [-s] [-r] [-k]"
    echo
    echo "THIS IS FOR USE WITH THE \"AUTO\" ARGUMENT (auto run)"
    echo "This does not deal with single alerts, reports, or logs"
    echo
    echo "This does not deal with the program running locally in the current user session"
    echo "without the \"nohup\" command.  See README.md"
    echo
    echo "positional arguments:"
    echo "  -h        show this help message"
    echo "  -s        start the automation program if not running"
    echo "            this will start the program in the background"
    echo "  -r        stop the program, then restart it"
    echo "  -k        stop the program from running in the background"
    echo "            this will find and kill the automation program process"
    echo
    echo "example usage:"
    echo "~# . admin_auto.sh -s"
    echo "This command will start the node operator automation program in the background with the \"auto\" variable."
    echo
    echo "~#: . admin_auto.sh -r"
    echo "This command will find the process that is running and \"kill\" it (stop it)."
    echo "then it will restart it with the auto command in the background (-s)."
    echo
    return
elif [[ $action = "none" ]]; then
    return
fi

echo -n "$action the automation script y or n [y] "
read confirm

if [[ $confirm = [Yy] || -z $confirm ]]; then
    auto_process="pgrep -f \"python3.*automation.py.*auto\""
    start_command="nohup python3 automation.py auto"
    invalid_error="Invalid request received\nno action taken...\n"
    already_error="The Automation Program Doesn't seem to be running already.\nNo Actions Needed...\n\n"

    echo "------"
    echo "This script is taking the following action = $action"

    process=$(eval "$auto_process")
    case "$action" in
        start) 
            if [[ -z $process ]]; then
                echo "starting..."
                $start_command &
                process=$(eval "$auto_process")
                sleep 2
                printf "New Automation Program Process: $process has been started.\nAction: Successful\n\n"
            else
                printf "Automation Program Process: $process is already running.  see --help\n\n"
            fi
            ;;
        restart) action="restart"
            if [[ -z $process ]]; then
                printf "$already_error"
            else
                echo "Removing the Automation Process: $process"
                pkill -f 'python3.*automation.py.*auto' > /dev/null 2>&1
                $start_command & > /dev/null 2>&1
                process=$(eval "$auto_process")
                sleep 2
                printf "New Automation Program Process: $process has been started.\nAction: Successful\n\n" 
            fi       
            ;;
        kill) action="kill"
            if [[ -z $process ]]; then
                printf "$already_error"
            else
                echo "Removing the Automation Process: $process"
                pkill -f 'python3.*automation.py.*auto'
                sleep 2
                echo "Automation Program Process: $process has been stopped/removed/killed.\nAction: Successful\n\n"
            fi
            ;;
        *) printf "$invalid_error"
            return
            ;;
    esac
else
    printf "$invalid_error"
    echo
fi

printf "\$DAG to node is to node.\n"
echo 