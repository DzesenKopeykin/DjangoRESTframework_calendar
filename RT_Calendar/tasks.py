from django.template import Template, Context
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from RT_test_challenge.celery import app
from datetime import datetime, time
from ics import Calendar
import RT_Calendar.models as models
import requests


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


@app.task
def get_holidays(user_id):
    user_model = get_user_model()
    user = user_model.objects.get(pk=user_id)
    response = requests.get('https://www.officeholidays.com/ics/ics_country.php?tbl_country={}'.format(user.country))
    calendar = Calendar(response.text)
    for event_number in range(0, len(calendar.events)):
        holiday = models.Event(name=calendar.events[event_number].name,
                               user=user,
                               is_holiday=True,
                               start_date=datetime.date(
                                   datetime.strptime(str(calendar.events[event_number].begin)[:10], '%Y-%m-%d')
                               ),
                               end_date=datetime.date(
                                   datetime.strptime(str(calendar.events[event_number].end)[:10], '%Y-%m-%d')
                               ),
                               start_time=time(0, 0),
                               end_time=time(0, 0))
        holiday.save()
