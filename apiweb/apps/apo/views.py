from __future__ import unicode_literals, absolute_import, division

from django.views.generic import TemplateView
from django.utils.encoding import python_2_unicode_compatible
from django.http import HttpResponseRedirect
from ...settings import FLICKR_APIKEY, FLICKR_SECRET, FLICKR_USERID
from ...settings import FLICKR_TOKEN_PATH
import flickrapi


@python_2_unicode_compatible
class Photo(object):

    def __init__(self, **kwargs):
        self.title = ""
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return self.title


class IndexView(TemplateView):
    template_name = 'apo/index.html'


class FiftyOneView(TemplateView):
    template_name = 'apo/51cm.html'


class SolarView(TemplateView):
    template_name = 'apo/solar.html'


class PracticumView(TemplateView):
    template_name = 'apo/practicum.html'


class GalleryView(TemplateView):
    template_name = 'apo/gallery.html'

    def get_context_data(self, **kwargs):
        context = super(GalleryView, self).get_context_data(**kwargs)
        pictures = {}
        flickr = flickrapi.FlickrAPI(FLICKR_APIKEY, FLICKR_SECRET)
        flickr.token.path = FLICKR_TOKEN_PATH
        flickr_response = flickr.photos_search(
            user_id=FLICKR_USERID,
            extras='description,last_update,o_dims,owner_name,date_upload,' \
            'url_s',
            per_page='12')
        pictures['latest'] = [
            Photo(
                id=photo.attrib['id'],
                title=photo.attrib['title'],
                url_image=photo.attrib['url_s'],
                url="http://www.flickr.com/photos/{}/{}".format(
                    photo.attrib['owner'], photo.attrib['id']),
                description=(photo.find('description').text or ''))
            for photo in flickr_response.find('photos')
        ]
        context['pictures'] = pictures
        return context


class ImageView(TemplateView):
    template_name = 'apo/image.html'

    def get_context_data(self, **kwargs):
        if 'id' not in kwargs:
            return HttpResponseRedirect(self.get_success_url())
        context = super(ImageView, self).get_context_data(**kwargs)
        flickr = flickrapi.FlickrAPI(FLICKR_APIKEY, FLICKR_SECRET)
        flickr.token.path = FLICKR_TOKEN_PATH
        flickr_response = flickr.photos_getInfo(photo_id=kwargs['id'])
        photo = flickr_response.find('photo')
        context['picture'] = Photo(
            title=photo.find('title').text,
            description=photo.find('description').text,
            image_url="http://farm{}.staticflickr.com/{}/{}_{}.jpg".format(
                photo.attrib['farm'], photo.attrib['server'],
                photo.attrib['id'], photo.attrib['secret']),
            url=photo.find('urls').find('url').text)
        return context
