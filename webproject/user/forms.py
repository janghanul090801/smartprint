from django import forms
from .models import CustomUser
import re
from django.contrib.auth.forms import PasswordChangeForm

class SignupForm(forms.ModelForm):
    varifyPassword = forms.CharField(
        label='비밀번호 확인',
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control w-50',
                'placeholder':'비밀번호를 다시 입력하세요'
            }
        ),
    )

    class Meta:
        model = CustomUser
        fields = [
            'userType',
            'name',
            'email',
            'password',
            'firstNumber',
            'middleNumber',
            'lastNumber',
            'postcode',
            'address',
            'detailAddress',
            'extraAddress',
            'exponent',
            'businessNumber',
        ]
        widgets = {
            'userType' : forms.HiddenInput(),
            'name' : forms.TextInput(
                attrs={
                    'class':'form-control w-50',
                    'placeholder':'이름을 입력하세요'
                }
            ),
            'email' : forms.EmailInput(
                attrs={
                    'class':'form-control w-75',
                    'placeholder':'이메일 주소를 입력하세요'
                }
            ),
            'password' : forms.PasswordInput(
                attrs={
                    'class':'form-control w-50',
                    'placeholder':'비밀번호를 입력하세요'
                }
            ),   
            'firstNumber' : forms.Select(
                attrs={
                    'class':'form-select',
                }
            ),      
            'middleNumber' : forms.NumberInput(
                attrs={
                    'class':'form-control',
                    "style":"text-align:right;",
                    "oninput":"this.value = this.value.slice(0,4)"
                }
            ),
            'lastNumber' : forms.NumberInput(
                attrs={
                    'class':'form-control',
                    "style":"text-align:right;",
                    "oninput":"this.value = this.value.slice(0,4)"
                }
            ),
            'postcode' : forms.TextInput(
                attrs={
                    'class':'form-control me-2',
                    'placeholder':'우편번호',
                    'readonly':True,
                    'id':'postcode'
                }
            ),
            'address' : forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'주소',
                    'readonly':True,
                    'id' :'address',
                }
            ),
            'detailAddress' : forms.TextInput(
                attrs={
                    'class':"form-control me-2",
                    'placeholder':'상세주소',
                    'id':'detailAddress',
                }
            ),
            'extraAddress' : forms.TextInput(
                attrs={
                    'class':"form-control",
                    'placeholder':'참고항목',
                    'id':'extraAddress',
                }
            ),
            'exponent' : forms.TextInput(
                attrs={
                    'class':"form-control",
                    'placeholder':'대표자명을 입력하세요.'
                }
            ),
            'businessNumber' : forms.TextInput(
                attrs={
                    'class':"form-control",
                    'placeholder':'사업자등록번호를 입력하세요.'
                }
            ),
        }
        labels = {
            'name':'이름',
            'email':'이메일',
            'password':'비밀번호',
            'firstNumber':'연락처',
            'middleNumber':'',
            'lastNumber':'',
            'address':'주소',
            'exponent':'대표자명',
            'businessNumber':'사업자등록번호',
        }

    def clean_middleNumber(self):
        middleNumber = self.cleaned_data.get("middleNumber")

        if middleNumber is not None and (middleNumber < 1000 or middleNumber > 9999):
            self.add_error('middleNumber', '전화번호는 4자리 숫자여야 합니다.')
        return middleNumber

    def clean_lastNumber(self):
        lastNumber = self.cleaned_data.get('lastNumber')
        if lastNumber is not None and (lastNumber < 1000 or lastNumber > 9999):
            self.add_error('lastNumber', '전화번호는 4자리 숫자여야 합니다.')
        return lastNumber
    
    def clean_password(self):
        password = self.cleaned_data.get("password")
      
        if password and len(password) < 8:
            self.add_error('password', '비밀번호는 8자리 이상이여야 합니다.')
    
        if password and re.search(r'[!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~]', password) is None:
            self.add_error('password', '비밀번호는 한 개 이상의 특수문자를 포함해야 합니다.')
        return password
    
    def clean_varifyPassword(self):
        password = self.cleaned_data.get("password")
        varifyPassword = self.cleaned_data.get('varifyPassword')
        if password and varifyPassword and password != varifyPassword:
            self.add_error('varifyPassword', '비밀번호가 일치하지 않습니다')
            
        return varifyPassword
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if email and CustomUser.objects.filter(email=email).exists():
            self.add_error('email', '이미 사용 중인 이메일 주소입니다.')
        return email
            
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class EditInfoForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'name',
            'email',
            'firstNumber',
            'middleNumber',
            'lastNumber',
            'postcode',
            'address',
            'detailAddress',
            'extraAddress',   
            'exponent',
            'businessNumber'
        ]
        widgets = {
            'userType' : forms.HiddenInput(),
            'name' : forms.TextInput(
                attrs={
                    'class':'form-control w-50',
                    'placeholder':'이름을 입력하세요'
                }
            ),
            'email' : forms.EmailInput(
                attrs={
                    'class':'form-control w-75',
                    'placeholder':'이메일 주소를 입력하세요'
                }
            ), 
            'firstNumber' : forms.Select(
                attrs={
                    'class':'form-select',
                }
            ),      
            'middleNumber' : forms.NumberInput(
                attrs={
                    'class':'form-control',
                    "style":"text-align:right;",
                    "oninput":"this.value = this.value.slice(0,4)"
                }
            ),
            'lastNumber' : forms.NumberInput(
                attrs={
                    'class':'form-control',
                    "style":"text-align:right;",
                    "oninput":"this.value = this.value.slice(0,4)"
                }
            ),
            'postcode' : forms.TextInput(
                attrs={
                    'class':'form-control me-2',
                    'placeholder':'우편번호',
                    'readonly':True,
                    'id':'postcode'
                }
            ),
            'address' : forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'주소',
                    'readonly':True,
                    'id' :'address',
                }
            ),
            'detailAddress' : forms.TextInput(
                attrs={
                    'class':"form-control me-2",
                    'placeholder':'상세주소',
                    'id':'detailAddress',
                }
            ),
            'extraAddress' : forms.TextInput(
                attrs={
                    'class':"form-control",
                    'placeholder':'참고항목',
                    'id':'extraAddress',
                }
            ),
            'exponent' : forms.TextInput(
                attrs={
                    'class':"form-control",
                    'placeholder':'대표자명을 입력하세요.'
                }
            ),
            'businessNumber' : forms.TextInput(
                attrs={
                    'class':"form-control",
                    'placeholder':'사업자등록번호를 입력하세요.'
                }
            ),
        }
        labels = {
            'name':'이름',
            'email':'이메일',
            'firstNumber':'연락처',
            'middleNumber':'',
            'lastNumber':'',
            'address':'주소',
            'exponent':'대표자명',
            'businessNumber':'사업자등록번호',
        }

class PasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="현재 비밀번호",
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "현재 비밀번호를 입력하세요.",
                "class":"form-control password-input",
            },
        )
    )
    new_password1 = forms.CharField(
        label="새 비밀번호",
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "새 비밀번호를 입력하세요.",
                "class":"form-control password-input",
            }
        )
    )
    new_password2 = forms.CharField(
        label="새 비밀번호 확인",
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "새 비밀번호를 다시 입력하세요.",
                "class":"form-control password-input",
            }
        )
    )

    def clean(self):
        old_password = self.cleaned_data.get("old_password")
        new_password1 = self.cleaned_data.get("new_password1")

        if old_password == new_password1:
            self.add_error(
                "old_password",
                forms.ValidationError("새 비밀번호가 현재 비밀번호와 같습니다."),
            )
        else:
            return self.cleaned_data