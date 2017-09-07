from django import forms
from files.models import FileObject

class DocumentForm(forms.ModelForm):
	class Meta:
		model = FileObject
		fields = ('data_type', 'description', 'document', )

		def __init__(self, *args, **kwargs):
			self.request = kwargs.pop('request', None)
			return super(DocumentForm, self).__init__(*args, **kwargs)

		def save(self, *args, **kwargs):
			kwargs['commit']=False
			obj = super(MyModelForm, self).save(*args, **kwargs)
			if self.request:
				obj.user = self.request.user
			obj.save()
			return obj