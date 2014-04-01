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


class Player(NameModel):
    tournament = models.ForeignKey(Tournament, verbose_name=_('Tournament'), related_name='players')
    rating = models.IntegerField(_('Rating'))
    
    class Meta:
        unique_together = ('name', 'tournament')


class Round(models.Model):
    serial_number = models.IntegerField(_('Serial number'), editable=False)
    tournament = models.ForeignKey(Tournament, verbose_name=_('Tournament'), related_name='rounds')
    players = models.ManyToManyField(Player, verbose_name=_('Players'), null=True, blank=True)
    
    class Meta:
        unique_together = ('serial_number', 'tournament')

    def __unicode__(self):
        return '%s %s' % (self.tournament.name, self.serial_number)


class Pair(models.Model):
    WINNER_CHOICES = (
        (0, _('White')),
        (1, _('Black')),
        (2, _('Draw')),
    )

    round = models.ForeignKey(Round, verbose_name=_('Round'))
    white = models.ForeignKey(Player, verbose_name=_('White'), related_name='white')
    black = models.ForeignKey(Player, verbose_name=_('Black'), related_name='black')
    winner = models.IntegerField(_('Winner'), choices = WINNER_CHOICES, blank=True, null=True)
    
    class Meta:
        unique_together = ('round', 'white', 'black')
