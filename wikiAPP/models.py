from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import UserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.hashers import make_password


class Author(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    date_modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True, null=True,
                                       blank=True)

    first_name = models.CharField(_('first name'), max_length=30, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True, null=True)

    language = models.CharField(blank=True, max_length=100)
    country = models.CharField(blank=True, max_length=20)
    organisation = models.CharField(blank=True, max_length=60)
    totem = models.CharField(blank=True, max_length=50)
    request = models.CharField(blank=True, max_length=120)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.email

    @property
    def manager(self):
        return self.manager_set_all()

    def save(self, *args, **kwargs):
        self.password = make_password(self.password, salt=None, hasher='default')
        super().save(*args, **kwargs)


class Article(models.Model):
    user_id = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    description = models.TextField()
    language = models.CharField(max_length=120)
    place_name = models.CharField(max_length=120)
    gps = models.CharField(max_length=120)
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=True)
    image_id = models.CharField(max_length=250)
    introduction = models.TextField()
    background = models.TextField()
    purpose_of_paper = models.TextField()
    methods_of_teaching = models.TextField()
    discussion = models.TextField()
    conclusion = models.TextField()
    tags = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title


class Image(models.Model):
    image = models.ImageField(upload_to='image', blank=True)


class Tags(models.Model):
    tags = models.CharField(max_length=100, blank=True)
