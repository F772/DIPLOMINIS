from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
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
    review = models.ForeignKey('Review', related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.review.title}"


class Reaction(models.Model):
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