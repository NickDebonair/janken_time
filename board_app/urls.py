from django.urls import path
from . import views
from django.conf import settings # 追記箇所(3～4行目)
from django.conf.urls.static import static

app_name = 'board_app'

urlpatterns = [
  path('create_topic/', views.create_topic, name='create_topic'),
  path('list_topics/', views.list_topics, name='list_topics'), # 追記箇所
  path('edit_topic/<int:id>', views.edit_topic, name='edit_topic'), # 追記箇所
  path('delete_topic/<int:id>', views.delete_topic, name='delete_topic'), # 追記箇所
  path('post_texts/<int:topic_id>/', views.post_texts, name='post_texts'),
  path('save_text', views.save_text, name='save_text'),
  path('profile/<int:user_id>', views.profile, name="profile"),
  path('ranking/<str:rule>/', views.ranking, name="ranking"),
]

if settings.DEBUG: # 以下追記箇所
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)