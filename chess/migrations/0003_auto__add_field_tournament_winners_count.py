# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Tournament.winners_count'
        db.add_column(u'chess_tournament', 'winners_count',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Tournament.winners_count'
        db.delete_column(u'chess_tournament', 'winners_count')


    models = {
        u'chess.pair': {
            'Meta': {'unique_together': "(('round', 'white', 'black'),)", 'object_name': 'Pair'},
            'black': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'black'", 'to': u"orm['chess.Player']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['chess.Round']"}),
            'white': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'white'", 'to': u"orm['chess.Player']"}),
            'winner': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'chess.player': {
            'Meta': {'unique_together': "(('name', 'tournament'),)", 'object_name': 'Player'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'rating': ('django.db.models.fields.IntegerField', [], {}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'players'", 'to': u"orm['chess.Tournament']"})
        },
        u'chess.round': {
            'Meta': {'unique_together': "(('serial_number', 'tournament'),)", 'object_name': 'Round'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'players': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['chess.Player']", 'symmetrical': 'False'}),
            'serial_number': ('django.db.models.fields.IntegerField', [], {}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rounds'", 'to': u"orm['chess.Tournament']"})
        },
        u'chess.tournament': {
            'Meta': {'object_name': 'Tournament'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'winners_count': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['chess']