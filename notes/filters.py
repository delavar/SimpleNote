from django_filters import rest_framework as filters


# We create filters for each field we want to be able to filter on
class NoteFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')
    updated__lte = filters.DateTimeFilter(field_name='updated_at', lookup_expr='lte')
    updated__gte = filters.DateTimeFilter(field_name='updated_at', lookup_expr='gte')

    class Meta:
        model = None
        fields = ['title', 'description', 'updated__lte', 'updated__gte']
