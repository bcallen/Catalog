from django.db import models

# Create your models here.


class Tag(models.Model):
	tag_name = models.CharField(max_length=25)
	questions = models.IntegerField(default=0)

class Note(models.Model):
	tags = models.ForeignKey(Tag, on_delete=models.CASCADE)
	note_text = models.CharField(max_length=2000)
	pub_date = models.DateTimeField('date published')