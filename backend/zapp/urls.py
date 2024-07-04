# urls.py

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import ImageURLView, RegisterView, LoginView,AddMovieView,LogoutView, ReadMoviesView, RetrieveImageView,UpdateMovieView, DeleteMovieView,getmovbyid 
from .views import isauthenticated, FilterMoviesView,SearchMoviesView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    #path('', IndexView.as_view(), name='index'),
   # path('add-zapp/', AddZappView.as_view(), name='add-zapp'),
    path('logout/',LogoutView.as_view(),name='logout'),
     path('add/', AddMovieView.as_view(), name='add'),
     path('read/',ReadMoviesView.as_view(),name='read'),
     path('update/<str:movie_id>/',UpdateMovieView.as_view(),name = 'update'),
     path('delete/<str:movie_id>/',DeleteMovieView.as_view(),name='delete'),
     path('getmovbyid/<str:movie_id>/',getmovbyid.as_view(),name = 'getmovbyid'),
     path('isauthenticated/',isauthenticated,name ='isauthenticated'),
     path('search/',SearchMoviesView.as_view(),name='search'),
     path('filter/',FilterMoviesView.as_view(),name='filter'),
      path('store/', ImageURLView.as_view(), name='store_image_url'),
    path('ret/', RetrieveImageView.as_view(), name='retrieve_images'),

]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
