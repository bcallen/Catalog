from django.db import models

# Create your models here.


class Tag(models.Model):
	tag_name = models.CharField(max_length=25)
	questions = models.IntegerField(default=0)
	def __str__(self):
		return self.tag_name

class Note(models.Model):
	tags = models.ManyToManyField(Tag)
	note_text = models.CharField(max_length=2000)
	pub_date = models.DateTimeField('date published')
	def __str__(self):
		return self.note_text[0:20] + '...'
	@property
	def get_tag_name(self):
		#just one tag for test verison
		return self.tags.tag_name