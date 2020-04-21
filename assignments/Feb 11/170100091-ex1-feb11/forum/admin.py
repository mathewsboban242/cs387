from django.contrib import admin
from forum.models import User, Topic, Comment

admin.site.register(Topic)
admin.site.register(Comment)
admin.site.register(User)