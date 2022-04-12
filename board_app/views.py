from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from django.contrib import messages
from .models import Topics, Texts # 追記箇所
from django.http import Http404 # 追記箇所
from django.http import JsonResponse
from django.core.cache import cache
from base.models import CustomUser
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q



def create_topic(request):
  create_topic_form = forms.CreateTopicForm(request.POST or None)
  if create_topic_form.is_valid():
    create_topic_form.instance.user = request.user
    create_topic_form.save()
    messages.success(request, 'You have been created board')
    topic = Topics.objects.last()
    topic_id = topic.id
    # topic_id = id + 1
    return redirect('board_app:post_texts', topic_id=topic_id)
  return render(
    request, 'board_app/create_topic.html', context={
      'create_topic_form': create_topic_form,
    }
  )

def list_topics(request): # 以下追記箇所
  topics = Topics.objects.pick_all_topics()
  topics_asc = Topics.objects.order_by('id').all()
  # topics_last = Topics.objects.all().last()
  # last_topic_id = topics_last.id
  len_topics = len(topics)
  print(len_topics)
  # topicのidのリストを作る
  topic_list = []
  for i in topics_asc:
    topic_list.append(i.id)
  print('topic_list')
  print(topic_list)
  # queryset = Texts.objects.order_by('-id').select_related('topic')
  # texts2 = Texts.objects.order_by('-id').all()
  # texts3 = Texts.objects.order_by('-id').select_related('topic_id').values('topic__title', 'text')
  # texts3 = Texts.objects.order_by('-id').select_related('topic_id').all()
  # print(texts2.topic_id.text)
  texts = Texts.objects.all()
  
  text_dict_list = Topics.objects.order_by('-id').values('id', 'texts__text')
  print(text_dict_list)
  for text_dict in text_dict_list:
    print(text_dict)

  text_dict_use = {}
  for text_dict in text_dict_list:
    pass
  text_dict2 = {}
  for i in topic_list:
    topic_texts = Texts.objects.order_by('id').filter(topic_id = i)[:3]
    print(topic_texts)
    text_list = []
    for obj in topic_texts:
      print(obj.text)
      text_list.append(obj.text)
    text_dict2[i] = text_list
  # print(text_list)
  print('text_dict2')
  print(text_dict2)
  #     for j in len(texts):
  #       if text_dict['id'] == i:
  #         text_list.append(text_dict['texts__text'])
  #         text_dict_use[i] = text_list
  # print(text_dict_use)
  # print('*'*30)
  # print(topics.text)
  # print(texts.topic_id.text)
  # print(queryset.query)
  # for obj in queryset:
  #   print(obj)
    # print(obj.topic_id.text)
  # print('*'*30)
  # for obj in texts2:
    # print(obj.topic_id)
  # print('*'*30)
  # for obj in texts3:
    # print(obj)

  '''
  検索機能
  '''
  keyword = request.GET.get('search_form')
  if keyword:
    keyword = keyword.split()
    for k in keyword:
      topics = topics.filter(
                  Q(title__icontains=k) |
                  Q(texts__text__icontains=k)
                )
  topics = topics.distinct()
  '''
  ページネーション
  # '''
  # if request.method == 'GET':
  #   page_num = request.GET.get('page', 1)
  #   paginator = Paginator(
  #       topics,
  #       5 # 1ページに表示するオブジェクト数
  #   )
  #   try:
  #       page_obj = paginator.get_page(page_num)
  #   except PageNotAnInteger:
  #       page_obj = paginator.page(1)
  #   except EmptyPage:
  #       page_obj = paginator.page(paginator.num_pages)
  
  paginator = Paginator(topics, 7)
  page = request.GET.get('page', 1)
  try:
    topics = paginator.page(page)
  except PageNotAnInteger:
    topics = paginator.page(1)
  except EmptyPage:
    topics = paginator.page(paginator.num_page)

  return render(
    request, 'board_app/list_topics.html', context={
      'topics': topics,
      # 'texts': texts,
      'text_dict_list': text_dict_list,
      'text_dict2': text_dict2,
      # 'page_obj': page_obj,
      # 'topic_list': page.object_list,
      # 'is_pagenated': page.has_other_pages,
    }
  )

def edit_topic(request, id): # 以下追記箇所
  topic = get_object_or_404(Topics, id=id)
  if topic.user.id != request.user.id:
    raise Http404
  edit_topic_form = forms.CreateTopicForm(request.POST or None, instance=topic)
  if edit_topic_form.is_valid():
    edit_topic_form.save()
    messages.success(request, 'You have been updated board')
    return redirect('board_app:list_topics')
  return render(
    request, 'board_app/edit_topic.html', context={
      'edit_topic_form': edit_topic_form,
      'id': id,
    }
  )

def delete_topic(request, id): # 以下追記箇所
  topic = get_object_or_404(Topics, id=id)
  if topic.user.id != request.user.id:
    raise Http404
  delete_topic_form = forms.DeleteTopicForm(request.POST or None)
  if delete_topic_form.is_valid():
    topic.delete()
    messages.success(request, 'You have been deleted board')
    return redirect('board_app:list_topics')
  return render(
    request, 'board_app/delete_topic.html', context={
      'delete_topic_form': delete_topic_form
    }
  )


def post_texts(request, topic_id): # 追記箇所
  post_text_form = forms.PostTextForm(request.POST or None)
  topic = get_object_or_404(Topics, id=topic_id)
  texts = Texts.objects.pick_by_topic_id(topic_id) # 追記箇所
  if post_text_form.is_valid():
    if not request.user.is_authenticated: # 追記箇所(65～66行目)
      raise Http404
    post_text_form.instance.topic = topic
    post_text_form.instance.user = request.user
    post_text_form.save()
    return redirect('board_app:post_texts', topic_id=topic_id)
  return render(
    request, 'board_app/post_texts.html', context={
      'post_text_form': post_text_form,
      'topic': topic,
      'texts': texts, 
    }
  )

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def save_text(request): # 以下追記箇所
  if is_ajax(request=request):
    text = request.GET.get('text')
    topic_id = request.GET.get('topic_id')
    if text and topic_id:
      cache.set(f'saved_text-topic_id={topic_id}-user_id={request.user.id}', text)
      return JsonResponse({'message':'temporarily saved'})


def profile(request, user_id):
  topic_user = CustomUser.objects.get(id=user_id)
  champ_list = []
  for i in topic_user.champions.all():
      champ_list.append(i)
  
  matches = topic_user.matches
  wins = topic_user.wins
  wins_rate = topic_user.wins_rate

  context = {
    'topic_user': topic_user, 
    'champions': champ_list,
    'matches': matches,
    'wins': wins,
    'wins_rate': wins_rate,
    }
  return render(request, 'board_app/profile.html', context)


# class ChampionDelete(DeleteView):
#     template_name = 'board_app/topic_delete.html'
#     model = Topics

#     success_url = reverse_lazy('baord_app:list_topics')

'''
Ranking
'''
def ranking(request, rule='wins'):
  if rule == 'wins_rate':
    users = CustomUser.objects.order_by('-wins_rate').all()
  elif rule == 'matches':
    users = CustomUser.objects.order_by('-matches').all()
  elif rule == 'wins':
    users = CustomUser.objects.order_by('-wins').all()
  else:
    users = CustomUser.objects.order_by('-donations').all()

  context = {'users': users}
  return render(request, 'board_app/ranking.html', context)