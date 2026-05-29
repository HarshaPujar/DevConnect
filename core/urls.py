from django.urls import path
from .views import home, about, login_page, signup_page, dashboard, post_page, logout_page, delete_post, edit_post, like_post, add_comment, profile_page, follow_user

urlpatterns = [
    path('', home),
    path('about/', about),
    path('login/', login_page),
    path('signup/', signup_page),
    path('dashboard/', dashboard),
    path('post/', post_page),
    path('logout/', logout_page),
    path('delete/<int:id>/', delete_post),
    path('edit/<int:id>/', edit_post),
    path('like/<int:id>/', like_post),
    path('comment/<int:id>/', add_comment),
    path('profile/<str:username>/', profile_page),
    path('follow/<str:username>/', follow_user),
]