from datetime import datetime
with open('/home/emilio/PycharmProjects/air-quality-design-testing/ReadingAPITest/Cron/append.txt', 'a') as myFile:
    myFile.write('\nAccessed on ' + str(datetime.now()))




