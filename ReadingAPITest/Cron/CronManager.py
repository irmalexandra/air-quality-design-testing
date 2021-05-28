from crontab import CronTab
import os
DATA_BASE_UPDATER_PATH = os.path.abspath("../DataBaseHandler/DatabaseUpdater.py")


def make_cron_job():
    cron = CronTab(user="emilio")
    the_job = cron.new(
        command="python3 " + DATA_BASE_UPDATER_PATH,
        comment="Data base updater job")
    the_job.hour.every(1)
    cron.write()




















