#!/usr/bin/env python3
import pywhatkit
import pandas as pd
import time
import datetime as dt
import logging
import sys
from dotenv import load_dotenv
import os
import schedule

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("whatsapp_automation.log"), logging.StreamHandler(sys.stdout)]
)

BROWSER_WAIT = int(os.getenv("BROWSER_WAIT", "15"))
RETRY_COUNT = int(os.getenv("RETRY_COUNT", "2"))
RETRY_DELAY = int(os.getenv("RETRY_DELAY", "5"))

def parse_time_hhmm(tstr):
    h, m = tstr.split(":")
    return int(h), int(m)

def safe_send_message(number, message, hour=None, minute=None, wait_time=BROWSER_WAIT, close_tab=True):
    attempt = 0
    while attempt <= RETRY_COUNT:
        try:
            if hour is None or minute is None:
                now = dt.datetime.now() + dt.timedelta(seconds=20)
                h, m = now.hour, now.minute
                logging.info(f"Sending (instant-ish) to {number} - will use time {h}:{m}")
                pywhatkit.sendwhatmsg(number, message, h, m, wait_time, close_tab)
            else:
                logging.info(f"Scheduling to {number} at {hour:02d}:{minute:02d}")
                pywhatkit.sendwhatmsg(number, message, hour, minute, wait_time, close_tab)
            logging.info(f"Message queued for {number}")
            return True
        except Exception as e:
            attempt += 1
            logging.warning(f"Attempt {attempt} failed for {number}: {e}")
            if attempt > RETRY_COUNT:
                logging.error(f"Failed sending to {number} after {RETRY_COUNT} retries.")
                return False
            time.sleep(RETRY_DELAY)

def send_image_to_number(number, image_path, caption=""):
    try:
        logging.info(f"Sending image {image_path} to {number}")
        pywhatkit.sendwhats_image(number, image_path, caption, 15)
        logging.info("Image send queued.")
        return True
    except Exception as e:
        logging.error(f"Error sending image to {number}: {e}")
        return False

def send_group_message(group_id, message):
    try:
        logging.info(f"Sending group message to {group_id}")
        pywhatkit.sendwhatmsg_to_group_instantly(group_id, message)
        logging.info("Group message queued.")
        return True
    except Exception as e:
        logging.error(f"Error sending group message: {e}")
        return False

def send_bulk_from_csv(csv_path="contacts.csv"):
    df = pd.read_csv(csv_path, dtype=str).fillna("")
    for idx, row in df.iterrows():
        name = row.get("name", "").strip()
        number = row.get("phone", "").strip()
        message = row.get("message", "").strip()
        send_time = row.get("send_time", "").strip()
        send_date = row.get("send_date", "").strip()

        if not number or not message:
            logging.warning(f"Skipping row {idx}: missing number or message")
            continue

        message = message.replace("{name}", name)

        if send_time:
            hour, minute = parse_time_hhmm(send_time)
            if send_date:
                target_dt = dt.datetime.strptime(send_date, "%Y-%m-%d").replace(hour=hour, minute=minute, second=0, microsecond=0)
                now = dt.datetime.now()
                if target_dt <= now:
                    logging.info(f"Target datetime {target_dt} is in the past. Sending immediately (instant).")
                    safe_send_message(number, message)
                else:
                    delta_seconds = (target_dt - now).total_seconds()
                    logging.info(f"Will schedule message to {number} in {int(delta_seconds)} seconds (at {target_dt}).")
                    schedule.every(int(delta_seconds)).seconds.do(lambda n=number, m=message, h=hour, mi=minute: safe_send_message(n, m, h, mi))
            else:
                now = dt.datetime.now()
                target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                if target_time <= now:
                    logging.info(f"Time {hour:02d}:{minute:02d} already passed, sending now.")
                    safe_send_message(number, message)
                else:
                    hhmm = f"{hour:02d}:{minute:02d}"
                    logging.info(f"Scheduling message to {number} at {hhmm}.")
                    schedule.every().day.at(hhmm).do(lambda n=number, m=message, h=hour, mi=minute: safe_send_message(n, m, h, mi))
        else:
            safe_send_message(number, message)

    if schedule.jobs:
        logging.info("Starting scheduler. Press Ctrl+C to stop.")
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("Scheduler stopped.")
    else:
        logging.info("No scheduled jobs. Done.")

def main():
    print("Whatsapp Automation - Options")
    print("1. Send single message now")
    print("2. Schedule single message")
    print("3. Send image to number")
    print("4. Send group message (instant)")
    print("5. Bulk from contacts.csv")
    print("0. Exit")

    choice = input("Choose: ").strip()
    if choice == "1":
        num = input("Phone (+countrycode): ").strip()
        msg = input("Message: ").strip()
        safe_send_message(num, msg)
    elif choice == "2":
        num = input("Phone (+countrycode): ").strip()
        msg = input("Message: ").strip()
        time_str = input("Send time (HH:MM): ").strip()
        h, m = parse_time_hhmm(time_str)
        safe_send_message(num, msg, h, m)
    elif choice == "3":
        num = input("Phone (+countrycode): ").strip()
        img = input("Image path: ").strip()
        caption = input("Caption: ").strip()
        send_image_to_number(num, img, caption)
    elif choice == "4":
        gid = input("Group ID: ").strip()
        msg = input("Message: ").strip()
        send_group_message(gid, msg)
    elif choice == "5":
        csv_path = input("CSV path (default contacts.csv): ").strip() or "contacts.csv"
        send_bulk_from_csv(csv_path)
    else:
        logging.info("Exiting.")

if __name__ == "__main__":
    main()
