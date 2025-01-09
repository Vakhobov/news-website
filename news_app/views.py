from django.shortcuts import render, get_object_or_404
from .models import News, Category, Comment
from .forms import ContactForm, CommentForm
from django.http import HttpResponse
from django.views.generic import TemplateView, UpdateView, ListView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from news_project.custom_permissions import OnlyLoggedSuperUser
from django.contrib.auth.models import User
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from django.db.models import Q
from hitcount.utils import get_hitcount_model

def news_list(request):
    news_list = News.objects.filter(status=News.Status.Published)
    # news_list = News.published.all()
    context = {
        "news_list": news_list
    }
    
    return render(request, 'news/news_list.html', context=context)


# from hitcount.views import HitCountDetailView
# class PostCountHitDetailView(HitCountDetailView):
#     model = News
#     count_hit = True



def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {}
    #hitcount logic 
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits


    comments = news.comments.filter(active=True)
    comments_count = comments.count()
    new_comment = None
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Yangi komment obyektini yaratamiz lekin DB ga saqlaymiz
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            # izoh egasini yuborayotgan userga bog'ladik
            new_comment.user = request.user
            # malumotlar bazasiga saqlash
            new_comment.save()
            comment_form = CommentForm
    else:
        comment_form = CommentForm()
    context = {
        "news":news,
        "comments": comments,
        "new_comment":new_comment,
        "comment_form":comment_form,
        'comments_count': comments_count,
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
        "categories": categories,
        "local_news": local_news,
        "foreign_news": foreign_news,
        "sport_news": sport_news,
        "technology_news": technology_news,
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

class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'category', 'status',)
    template_name = 'crud/news_edit.html'

class NewsDeleteView(OnlyLoggedSuperUser, DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')

class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ('title', 'slug', 'body', 'image', 'category', 'status')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_page_view(request):
    admin_user = User.objects.filter(is_superuser=True)

    context = {
        'admin_user': admin_user
    }
    return render(request, 'pages/admin_page.html', context)




class SearchResults(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name ='barcha_yangiliklar'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        half = len(context[self.context_object_name]) // 2
        context['search_news_left'] = context[self.context_object_name][:half]
        context['search_news_right'] = context[self.context_object_name][half:]
        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query))



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
