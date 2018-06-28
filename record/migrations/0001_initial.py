# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Record'
        db.create_table('record_record', (
            ('comment', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('coloring', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('contacts', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('catering', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('woman_haircut', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('man_haircut', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('haircare', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
        ))
        db.send_create_signal('record', ['Record'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Record'
        db.delete_table('record_record')
    
    
    models = {
        'record.record': {
            'Meta': {'object_name': 'Record'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'catering': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'coloring': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'comment': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'contacts': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
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
