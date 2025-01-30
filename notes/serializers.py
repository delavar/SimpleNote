from rest_framework import serializers
from .models import Note
from django.contrib.auth.models import User


class NoteSerializer(serializers.ModelSerializer):  # create class to serializer model
    creator = serializers.ReadOnlyField(source='creator.first_name')

    class Meta:
        model = Note
        fields = ('id', 'title', 'description', 'creator')


class UserSerializer(serializers.ModelSerializer):  # create class to serializer user model
    notes = serializers.PrimaryKeyRelatedField(many=True, queryset=Note.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'notes')
