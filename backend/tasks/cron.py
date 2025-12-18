from django_cron import CronJobBase, Schedule
from datetime import datetime, date
from django.utils.timezone import now
from .models import Task
from django.db import models
from time import sleep
from django.conf import settings
from django.core.mail import send_mail


class checkForOverdueTasks(CronJobBase):
    RUN_EVERY_MINS = 1  # every 1 minutes

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'tasks.checkForOverdueTasks'  # a unique code

    def do(self):
        print(f"Task cron running at {datetime.now()}")

        # Get current month as a string number (e.g., '8' for August)
        # Calculate previous month (1–12)
        previous_month = 12 if now().month == 1 else now().month - 1
        previous_month_str = str(previous_month)  # e.g., '7' for July

        today = date.today()

        # Filter tasks where month_correlation matches current month string
        # OR time_correlation date is today or earlier
        tasks = Task.objects.filter(
            models.Q(month_correlation=previous_month_str) |
            models.Q(time_correlation__lte=today)
        )

        for task in tasks:
            if task.status != 'overdue' and task.status != 'done' and task.owner.stripe_subscription != 'Basic':
                print(f"Matched Task: Id:{task.id}")
                task.status = 'overdue'
                task.save(update_fields=['status'])
                if task.Responsible_for_the_task.email:
                    send_mail(
                        subject="You have overdue tasks!",
                        message=f"You have overdue tasks that need your attention. Task name: {task.name} Cottage name: {task.owner.name}",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[task.Responsible_for_the_task.email],
                    )
                else:
                    emails = list(task.owner.CottageUsers.values_list('email', flat=True))
                    if self.owner and self.owner.email:
                        emails.append(self.owner.email)

                    send_mail(
                        subject="You have overdue tasks!",
                        message=(f"You have overdue tasks that need your attention.\n\n"
                        f"Task name: {task.name}\n"
                        f"Cottage name: {task.owner.name}"
                        ),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=list(set(emails)),
                    )
        sleep(5)