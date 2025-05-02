from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.core.validators import EmailValidator

# https://engineer-mole.tistory.com/301
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("이메일 필드를 설정해야 합니다.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("is_staff=True 여야 합니다.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("is_superuser=True 여야 합니다.")
        
        extra_fields.setdefault('name', '관리자') 
        extra_fields.setdefault('userType', '기본회원')  
        extra_fields.setdefault('firstNumber', '010') 
        extra_fields.setdefault('middleNumber', 0) 
        extra_fields.setdefault('lastNumber', 0)  
        extra_fields.setdefault('postcode', '')  
        extra_fields.setdefault('address', '') 
        extra_fields.setdefault('detailAddress', '')  

        return self.create_user(email, password, **extra_fields)
    

    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    FIRST_NUMBER_LIST=[
        ('010', '010'),
        ('011', '011'),
        ('016', '016'),
        ('017','017'),
        ('019','019')
    ]
    USER_TYPE_LIST = [
        ('기본회원','기본회원'),
        ('기업회원','기업회원'),
        ('외국회원','외국회원')
    ]
    userType = models.CharField(max_length=30, choices=USER_TYPE_LIST)
    username_validator = UnicodeUsernameValidator()
    name = models.CharField(max_length=50, validators=[username_validator])
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    firstNumber = models.CharField(max_length=4, choices=FIRST_NUMBER_LIST)
    middleNumber = models.IntegerField()
    lastNumber = models.IntegerField()
    postcode = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    detailAddress = models.CharField(max_length=20)
    extraAddress = models.CharField(max_length=50, null=True, blank=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now) 
    
    #enterprise
    exponent = models.CharField(max_length=50, validators=[username_validator], null=True, blank=True)
    businessNumber = models.CharField(max_length=20, null=True, blank=True)
    
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ['name']
    objects = UserManager()
 