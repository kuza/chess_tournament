# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Player'
        db.create_table(u'chess_player', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('rating', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'chess', ['Player'])

        # Adding model 'Tournament'
        db.create_table(u'chess_tournament', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'chess', ['Tournament'])

        # Adding model 'RatingHistory'
        db.create_table(u'chess_ratinghistory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['chess.Player'])),
            ('tournament', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['chess.Tournament'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('rating', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'chess', ['RatingHistory'])

        # Adding unique constraint on 'RatingHistory', fields ['player', 'tournament', 'date']
        db.create_unique(u'chess_ratinghistory', ['player_id', 'tournament_id', 'date'])

        # Adding model 'Round'
        db.create_table(u'chess_round', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('serial_number', self.gf('django.db.models.fields.IntegerField')()),
            ('tournament', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['chess.Tournament'])),
        ))
        db.send_create_signal(u'chess', ['Round'])

        # Adding unique constraint on 'Round', fields ['serial_number', 'tournament']
        db.create_unique(u'chess_round', ['serial_number', 'tournament_id'])

        # Adding M2M table for field players on 'Round'
        m2m_table_name = db.shorten_name(u'chess_round_players')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('round', models.ForeignKey(orm[u'chess.round'], null=False)),
            ('player', models.ForeignKey(orm[u'chess.player'], null=False))
        ))
        db.create_unique(m2m_table_name, ['round_id', 'player_id'])

        # Adding model 'Pair'
        db.create_table(u'chess_pair', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('round', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['chess.Round'])),
            ('white', self.gf('django.db.models.fields.related.ForeignKey')(related_name='white', to=orm['chess.Player'])),
            ('black', self.gf('django.db.models.fields.related.ForeignKey')(related_name='black', to=orm['chess.Player'])),
            ('winner', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'chess', ['Pair'])

        # Adding unique constraint on 'Pair', fields ['round', 'white', 'black']
        db.create_unique(u'chess_pair', ['round_id', 'white_id', 'black_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Pair', fields ['round', 'white', 'black']
        db.delete_unique(u'chess_pair', ['round_id', 'white_id', 'black_id'])

        # Removing unique constraint on 'Round', fields ['serial_number', 'tournament']
        db.delete_unique(u'chess_round', ['serial_number', 'tournament_id'])

        # Removing unique constraint on 'RatingHistory', fields ['player', 'tournament', 'date']
        db.delete_unique(u'chess_ratinghistory', ['player_id', 'tournament_id', 'date'])

        # Deleting model 'Player'
        db.delete_table(u'chess_player')

        # Deleting model 'Tournament'
        db.delete_table(u'chess_tournament')

        # Deleting model 'RatingHistory'
        db.delete_table(u'chess_ratinghistory')

        # Deleting model 'Round'
        db.delete_table(u'chess_round')

        # Removing M2M table for field players on 'Round'
        db.delete_table(db.shorten_name(u'chess_round_players'))

        # Deleting model 'Pair'
        db.delete_table(u'chess_pair')


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
            'Meta': {'object_name': 'Player'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'rating': ('django.db.models.fields.IntegerField', [], {})
        },
        u'chess.ratinghistory': {
            'Meta': {'unique_together': "(('player', 'tournament', 'date'),)", 'object_name': 'RatingHistory'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['chess.Player']"}),
            'rating': ('django.db.models.fields.IntegerField', [], {}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['chess.Tournament']"})
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