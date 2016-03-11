from django.db import models
import re

# Create your models here.


class Tag(models.Model):
	tag_name = models.CharField(max_length=25)
	questions = models.IntegerField(default=0)
	def __str__(self):
		return self.tag_name
	def __eq__(self, other):
		return self.__str__ == other.__str__

class Note(models.Model):
	title = models.CharField(max_length=20,default="Note_Title")
	tags = models.ManyToManyField(Tag)
	note_text = models.CharField(max_length=2000)
	pub_date = models.DateTimeField('date published')
	def __str__(self):
		return self.note_text[0:20] + '...'
	def add_tag(self, add_tag_name):
		if add_tag_name in [t.tag_name for t in self.tags.all()]:
			pass
		else:
			t = Tag.objects.filter(tag_name=add_tag_name)
			if len(t) == 0:
				t_obj = Tag(tag_name=add_tag_name)
				t_obj.save()
				t = [t_obj]
			self.tags.add(t[0])
			self.save()
	def remove_tag(self, rm_tag_name):
		t = self.tags.filter(tag_name = rm_tag_name)
		if len(t) > 0:
			self.tags.remove(t[0])
			if t[0].note_set.count() == 0:
				t[0].delete()
		self.save()

def parse_note_updates(update_text):
	title_re = re.compile(r'\*([a-zA-Z_]+)')
	tag_re = re.compile(r'#([a-zA-Z_]+)')
	
	ttl = title_re.search(update_text)
	if ttl is None:
		new_title = "New_Note"
	else:
		new_title = ttl.groups(1)[0]

	tgs = tag_re.search(update_text)
	if tgs is None:
		new_tags = []
	else:
		new_tags = [tag for tag in tag_re.findall(update_text)]
	update_text = title_re.sub('', update_text)
	update_text = tag_re.sub('', update_text)
	
	update_text = re.sub(r'(^[\n\t\s]+|[\n\t\s]+$)','',update_text)
	return new_title, new_tags, update_text