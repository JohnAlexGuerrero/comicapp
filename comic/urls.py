from django.urls import path

from .views import ComicDetailView

urlpatterns = [
    path('<slug:comic_slug>/', ComicDetailView.as_view(), name='show_comic'),
]
