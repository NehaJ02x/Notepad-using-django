from django.contrib import admin
from django.urls import path, include
from notes import api_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('notes.urls')),

    # REST API
    path('api/notes/', api_views.NoteListAPI.as_view(), name='api_note_list'),
    path('api/create-note/', api_views.NoteCreateAPI.as_view(), name='api_note_create'),
    path('api/notes/<int:pk>/', api_views.NoteDetailAPI.as_view(), name='api_note_detail'),
]
