from rest_framework import routers
from django.conf.urls import url
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'article', views.ArticleViewSet)
router.register(r'post-article', views.PostArticleViewSet)
router.register(r'image', views.ImageArticleViewSet)
router.register(r'user_info', views.UserInfoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r"^user-key/", views.Userdata.as_view(), name="weather"),
    url(r"^tags-article/", views.TagsArticle.as_view(), name="tags"),
    url(r"^search-location/", views.SearchArticle.as_view(), name="search"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
