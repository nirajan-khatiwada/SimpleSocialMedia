from django.contrib import admin
from .models import Profile,Post,Follower,Like
# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Follower)
admin.site.register(Like)