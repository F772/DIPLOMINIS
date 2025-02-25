from django.contrib import admin
from .models import Movie, Genre, Director, Review, Comment, Reaction
from django.utils.html import format_html


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """
    Filmo administravimo klasė.

    Ši klasė leidžia valdyti 'Movie' modelį Django administravimo sąsajoje. Ji nustato, kokie duomenys bus rodomi sąraše,
    paieškos laukus ir filtrus, taip pat prideda nuotraukos peržiūros funkciją.

    Atributai:
    - list_display: Apibrėžia stulpelius, kurie bus rodomi filmo sąraše (pavadinimas, metai, režisierius ir nuotraukos peržiūra).
    - search_fields: Apibrėžia laukus, pagal kuriuos bus galima ieškoti (pavadinimas ir režisierius).
    - list_filter: Leidžia filtruoti sąrašą pagal metus ir žanrus.

    Metodai:
    - image_preview: Atsakingas už filmo nuotraukos atvaizdavimą administravimo sąsajoje. Jei nuotrauka yra, ji bus rodoma,
      jei ne – bus parodyta žinutė "Nėra nuotraukos".
    """
    list_display = ('title', 'year', 'director', 'image_preview')
    search_fields = ('title', 'director__name')
    list_filter = ('year', 'genres')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" style="border-radius: 5px;" />', obj.image.url)
        return "Nėra nuotraukos"

    image_preview.short_description = 'Nuotrauka'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """
    Žanro administravimo klasė.

    Ši klasė leidžia valdyti 'Genre' modelį Django administravimo sąsajoje.
    Ji nustato, kokie duomenys bus rodomi žanro sąraše.

    Atributai:
    - list_display: Apibrėžia stulpelius, kurie bus rodomi žanro sąraše (tik žanro pavadinimas).
    """
    list_display = ('name',)


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    """
    Režisieriaus administravimo klasė.

    Ši klasė leidžia valdyti 'Director' modelį Django administravimo sąsajoje.
    Ji nustato, kokie duomenys bus rodomi režisieriaus sąraše ir pagal kokius laukus bus galima ieškoti.

    Atributai:
    - list_display: Apibrėžia stulpelius, kurie bus rodomi režisieriaus sąraše (tik režisieriaus vardas).
    - search_fields: Apibrėžia laukus, pagal kuriuos bus galima ieškoti (režisieriaus vardas).
    """
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Apžvalgos administravimo klasė.

    Ši klasė leidžia valdyti 'Review' modelį Django administravimo sąsajoje.
    Ji nustato, kokie duomenys bus rodomi apžvalgos sąraše, pagal kokius laukus bus galima filtruoti ir ieškoti.

    Atributai:
    - list_display: Apibrėžia stulpelius, kurie bus rodomi apžvalgos sąraše (pavadinimas, filmas, įvertinimas).
    - list_filter: Leidžia filtruoti apžvalgas pagal įvertinimą.
    - search_fields: Apibrėžia laukus, pagal kuriuos bus galima ieškoti (apžvalgos pavadinimas ir filmo pavadinimas).
    """
    list_display = ('title', 'movie', 'rating')
    list_filter = ('rating',)
    search_fields = ('title', 'movie__title')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Komentaro administravimo klasė.

    Ši klasė leidžia valdyti 'Comment' modelį Django administravimo sąsajoje.
    Ji nustato, kokie duomenys bus rodomi komentaro sąraše.

    Atributai:
    - list_display: Apibrėžia stulpelius, kurie bus rodomi komentaro sąraše (komentaro turinys ir su juo susijusi apžvalga).
    """
    list_display = ('content', 'review')


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    """
    Reakcijos administravimo klasė.

    Ši klasė leidžia valdyti 'Reaction' modelį Django administravimo sąsajoje.
    Ji nustato, kokie duomenys bus rodomi reakcijų sąraše.

    Atributai:
    - list_display: Apibrėžia stulpelius, kurie bus rodomi reakcijos sąraše (reakcijos tipas ir susijusi apžvalga).
    """
    list_display = ('reaction_type', 'review')



