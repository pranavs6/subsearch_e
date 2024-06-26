from django.contrib import admin
from django.urls import path
from subtitle_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload_video/', views.upload_video, name='upload_video'),
    path('search/', views.SearchSubtitlesView.as_view(), name='search_subtitles'),
]

