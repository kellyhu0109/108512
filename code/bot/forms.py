from django.forms import ModelForm, Form, BooleanField
from .models import OcrTable


class OcrModelForm(ModelForm):
    class Meta:
        model = OcrTable
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     super(OcrModelForm, self).__init__(*args,**kwargs)
    #     self.fields['ocr_no'].widget.attrs['readonly'] = True
