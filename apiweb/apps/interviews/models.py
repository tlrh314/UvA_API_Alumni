from __future__ import unicode_literals, absolute_import, division

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

from tinymce.models import HTMLField

from ..alumni.models import Alumnus

# class Category(models.Model):
#     title           = models.CharField(max_length=200, default="Category")
#     type_id         = models.CharField(max_length=25, default="Unique ID")
#
#     def __str__(self):
#         return self.title


class Post(models.Model):
    author          = models.ForeignKey('auth.User', default=None)
    title           = models.CharField(max_length=300)
    slug            = models.SlugField(unique=True, blank=True, null=True,
        help_text="Short teaser for in the bloglist")
    teaser          = models.CharField(max_length=300, blank=True,
        help_text="Short teaser for in the bloglist")
    content         = HTMLField(default="")
    is_published    = models.BooleanField(default=False)
    date_created    = models.DateTimeField(blank=True, null=True)
    date_published  = models.DateTimeField(default=timezone.now, blank=True, null=True)

    # category = models.ForeignKey(Category, help_text='Category', default=1)
    # featured = models.BooleanField(default=False,
    #         help_text="Should this post be shown in the featured list?")
    # top_story = models.BooleanField(default=False,
    #         help_text="Should this post be shown in the top stories list?")
    # front_page = models.BooleanField(default=False,
    #         help_text="Should this post be shown on the home page?")

    class Meta:
        ordering = ['-date_published',]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.teaser = self.content[0:200]
        self.date_created = timezone.now()
        super(Post, self).save(*args, **kwargs)

    def publish(self):
        self.date_published = timezone.now()
        self.is_published = True
        self.save()

    @property
    def author_name(self):
        alumnus = Alumnus.objects.get(user=self.author)
        print(alumnus)
        return alumnus.full_name

    def __str__(self):
        return self.title

