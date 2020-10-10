from django.db import models
from django.views.generic import DeleteView
from django import forms

class EntryTable(models.Model):
    kontakt = models.CharField(max_length=20)
    proizvodjac = models.CharField(max_length=20)
    model = models.CharField(max_length=20, blank=True, default='', null=True)
    imei = models.CharField(max_length=15)
    unlock = models.CharField(max_length=100, blank=True, default='', null=True)
    status = models.IntegerField(default=0)
    log = models.TextField()
    winlock = models.CharField(max_length=20, blank=True, default='', null=True)
    winlockversion = models.CharField(max_length=20, blank=True, default='', null=True)
    createdby = models.CharField(max_length=100)
    createdbygroup = models.CharField(max_length=100)
    datecreated = models.DateTimeField(auto_now_add=True)
    datemodified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s' %(self.proizvodjac, self.imei)

class DataTable(models.Model):
    kontakt = models.CharField(max_length=20)
    proizvodjac = models.CharField(max_length=20)
    model = models.CharField(max_length=20, blank=True, default='', null=True)
    imei = models.CharField(max_length=15)
    unlock = models.CharField(max_length=100, blank=True, default='', null=True)
    status = models.IntegerField(default=0)
    log = models.TextField()
    winlock = models.CharField(max_length=20, blank=True, default='', null=True)
    winlockversion = models.CharField(max_length=20, blank=True, default='', null=True)
    createdby = models.CharField(max_length=100)
    createdbygroup = models.CharField(max_length=100)
    datecreated = models.DateTimeField()
    datesent = models.DateTimeField(auto_now_add=True)
    datemodified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s' %(self.proizvodjac, self.imei)

class DeletedTable(models.Model):
    kontakt = models.CharField(max_length=20)
    proizvodjac = models.CharField(max_length=20)
    model = models.CharField(max_length=20, blank=True, default='', null=True)
    imei = models.CharField(max_length=15)
    unlock = models.CharField(max_length=100, blank=True, default='', null=True)
    status = models.IntegerField(default=0)
    log = models.TextField()
    winlock = models.CharField(max_length=20, blank=True, default='', null=True)
    winlockversion = models.CharField(max_length=20, blank=True, default='', null=True)
    createdby = models.CharField(max_length=100)
    createdbygroup = models.CharField(max_length=100)
    datecreated = models.DateTimeField()
    datesent = models.DateTimeField(auto_now_add=True)
    datemodified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s' %(self.proizvodjac, self.imei)

class UnlockTable(models.Model):
    imei = models.CharField(max_length=15)
    proizvodjac = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    unlock = models.CharField(max_length=50)

    def __str__(self):
        return self.imei

class MyTAC(models.Model):
    tac = models.CharField(max_length=8)
    proizvodjac = models.CharField(max_length=20)
    model = models.CharField(max_length=20)

    def __str__(self):
        return '%s %s' %(self.tac, self.model)

class Vendor(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=200, default='a.miljkovic@vipmobile.rs')
    cc = models.CharField(max_length=200, default='a.miljkovic@vipmobile.rs')
    subject = models.CharField(max_length=50)
    mailbody = models.TextField()
    
    def __str__(self):
        return self.name

class AceTable(models.Model):
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=200, default='polls/static/acebackup/')
    log = models.TextField()
    datecreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class NokiaModels(models.Model):
    model = models.CharField(max_length=20)
    modeltype = models.CharField(max_length=20)
    typeid = models.CharField(max_length=20, blank=True, default='', null=True)
    fullwinlock = models.CharField(max_length=20, blank=True, default='', null=True)
    winlock = models.CharField(max_length=20, blank=True, default='', null=True)
    version = models.CharField(max_length=20, blank=True, default='', null=True)
    altversion = models.CharField(max_length=20, blank=True, default='', null=True)

    def __str__(self):
        return self.model

class AlcatelUnlock(models.Model):
    imei = models.CharField(max_length=15)
    unlock = models.CharField(max_length=50)
    
    def __str__(self):
        return '%s %s' %(self.imei, self.unlock)

class HtcUnlock(models.Model):
    imei = models.CharField(max_length=15)
    unlock = models.CharField(max_length=50)
    
    def __str__(self):
        return '%s %s' %(self.imei, self.unlock)

class HuaweiUnlock(models.Model):
    imei = models.CharField(max_length=15)
    unlock = models.CharField(max_length=50)
    
    def __str__(self):
        return '%s %s' %(self.imei, self.unlock)

class LgUnlock(models.Model):
    imei = models.CharField(max_length=15)
    unlock = models.CharField(max_length=50)
    
    def __str__(self):
        return '%s %s' %(self.imei, self.unlock)

class LumiaUnlock(models.Model):
    imei = models.CharField(max_length=15)
    unlock = models.CharField(max_length=50)
    
    def __str__(self):
        return '%s %s' %(self.imei, self.unlock)

class NokiaUnlock(models.Model):
    imei = models.CharField(max_length=15)
    unlock = models.CharField(max_length=50)
    
    def __str__(self):
        return '%s %s' %(self.imei, self.unlock)

class SamsungUnlock(models.Model):
    imei = models.CharField(max_length=15)
    unlock = models.CharField(max_length=50)
    
    def __str__(self):
        return '%s %s' %(self.imei, self.unlock)

class SonyUnlock(models.Model):
    imei = models.CharField(max_length=15)
    unlock = models.CharField(max_length=50)
    
    def __str__(self):
        return '%s %s' %(self.imei, self.unlock)

class ZteUnlock(models.Model):
    imei = models.CharField(max_length=15)
    unlock = models.CharField(max_length=50)
    
    def __str__(self):
        return '%s %s' %(self.imei, self.unlock)

class SearchLog(models.Model):
    imei = models.CharField(max_length=15)
    username = models.CharField(max_length=100)
    usergroup = models.CharField(max_length=100)
    lockstatus = models.CharField(max_length=1)
    datenow = models.DateTimeField(auto_now_add=True)    
    
    def __str__(self):
        return '%s %s' %(self.imei, self.username)

class Counters(models.Model):
    name_01 = models.CharField(max_length=30, blank=True, default='', null=True)
    counter_01 = models.IntegerField(default=0)
    name_02 = models.CharField(max_length=30, blank=True, default='', null=True)
    counter_02 = models.IntegerField(default=0)
    name_03 = models.CharField(max_length=30, blank=True, default='', null=True)
    counter_03 = models.IntegerField(default=0)
    name_04 = models.CharField(max_length=30, blank=True, default='', null=True)
    counter_04 = models.IntegerField(default=0)
    name_05 = models.CharField(max_length=30, blank=True, default='', null=True)
    counter_05 = models.IntegerField(default=0)
    name_06 = models.CharField(max_length=30, blank=True, default='', null=True)
    counter_06 = models.IntegerField(default=0)
    name_07 = models.CharField(max_length=30, blank=True, default='', null=True)
    counter_07 = models.IntegerField(default=0)
    name_08 = models.CharField(max_length=30, blank=True, default='', null=True)
    counter_08 = models.IntegerField(default=0)
    name_09 = models.CharField(max_length=30, blank=True, default='', null=True)
    counter_09 = models.IntegerField(default=0)
    name_10 = models.CharField(max_length=30, blank=True, default='', null=True)
    counter_10 = models.IntegerField(default=0)


