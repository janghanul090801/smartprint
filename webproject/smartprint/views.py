from django.shortcuts import render, redirect, get_object_or_404
from order.models import Goods
from board.models import Posts, QuoteInquiry

# Create your views here.
def home(request):
    namecard = Goods.objects.filter(category="namecard")
    promotion = Goods.objects.filter(category='promotion')
    sticker = Goods.objects.filter(category='sticker')
    book = Goods.objects.filter(category='book')
    envelope = Goods.objects.filter(category='envelope')
    other = Goods.objects.filter(category='other')
    notice = Posts.objects.order_by('-createdTime')[:4]
    quote = QuoteInquiry.objects.order_by('-createdTime')[:4]
    return render(request, 'home.html', {"namecard":namecard, 'promotion':promotion, 'sticker':sticker, 'book':book, 'envelope':envelope, 'other':other, 'notice':notice,"quote":quote})

def terms(request):
    return render(request, 'terms.html')

def privacy(request):
    return render(request, 'privacy.html')

def direction(request):
    return render(request, 'direction.html')