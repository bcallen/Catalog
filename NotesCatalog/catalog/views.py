from django.shortcuts import render, get_object_or_404
#from django.template import loader

from .models import Note, Tag
# Create your views here.
from django.http import HttpResponse

def index(request, note_list = None):
	#should this kind of selection logic be somewhere else?
	if note_list == None:
		note_list = Note.objects.all()
	note_list = note_list.order_by('-pub_date')[:10]
	context = {
		'note_list': {note : [tag for tag in note.tags.all()] for note in note_list}
	}
	return render(request, 'catalog/index.html', context)
#	render is shortcut for
#	template = loader.get_template('catalog/index.html')
#	return HttpResponse(template.render(context, request))

def detail(request, note_id):
	try:
		note = Note.objects.get(pk=note_id)
	except Note.DoesNotExist:
		raise Http404('Note does not exist')
	#can also use shortcut get_object_or_404() [import from django.shortcuts]
	return render(request, 'catalog/detail.html', {'note': note})

def tags(request, tag_name):
	#tag = get_object_or_404(Tag, pk = tag_id)
	note_list = Note.objects.filter(tags__tag_name = tag_name)
	return index(request, note_list)