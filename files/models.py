from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
import os
from django.dispatch import receiver
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from Bio import SeqIO

class FileObject(models.Model):

	user = models.ForeignKey(User, verbose_name="Owner")
	
	DATA_TYPE_CHOICES = (
		('RNA','RNA'),
	)
	data_type = models.CharField(max_length=10, choices=DATA_TYPE_CHOICES)

	def dir_path(instance,filename):
		return '{0}/user_{1}/{2}'.format(instance.data_type,instance.user,filename)

	description = models.CharField(max_length=255, blank=False)

	document = models.FileField(upload_to=dir_path)

	uploaded_at = models.DateTimeField(auto_now_add=True)

	def clean(self):
		# Make uploaded file accessible for analysis by saving in tmp
		tmp_path = 'tmp/%s' % self.document.name[2:]
		default_storage.save(tmp_path, ContentFile(self.document.file.read()))
		full_tmp_path = os.path.join(settings.MEDIA_ROOT, tmp_path)
		try:
			records = list(SeqIO.parse(full_tmp_path, "fasta"))
			default_storage.delete(tmp_path)
		except:
			default_storage.delete(tmp_path)
			raise ValidationError('Not a Fasta File!')		

@receiver(models.signals.post_delete, sender=FileObject)
def auto_delete_file_on_delete(sender, instance, **kwargs):
	"""
	Deletes file from filesystem
	when corresponding `MediaFile` object is deleted.
	"""
	if instance.document:
		if os.path.isfile(instance.document.path):
			os.remove(instance.document.path)

@receiver(models.signals.pre_save, sender=FileObject)
def auto_delete_file_on_change(sender, instance, **kwargs):
	"""
	Deletes old file from filesystem
	when corresponding `MediaFile` object is updated
	with new file.
	"""
	if not instance.pk:
		return False

	try:
		old_file = FileObject.objects.get(pk=instance.pk).document
	except FileObject.DoesNotExist:
		return False

	new_file = instance.document
	if not old_file == new_file:
		if os.path.isfile(old_file.path):
			os.remove(old_file.path)