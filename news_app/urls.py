from django.urls import path
from .views import *
urlpatterns = [
    path('', HomePage, name='home_page'),
    path('news/', news_list, name='all_news_list'),
    path('news/<slug:news>/', news_detail, name='news_detail'),
    path('news/contact/', contactPage, name='contact_page'),
    path('404/', page_404, name='page_404'),
    path('local-news/', local_news, name='local_news_page'),
    path('foreign-news/', foreign_news, name='foreign_news_page'),
    path('technology-news/', technology_news, name='technology_news_page'),
    path('sport-news/', sport_news, name='sport_news_page'),
]