# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'RatingHistory', fields ['player', 'tournament', 'date']
        db.delete_unique(u'chess_ratinghistory', ['player_id', 'tournament_id', 'date'])

        # Deleting model 'RatingHistory'
        db.delete_table(u'chess_ratinghistory')

        # Adding field 'Player.tournament'
        db.add_column(u'chess_player', 'tournament',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='players', to=orm['chess.Tournament']),
                      keep_default=False)

        # Adding unique constraint on 'Player', fields ['name', 'tournament']
        db.create_unique(u'chess_player', ['name', 'tournament_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Player', fields ['name', 'tournament']
        db.delete_unique(u'chess_player', ['name', 'tournament_id'])

        # Adding model 'RatingHistory'
        db.create_table(u'chess_ratinghistory', (
            ('rating', self.gf('django.db.models.fields.IntegerField')()),
            ('tournament', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['chess.Tournament'])),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['chess.Player'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'chess', ['RatingHistory'])

        # Adding unique constraint on 'RatingHistory', fields ['player', 'tournament', 'date']
        db.create_unique(u'chess_ratinghistory', ['player_id', 'tournament_id', 'date'])

        # Deleting field 'Player.tournament'
        db.delete_column(u'chess_player', 'tournament_id')


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
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['chess.Tournament']"})
        },
        u'chess.tournament': {
            'Meta': {'object_name': 'Tournament'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['chess']