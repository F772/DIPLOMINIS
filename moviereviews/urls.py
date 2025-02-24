from django.urls import path
from django.contrib.auth import views as auth_views
from .views import movie_list, MovieDetailView, add_review, CommentCreateView, ReactionCreateView, RegisterView, UserProfileView, MyReviewsView, ReviewListView, SearchResultsView


urlpatterns = [
    path('', movie_list, name='movie_list'),
    path('movie/<int:movie_id>/', MovieDetailView.as_view(), name='movie_detail'),
    path('reviews/', ReviewListView.as_view(), name='reviews'),
    path('my-reviews/', MyReviewsView.as_view(), name='my_reviews'),
    path('search/', SearchResultsView.as_view(), name='search'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('movie/<int:movie_id>/review/', add_review, name='add_review'),
    path('review/<int:review_id>/comment/', CommentCreateView.as_view(), name='add_comment'),
    path('review/<int:review_id>/reaction/<str:reaction_type>/', ReactionCreateView.as_view(), name='add_reaction'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]