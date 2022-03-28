from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from base import forms
from base.models import Champion, CustomUser, Category

@login_required
def self_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    if request.method == 'POST':
      edit_form = forms.UserEditForm(
      request.POST or None, 
      request.FILES or None, 
      instance = request.user
      )
      if edit_form.is_valid():
        messages.success(request, 'You have been updated')
        edit_form.save()


    champ_list = []
    for i in user.champions.all():
        champ_list.append(i)
    matches = user.matches
    wins = user.wins
    wins_rate = user.wins_rate
    print(matches)
    context = {
      'champions': champ_list,
      'matches': matches,
      'wins': wins,
      'wins_rate': wins_rate,
      }
    return render(request, 'account/self_profile.html', context)


@login_required # 以下追記箇所
def edit_page(request):
  edit_form = forms.UserEditForm(
    request.POST or None, 
    request.FILES or None, 
    instance = request.user
    )
  if edit_form.is_valid():
    messages.success(request, 'You have been updated')
    edit_form.save()
  return render(request, 'account/edit_page.html', context={
      'edit_form': edit_form,
  })
  # return redirect('base:self_profile')