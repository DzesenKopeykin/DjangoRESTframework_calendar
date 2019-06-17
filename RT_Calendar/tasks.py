from django.template import Template, Context
from django.core.mail import send_mail
from RT_test_challenge.celery import app
import RT_Calendar.models as models


REMINDER_TEMPLATE = """
Событие {{ event.name }}
C {{ event.start_date }} {{event.start_time }}
По {{ event.end_date }} {{event.end_time }}
"""

@app.task
def send_reminder_email(event_id):
    event = models.Event.objects.get(pk=event_id)
    template = Template(REMINDER_TEMPLATE)
    send_mail(
        'Напоминание о событии',
        template.render(context=Context({'event': event})),
        'dzesentest@gmail.com',
        [event.user.email],
        fail_silently=False
    )
