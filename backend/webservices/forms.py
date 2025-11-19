from django import forms
from multiupload.fields import MultiFileField


class UploadImageTempForm(forms.Form):
	images = MultiFileField(min_num=1, max_num=10, max_file_size=1024 * 1024 * 10)
