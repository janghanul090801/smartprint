from django import forms
from .models import Cart, OrderedCart

class SubmissonForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = [
            'category',
            'name',
            'price',
            'paperType',
            'process',
            'width',
            'height',
            'coating',
            'quantity',
            'noc',
            'additionalRequest',
            'imgFile',
            'coverPaperType',
            'coverProcess',
            'coverCoating',
            'binding',
            'bindingType',
            'page',
            'shape',
        ]
        
    category = forms.CharField(
        widget=forms.HiddenInput()
    )  
    
    name = forms.CharField(
        widget=forms.HiddenInput()
    )  
    
    price = forms.IntegerField(
        widget=forms.HiddenInput()
    )
    
    paperType = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select form-input'}),
    )
    process = forms.ChoiceField(
        choices=[
            (8, '8도(컬러 양면)'),
            (4, '4도(컬러 단면)'),
            (2, '2도(흑백 양면)'),
            (1, '1도(흑백 단면)')
        ],
        widget=forms.Select(attrs={'class': 'form-select form-input'}),
    )
    
    width = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control input-numbers', 'placeholder': '가로', 'readonly':True}),
    )
    
    height = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control input-numbers', 'placeholder': '세로', 'readonly':True}),
    )
    
    coating = forms.ChoiceField(
        required=False,
        choices=[
            ('glossyCoating', '유광코팅'),
            ('matteCoating', '무광코팅'),
            ('noCoating', '코팅안함')
        ],
        widget=forms.Select(attrs={'class': 'form-select form-input'}),
    )
    
    noc = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=150,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control input-numbers', 'placeholder': '주문 건수'}),
    )
    
    additionalRequest = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': '추가요청사항을 입력하세요.', 'style':'height:170px;'}),
    )
    
    imgFile = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'id': 'file'}),
    )
    
    coverProcess = forms.ChoiceField(
        required=False,
        choices=[
            (8, '8도(컬러 양면)'),
            (4, '4도(컬러 단면)'),
            (2, '2도(흑백 양면)'),
            (1, '1도(흑백 단면)')
        ],
        widget=forms.Select(attrs={'class': 'form-select form-input'}),
    )
    
    coverCoating = forms.ChoiceField(
        required=False,
        choices=[
            ('glossyCoating', '유광코팅'),
            ('matteCoating', '무광코팅'),
            ('noCoating', '코팅안함')
        ],
        widget=forms.Select(attrs={'class': 'form-select form-input'}),
    )
    
    bindingType = forms.ChoiceField(
        required=False,
        choices=[
            ('verticalLeft', '세로형 좌철'),
            ('horizontalLeft', '가로형 좌철'),
            ('verticalTop', '세로형 상철'),
            ('horizontalTop', '가로형 상철'),
            ('verticalRight', '세로형 우철'),
            ('horizontalRight', '가로형 우철'),
        ],
        widget=forms.Select(attrs={'class': 'form-select form-small-input ms-3'}),
    )
    
    page = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control input-numbers form-input'}),
    )
 
    shape = forms.ChoiceField(
        required=False,
        choices=Cart.SHAPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    
    def clean_coverProcess(self):
        coverProcess = self.cleaned_data.get('coverProcess')
        return int(coverProcess) if coverProcess else None

class OrderInfoForm(forms.Form):
    cartId = forms.CharField(
        widget=forms.HiddenInput()
    )
    
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': '이름을 입력하세요', 
            'class': 'form-control'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': '이메일을 입력하세요', 
            'class': 'form-control'
        })
    )
    
    postcode = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            'placeholder': '우편번호',
            'class': 'form-control w-25 me-2', 
            'readonly': 'readonly'
        })
    )
    
    address = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': '주소', 
            'class': 'form-control w-50', 
            'readonly': 'readonly'
        })
    )
    
    detailAddress = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': '상세주소', 
            'class': 'form-control w-25'
        })
    )
    
    extraAddress = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': '참고항목', 
            'class': 'form-control w-25'
        })
    )
    
    shippingWay = forms.ChoiceField(
        choices=OrderedCart.SHIPPING_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }), 
    )
    
    paymentMethod = forms.ChoiceField(
        choices=OrderedCart.PAYMENT_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
        }),
        initial='신용카드'  
    )
    
    cardName = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    creditCardName = forms.ChoiceField(
        choices=OrderedCart.CREDIT_CARD_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        required=False
    )
    
    debitCardName = forms.ChoiceField(
        choices=OrderedCart.DEBIT_CARD_CHOICES,
        widget=forms.Select(attrs={
            'class':"form-select",
            'style':'display:none',
        }),
        required=False
    )
    
    cardNumber = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': '', 
            'class': 'form-control'
        }),
        required=False
    )
    
    expirationDate = forms.CharField(
        max_length=7, 
        widget=forms.TextInput(attrs={
            'placeholder': '', 
            'class': 'form-control'
        }),
        required=False
    )
    
    cvv = forms.CharField(
        max_length=4,
        widget=forms.TextInput(attrs={
            'placeholder': '', 
            'class': 'form-control'
        }),
        required=False
    )
    

    def clean(self):
        cleanedData = super().clean()
        creditCardName = cleanedData.get('creditCardName')
        debitCardName = cleanedData.get('debitCardName')

        if creditCardName:
            cleanedData['cardName'] = creditCardName
        elif debitCardName:
            cleanedData['cardName'] = debitCardName

        return cleanedData