from django.db import models
from django.contrib.auth.models import User


NOTE_COLORS = [
    ('#ffffff', 'White'),
    ('#fff9c4', 'Yellow'),
    ('#f8bbd0', 'Pink'),
    ('#c8e6c9', 'Green'),
    ('#bbdefb', 'Blue'),
    ('#d1c4e9', 'Purple'),
    ('#ffe0b2', 'Orange'),
    ('#f5f5f5', 'Gray'),
]


class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')

    class Meta:
        verbose_name_plural = 'categories'
        unique_together = ['name', 'user']

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tags')

    class Meta:
        unique_together = ['name', 'user']

    def __str__(self):
        return self.name


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='notes')
    tags = models.ManyToManyField(Tag, blank=True, related_name='notes')
    color = models.CharField(max_length=7, choices=NOTE_COLORS, default='#ffffff')
    is_pinned = models.BooleanField(default=False)
    is_trashed = models.BooleanField(default=False)
    reminder = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_pinned', '-updated_at']

    def __str__(self):
        return self.title
