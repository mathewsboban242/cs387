from django.shortcuts import render

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from ideas.serializers import IdeaSerializer
from ideas.models import Idea

class IdeaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer

def home(request):
	# if request.user.is_authenticated:
	return render(None, 'ideas.html')
