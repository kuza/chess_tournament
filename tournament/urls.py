from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from chess import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tournament.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', views.HomePageView.as_view(), name='home'),
    
    url(r'^signin$', 'django.contrib.auth.views.login', {'template_name': 'chess/signin.html', 'extra_context': {'signin': True}}),
    url(r'^signout$', 'django.contrib.auth.views.logout_then_login', {'login_url': '/signin'}),
    
    url(r'^manage/tournament/$', views.TournamentCreate.as_view(), name='tournaments'),
    url(r'^manage/tournament/(?P<pk>\d+)/$', views.TournamentDetail.as_view(), name='tournament_detail'),
    url(r'^manage/tournament/(?P<pk>\d+)/delete/$', views.TournamentDelete.as_view(), name='tournament_delete'),

    url(r'^manage/player/$', views.PlayerCreate.as_view(), name='player_create'),
    url(r'^manage/player/(?P<pk>\d+)/delete/$', views.PlayerDelete.as_view(), name='player_delete'),

    url(r'^manage/round/$', views.RoundCreate.as_view(), name='round_create'),
)
