from crontab import CronTab

cron = CronTab(user="emilio")
the_job = cron.new(command="python3 /home/emilio/PycharmProjects/air-quality-design-testing/ReadingAPITest/Cron/example1.py", comment="my comment 2! :D")
the_job.minute.every(1)

cron.write()
















