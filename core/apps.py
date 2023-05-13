from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    
    def ready(self):
        '''
        Run async task to archive old service requests 
        '''
        from apscheduler.schedulers.background import BackgroundScheduler
        from .jobs import check_old_requests 
        scheduler = BackgroundScheduler({'apscheduler.timezone': 'Asia/Riyadh'})
        scheduler.add_job(check_old_requests, 'cron', hour=0 , minute = 0) 
        scheduler.start()