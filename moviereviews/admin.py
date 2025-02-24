from django.contrib import admin
from .models import Movie, Genre, Director, Review, Comment, Reaction
from django.utils.html import format_html


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'director', 'image_preview')  # Pridėta nuotraukų peržiūra
    search_fields = ('title', 'director__name')
    list_filter = ('year', 'genres')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" style="border-radius: 5px;" />', obj.image.url)
        return "Nėra nuotraukos"

    image_preview.short_description = 'Nuotrauka'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'movie', 'rating')
    list_filter = ('rating',)
    search_fields = ('title', 'movie__title')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'review')


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ('reaction_type', 'review')



