from django.shortcuts import render, get_object_or_404
from .models import News, Category
from .forms import ContactForm
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView


def news_list(request):
    news_list = News.objects.filter(status=News.Status.Published)
    # news_list = News.published.all()
    context = {
        "news_list": news_list
    }
    
    return render(request, 'news/news_list.html', context=context)

def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)

    context = {
        "news":news
    }
    return render(request, 'news/news_detail.html', context)

def HomePage(request):
    news_list = News.published.all().order_by('-publish_time')[:5]
    categories = Category.objects.all()
    local_news = News.published.all().filter(category__name="Mahally").order_by('-publish_time')[:5]
    foreign_news = News.published.all().filter(category__name="Xorij").order_by('-publish_time')[:5]
    sport_news = News.published.all().filter(category__name="Sport").order_by('-publish_time')[:5]
    technology_news = News.published.all().filter(category__name="Texnologiya").order_by('-publish_time')[:5]
    context = {
        "news_list": news_list,
        "categories":categories,
        "local_news":local_news,
        "foreign_news":foreign_news,
        "sport_news":sport_news,
        "technology_news":technology_news,
    }
    return render(request, 'news/home.html', context)



def page_404(request):
    news_list = News.objects.filter(status=News.Status.Published)
    if news_list:

        context = {
            "news_list": news_list
        }
    return render(request, 'news/404.html', context)

def contactPage(request):
    categories = Category.objects.all()
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return HttpResponse("<h2>Biz bilan bog'langaningiz uchun tashakkur!</h2>")
    
    context = {
        "form":form,
        'categories':categories,
    }
    return render(request, 'news/contact.html', context)

 
def local_news(request):
    local_news = News.published.all().filter(category__name="Mahally")
    half = len(local_news)//2
    local_news_left = local_news[:half]
    local_news_right = local_news[half:]
    context={
        'local_news_left':local_news_left,
        'local_news_right':local_news_right,
        }
    return render(request, 'news/local.html', context)


def foreign_news(request):
    foreign_news = News.published.all().filter(category__name="Xorij")
    half = len(foreign_news)//2
    foreign_news_left = foreign_news[:half]
    foreign_news_right = foreign_news[half:]

    context = {
        'foreign_news_left':foreign_news_left,
        'foreign_news_right':foreign_news_right,
        }
    return render(request, 'news/foreign.html', context)

def technology_news(request):
    technology_news = News.published.all().filter(category__name="Texnologiya")
    half = len(technology_news)//2
    technology_news_left = technology_news[:half]
    technology_news_right = technology_news[half:]
    
    context = {
        'technology_news_left':technology_news_left,
        'technology_news_right':technology_news_right,
        }
    return render(request, 'news/technology.html', context)

    
def sport_news(request):
    sport_news = News.published.all().filter(category__name="Sport")
    half = len(sport_news)//2
    sport_news_left = sport_news[:half]
    sport_news_right = sport_news[half:]
    
    context = {
        'sport_news_left':sport_news_left,
        'sport_news_right':sport_news_right,
        }
    return render(request, 'news/sport.html', context)


def detail_news(request):
    return render(request, 'news/single_page.html')





# class contactPage(TemplateView):
#     template_name = 'news/contact.html'


#     def get(self, request, *args, **kwargs):
#         form = ContactForm()
#         context = {
#             'form': form
#         }
#         return render(request, 'news/contact.html', context)
#     def post(self, request, *args, **kwargs):
#         form = ContactForm(request.POST)
#         if request.method == 'POST' and form.is_valid():
#             form.save()
#             return HttpResponse("<h2> THanks to contact us!</h2>")
#         context = {
#             "form":form
#         }
#         return render(request, 'news/contact.html', context)
