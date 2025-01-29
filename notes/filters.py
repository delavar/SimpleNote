from django_filters import rest_framework as filters

# We create filters for each field we want to be able to filter on
class NoteFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')
    creator__username = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = None
        fields = ['title', 'description', 'creator__username']
