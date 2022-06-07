from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('overall', views.overall, name='overall'),
    path('author/<int:a_id>', views.author_det, name='author'),
]
