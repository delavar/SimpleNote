from rest_framework import serializers
from .models import Note
from django.contrib.auth import get_user_model

User = get_user_model()


class NoteSerializer(serializers.ModelSerializer):

    creator_name = serializers.SerializerMethodField()
    creator_username = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Note
        fields = ('id', 'title', 'description', 'created_at',
                  'updated_at', 'creator_name', 'creator_username')
        read_only_fields = ['created_at', 'updated_at',
                            'id', 'creator_name', 'creator_username']
        list_serializer_class = serializers.ListSerializer

    def get_creator_name(self, obj):
        if obj.creator:
            return f"{obj.creator.first_name} {obj.creator.last_name}".strip() or obj.creator.username
        return None
