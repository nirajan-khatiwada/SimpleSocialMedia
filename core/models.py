from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.
class Profile(models.Model):
    user=models.ForeignKey(User,null=False,blank=False,on_delete=models.CASCADE)
    userid=models.IntegerField()
    location=models.CharField(max_length=50)
    bio=models.CharField(max_length=50,blank=True)
    profile_img=models.ImageField(upload_to="profile",default="default.png")

    def __str__(self):
        return self.user.username
    def follower(self):
        return Follower.objects.filter(user=self.user).count()
    






class Follower(models.Model):
    user=models.ForeignKey(User,null=False,blank=False,on_delete=models.CASCADE,related_name="usr")
    followers=models.ForeignKey(User,null=False,blank=False,on_delete=models.CASCADE,related_name="usrflr")
    def __str__(self):
        return f'follower of {self.user} by {self.followers}'


class Like(models.Model):
    post_id=models.CharField(max_length=50,null=True)
    user=models.ForeignKey(User,null=False,blank=False,on_delete=models.CASCADE)


class Post(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    user=models.ForeignKey(User,null=False,blank=False,on_delete=models.CASCADE)
    image=models.ImageField(upload_to="post")
    caption=models.CharField(max_length=100)
    create=models.DateTimeField(auto_now=True,blank=True)
    like=models.IntegerField(default=0)
    def __str__(self):
        return self.user.username
    def profile(self):
        return Profile.objects.get(user=self.user)
    
    

