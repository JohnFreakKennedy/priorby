from django.db import models


# Create your models here.
class TelegramBot(models.Model):
    token = models.CharField(max_length=255, verbose_name="Bot token")
    name = models.CharField(max_length=255, verbose_name="Bot name")
    username = models.CharField(max_length=255, verbose_name="Bot username")
    group_id = models.CharField(max_length=255, verbose_name="Group ID")

    def __str__(self):
        return self.name


class ProcessedLead(models.Model):
    lead_id = models.CharField(max_length=255, verbose_name="Lead ID")
    lead_owner = models.CharField(max_length=255, verbose_name="Lead owner")
