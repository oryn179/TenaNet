#!/bin/bash

# Resolve script directory (works with sudo)
BASEDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

LOG_DIR="$BASEDIR/logs"
LOG_FILE="$LOG_DIR/scan_results.txt"
DATA_DIR="$BASEDIR/data"

mkdir -p "$LOG_DIR"   # ensure logs folder exists
mkdir -p "$DATA_DIR"

banner() {
printf "\e[1;77m ████████╗███████╗███╗   ██╗ █████╗ ███╗   ██╗███████╗████████╗\e[0m\n"
printf "\e[1;77m ╚══██╔══╝██╔════╝████╗  ██║██╔══██╗████╗  ██║██╔════╝╚══██╔══╝\e[0m\n"
printf "\e[1;77m    ██║   █████╗  ██╔██╗ ██║███████║██╔██╗ ██║█████╗     ██║   \e[0m\n"
printf "\e[1;77m    ██║   ██╔══╝  ██║╚██╗██║██╔══██║██║╚██╗██║██╔══╝     ██║   \e[0m\n"
printf "\e[1;77m    ██║   ███████╗██║ ╚████║██║  ██║██║ ╚████║███████╗   ██║   \e[0m\n"
printf "\e[1;77m    ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   \e[0m\n"
printf "\n"
printf "\e[1;93m       .:.:.:.\e[0m\e[1;77m   If U Got Scam Send us @oryn179   \e[0m\e[1;93m.:.:.:.\e[0m\n"
printf "\n"
}

menu() {
echo -e "\e[1;96mChoose an option:\e[0m"
echo "1) Email Attack Detection"
echo "2) SMS Attack Detection"
echo "3) URL/Website Scam Detection"
echo "4) View Logs"
echo "5) Clear Logs"
echo "6) Exit"
echo "7) Install sample datasets (data/all_*.csv)"
read -p "Select: " choice

case $choice in
    1)
       echo -e "\e[1;92m[+] Starting Email Attack Detection...\e[0m"
       python3 -u "$BASEDIR/tenanet/email_detect.py" 2>&1 | stdbuf -oL tee -a "$LOG_FILE"
       # append only SCAN-RESULT lines
       grep "^\[SCAN-RESULT\]" /tmp/tenanet_last.txt >> "$LOG_FILE" 2>/dev/null || true
       ;;
    2)
       echo -e "\e[1;92m[+] Starting SMS Attack Detection...\e[0m"
       python3 -u "$BASEDIR/tenanet/sms_detect.py" 2>&1 | stdbuf -oL tee -a "$LOG_FILE"
       ;;
    3)
       echo -e "\e[1;92m[+] Starting URL/Website Scam Detection...\e[0m"
       python3 -u "$BASEDIR/tenanet/url_detect.py" 2>&1 | stdbuf -oL tee -a "$LOG_FILE"
       ;;
    4)
       echo -e "\e[1;96m--- TENANET Logs ---\e[0m"
       if [ -s "$LOG_FILE" ]; then
           nl -ba "$LOG_FILE"
       else
           echo "No logs yet."
       fi
       ;;
    5)
       read -p "Are you sure you want to clear logs? (y/N): " yn
       if [[ "$yn" =~ ^[Yy]$ ]]; then
           : > "$LOG_FILE"
           echo "Logs cleared."
       else
           echo "Aborted."
       fi
       ;;
    6) echo -e "\e[1;91mExiting TENANET... Stay Safe!\e[0m"; exit;;
    7)
       echo -e "\e[1;92m[+] Installing sample datasets into $DATA_DIR ...\e[0m"
       # check for files in same folder as script first
       for f in all_emails.csv all_sms.csv all_urls.csv; do
           if [ -e "$BASEDIR/$f" ]; then
               cp -v "$BASEDIR/$f" "$DATA_DIR/"
           elif [ -e "$BASEDIR/tenanet_data/$f" ]; then
               cp -v "$BASEDIR/tenanet_data/$f" "$DATA_DIR/"
           else
               echo "Missing $f — download it and place in $BASEDIR or $BASEDIR/tenanet_data"
           fi
       done
       echo "Done."
       ;;
    *) echo -e "\e[1;91mInvalid option!\e[0m";;
esac
}

banner
while true; do
    menu
done
