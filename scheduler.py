import schedule
import time
from threading import Thread

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

def add_job(job_func, day, time_str):
    getattr(schedule.every(), day).at(time_str).do(job_func)

scheduler_thread = Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()
