# from django.db import models
#
#
# class Course(models.Model):
#     couno = models.CharField(primary_key=True, max_length=3)
#     course = models.CharField(max_length=255, blank=True, null=True)
#     credit = models.IntegerField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'course'
#
#
# class Score(models.Model):
#     serno = models.IntegerField(primary_key=True)
#     stuno = models.ForeignKey('Student', models.DO_NOTHING, db_column='stuno', blank=True, null=True)
#     couno = models.ForeignKey(Course, models.DO_NOTHING, db_column='couno', blank=True, null=True)
#     score = models.IntegerField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'score'
#
#
# class Student(models.Model):
#     stuno = models.CharField(primary_key=True, max_length=6)
#     stuname = models.CharField(max_length=20, blank=True, null=True)
#     gender = models.CharField(max_length=1, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'student'
#
#
# class Medicinebot(models.Model):
#     userid = models.CharField(db_column='userId', primary_key=True, max_length=500)  # Field name made lowercase.
#     date = models.DateField(blank=True, null=True)
#     time = models.TimeField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'medicinebot'
