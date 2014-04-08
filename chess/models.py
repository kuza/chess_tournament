from math import log

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator
from django.db import connection

class NameModel(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    
    class Meta:
        abstract = True
    
    def __unicode__(self):
        return self.name


class Tournament(NameModel):
    winners_count = models.IntegerField(_('Count of winners'), default=1, validators=[MinValueValidator(1)])
    
    @property
    def last_round(self):
        return self.rounds.order_by('-serial_number').first()
    
    @property
    def in_progress(self):
        if self.last_round:
            return self.last_round.in_progress
        return False
    
    @property
    def list_rounds(self):
        last_round = self.last_round
        last_serial_number = last_round.serial_number if last_round else 0
        real_count_rounds = self.count_rounds
        result = []
        for i in range(self.get_count_rounds(self.players.count())):
            result.append(dict(serial_number=i+1, is_current=bool(last_serial_number==i+1), is_canceled=bool(real_count_rounds<i+1)))
        return result
        
    @property
    def count_rounds(self):
        if self.last_round:
            players = self.last_round.players.count()
        else:
            players = self.players.count()
        
        return self.get_count_rounds(players)
    
    def get_count_rounds(self, players=None):
        if players and self.winners_count:
            return int(log(players, 2)) + (int(log(self.winners_count-1, 2)) if self.winners_count > 1 else 0)

        return 0


class Player(NameModel):
    tournament = models.ForeignKey(Tournament, verbose_name=_('Tournament'), related_name='players')
    rating = models.IntegerField(_('Rating'))
    
    class Meta:
        unique_together = ('name', 'tournament')
        
    @property
    def new_rating(self):
        return self.rating + (self.rivals.aggregate(rating=models.Sum('rating')).get('rating') or 0)
    
    @property
    def k_factor(self):
        #### I have used USCF
        if self.new_rating < 2100:
            return 32
        elif self.new_rating < 2400:
            return 24
        else:
            return 16


class Round(models.Model):
    serial_number = models.IntegerField(_('Round number'))
    tournament = models.ForeignKey(Tournament, verbose_name=_('Tournament'), related_name='rounds')
    players = models.ManyToManyField(Player, verbose_name=_('Players'))
    
    class Meta:
        unique_together = ('serial_number', 'tournament')

    def __unicode__(self):
        return '%s %s' % (self.tournament.name, self.serial_number)
    
    @property
    def progress(self):
        return '{pairs} / {winners}'.format(pairs=self.pairs.count(), winners=self.pairs.filter(winner__isnull=False).count())
    
    @property
    def in_progress(self):
        return self.pairs.count() != self.pairs.filter(winner__isnull=False).count()

    def _get_user_group(self, group, exclude_user):
        return self.players.exclude(id__in=[exclude_user.id] if exclude_user else []).filter(id__in=Rival.objects.values('player').annotate(sum_score=models.Sum('score')).filter(sum_score=group).values_list('player', flat=True)).order_by('-rating')
    
    def _get_colors(self, player1, player2=None, winner=None):
        colors = {0: 'white', 1: 'black'}
        if player2:
            player1_prev = player1.rivals.order_by('-round__id')[0].color
            player2_prev = player2.rivals.order_by('-round__id')[0].color 
            if player1_prev == player2_prev:
                if self.serial_number != 2:
                    player1_prev_prev = player1.rivals.order_by('-round__id')[1].color
                    player2_prev_prev = player2.rivals.order_by('-round__id')[1].color
                else:
                    player1_prev_prev = player2_prev_prev = player1_prev
                    
                if player1_prev_prev == player1_prev_prev:
                    return {colors[player1_prev_prev]: player2, colors[0 if player1_prev_prev else 1]: player1}
                elif player2_prev_prev == player2_prev_prev:
                    return {colors[player2_prev_prev]: player1, colors[0 if player2_prev_prev else 1]: player2}
                else:
                    return {colors[player2_prev_prev]: player1, colors[player1_prev_prev]: player2}
            else:
                return {colors[player2_prev]: player1, colors[player1_prev]: player2}
                
        player1_prev = player1.rivals.order_by('-round__id')[0].color
        return {colors[0 if player1_prev else 1]: player1, colors[player1_prev]: None, "winner": winner or (0 if player1_prev else 1)}

    def create_pairs(self):
        winner = None
        if self.serial_number > self.tournament.get_count_rounds(self.players.count()):
            winner = 3
            
        if self.serial_number == 1:
            count_players_in_first_group = self.players.count() // 2
            second_group = self.players.order_by('-rating')[count_players_in_first_group:]
            pair = 0
            for player in self.players.order_by('-rating')[:count_players_in_first_group]:
                Pair.objects.create(serial_number=pair+1, round=self, white=player, black=second_group[pair], winner=winner)
                pair += 1
            
            try:
                Pair.objects.create(serial_number=pair+1, round=self, white=second_group[pair], black=None, winner=winner or 0)
            except IndexError:
                pass
        else:
            cursor = connection.cursor()
            groups = [ group for (group, ) in cursor.execute('''
                SELECT score FROM (
                    SELECT SUM(score) AS score FROM chess_rival
                    INNER JOIN chess_round ON (chess_rival.round_id = chess_round.id)
                    WHERE chess_round.tournament_id = %s AND player_id IN (
                        SELECT player_id FROM chess_round_players WHERE round_id = %s)
                    GROUP BY player_id)
                GROUP BY score 
                ORDER BY score DESC''', [self.tournament.id, self.id]).fetchall()]
            exclude_user = None
            pair_number = 1
            for i in range(len(groups)) :
                group = groups[i]
                
                cur_group = self._get_user_group(group, exclude_user)
                exclude_user = None
                cur_group_count = cur_group.count()
                
                if cur_group_count % 2 != 0 and i != len(groups)-1:
                    exclude_user = self._get_user_group(groups[i+1], []).first()
                    cur_group_count += 1
                
                count_players_in_first_group = cur_group_count // 2
                second_group = cur_group[count_players_in_first_group:]
                
                pair = 0
                for player in cur_group[:count_players_in_first_group]:
                    try:
                        Pair.objects.create(serial_number=pair_number, round=self, winner=winner, **self._get_colors(player, second_group[pair]))
                        pair += 1
                    except IndexError:
                        Pair.objects.create(serial_number=pair_number, round=self, winner=winner, **self._get_colors(player, exclude_user))
                    pair_number += 1

                try:
                    Pair.objects.create(serial_number=pair_number, round=self, **self._get_colors(second_group[pair], winner=winner))
                except IndexError:
                    pass


class Pair(models.Model):
    WINNER_CHOICES = (
        (0, _('White')),
        (1, _('Black')),
        (2, _('Draw')),
        (3, _('Cancel'))
    )

    serial_number = models.IntegerField(_('Pair number'))
    round = models.ForeignKey(Round, verbose_name=_('Round'), related_name='pairs')
    white = models.ForeignKey(Player, verbose_name=_('White'), related_name='white', blank=True, null=True)
    black = models.ForeignKey(Player, verbose_name=_('Black'), related_name='black', blank=True, null=True)
    winner = models.IntegerField(_('Winner'), choices = WINNER_CHOICES, blank=True, null=True)
    
    class Meta:
        unique_together = ('round', 'white', 'black')


class Rival(models.Model):
    COLOR_CHOICES = (
        (0, _('White')),
        (1, _('Black')),
    )

    round = models.ForeignKey(Round, verbose_name=_('Round'), related_name='rivals')
    player = models.ForeignKey(Player, verbose_name=_('Player'), related_name='rivals')
    rival = models.ForeignKey(Player, verbose_name=_('Rival'), blank=True, null=True)
    score = models.FloatField(_('Score'), default=0)
    color = models.IntegerField(_('Color'), choices = COLOR_CHOICES)
    rating = models.IntegerField(_('Rating'), default=0)
    
    class Meta:
        unique_together = ('round', 'player')

def post_save_task(sender, instance, **kwargs):
    if isinstance(instance, Pair):
        if instance.white:
            try:
                rival = Rival.objects.get(round=instance.round, player=instance.white)
            except Rival.DoesNotExist:
                rival = Rival(round=instance.round, player=instance.white)
                
            rival.rival = instance.black
            rival.color = 0
            rival.score = 0.5 if instance.winner == 2 else 1 if instance.winner == 0 else 0
            if instance.black:
                rival.rating = round(instance.white.k_factor*(rival.score - (1/(1+10**((instance.black.new_rating-instance.white.new_rating)/400)))), 0)
            
            rival.save()

        if instance.black:
            try:
                rival = Rival.objects.get(round=instance.round, player=instance.black)
            except Rival.DoesNotExist:
                rival = Rival(round=instance.round, player=instance.black)
                
            rival.rival = instance.white
            rival.color = 1
            rival.score = 0.5 if instance.winner == 2 else 1 if instance.winner == 1 else 0
            if instance.white:
                rival.rating = round(instance.black.k_factor*(rival.score - (1/(1+10**((instance.white.new_rating-instance.black.new_rating)/400)))), 0)
    
            rival.save()

models.signals.post_save.connect(post_save_task)
