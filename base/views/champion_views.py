from django.shortcuts import render, redirect
from base.models import Champion, CustomUser, Category
from django.http import JsonResponse
# from . import winners
import json
# from rest_framework import serializers
from django.core import serializers
from django.contrib.auth.decorators import login_required
import random
# Create your views here.
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.urls import reverse
from django.views import View
from django.db.models import Q



def simpleCheckout(request):
    return render(request, 'base/donation.html')

def paymentComplete(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
        except Exception:
            pass
        
        amount = body['amount']
        print(body)
        user_id = body['user_id']
        user = CustomUser.objects.get(id=user_id)
        user.donations += float(amount)
        user.save()
        print('context代入前')
        context = {'amount': amount}
        # context = {'amount': 5.00 }
        print('context代入後')
    return render(request, 'base/complete.html')
    #return redirect('base:complete')
    # return JsonResponse('hello',safe=False)



# def reviewbase(request):
#     return render(request, 'base.html')


def index(request):
    return render(request, 'index.html')


def settings(request):
    champions = Champion.objects.all()
    context = {'champions': champions}
    return render(request, 'base/settings.html', context)

def champion(request):
    champions = Champion.objects.all()
    keyword = request.GET.get('search_form')
    if keyword:
      keyword = keyword.split()
      for k in keyword:
        champions = champions.filter(
                    Q(name__icontains=k) |
                    Q(description__icontains=k) |
                    Q(category__name__icontains=k)
                  )
    print(champions.query)
    champions = champions.distinct()
    print(champions)
    context = {'champions': champions}
    return render(request, 'base/champion_list.html', context)

def category(request, category):
    category_data = Category.objects.get(name=category)
    champions = Champion.objects.filter(category=category_data)
    print(champions)
    context = {'champions': champions}
    return render(request, 'base/champion_list.html', context)

class CategoryView(View):
    def get(self, request, *args, **kwargs):
        category_data = Category.objects.get(name=self.kwargs['category'])
        champion = Champion.objects.filter(category=category_data)
        context = {'champion': champion}
        return render(request, 'base/champion_list.html', context)


class AddChampion(CreateView):
    template_name = 'base/add_champion.html'
    model = Champion
    fields = ('name', 'category', 'picture', 'description')
    success_url = reverse_lazy('base:champion_list')


class ChampionDetail(DetailView):
    #Championテーブル連携
    model = Champion
    #レコード情報をテンプレートに渡すオブジェクト
    context_object_name = "champion"
    #テンプレートファイル連携
    template_name = "base/champion_detail.html"



class ChampionUpdate(UpdateView):
    template_name = 'base/champion_update.html'
    model = Champion
    fields = ['name', 'category', 'picture', 'description']

    def get_success_url(self):
        return reverse('base:champion_detail', kwargs={'pk': self.object.pk})


class ChampionDelete(DeleteView):
    template_name = 'base/champion_delete.html'
    model = Champion

    success_url = reverse_lazy('base:champion_list')




def pickedview(request):
    if request.method == 'POST':
        results = request.POST.getlist("champion")
        user = CustomUser.objects.get(id=request.user.id)
        print(results)
        result_list = []
        CustomUser.champions.through.objects.filter(customuser_id=request.user.id).delete()
        for i in results:
            result_list.append(Champion.objects.get(id=i))
            print(i)
            user.champions.add(Champion.objects.get(id=i))
        # print(dir(user.champions))
        print(user.champions)
        user.champions.update()
        print(result_list)
        champ_list = []
        for i in user.champions.all():
            champ_list.append(i)
        context = {'champions': champ_list}
    else:
        user = CustomUser.objects.get(id=request.user.id)
        champ_list = []
        for i in user.champions.all():
            champ_list.append(i)
        context = {'champions': champ_list}

    return render(request, 'base/picked.html', context)

def refresh(request):
    CustomUser.champions.through.objects.filter(customuser_id=request.user.id).delete()
    return redirect('base:picked')
