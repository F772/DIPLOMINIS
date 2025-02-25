from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Movie, Review, Comment, Genre, Reaction
from .forms import ReviewForm, CommentForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from imdb import IMDb


def movie_list(request):
    """
    Rodo filmų sarašą.
    Filtruoja filmus pagal žanrą arba metus.
    :param request: Pasirinkimas pagal žanrą arba metus
    :return:
    """
    genre_filter = request.GET.get('genre', '')
    year_filter = request.GET.get('year', '')

    movies = Movie.objects.all()

    if genre_filter.isdigit():
        movies = movies.filter(genres__id=int(genre_filter))

    if year_filter.isdigit():
        movies = movies.filter(year=int(year_filter))

    genres = Genre.objects.all()
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('-year')

    return render(request, 'movie_list.html', {'movies': movies, 'genres': genres, 'years': years})


class MovieDetailView(View):
    """
    Ši klasė rodo pasirinkto filmo detales.
    Ji parodo filmą, jo atsiliepimus su laikais ir IMDb reitingą.

    :param request: vartotojo užklausa
    :param movie_id: filmo ID, kad žinotume, kurį filmą parodyti
    :return: HTML puslapis su filmo informacija, atsiliepimais ir IMDb įvertinimu
    """

    def get(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)

        reviews = Review.objects.filter(movie=movie)

        ia = IMDb()

        for review in reviews:
            review.likes_count = review.reactions.filter(reaction_type=Reaction.LIKE).count()
            review.dislikes_count = review.reactions.filter(reaction_type=Reaction.DISLIKE).count()

        imdb_rating = None

        if movie.imdb_id:
            imdb_movie = ia.get_movie(movie.imdb_id[2:])
            imdb_rating = imdb_movie.get('rating', None)

        return render(request, 'movie_detail.html', {
            'movie': movie,
            'reviews': reviews,
            'imdb_rating': imdb_rating,
        })


class ReviewListView(View):
    """
    Ši klasė rodo visų atsiliepimų sąrašą, pradedant nuo naujausių.
    """

    def get(self, request):
        reviews = Review.objects.all().order_by('-created_at')

        return render(request, 'review_list.html', {'reviews': reviews})


class CommentCreateView(View):
    """
    Ši klasė leidžia vartotojui kurti komentarus atsiliepimams.
    Ji rodo formą komentaro rašymui ir įrašo komentarą, jei forma užpildyta teisingai.
    """

    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        form = CommentForm()
        return render(request, 'comment_form.html', {'form': form,
                                                     'review': review})

    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.review = review
            comment.user = request.user
            comment.save()
            return redirect('movie_detail',
                            movie_id=review.movie.id)
        return render(request, 'comment_form.html', {'form': form,
                                                     'review': review})


@method_decorator(login_required, name='dispatch')
class MyReviewsView(View):
    """
    Ši klasė rodo visus tavo parašytus atsiliepimus.
    Tik prisijungę vartotojai gali matyti savo atsiliepimus.
    """

    def get(self, request):
        reviews = Review.objects.filter(user=request.user)
        return render(request, 'my_reviews.html',
                      {'reviews': reviews})


def home(request):
    return render(request,
                  'registration/home.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'registration/register.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class UserProfileView(View):
    def get(self, request):
        return render(request, 'profile.html', {'user': request.user})


class SearchResultsView(View):
    """
    Ši klasė rodo paieškos rezultatus filmų sąraše.
    Jei įvedei paieškos tekstą, parodoma tik filmų pavadinimai, kurie atitinka tą tekstą.
    """

    def get(self, request):
        query = request.GET.get('search_text', '').strip()
        results = Movie.objects.all()

        if query:
            results = results.filter(title__icontains=query)

        return render(request, 'search_results.html', {'results': results, 'query': query})


def add_review(request, movie_id):
    """
    Ši funkcija leidžia vartotojui pridėti atsiliepimą apie pasirinktą filmą.

    :param request: vartotojo užklausa su įvestais duomenimis
    :param movie_id: filmo identifikatorius, kad žinotume, kurio filmo atsiliepimą rašome
    :return: HTML puslapis su atsiliepimo forma arba nukreipimas į filmo puslapį po sėkmingo išsaugojimo
    """
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()

            return redirect('movie_detail', movie_id=movie.id)
    else:
        form = ReviewForm()

    context = {
        'movie': movie,
        'form': form,
    }
    return render(request, 'review_form.html', context)


class ReactionCreateView(View):
    """
    Ši klasė leidžia vartotojui pateikti balsą („patinka“ arba „nepatinka“) atsiliepimui.
    """

    def post(self, request, review_id, reaction_type):
        review = get_object_or_404(Review,
                                   id=review_id)

        if reaction_type in ['like', 'dislike']:

            reaction, created = Reaction.objects.get_or_create(
                user=request.user,
                review=review,
                defaults={'reaction_type': reaction_type}
            )

            if not created:
                reaction.reaction_type = reaction_type
                reaction.save()

        return redirect('movie_detail', movie_id=review.movie.id)
