from django.urls import path
from . import views
from django.conf import settings # 追記箇所(3～4行目)
from django.conf.urls.static import static


app_name = 'base'

urlpatterns = [
    path('edit_page/', views.edit_page, name='edit_page'), # 追記箇所(13～14行目)
    path('self_profile/', views.self_profile, name='self_profile'),

    # path('base/', views.reviewbase, name='base'),
    path('', views.index, name='index'),
    path('settings/', views.settings, name='settings'),
    path('picked/', views.pickedview, name='picked'),
    path('donation/', views.simpleCheckout, name='donation'),
    path('complete/', views.paymentComplete, name='complete'),
    path('exec-ajax/', views.exec, name='exec_ajax'),
    path('ajax-number/', views.ajax_number, name='ajax_number'),

    path('champion_list/', views.champion, name='champion_list'),
    path('add_champion/', views.AddChampion.as_view(), name='add_champion'),
    path('champion_detail/<int:pk>/', views.ChampionDetail.as_view(), name="champion_detail"),
    path('champion_refresh/', views.refresh, name='champion_refresh'),
    path('champion_update/<int:pk>/', views.ChampionUpdate.as_view(), name="champion_update"),
    path('champion_delete/<int:pk>/', views.ChampionDelete.as_view(), name='champion_delete'),
    # path('champion_category/<str:category>/', views.CategoryView.as_view(), name='champion_category'),
    path('champion_category/<str:category>/', views.category, name='champion_category'),
]

if settings.DEBUG: # 以下追記箇所
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)