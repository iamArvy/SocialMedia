
from django.urls import path

from . import views

urlpatterns = [
    # path("p/following", views.index, name="index_check"),
    path('', views.index, {'type': 'all'}, name='index'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create/<str:type>', views.create, name='create_post'),
    path('edit/<str:type>/<int:id>', views.edit, name='edit'),
    path('delete/<str:type>/<int:id>', views.delete, name='delete'),
    path('like/<str:type>/<int:id>', views.like, name='like'),
    path('profile/<str:name>/<str:type>', views.follow, name='follow'),
    path('profile/<str:name>/', views.profile, name='profile'),
    path('following', views.index, {'type': 'following'}, name='following'),
    path('posts/<str:type>', views.Post, name='posts' )
]
