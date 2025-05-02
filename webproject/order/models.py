from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)
    # 보이는 부분
    category = models.CharField(max_length=20)
    imgFile = models.ImageField(upload_to='image/cart/')
    quantity = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    noc = models.IntegerField(default=1, null=True, blank=True)

    # hidden
    paperType = models.CharField(max_length=50)  # 종이 타입
    process = models.IntegerField(default=4)  # 인쇄도수
    width = models.IntegerField(default=0)  # 가로
    height = models.IntegerField(default=0)  # 세로
    coating = models.CharField(max_length=30, default='코팅 없음')  # 코팅
    additionalRequest = models.TextField(null=True, blank=True)

    # hidden - books
    coverProcess = models.IntegerField(null=True, blank=True)
    coverPaperType = models.CharField(max_length=50, blank=True)
    coverCoating = models.CharField(max_length=10, blank=True)
    binding = models.CharField(max_length=15, blank=True) # 제본
    bindingType = models.CharField(max_length=20, blank=True, null=True)
    page = models.IntegerField(null=True, blank=True)
    
    #hidden -sticker
    SHAPE_CHOICES = [
        ('circle','원'),
        ('quandrangle','사각형'),
        ('triangle','삼각형'),
        ('star','별'),
        ('hart','하트'),
        ('free','자유형'),
    ]
    shape = models.CharField(max_length=20, choices=SHAPE_CHOICES, null=True, blank=True)

class Goods(models.Model):
    CATEGORY_CHOICES = [
        ('namecard','명함'),
        ('promotion','홍보물'),
        ('sticker','스티커'),
        ('book','책자'),
        ('envelope','봉투'),
        ('other','기타'),
    ]
    
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    img = models.ImageField(upload_to='image/goods')
    price = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    explanation = models.TextField()
    defaultWidth = models.IntegerField()
    defaultHeight = models.IntegerField()
    
    cover = models.BooleanField(default=False)
    binding = models.BooleanField(default=False)
    page = models.BooleanField(default=False)
    paperClass = models.CharField(max_length=10, choices=[
        ('normal','일반'),
        ('high','고급'),
        ('pet','PET')
    ])
    
    def __str__(self):
        return self.name
    
class PaperType(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=20, choices=Goods.CATEGORY_CHOICES)
    grade = models.CharField(max_length=10,choices=[
        ('high','고급'),
        ('normal','일반'),
        ('pet','PET'),
    ])
    
    def __str__(self) :
        return f'{self.get_category_display()} / {self.get_grade_display()}지 / {self.name}'
    
class OrderedCart(models.Model):
    SHIPPING_CHOICES = [
        ('선불', '선불'),
        ('착불', '착불'),
        ('방문','방문')
    ]
    
    PAYMENT_CHOICES = (
        ("신용카드", "신용카드"),
        ("체크카드", "체크카드"),
    )

    CREDIT_CARD_CHOICES = [
        ("VISA", "VISA"),
        ("MasterCard", "MasterCard"),
        ("Amex", "Amex"),
        ("UnionPay", "UnionPay"),
        ("JCB", "JCB"),
    ]
    
    DEBIT_CARD_CHOICES = [
        ("신한카드",'신한카드'),
        ("하나카드",'하나카드'),
        ("토스뱅크",'토스뱅크')
    ]
    
    PRODUCT_STATUS = [
        ("파일 작업", "파일 작업"),  
        ("시안 확인", "시안 확인"),    
        ("인쇄 중", "인쇄 중"),    
        ("후가공 중", "후가공 중"),  
        ("배송 중", "배송 중"),
        ('배송 완료','배송 완료'),
        ('취소 완료','취소 완료')    
    ]

    product = models.OneToOneField(Cart, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    postcode = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    detailAddress = models.CharField(max_length=255)
    extraAddress = models.CharField(max_length=255, blank=True, null=True)
    shippingWay = models.CharField(max_length=20, choices=SHIPPING_CHOICES)
    paymentMethod = models.CharField(max_length=20, choices=PAYMENT_CHOICES, blank=True, null=True)
    cardName = models.CharField(max_length=100, blank=True, null=True)
    cardNumber = models.CharField(max_length=20, blank=True, null=True)  
    expirationDate = models.CharField(max_length=7, blank=True, null=True) 
    cvv = models.CharField(max_length=4, blank=True, null=True)
    status = models.CharField(max_length=20, choices=PRODUCT_STATUS, default="파일 작업")
    deliveryTime = models.DateTimeField(null=True, blank=True)
        
    def __str__(self):
        return f'{self.name}님 / {self.product.name} / 현재상태:{self.status}'