from django.conf.urls import url, include
from .views import post_list, post_detail, post_create, user_profile_page, PostLikeToggle

urlpatterns = [
    url(r'^$', post_list,name='post_list'),
    url(r'^detail/(?P<slug>[\w-]+)/$', post_detail, name='detail'),
    url(r'^create/$',post_create, name='create'),
    url(r'user/(?P<username>[\w-]+)/$', user_profile_page, name='user_profile_page'),
    url(r'^(?P<slug>[\w-]+)/like/$', PostLikeToggle.as_view(), name='like-toggle'),
]
