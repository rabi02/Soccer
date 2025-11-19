from datetime import datetime
import os
from apscheduler.schedulers.background import BackgroundScheduler
# from soccer import testData
        
def start():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(testData.main, 'interval', minutes=100)
    # scheduler.start()