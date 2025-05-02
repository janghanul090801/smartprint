from django import forms
from .models import Posts, Attachment, QuoteInquiry

class PostWriteForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = [
            'title',
            'content',
            'image',
        ]
        widgets = {
            'title' : forms.TextInput(
                attrs={'class':'form-control', 'placeholder':'제목을 입력하세요.'}
            ),
            'content' : forms.Textarea(
                attrs={'class':'form-control', 'placeholder':'내용을 입력하세요.'}
            ),
            'image' : forms.FileInput(
                attrs={}
            )
        }
        labels = {
            'title' : '제목',
            'content' : '내용',
            'image' : '첨부 파일',
        }
        
class QuoteInquiryForm(forms.ModelForm):
    class Meta:
        model = QuoteInquiry
        fields = [
            'username',
            'userLastNumber',
            'userEmail',
            'title',
            'content',
        ] 
        
        widgets = {
            'username' : forms.TextInput(
                attrs={'class':'form-control', 'placeholder':'이름을 입력하세요.'}
            ),
            'userLastNumber' : forms.TextInput(
                attrs={
                    'class':'form-control w-50', 'placeholder':'휴대전화 마지막 4자리를 입력하세요.',
                    "oninput":"this.value = this.value.slice(0,4)",
                }
            ),
            'userEmail' : forms.EmailInput(
                attrs={
                    'class':'form-control w-75',
                    'placeholder':'이메일 주소를 입력하세요'
                }
            ),
            'title' : forms.TextInput(
                attrs={'class':'form-control', 'placeholder':'제목을 입력하세요.'}
            ),
            'content' : forms.Textarea(
                attrs={'class':'form-control', 'placeholder':'내용을 입력하세요.'}
            ),
        }
        labels = {
            'username':'성명',
            'userLastNumber':'휴대전화 마지막 4자리',
            'userEmail':'이메일',
            'title' : '제목',
            'content' : '내용',
        }     

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True
    
    def __init__(self, attrs=None):
        default_attrs = {'class': 'form-control'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class AttachmentForm(forms.ModelForm):
    image = MultipleFileField(
        label='첨부파일',
    )
    
    class Meta:
        model = Attachment
        fields = ['image',]
        
