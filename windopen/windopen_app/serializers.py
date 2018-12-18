from django.forms import widgets
from rest_framework import serializers
from windopen.models import Snippet


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ("id", "title", "code", "linenos")