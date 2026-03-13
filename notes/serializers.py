from rest_framework import serializers
from .models import Note, Category, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class NoteSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True, default=None)

    class Meta:
        model = Note
        fields = [
            'id', 'title', 'body', 'category', 'category_name',
            'tags', 'color', 'is_pinned', 'is_trashed',
            'reminder', 'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']
