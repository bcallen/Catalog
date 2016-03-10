from django.conf.urls import url
from . import views

app_name = 'catalog'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<note_id>[0-9]+)/$', views.detail, name='detail'),
	url(r'^tags/(?P<tag_name>[ _a-zA-Z0-9]+)/$', views.tags, name='tags'),
	url(r'^edit/(?P<note_id>[0-9]+)/$', views.edit, name='edit')
	url(r'^edit/$', views.edit, name='create')
	url(r'^add/$', views.detail, name='add')
]