from django.contrib import admin
from chess import models


class BaseAdmin(admin.ModelAdmin):
    pass


class RoundAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'tournament')


class PairAdmin(admin.ModelAdmin):
    list_display = ('round', 'white', 'black', 'winner')


admin.site.register(models.Player, BaseAdmin)
admin.site.register(models.Tournament, BaseAdmin)
admin.site.register(models.Round, RoundAdmin)
admin.site.register(models.Pair, PairAdmin)
