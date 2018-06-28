# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Deleting field 'Record.session'
        db.delete_column('record_record', 'session_id')
    
    
    def backwards(self, orm):
        
        # Adding field 'Record.session'
        db.add_column('record_record', 'session', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['sessions.Session']), keep_default=False)
    
    
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'woman_haircut': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        }
    }
    
    complete_apps = ['record']
