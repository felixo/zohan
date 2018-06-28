# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'DayStatus'
        db.create_table('record_daystatus', (
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('status', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('record', ['DayStatus'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'DayStatus'
        db.delete_table('record_daystatus')
    
    
    models = {
        'record.daystatus': {
            'Meta': {'object_name': 'DayStatus'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        },
        'record.record': {
            'Meta': {'object_name': 'Record'},
            'address': ('django.db.models.fields.TextField', [], {'max_length': '128'}),
            'catering': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'coloring': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'haircare': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'laminate': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'man_haircut': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'metro': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'session_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'woman_haircut': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        }
    }
    
    complete_apps = ['record']
