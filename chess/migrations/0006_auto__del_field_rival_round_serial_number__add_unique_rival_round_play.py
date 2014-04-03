# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Rival.round_serial_number'
        db.delete_column(u'chess_rival', 'round_serial_number')

        # Adding unique constraint on 'Rival', fields ['round', 'player']
        db.create_unique(u'chess_rival', ['round_id', 'player_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Rival', fields ['round', 'player']
        db.delete_unique(u'chess_rival', ['round_id', 'player_id'])

        # Adding field 'Rival.round_serial_number'
        db.add_column(u'chess_rival', 'round_serial_number',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    models = {
        u'chess.pair': {
            'Meta': {'unique_together': "(('round', 'white', 'black'),)", 'object_name': 'Pair'},
            'black': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'black'", 'to': u"orm['chess.Player']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pairs'", 'to': u"orm['chess.Round']"}),
            'serial_number': ('django.db.models.fields.IntegerField', [], {}),
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
        u'chess.rival': {
            'Meta': {'unique_together': "(('round', 'player'),)", 'object_name': 'Rival'},
            'color': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rivals'", 'to': u"orm['chess.Player']"}),
            'rival': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['chess.Player']"}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rivals'", 'to': u"orm['chess.Round']"}),
            'score': ('django.db.models.fields.FloatField', [], {})
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