# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Medicineopendata(models.Model):
    ch_name = models.CharField(db_column='ch-name', max_length=500, blank=True, null=True)   # Field renamed to remove unsuitable characters.
    en_name = models.CharField(db_column='en-name', max_length=500, blank=True, null=True)   # Field renamed to remove unsuitable characters.
    indication = models.CharField(max_length=2000, blank=True, null=True)
    component = models.CharField(max_length=2000, blank=True, null=True)
    formulation = models.CharField(max_length=1000, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    dosage = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'medicineopendata'
