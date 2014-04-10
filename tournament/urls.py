from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

admin.autodiscover()

from chess import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tournament.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', views.HomePageView.as_view(), name='home'),
    url(r'^tournament/(?P<pk>\d+)/$', views.TournamentDetail.as_view(), name='tournament'),
    url(r'^player/(?P<pk>\d+)/$', views.PlayerDetail.as_view(), name='player'),
    
    url(r'^signin$', 'django.contrib.auth.views.login', {'template_name': 'chess/signin.html', 'extra_context': {'signin': True}}),
    url(r'^signout$', 'django.contrib.auth.views.logout_then_login', {'login_url': '/signin'}),
    
    url(r'^manage/tournament/$', login_required(views.TournamentCreate.as_view(), login_url='/signin'), name='tournaments'),
    url(r'^manage/tournament/(?P<pk>\d+)/$', login_required(views.TournamentDetail.as_view(), login_url='/signin'), name='tournament_detail'),
    url(r'^manage/tournament/(?P<pk>\d+)/delete/$', login_required(views.TournamentDelete.as_view(), login_url='/signin'), name='tournament_delete'),

    url(r'^manage/player/$', login_required(views.PlayerCreate.as_view(), login_url='/signin'), name='player_create'),
    url(r'^manage/player/(?P<pk>\d+)/delete/$', login_required(views.PlayerDelete.as_view(), login_url='/signin'), name='player_delete'),

    url(r'^manage/round/$', login_required(views.RoundCreate.as_view(), login_url='/signin'), name='round_create'),
    url(r'^manage/round/(?P<pk>\d+)/$', login_required(views.RoundDetail.as_view(), login_url='/signin'), name='round_detail'),
    url(r'^manage/round/(?P<pk>\d+)/delete/$', login_required(views.RoundDelete.as_view(), login_url='/signin'), name='round_delete'),
    
    url(r'^manage/pair/(?P<pk>\d+)/$', login_required(views.PairUpdate.as_view(), login_url='/signin'), name='pair_update'),

    url(r'^manage/player/(?P<pk>\d+)/$', login_required(views.PlayerDetail.as_view(), login_url='/signin'), name='player_detail'),
    
 )
