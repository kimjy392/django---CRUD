from django.shortcuts import render, redirect
from .models import Article

# Create your views here.
def index(request):
    articles = Article.objects.order_by('-id') # 최신글로 정렬하기
    context = {
        'articles': articles
    }
    return render(request, 'article/index.html', context)

def new(request):
    return render(request, 'article/new.html')

def create(request):
    # 저장 로직
    title = request.GET.get('title')
    content = request.GET.get('content')
    article = Article.objects.create(title=title, content=content)
    context = {
        'article' : article
    }
    # return render(request, 'article/create.html', context)
    return redirect('/article/')
