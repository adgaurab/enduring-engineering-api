from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.conf import settings
from .models import Article, Author, Image
from django.core.mail import send_mail


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Author
        fields = ['id', 'email', 'first_name', 'last_name', 'password', 'date_of_birth', 'language', 'country',
                  'organisation', 'totem']

    def create(self, validated_data):
        name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        subject = 'Enduring Engineering'
        message = f'<h2>Hi {name} {last_name} , <br> Thank you for registering in enduring Engineering web Portal.' \
                  f'<br><a href="https://wiki-front-test.web.app"><button type="button">Click For Website</button>' \
                  f'</a></h2>'
        email_from = settings.EMAIL_HOST_USER
        email = validated_data.get('email')
        recipient_list = [email]
        send_mail(subject, message, email_from, recipient_list, html_message=message)
        return Author.objects.create(**validated_data)


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'user_id', 'title', 'description', 'language', 'place_name', 'gps', 'status', 'image_id',
                  'introduction', 'background', 'purpose_of_paper', 'methods_of_teaching', 'discussion', 'conclusion',
                  'tags']


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = ['image']


class UserInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Token
        fields = ['user_id']
