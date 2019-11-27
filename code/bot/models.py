from django.db import models


class Medicineopendata(models.Model):
    ch_name = models.CharField(db_column='ch-name', max_length=500, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    en_name = models.CharField(db_column='en-name', max_length=500, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    indication = models.CharField(max_length=2000, blank=True, null=True)
    component = models.CharField(max_length=2000, blank=True, null=True)
    formulation = models.CharField(max_length=1000, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    dosage = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'medicineopendata'


class UserMessage(models.Model):
    no = models.IntegerField(primary_key=True)
    userid = models.CharField(max_length=50, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_message'


class News(models.Model):
    title = models.CharField(primary_key=True, max_length=250)
    url = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'news'
