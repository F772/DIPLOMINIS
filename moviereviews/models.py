from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    """
    Modelis, skirtas filmų žanrams saugoti.

    Laukai:
    - name: Žanro pavadinikmas (maksimalus ilgis - 100 simobiliai, unikalus).

    Metodai:
    - __str__(): Grąžina žanro pavadinimą kaip teksto atvaizdavimą.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Director(models.Model):
    """
    Modelis, skirtas filmų režisieriams saugoti.

    Laukai:
    - name: Režisieriaus vardas ir pavardė (maksimalus ilgis – 255 simboliai).
    - bio: Režisieriaus biografija (gali būti tuščia).

    Metodai:
    - __str__(): Grąžina režisieriaus vardą kaip teksto atvaizdavimą.
    """
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    """
    Modelis, skirtas filmų duomenims saugoti.

    Laukai:
    - title: Filmo pavadinimas (maksimalus ilgis – 255 simboliai).
    - description: Filmo aprašymas.
    - year: Filmo išleidimo metai.
    - genres: Daugelio prie daugelio ryšys su žanrais (gali būti tuščias).
    - director: Užsienio raktas į režisierių (gali būti tuščias, nustatomas kaip NULL pašalinus susijusį įrašą).
    - imdb_id: IMDb identifikacinis numeris (unikalus, gali būti tuščias).
    - image: Filmo plakato ar nuotraukos laukas (gali būti tuščias).

    Metodai:
    - display_genres(): Gražina pirmus tris filmo žanrus kaip eilutę.
    - __str__(): Grąžina filmo pavadinimą kaip teksto atvaizdavimą.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    year = models.IntegerField()
    genres = models.ManyToManyField(Genre, blank=True)
    director = models.ForeignKey(Director, on_delete=models.SET_NULL, null=True, blank=True)
    imdb_id = models.CharField(max_length=20, blank=True, null=True, unique=True)
    image = models.ImageField(upload_to='movie_images/', blank=True, null=True)

    def display_genres(self):
        res = ', '.join(elem.name for elem in self.genres.all()[:3])
        return res

    def __str__(self):
        return self.title


class Review(models.Model):
    """
    Modelis, skirtas filmų apžvalgoms saugoti.

    Laukai:
    - user: Užsienio raktas į vartotoją, kuris parašė apžvalgą (susieta su User modeliu).
    - movie: Užsienio raktas į filmą, kuriam skirta apžvalga (susieta su Movie modeliu).
    - title: Apžvalgos pavadinimas (maksimalus ilgis – 255 simboliai).
    - content: Apžvalgos turinys.
    - rating: Įvertinimas nuo 1 iki 5 (pasirinkimų laukas).
    - created_at: Apžvalgos sukūrimo data ir laikas (nustatomas automatiškai).
    - approved: Laukas, nurodantis, ar apžvalga patvirtinta (numatytasis – `False`).

    Metodai:
    - __str__(): Grąžina apžvalgos pavadinimą kartu su vartotojo vardu kaip teksto atvaizdavimą.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.user.username}"


class Comment(models.Model):
    """
    Modelis, skirtas apžvalgų komentarams saugoti.

    Laukai:
    - review: Užsienio raktas į apžvalgą, kuriai priklauso komentaras (susieta su Review modeliu).
    - user: Užsienio raktas į vartotoją, kuris parašė komentarą (susieta su User modeliu).
    - content: Komentaro turinys.
    - created_at: Komentaro sukūrimo data ir laikas (nustatomas automatiškai).

    Metodai:
    - __str__(): Grąžina vartotojo vardą ir apžvalgos pavadinimą kaip teksto atvaizdavimą.
    """
    review = models.ForeignKey('Review', related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.review.title}"


class Reaction(models.Model):
    """
    Modelis, skirtas apžvalgų reakcijoms (patinka/nepatinka) saugoti.

    Laukai:
    - LIKE, DISLIKE: Galimos reakcijų reikšmės.
    - REACTION_CHOICES: Pasirinkimų sąrašas, leidžiantis pasirinkti tarp "Like" ir "Dislike".
    - user: Užsienio raktas į vartotoją, kuris paliko reakciją (susieta su User modeliu).
    - review: Užsienio raktas į apžvalgą, kuriai taikoma reakcija (susieta su Review modeliu).
    - reaction_type: Reakcijos tipas ("like" arba "dislike").

    Meta:
    - unique_together: Užtikrina, kad vienas vartotojas gali palikti tik vieną reakciją tam pačiam atsiliepimui.

    Metodai:
    - __str__(): Grąžina vartotojo vardą, reakcijos tipą ir apžvalgos pavadinimą kaip teksto atvaizdavimą.
    """
    LIKE = 'like'
    DISLIKE = 'dislike'
    REACTION_CHOICES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='reactions')
    reaction_type = models.CharField(max_length=10, choices=[('like', 'Like'), ('dislike', 'Dislike')])

    class Meta:
        unique_together = ('user', 'review')

    def __str__(self):
        return f"{self.user.username} {self.reaction_type} {self.review}"
