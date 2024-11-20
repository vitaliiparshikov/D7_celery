from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from apscheduler.schedulers.background import BackgroundScheduler
from news.tasks import send_weekly_newsletter

class Command(BaseCommand):
    help = 'Runs APScheduler.'

    def handle(self, *args, **options):
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")

        @register_job(scheduler, "cron", day_of_week='fri', hour=18, minute=0, id="send_weekly_newsletter")
        def job():
            send_weekly_newsletter()

        register_events(scheduler)
        scheduler.start()

        self.stdout.write(self.style.SUCCESS('Scheduler started...'))