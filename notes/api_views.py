from rest_framework import generics
from .models import Note
from .serializers import NoteSerializer


class NoteListAPI(generics.ListAPIView):
    serializer_class = NoteSerializer

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user, is_trashed=False)


class NoteCreateAPI(generics.CreateAPIView):
    serializer_class = NoteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NoteDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)
