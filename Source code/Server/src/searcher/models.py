# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Definition(models.Model):
    def_field = models.CharField(db_column='def', max_length=1000, blank=True, null=True)  # Field renamed because it was a Python reserved word.
    idword = models.ForeignKey('Word', models.DO_NOTHING, db_column='idword', blank=True, null=True)
    isapproved = models.BooleanField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'definition'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Example(models.Model):
    idex = models.AutoField(primary_key=True)
    sentence = models.CharField(max_length=500, blank=True, null=True)
    iddef = models.ForeignKey(Definition, models.DO_NOTHING, db_column='iddef', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'example'


class Phonetic(models.Model):
    prefix = models.CharField(max_length=60, blank=True, null=True)
    ipa = models.CharField(max_length=45, blank=True, null=True)
    sound = models.CharField(max_length=500, blank=True, null=True)
    idword = models.ForeignKey('Word', models.DO_NOTHING, db_column='idword', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'phonetic'


class Word(models.Model):
    idword = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    pos = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'word'
