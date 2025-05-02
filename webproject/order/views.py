from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Goods, Cart, PaperType
import json
from django.views import View
from django.core.serializers.json import DjangoJSONEncoder
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import timedelta

# Create your views here.

class OrderCartView(LoginRequiredMixin, View):
    login_url = '/user/login/'
    def getGoodsList(self, request):
        goodsList = list(Cart.objects.filter(user=request.user).filter(is_ordered=False).values())
        return goodsList

    def get(self, request):
        goodsList = self.getGoodsList(request)
        goodsListJson = json.dumps(goodsList, cls=DjangoJSONEncoder)  
        return render(request, 'orderCart.html', {'goodsList': goodsListJson})

    def post(self, request):
        try:
            deleteId = request.POST.get('deleteId')
            Cart.objects.filter(id=deleteId).delete()
                
            goodsList = self.getGoodsList(request)            

            response_data = {'status': 'success', 'goodsList': goodsList}
            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({'error': e}, status=400)

@login_required
def orderDetails(request):
    if request.method == 'POST':
        deleteId = request.POST.get('deleteId')
        deleteCart = OrderedCart.objects.get(id=deleteId)
        if deleteCart.status in ('파일 작업','시안 확인'):
            deleteCart.delete()
            cartList = list(OrderedCart.objects.all().values())
            responseData = {'status': 'success', 'list': cartList}
        else :
            responseData = {'status':'success', 'list':None}
        
        return JsonResponse(responseData)
    else:
        cart = Cart.objects.filter(user=request.user)
        orderedCart = list(OrderedCart.objects.filter(product__in=cart).values())
        orderedCartJson = json.dumps(orderedCart, cls=DjangoJSONEncoder) 
        cartJson = json.dumps(list(cart.values()), cls=DjangoJSONEncoder)
        OrderedCart.objects.filter(status='배송 완료',deliveryTime__lt=timezone.now()-timedelta(days=30)).delete()
    return render(request, 'orderDetails.html', {'orderedCart':orderedCartJson, 'cart':cartJson})

@login_required
def orderInfo(request):
    if request.method == 'POST':
        form = OrderInfoForm(request.POST)
        
        if form.is_valid():
            cartIdList = form.cleaned_data['cartId'].split(',')

            for cartId in cartIdList:
                cart = Cart.objects.get(id=cartId)
                cart.is_ordered = True
                cart.save()
                OrderedCart.objects.create(
                    product=cart,
                    name=form.cleaned_data['name'],
                    email=form.cleaned_data['email'],
                    postcode=form.cleaned_data['postcode'],
                    address=form.cleaned_data['address'],
                    detailAddress=form.cleaned_data['detailAddress'],
                    extraAddress=form.cleaned_data['extraAddress'],
                    shippingWay=form.cleaned_data['shippingWay'],
                    paymentMethod=form.cleaned_data['paymentMethod'],
                    cardName=form.cleaned_data['cardName'],
                    cardNumber=form.cleaned_data['cardNumber'],
                    expirationDate=form.cleaned_data['expirationDate'],
                    cvv=form.cleaned_data['cvv']
                )
            return redirect('smartprint:home')
        else:
            print(form.errors)
    else:
        goodsIdList = request.GET.get('goods')
        if goodsIdList:
            goodsIdList = list(map(int, json.loads(goodsIdList)))
            goodsList = list(Cart.objects.filter(id__in=goodsIdList).values())
            goodsListJson = json.dumps(goodsList, cls=DjangoJSONEncoder)  
            form = OrderInfoForm(initial={
                'name':request.user.name,
                'email':request.user.email,
                'postcode':request.user.postcode,
                'address':request.user.address,
                'detailAddress':request.user.detailAddress,
                'extraAddress':request.user.extraAddress,
            })
    return render(request, 'orderInfo.html',{"goodsList":goodsListJson,"form":form})

def orderForm(request):
    return render(request, 'orderForm.html')

class SubmissionFormView(View):
    def setPaperTypeChoices(self, category, grade, form):
        paperTypeList = list(PaperType
                             .objects
                             .filter(category=category, grade=grade)
                             .values('name'))
        newList = []
        for i in paperTypeList :
            newList.append((i['name'],i['name']))
        newList.sort(reverse=True)
        
        form.fields['paperType'].choices = newList
    
    def get(self, request, category, id):
        form = SubmissonForm(initial={
            'width':Goods.objects.get(id=id).defaultWidth,
            'height':Goods.objects.get(id=id).defaultHeight,
        })
        self.setPaperTypeChoices(category, Goods.objects.get(id=id).paperClass, form)
        goodsInfo = get_object_or_404(Goods,id=id)
        return render(request,'submissionForm.html',{"goodsInfo":goodsInfo,"form":form, 'formName':f'./submissions/{category}.html'})
        
    def post(self, request, category, id):
        form = SubmissonForm(request.POST, request.FILES)
        self.setPaperTypeChoices(category,Goods.objects.get(id=id).paperClass, form)
        if form.is_valid():
            cart = form.save(commit=False)
            cart.user = request.user
            cart.save()
            return redirect('order:orderCart')
    
def showProduct(request, category):
    products = Goods.objects.filter(category=category)
    return render(request, 'showProduct.html', {'product':products,'category':products.first().get_category_display()})