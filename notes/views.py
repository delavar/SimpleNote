from .filters import NoteFilter
from .pagination import CustomPagination
from .serializers import NoteSerializer
from .permissions import IsOwnerOrReadOnly
from .models import Note
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView, ListAPIView,
    CreateAPIView)


class ListCreateNoteAPIView(ListCreateAPIView):
    """API view for listing and creating a single note"""
    serializer_class = NoteSerializer
    queryset = Note.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return self.queryset.filter(creator=self.request.user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class BulkCreateNoteAPIView(CreateAPIView):
    """API view for batch creation of multiple notes at once"""
    serializer_class = NoteSerializer
    queryset = Note.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        if not isinstance(request.data, list):
            raise ValidationError(
                "invalid data format. expected a list of items.")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(creator=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RetrieveUpdateDestroyNoteAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class FilterNotesAPIView(ListAPIView):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = NoteFilter
    pagination_class = CustomPagination

    def get_queryset(self):
        return self.queryset.filter(creator=self.request.user)
