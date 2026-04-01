from django import forms
from .models import User

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'image',
            'username',
            'jenis_kelamin',
            'email',
            'location',
            'website',
            'date_of_birth',
            'hobi',
            'bio',
            'theme',
            'dark_mode'
        ]
        
        widgets = {
            'bio': forms.Textarea(attrs={"rows": 4}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'theme': forms.Select(attrs={'class': 'form-control'}),
            'dark_mode': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
          if field_name == 'dark_mode':
            field.widget.attrs['class'] = 'form-check-input'
          else:
            field.widget.attrs['class'] = 'form-control'
