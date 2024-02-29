from django.urls import path
from .views import home,signup,logins,logouts,settings,upload,like,profile,follow,search,follow_home

urlpatterns = [
    path("",home,name="home"),
    path("signup/",signup,name='signup'),
    path("login/",logins,name='login'),
    path("logout/",logouts,name='logout'),
    path("settings/",settings,name='settings'),
    path("upload/",upload,name="upload"),
    path("like/<id>",like,name="like"),
    path("profile/<id>/",profile,name="profile"),
    path("follow/<id>/",follow,name="follow"),
    path("follow_home/<id>/",follow_home,name="follow_home"),
    path("search/",search,name="search")

]
