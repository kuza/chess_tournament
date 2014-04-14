from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Tournament, Player, Round, Pair 

class TournamentForms(forms.ModelForm):
    class Meta:
        model = Tournament
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control', 'required' : True, 'autofocus': True}),
            'winners_count': forms.NumberInput(attrs={'placeholder':'Count of winners', 'class': 'form-control', 'required' : True}),
        }

class PlayerForms(forms.ModelForm):
    error_messages = {
        'duplicate_name': _("A player with that name already exists."),
    }

    class Meta:
        model = Player
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control', 'required' : True, 'autofocus': True}),
            'rating': forms.NumberInput(attrs={'placeholder':'Rating', 'class': 'form-control', 'required' : True}),
            'tournament': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super(PlayerForms, self).__init__(*args, **kwargs)
        ordered_fields = ['tournament', 'name']
        self.fields.keyOrder = ordered_fields + [k for k in self.fields.keys() if k not in ordered_fields]

    def clean_name(self):
        name = self.cleaned_data["name"]
        tournament = self.cleaned_data["tournament"]
        
        try:
            Player.objects.get(name=name, tournament=tournament)
        except Player.DoesNotExist:
            return name
        raise forms.ValidationError(
            self.error_messages['duplicate_name'],
            code='duplicate',
        )


class RoundForms(forms.ModelForm):
    serial_number = forms.IntegerField(widget=forms.HiddenInput(), label=_('Round number'))
    
    error_messages = {
        'round_error': _("You can't create more rounds than calculated."),
    }

    class Meta:
        model = Round
        widgets = {
            'tournament': forms.HiddenInput(),
            'players': forms.CheckboxSelectMultiple(attrs={'class': 'list-unstyled'}),
        }

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial')
        tournament = initial.get('tournament') if initial else None
        players = initial.get('players') if initial else None
        
        super(RoundForms, self).__init__(*args, **kwargs)
        
        queryset = self.fields['players'].queryset
        if tournament: 
            queryset = queryset.filter(tournament=tournament)
        if players:
            queryset = queryset.filter(id__in=[player.id for player in players])
            
        self.fields['players'].queryset = queryset 

    def clean_players(self):
        players = self.cleaned_data["players"]
        tournament = self.cleaned_data["tournament"]
        last_round = tournament.last_round
        serial_number = last_round.serial_number if last_round else 0
        if (serial_number > tournament.get_count_rounds(len(players))
            or serial_number == tournament.count_rounds):
            raise forms.ValidationError(
                self.error_messages['round_error'],
                code='round_error',
            )
        return players

    def save(self, commit=True):
        cur_round = super(RoundForms, self).save(commit)
        if commit:
            cur_round.create_pairs()
        return cur_round


class PairForms(forms.ModelForm):
    class Meta:
        model = Pair
        fields = ('winner', )