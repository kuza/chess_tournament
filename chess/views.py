from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy

from .models import Tournament, Player, Round, Pair
from .forms import TournamentForms, PlayerForms, RoundForms, PairForms

class HomePageView(TemplateView):
    template_name = 'chess/home.html'
    
    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['home'] = True
        return context


class TournamentCreate(CreateView):
    model = Tournament
    form_class = TournamentForms
    success_url = reverse_lazy('tournaments')

    def get_context_data(self, **kwargs):
        context = super(TournamentCreate, self).get_context_data(**kwargs)
        context['object_list'] = Tournament.objects.order_by('-id').all()
        context['manage'] = True
        return context


class TournamentDetail(DetailView):
    model = Tournament

    def get_context_data(self, **kwargs):
        context = super(TournamentDetail, self).get_context_data(**kwargs)
        
        context['players'] = context['object'].players.all()
        context['player_form'] = PlayerForms(initial={'tournament': context['object']})
        
        context['rounds'] =context['object'].rounds.all()
        context['round_form'] = RoundForms(initial={'tournament': context['object']})
        
        context['manage'] = True
        return context


class TournamentDelete(DeleteView):
    model = Tournament
    success_url = reverse_lazy('tournaments')


class RoundCreate(CreateView):
    model = Round
    form_class = RoundForms
    
    def get(self, request, *args, **kwargs):
        try:
            tournament = Tournament.objects.get(id = request.GET.get('tournament'))
            last_round = tournament.rounds.order_by('-serial_number').first()
            serial_number = last_round.serial_number if last_round else 0
            self.initial.update(tournament=tournament, players=last_round.players.all() if last_round else tournament.players.all(), serial_number=serial_number+1)
        except Tournament.DoesNotExist:
            pass
        
        return super(RoundCreate, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RoundCreate, self).get_context_data(**kwargs)
        
        context['manage'] = True
        return context

    def get_success_url(self):
        return reverse_lazy('round_detail', kwargs={'pk': self.object.pk})


class RoundDetail(DetailView):
    model = Round

    def get_context_data(self, **kwargs):
        context = super(RoundDetail, self).get_context_data(**kwargs)
        context['pairs'] = context['object'].pairs.order_by('serial_number')
        context['manage'] = True
        return context


class RoundDelete(DeleteView):
    model = Round
    
    def get_success_url(self):
        return reverse_lazy('tournament_detail', kwargs={'pk': self.object.tournament.pk})


class PairUpdate(UpdateView):
    model = Pair
    form_class = PairForms
    
    def get_success_url(self):
        return reverse_lazy('round_detail', kwargs={'pk': self.object.round.pk})


class PlayerCreate(CreateView):
    model = Player
    form_class = PlayerForms

    def get_success_url(self):
        return reverse_lazy('tournament_detail', kwargs={'pk': self.object.tournament.pk})


class PlayerDelete(DeleteView):
    model = Player

    def get_success_url(self):
        return reverse_lazy('tournament_detail', kwargs={'pk': self.object.tournament.pk})
    