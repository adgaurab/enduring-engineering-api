from rest_framework import viewsets, mixins

from . import serializers
from .models import Article, Author, Image
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.http import HttpResponse

from .serializers import UserSerializer, ArticleSerializer, ImageSerializer, UserInfoSerializer
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Author.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class PostArticleViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class ImageArticleViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class UserInfoViewSet(ModelViewSet):
    serializer_class = UserInfoSerializer
    queryset = Token.objects.all()


class Userdata(APIView):
    def get_user(self, token):
        auth_id = Token.objects.values_list('user_id', flat=True).get(key=token)
        user_details = Author.objects.filter(id=auth_id).values('id', 'first_name', 'last_name', 'email')
        return user_details

    def get_post(self, id):
        auth_id = Token.objects.values_list('user_id', flat=True).get(key=id)
        post = Article.objects.filter(user_id_id=auth_id).values('id', 'title')
        return post

    def get(self, request):
        token = request.query_params.get('token')
        id = self.get_user(token)
        post = self.get_post(token)
        data = {
            'user_info': id,
            'mypost': post
        }
        return Response(data)


class TagsArticle(APIView):
    def get_article(self, tag):
        tags_article = Article.objects.filter(tags=tag).values('id', 'title')
        return tags_article

    def get(self, request):
        tag = request.query_params.get('tag')
        data = self.get_article(tag)
        return Response(data)


class SearchArticle(APIView):
    def get_article(self, place_name):
        tags_article = Article.objects.filter(place_name__contains=place_name).values('id', 'title')
        return tags_article

    def get(self, request):
        tag = request.query_params.get('tag')
        data = self.get_article(tag.lower())
        if not data:
            return Response('Data empty')
        return Response(data)
