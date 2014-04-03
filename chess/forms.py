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
        'duplicate_name': _("A user with that name already exists."),
    }

    class Meta:
        model = Player
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control', 'required' : True, 'autofocus': True}),
            'rating': forms.NumberInput(attrs={'placeholder':'Rating', 'class': 'form-control', 'required' : True}),
            'tournament': forms.HiddenInput()
        }

    def cleam_name(self):
        name = self.cleaned_data["name"]
        try:
            Player.objects.get(name=name, tournament=self.tournament)
        except Player.DoesNotExist:
            return name
        raise forms.ValidationError(
            self.error_messages['duplicate_name'],
            code='duplicate',
        )


class RoundForms(forms.ModelForm):
    serial_number = forms.IntegerField(widget=forms.HiddenInput(), label=_('Round number'))
    
    class Meta:
        model = Round
        widgets = {
            'tournament': forms.HiddenInput(),
            'players': forms.CheckboxSelectMultiple(attrs={'class': 'list-unstyled'}),
        }

    def save(self, commit=True):
        cur_round = super(RoundForms, self).save(commit)
        if commit:
            cur_round.create_pairs()
        return cur_round


class PairForms(forms.ModelForm):
    class Meta:
        model = Pair
        fields = ('winner', )