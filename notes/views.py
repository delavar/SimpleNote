from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from .models import Note
from .permissions import IsOwnerOrReadOnly
from .serializers import NoteSerializer
from .pagination import CustomPagination
from .filters import NoteFilter


class ListCreateNoteAPIView(ListCreateAPIView):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = NoteFilter

    def perform_create(self, serializer):
        # Assign the user who created the note
        serializer.save(creator=self.request.user)


class RetrieveUpdateDestroyNoteAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
