from django.shortcuts import render, get_object_or_404, redirect
from .models import Posts, Attachment, QuoteInquiry, FAQ
from .forms import PostWriteForm, AttachmentForm, QuoteInquiryForm
from django.http import JsonResponse
from django.core.paginator import Paginator

# Create your views here.

def notice(request):
    q = request.GET.get('q', '')
    searchType = request.GET.get('type', '')
    if q:
        if searchType == 'title':
            noticePost = Posts.objects.filter(title__icontains=q).order_by('-createdTime')
    else :
        noticePost = Posts.objects.order_by('-createdTime')
    paginator = Paginator(noticePost, 20)
    page = request.GET.get('page','1')
    page_obj = paginator.get_page(page)
    return render(request, 'notice.html', {'posts':page_obj,'type':searchType, 'q':q})

def faq(request):
    q = request.GET.get('q', '')
    searchType = request.GET.get('type', '')
    if q:
        if searchType == 'title':
            faq = FAQ.objects.filter(title__icontains=q).order_by('-createdTime')
    else :
        faq = FAQ.objects.order_by('-createdTime')
    return render(request, 'faq.html', {'posts':faq})

def postView(request, id):
    if request.method == 'POST':
        if id:
            Posts.objects.filter(id=id).delete()
            return redirect('board:notice')
    else :
        post = get_object_or_404(Posts, id=id)
        post.views += 1
        post.save()
    return render(request, 'postView.html', {'post':post})

def postWrite(request, category):
    if request.method == 'POST':
        form = PostWriteForm(request.POST, request.FILES)  
        if form.is_valid():
            form.save()
            return redirect('board:'+category)
    else:
        form = PostWriteForm(initial={'category': category})
    return render(request, 'postWrite.html', {'form':form, 'category':category})

def quoteWrite(request):
    if request.method == 'POST':
        form = QuoteInquiryForm(request.POST)
        images = request.FILES.getlist('image')
        if form.is_valid():
            quote = form.save()
            
            for i in images:
                Attachment.objects.create(quote=quote, image=i)
            return redirect('board:quoteInquiry')
    
    else:
        if request.user.is_authenticated:     
            form = QuoteInquiryForm(initial={
                "username" : request.user.name,
                'userLastNumber' : request.user.lastNumber,
                'userEmail' : request.user.email,
            })
        else :
            form = QuoteInquiryForm()
        imageForm = AttachmentForm()
    return render(request, 'quoteWrite.html', {'form':form,"imageForm":imageForm})
        

def quoteInquiry(request):
    if request.method == "POST":
        try:
            id = request.POST.get('id')
            number = request.POST.get('number')
            if QuoteInquiry.objects.get(id=id).userLastNumber == int(number):
                return JsonResponse({'status': 'success', 'is_match': True})
            else :
                return JsonResponse({'status':'success', 'is_match':False})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else :  
        q = request.GET.get('q', '')
        searchType = request.GET.get('type', '')
        if q:
            if searchType == 'title':
                quote = QuoteInquiry.objects.filter(
                    title__icontains=q).order_by('-createdTime')
            elif searchType == 'writer':
                quote = QuoteInquiry.objects.filter(
                    username__icontains=q).order_by('-createdTime')
        else :
            quote = QuoteInquiry.objects.order_by('-createdTime')
        paginator = Paginator(quote, 20)
        page = request.GET.get('page','1')
        page_obj = paginator.get_page(page)
    return render(request, 'quoteInquiry.html', {'board':page_obj})

def quoteView(request, id):
    quote = get_object_or_404(QuoteInquiry, id=id)
    attachments = quote.attachment_set.all()
    return render(request, 'quoteView.html', {'post':quote, 'attachments': attachments, 'id':id})