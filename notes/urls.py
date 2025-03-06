from django.urls import path
from . import views


urlpatterns = [
    path('', views.ListCreateNoteAPIView.as_view(), name='get_post_notes'),
    path('bulk', views.BulkCreateNoteAPIView.as_view(), name='batch_create_notes'),
    path('filter', views.FilterNotesAPIView.as_view(), name='get_filter_notes'),
    path('<int:pk>/', views.RetrieveUpdateDestroyNoteAPIView.as_view(), name='get_delete_update_note'),
]
