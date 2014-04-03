from math import log

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator


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
    def count_rounds(self):
        if self.last_round:
            players = self.last_round.players.count()
        else:
            players = self.players.count()
            
        if players and self.winners_count:
            return log(players, 2) + log(self.winners_count, 2)

        return 0


class Player(NameModel):
    tournament = models.ForeignKey(Tournament, verbose_name=_('Tournament'), related_name='players')
    rating = models.IntegerField(_('Rating'))
    
    class Meta:
        unique_together = ('name', 'tournament')


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

    def create_pairs(self):
        count_players_in_first_group = self.players.count() // 2
        if self.serial_number == 1:
            second_group = self.players.order_by('-rating')[count_players_in_first_group:]
            pair = 0
            for player in self.players.order_by('-rating')[:count_players_in_first_group]:
                Pair.objects.create(serial_number=pair+1, round=self, white=player, black=second_group[pair])
                pair += 1
            
            try:
                Pair.objects.create(serial_number=pair+1, round=self, white=second_group[pair], black=second_group[pair], winner=0)
            except IndexError:
                pass


class Pair(models.Model):
    WINNER_CHOICES = (
        (0, _('White')),
        (1, _('Black')),
        (2, _('Draw')),
    )

    serial_number = models.IntegerField(_('Pair number'))
    round = models.ForeignKey(Round, verbose_name=_('Round'), related_name='pairs')
    white = models.ForeignKey(Player, verbose_name=_('White'), related_name='white')
    black = models.ForeignKey(Player, verbose_name=_('Black'), related_name='black')
    winner = models.IntegerField(_('Winner'), choices = WINNER_CHOICES, blank=True, null=True)
    
    class Meta:
        unique_together = ('round', 'white', 'black')

