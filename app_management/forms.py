from django import forms
from .models import AppManagement

class AppManagementForm(forms.ModelForm):
    class Meta:
        model = AppManagement
        fields = ['name', 'apk_file_path']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'apk_file_path': forms.FileInput(attrs={'class': 'form-control-file'})
        }