from django.contrib import admin
from bioinfuse.models import *


class MemberAdmin(admin.ModelAdmin):
    list_filter = ('user', 'show_name', 'role')
    list_display = ('user', 'show_name', 'role')


class ChallengeAdmin(admin.ModelAdmin):
    list_filter = ('title', 'is_open', 'start_date', 'subs_start_date',
                   'subm_start_date')
    list_display = ('title', 'is_open', 'start_date', 'stop_date',
                    'subs_start_date', 'subs_stop_date', 'subm_start_date',
                    'subm_stop_date')


class AssociatedKeyAdmin(admin.ModelAdmin):
    list_filter = ('challenge', 'candidate')
    list_display = ('challenge', 'candidate')


class MovieAdmin(admin.ModelAdmin):
    list_filter = ('challenge', 'title', 'submit_date')
    list_display = ('challenge', 'title', 'submit_date')


class ArticleAdmin(admin.ModelAdmin):
    list_filter = ['author', 'creation_date', 'edit_date', 'published']
    list_display = ('title', 'author', 'creation_date', 'edit_date', 'published')


class PageAdmin(admin.ModelAdmin):
    list_filter = ['author', 'creation_date', 'edit_date', 'published']
    list_display = ('title', 'author', 'creation_date', 'edit_date', 'published')


class VoteAdmin(admin.ModelAdmin):
    list_filter = ['id_jury', 'id_challenge']
    list_display = ('id_jury', 'id_challenge', 'id_movie', 'global_note')

admin.site.register(Member, MemberAdmin)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(AssociatedKey, AssociatedKeyAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Vote, VoteAdmin)
