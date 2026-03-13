from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Auth
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='notes/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),

    # Notes
    path('', views.note_list, name='note_list'),
    path('note/new/', views.note_create, name='note_create'),
    path('note/<int:pk>/', views.note_detail, name='note_detail'),
    path('note/<int:pk>/edit/', views.note_edit, name='note_edit'),
    path('note/<int:pk>/delete/', views.note_delete, name='note_delete'),
    path('note/<int:pk>/pin/', views.note_pin, name='note_pin'),
    path('note/<int:pk>/autosave/', views.note_autosave, name='note_autosave'),

    # Export
    path('note/<int:pk>/export/txt/', views.note_export_txt, name='note_export_txt'),
    path('note/<int:pk>/export/md/', views.note_export_md, name='note_export_md'),

    # Trash
    path('trash/', views.trash_list, name='trash_list'),
    path('trash/<int:pk>/restore/', views.note_restore, name='note_restore'),
    path('trash/<int:pk>/delete/', views.note_permanent_delete, name='note_permanent_delete'),

    # Categories
    path('categories/', views.category_manage, name='category_manage'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
]
