from django.db import models
import datetime
from django.conf import settings

dart_schema = settings.DART_SCHEMA
if dart_schema:
    dart_schema = '"%s".' % dart_schema
else:
    dart_schema = ''


class Data_gaps(models.Model):
    pipeline = models.CharField(max_length=500, null = False)
    trace_id = models.CharField(max_length=500, null = False)
    metric = models.CharField(max_length=500)
    brand = models.CharField(max_length=500)
    json_data = models.TextField()
    run_ts = models.DateTimeField(null = False,default=datetime.datetime.now())
    dt = models.DateField(null = False, default=datetime.datetime.now())

    class Meta:
        managed = settings.MODEL_MANGED
        db_table = u'%s"data_gaps"' % dart_schema

    def __str__(self):
        return str(self.pipeline)

class Pipeline_traceability(models.Model):
    point = models.CharField(max_length=500, null = False)
    trace_id = models.CharField(max_length=500, null = False)
    count = models.BigIntegerField()
    metadata = models.TextField()
    metric = models.CharField(max_length=500)
    run_ts = models.DateTimeField(null = False,default=datetime.datetime.now())
    dt = models.DateField(null = False,default=datetime.datetime.now())
    brand = models.CharField(max_length=50)
    step = models.IntegerField()
    step_detail = models.CharField(max_length=200)
    # system = models.CharField(max_length=200,null=False)
    class Meta:
        managed = settings.MODEL_MANGED
        db_table = u'%s"pipeline_traceability"' % dart_schema

    def __str__(self):
        return self.point

class System_traceability(models.Model):
    system = models.CharField(max_length=200,null=False)
    trace_id = models.CharField(max_length=500, null = False)
    brand = models.CharField(max_length=50)
    metric = models.CharField(max_length=500)
    count = models.BigIntegerField()
    run_ts = models.DateTimeField(null = False,default=datetime.datetime.now())
    dt = models.DateField(null = False,default=datetime.datetime.now())
    step = models.IntegerField()
    step_detail = models.CharField(max_length=500)
    # trace_id = models.CharField(max_length=500, null = False)
    class Meta:
        managed = settings.MODEL_MANGED
        db_table = u'%s"system_traceability"' % dart_schema
    def __str__(self): 
        return self.system

class Trace_ids(models.Model):
    pipeline = models.CharField(max_length=500, null = False)
    trace_id = models.CharField(max_length=500, null = False)
    run_ts = models.DateTimeField(null = False, default=datetime.datetime.now())
    dt = models.DateField(null = False, default=datetime.datetime.now())
    type =models.CharField(max_length=100)
    # stages = models.TextField(default=True)
    class Meta:
        managed = settings.MODEL_MANGED
        db_table = u'%s"trace_ids"' % dart_schema
    def __str__(self):
        return self.pipeline

class Traceability_results(models.Model):
    pipeline = models.CharField(max_length=500, null = False)
    trace_id = models.CharField(max_length=500, null = False)
    status = models.CharField(max_length=50)
    message = models.CharField(max_length=500)
    results = models.TextField()
    run_ts = models.DateTimeField(null = False, default=datetime.datetime.now())
    dt = models.DateField(null = False, default=datetime.datetime.now())

    class Meta:
        managed = settings.MODEL_MANGED
        db_table = u'%s"traceability_results"' % dart_schema