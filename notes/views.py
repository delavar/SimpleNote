from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from rest_framework.response import Response

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

    def create(self, request, *args, **kwargs):
        # Override create to support batch creation
        if isinstance(request.data, list):
            # When request data is a list, handle batch creation
            serializer = self.get_serializer(data=request.data, many=True)
            if serializer.is_valid():
                serializer.save(creator=self.request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                # Detail validation error for each item
                errors = []
                for index, error in enumerate(serializer.errors):
                    if error:
                        error['index'] = index
                        errors.append(error)
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Default single instance creation
            return super().create(request, *args, **kwargs)

    def get_queryset(self):
        return self.queryset.filter(creator=self.request.user)

    def perform_create(self, serializer):
        # Assign the user who created the note
        serializer.save(creator=self.request.user)


class RetrieveUpdateDestroyNoteAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class FilterNotesAPIView(ListCreateAPIView):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = NoteFilter

    def get_queryset(self):
        return self.queryset.filter(creator=self.request.user)

    def perform_create(self, serializer):
        # Assign the user who created the note
        serializer.save(creator=self.request.user)
