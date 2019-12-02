# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DivisionType(models.Model):
    type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'division_type'


class DivisionType1(models.Model):
    type_id = models.IntegerField(primary_key=True)
    type_name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'division_type1'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoQOrmq(models.Model):
    key = models.CharField(max_length=100)
    payload = models.TextField()
    lock = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_q_ormq'


class DjangoQSchedule(models.Model):
    func = models.CharField(max_length=256)
    hook = models.CharField(max_length=256, blank=True, null=True)
    args = models.TextField(blank=True, null=True)
    kwargs = models.TextField(blank=True, null=True)
    schedule_type = models.CharField(max_length=1)
    repeats = models.IntegerField()
    next_run = models.DateTimeField(blank=True, null=True)
    task = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    minutes = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_q_schedule'


class DjangoQTask(models.Model):
    name = models.CharField(max_length=100)
    func = models.CharField(max_length=256)
    hook = models.CharField(max_length=256, blank=True, null=True)
    args = models.TextField(blank=True, null=True)
    kwargs = models.TextField(blank=True, null=True)
    result = models.TextField(blank=True, null=True)
    started = models.DateTimeField()
    stopped = models.DateTimeField()
    success = models.IntegerField()
    id = models.CharField(primary_key=True, max_length=32)
    group = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_q_task'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DoctorEvent1(models.Model):
    doctortime_id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=45, blank=True, null=True)
    doctor_name = models.CharField(max_length=45, blank=True, null=True)
    doctor_date = models.CharField(max_length=45, blank=True, null=True)
    doctor_time = models.CharField(max_length=45, blank=True, null=True)
    doctor_text = models.CharField(max_length=200, blank=True, null=True)
    doctor_yes_no = models.IntegerField(blank=True, null=True)
    seting_finish_time = models.CharField(max_length=50, blank=True, null=True)
    hospital_name = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'doctor_event1'


class HealthInformation(models.Model):
    health_informationcol_id = models.AutoField(primary_key=True)
    title = models.TextField(blank=True, null=True)
    information_url = models.TextField(db_column='Information_url', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'health_information'


class MedicineInformation(models.Model):
    medicine_id = models.CharField(primary_key=True, max_length=30)
    chi_name = models.CharField(max_length=500, blank=True, null=True)
    eng_name = models.CharField(max_length=500, blank=True, null=True)
    medicine_type = models.CharField(max_length=50, blank=True, null=True)
    indication = models.CharField(max_length=500, blank=True, null=True)
    formulation = models.CharField(max_length=100, blank=True, null=True)
    package = models.CharField(max_length=200, blank=True, null=True)
    controlld_type = models.CharField(max_length=45, blank=True, null=True)
    main_ingredient = models.CharField(max_length=500, blank=True, null=True)
    dosage_usage = models.CharField(max_length=500, blank=True, null=True)
    barcode = models.CharField(max_length=500, blank=True, null=True)
    factory_address = models.CharField(max_length=500, blank=True, null=True)
    company_address = models.CharField(max_length=500, blank=True, null=True)
    manufacturer_country = models.CharField(max_length=500, blank=True, null=True)
    manufacturer_name = models.CharField(max_length=500, blank=True, null=True)
    manufacturer_process = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'medicine_information'


class OcrTable(models.Model):
    ocr_no = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserInformation', models.DO_NOTHING)
    user_name = models.CharField(max_length=45)
    see_doctor_date = models.DateField(blank=True, null=True)
    hospital_name = models.CharField(max_length=45, blank=True, null=True)
    med_name = models.CharField(max_length=45, blank=True, null=True)
    dossage = models.IntegerField(blank=True, null=True)
    time = models.IntegerField(blank=True, null=True)
    days = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ocr_table'


class Reminderevent(models.Model):
    reminder_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserInformation', models.DO_NOTHING, blank=True, null=True)
    medicine = models.ForeignKey(MedicineInformation, models.DO_NOTHING, blank=True, null=True)
    reminder_date = models.CharField(max_length=15, blank=True, null=True)
    reminder_time = models.CharField(max_length=15, blank=True, null=True)
    reminder_text = models.CharField(max_length=200, blank=True, null=True)
    reminder_yes_no = models.IntegerField(blank=True, null=True)
    seting_finish_time = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reminderevent'


class UserInformation(models.Model):
    user_id = models.CharField(primary_key=True, max_length=45)
    group_id = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_information'
