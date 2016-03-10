from django.shortcuts import render, get_object_or_404
#from django.template import loader
from django.core.urlresolvers import reverse
from .models import Note, Tag, parse_note_updates
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone

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

def detail(request, note_id = None):
	try:
		note = Note.objects.get(pk=note_id)
	except Note.DoesNotExist:
		raise Http404('Note does not exist')
	#can also use shortcut get_object_or_404() [import from django.shortcuts]
	return render(request, 'catalog/detail.html', {'note': note,
													'tags': [tag for tag in note.tags.all()]
													})

def tags(request, tag_name):
	#tag = get_object_or_404(Tag, pk = tag_id)
	note_list = Note.objects.filter(tags__tag_name = tag_name)
	return index(request, note_list)

def edit(request, note_id = None):
	if note_id == None:
		note = Note(pub_date=timezone.now())
		note.save()
	else:
		note = get_object_or_404(Note, pk=note_id)
	new_tags, new_text = parse_note_updates(request.POST['new_text'])
	new_tags = set(new_tags)
	old_tags = set([t.tag_name for t in note.tags.all()])

	rm_tags = old_tags - new_tags
	add_tags = new_tags - old_tags 
	
	for tag in rm_tags:
		note.remove_tag(tag)
	for tag in add_tags:
		note.add_tag(tag)
		
	note.note_text = new_text
	note.save()
	return HttpResponseRedirect(reverse('catalog:index'))
