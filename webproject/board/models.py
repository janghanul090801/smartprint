from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
import os
from django.conf import settings
from django.core.validators import EmailValidator

class Posts(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='image/posts', blank=True)
    views = models.IntegerField(default=0)
    createdTime = models.DateTimeField(auto_now_add=True)

class FAQ(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    createdTime = models.DateTimeField(auto_now_add=True)

# 견적문의
# https://support-u-oneday.tistory.com/104
class QuoteInquiry(models.Model):
    STATUS_CHOICES = [
        ('답변대기중','답변대기중'),
        ('답변완료','답변완료')
    ]
    
    username = models.CharField(max_length=50)
    userLastNumber = models.IntegerField()
    userEmail = models.EmailField(validators=[EmailValidator()])
    title = models.CharField(max_length=50)
    content = models.TextField()
    status = models.CharField(max_length=20, default='답변대기중', choices=STATUS_CHOICES)
    createdTime = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) :
        return f'{self.username}님 / {self.title} / {self.status}'
    
class Attachment(models.Model):
    quote = models.ForeignKey(QuoteInquiry, on_delete=models.CASCADE)
    def quote_image_path(instance, filename):
        return f'attachment/{instance.quote.pk}/{filename}'
    image = ProcessedImageField(upload_to = quote_image_path,
                                processors= [ResizeToFill(400, 400)],  
                                format='JPEG',
                                options={'quality' : 90},
                                ) 
    
    def delete(self, *args, **kargs):
        if self.image:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image.name))
            dir_path = os.path.dirname(os.path.join(settings.MEDIA_ROOT, self.image.name))
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
        super(Attachment, self).delete(*args, **kargs)
