# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'Record.metro'
        db.add_column('record_record', 'metro', self.gf('django.db.models.fields.CharField')(default='', max_length=32), keep_default=False)
    
    
    def backwards(self, orm):
        
        # Deleting field 'Record.metro'
        db.delete_column('record_record', 'metro')
    
    
    models = {
        'record.record': {
            'Meta': {'object_name': 'Record'},
            'address': ('django.db.models.fields.TextField', [], {'max_length': '128'}),
            'catering': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'coloring': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'haircare': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'man_haircut': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'metro': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'session_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'woman_haircut': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        }
    }
    
    complete_apps = ['record']
