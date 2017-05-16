from __future__ import unicode_literals, absolute_import, division

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from tinymce.models import HTMLField

from ..alumni.models import Alumnus


# def save_teaser_picture(instance, filename):
#     """ Determine upload path for teaser pictures. The instance's _meta attribute
#     carries the verbose name. Verbose names are therefore explicitly defined for
#     the BaseEvent class and each derived class Path names are dependent on the
#     class, and will have increasing numbering if files with similar names exist """
#
#     MAXCOUNT = 100
#     subdir = instance._meta.verbose_name_raw
#     if instance._meta.verbose_name_raw == 'base event':
#         subdir = "base"
#     elif instance._meta.verbose_name_raw == 'pizza lunch talk':
#         subdir = "pizza"
#     fullpath = os.path.join("uploads/images/news", subdir, filename)
#     basename, ext = os.path.splitext(fullpath)
#     count = 0
#     while count < MAXCOUNT:
#         if os.path.exists(os.path.join(MEDIA_ROOT, fullpath)):
#             count += 1
#             fullpath = "{}_{}{}".format(basename, count, ext)
#         else:
#             break
#     return fullpath


class Category(models.Model):
    name             = models.CharField(max_length=200)
    slug             = models.SlugField(unique=True, blank=True, null=True)

    date_created     = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated     = models.DateTimeField(_("Date Last Changed"), auto_now=True)
    last_updated_by  = models.ForeignKey('auth.User', related_name="categories_updated",
        on_delete=models.SET_DEFAULT, default=270)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Post(models.Model):
    author          = models.ForeignKey(Alumnus)
    title           = models.CharField(max_length=300)
    slug            = models.SlugField(unique=True, blank=True, null=True)
    teaser          = models.TextField(blank=True, help_text=_("Short teaser for the list of posts."))

    # TODO: implement the teaser picture
    # teaser_picture  = models.ImageField(
    #     upload_to=save_teaser_picture, blank=True, null=True,
    #     help_text=_("Small (100x100 pixels maximum) teaser picture for the list of posts.")
    # )
    content         = HTMLField(default="")

    alumnus         = models.ForeignKey(Alumnus, related_name="interviews", blank=True, null=True)

    is_published    = models.BooleanField(default=False)
    date_created    = models.DateTimeField(auto_now_add=True)
    date_published  = models.DateTimeField(auto_now=True, blank=True, null=True)
    last_updated_by = models.ForeignKey('auth.User', related_name="posts_updated",
        on_delete=models.SET_DEFAULT, default=270)

    category = models.ForeignKey(Category, blank=True, null=True)
    # featured = models.BooleanField(default=False,
    #         help_text="Should this post be shown in the featured list?")
    # top_story = models.BooleanField(default=False,
    #         help_text="Should this post be shown in the top stories list?")
    # front_page = models.BooleanField(default=False,
    #         help_text="Should this post be shown on the home page?")

    class Meta:
        verbose_name = _("Interview")
        verbose_name_plural = _("Interviews")
        ordering = ['-date_published',]


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

