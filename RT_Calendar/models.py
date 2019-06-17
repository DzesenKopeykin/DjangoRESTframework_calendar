from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from datetime import datetime, timedelta
import pytz

from django.db.models import signals
import RT_Calendar.tasks as tasks


REMINDER_HOURS = ((1, '1'), (2, '2'), (3, '4'), (4, '24'), (5, '168'))


class UserAccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email address must be provided')

        if not password:
            raise ValueError('Password must be provided')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = UserAccountManager()

    email = models.EmailField('email', unique=True, blank=False, null=False)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=True)

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return self.email

    def __unicode__(self):
        return self.email


class Event(models.Model):
    name = models.CharField(max_length=255, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    reminder_hours = models.IntegerField(choices=REMINDER_HOURS)

    class Meta:
        ordering = ('start_date', 'start_time',)


def event_post_save(sender, instance, signal, *args, **kwargs):
    mytime = datetime(instance.start_date.year, instance.start_date.month, instance.start_date.day,
                      instance.start_time.hour, instance.start_time.minute) - timedelta(hours=instance.reminder_hours)
    timezone = pytz.timezone('Europe/Minsk')
    mytime = timezone.localize(mytime)
    tasks.send_reminder_email.apply_async(args=[instance.pk], eta=mytime)


signals.post_save.connect(event_post_save, sender=Event)
