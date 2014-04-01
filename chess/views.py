from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy

from .models import Tournament, Player
from .forms import TournamentForms, PlayerForms, RoundForms

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
        
        context['players'] =context['object'].players.all()
        context['player_form'] = PlayerForms(initial={'tournament': context['object']})
        
        context['rounds'] =context['object'].rounds.all()
        context['round_form'] = RoundForms(initial={'tournament': context['object']})
        
        context['manage'] = True
        return context

class TournamentDelete(DeleteView):
    model = Tournament
    success_url = reverse_lazy('tournaments')


class RoundCreate(CreateView):
    model = Player
    form_class = RoundForms

class PlayerCreate(CreateView):
    model = Player
    form_class = PlayerForms

    def get_success_url(self):
        return reverse_lazy('tournament_detail', kwargs={'pk': self.object.tournament.pk})

class PlayerDelete(DeleteView):
    model = Player

    def get_success_url(self):
        return reverse_lazy('tournament_detail', kwargs={'pk': self.object.tournament.pk})
    