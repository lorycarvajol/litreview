from django.urls import path
from .views import (
    CustomLoginView,
    register,
    home_view,
    custom_logout_view,
    create_review_autonomous,
    create_ticket,
    create_review,
    user_posts_view,
    edit_ticket,
    delete_ticket,
    edit_review,
    delete_review,
    subscription_view,  # Vue pour afficher la page d'abonnement
    follow_user,  # Vue pour suivre un utilisateur
    unfollow_user,  # Vue pour se désabonner d'un utilisateur
    followed_user_posts_view,  # Vue pour afficher les posts d'un utilisateur suivi
    search_users,  # Vue pour la recherche d'utilisateurs
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("register/", register, name="register"),
    path("home/", home_view, name="home"),
    path("logout/", custom_logout_view, name="logout"),
    path("ticket/create/", create_ticket, name="create_ticket"),
    path("review/create/<int:ticket_id>/", create_review, name="create_review"),
    path(
        "create_review_autonomous/",
        create_review_autonomous,
        name="create_review_autonomous",
    ),
    path("posts/", user_posts_view, name="user_posts"),
    path("edit_ticket/<int:ticket_id>/", edit_ticket, name="edit_ticket"),
    path("delete_ticket/<int:ticket_id>/", delete_ticket, name="delete_ticket"),
    path("edit_review/<int:review_id>/", edit_review, name="edit_review"),
    path("delete_review/<int:review_id>/", delete_review, name="delete_review"),
    path("subscriptions/", subscription_view, name="subscription"),  # Page d'abonnement
    path(
        "follow/<int:user_id>/", follow_user, name="follow_user"
    ),  # Suivre un utilisateur
    path(
        "unfollow/<int:user_id>/", unfollow_user, name="unfollow_user"
    ),  # Se désabonner
    path(
        "user_posts/<int:user_id>/",
        followed_user_posts_view,
        name="followed_user_posts",
    ),  # Afficher les posts d'un utilisateur suivi
    path(
        "subscriptions/search/", search_users, name="search_users"
    ),  # Recherche d'utilisateurs
]
