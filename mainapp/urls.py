from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('item_body/', views.item_body, name='item_body'),
    path('item_lens/', views.item_lens, name='item_lens'),
    path('rank/', views.rank, name='rank'),
    path('album/', views.album, name='album'),
    path('create_album/', views.create_album, name='create_album'),
    path('search/', views.search, name='search'),
    path('album_detail/<int:pk>', views.album_detail, name='album_detail'),
    path('item_detail/<int:pk>', views.item_detail, name='item_detail'),
    path('buy/<int:pk>', views.buy, name='buy'),
    path('not_buy/<int:pk>', views.not_buy, name='not_buy'),
    path('create_review/',views.create_review, name='create_review'),
    path('buy_check/<int:pk>', views.buy_check, name='buy_check'),

    # path('', views.index, name='index'),
    # path('item/', views.item, name='item'),
    # path('rank/', views.rank, name='rank'),
    # path('album/', views.album, name='album'),
    # path('item_detail/', views.item_detail, name = 'item_detail'),
]