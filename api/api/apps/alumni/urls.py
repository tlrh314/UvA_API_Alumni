# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from . import views

app_name = 'alumni'
urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^$', views.HomePageView.as_view(), name='home'),
    url(r'^formset$', views.DefaultFormsetView.as_view(), name='formset_default'),
    url(r'^form$', views.DefaultFormView.as_view(), name='form_default'),
    url(r'^form_by_field$', views.DefaultFormByFieldView.as_view(), name='form_by_field'),
    url(r'^form_horizontal$', views.FormHorizontalView.as_view(), name='form_horizontal'),
    url(r'^form_inline$', views.FormInlineView.as_view(), name='form_inline'),
    url(r'^form_with_files$', views.FormWithFilesView.as_view(), name='form_with_files'),
    url(r'^pagination$', views.PaginationView.as_view(), name='pagination'),
    url(r'^misc$', views.MiscView.as_view(), name='misc'),
]

