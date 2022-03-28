from django.shortcuts import render, redirect
from base.models import Champion, CustomUser, Category, Enemy
from django.http import JsonResponse
from base import winners
import json
# from rest_framework import serializers
from django.core import serializers
from django.contrib.auth.decorators import login_required
import random
# Create your views here.


class User:
    name = None
    hand = 0
    is_user = True

class PC:
    name = None
    hand = 0
    is_user = False


def hand_func():
    hand = random.randint(0, 2)
    return hand



# Ajax Ajax Ajax Ajax Ajax Ajax Ajax Ajax Ajax Ajax Ajax Ajax Ajax Ajax Ajax Ajax Ajax
@login_required
def exec(request):
    picked = CustomUser.champions.through.objects.filter(customuser_id=request.user.id)
    picked_list = []
    for i in picked:
        picked_list.append(i.champion_id)
    show_list = []
    for i in picked_list:
        show_list.append(Champion.objects.get(id=i))
    
    show_champions = show_list
    '''
    敵機作成
    '''
    enemies = Enemy.objects.order_by('?')[:3]
    print('***enemies')
    show_enemies = []
    for i in enemies:
        show_enemies.append(i)

    print(enemies)


    context = {'show_champions': show_champions, 'enemies': show_enemies}
    # sessionを削除しておく
    if 'user_list' in request.session:
        del request.session['user_list']
    if 'pc_list' in request.session:
        del request.session['pc_list']
    if 'index_number' in request.session:
        del request.session['number_index']
    if 'user_stable_list' in request.session:
        del request.session['user_stable_list']
    '''
    # session PCリストの作成
    '''
    pc_name_list = ['Enemy1', 'Enemy2', 'Enemy3']
    pc_list = ['enemy1', 'enemy2', 'enemy3']
    for i in range(len(pc_list)):
        pc=PC()
        pc.name=pc_name_list[i]
        pc.hand=hand_func()
        pc_list[i] = json.dumps(pc.__dict__)

    
    print(pc_list)
    # print(pc_hand_list)
    # request.session['pc_list'] = serializers.serialize('json', pc_list)
    request.session['pc_list'] = pc_list
    # print(request.session['pc_list'])
    # print(serializers.json.Deserializer(request.session['pc_list']))
    # pc_gen = serializers.json.Deserializer(request.session['pc_list'])
    # print(pc_gen)
    # for i in list(pc_gen):
    #     print(i)
    # pc_gen_list = list(pc_gen)
    # print(pc_gen_list)
    # for i in pc_gen_list:
    #     print(i)
    '''
    # session ユーザーのキャラリストとそのidリストの作成
    '''
    user = CustomUser.objects.get(id=request.user.id)
    user_list = []
    user_id_list = []
    # デフォルトのユーザーのキャラとそのidをリストで取得
    for i in user.champions.all():
        user_obj = User()
        user_obj.name = i.name
        user_list.append(json.dumps(user_obj.__dict__))
        user_id_list.append(i.id)
    print(user_list)
    print(user_id_list)
    request.session['user_list'] = user_list
    request.session['user_stable_list'] = user_list
    # request.session['user_list'] = serializers.serialize('json', user_list)
    # request.session['user_id_list'] = user_id_list

    # player_list = user_list + pc_list
    # request.session['player_list'] = player_list
    number_index = []
    for i in range(len(user_list)):
        number_index.append(i+1)
    request.session['number_index'] = number_index
    print(number_index)


    return render(request, 'base/exec_ajax.html', context)



def ajax_number(request):
    if request.POST.get('number1'):
       number1 = int(request.POST.get('number1'))
    if request.POST.get('number2'):
        number2 = int(request.POST.get('number2'))
    if request.POST.get('number3'):
        number3 = int(request.POST.get('number3'))
    print('***number1,number2,number3')
    print(request.POST.get('number1'))
    print(request.POST.get('number2'))
    print(request.POST.get('number3'))
    # if request.POST.get('number1') == None and request.POST.get('number2') == None and request.POST.get('number3') == None:
    #     number1 = 1
    #     number2 = 1
    #     number3 = 0
    # plus = number1 + number2 + number3
    '''
    テスト開始
    '''
    '''
    # session deserialize PCインスタンスをsessionから取得 オブジェクトのリストを作成
    手はここで入力するようにする。
    '''
    pc_gen = request.session['pc_list']
    print('***pc_gen')
    print(pc_gen)
    # テスト
    pc_hand_list = []
    pc_chara_list = []

    for i in pc_gen:
        print(i)
        pc_dict = json.loads(i)
        print(pc_dict['name'])
        pc = PC()
        pc.name = pc_dict['name']
        pc.hand = hand_func()
        # pc.hand = 1
        pc_hand_list.append(pc.hand)
        pc_chara_list.append(pc)


    # pc_gen = serializers.json.Deserializer(request.session['pc_list'])
    # print(pc_gen)
    # for i in list(pc_gen):
    #     i.object.hand = hand_func()
    #     print(i)
    #     pc_hand_list.append(i.object.hand)
    #     pc_chara_list.append(i)
        
    print(pc_hand_list)
    print(pc_chara_list)

    # for i in range(len(pc_json_list)):
    #     pc_dict=json.loads(pc_json_list[i])
    #     pc=PC()
    #     pc.name=pc_dict['name']
    #     pc.hand=pc_dict['hand']
    #     # pc_list[i].hand = pc_list[i].hand_func()
    #     pc_hand_list.append(pc.hand)
    # print(pc_hand_list)
    '''
    # session deserialize sessionからUserのキャラを取得し、オブジェクトのリストを作成　
    # 手を入力
    '''
    user = CustomUser.objects.get(id=request.user.id)
    # 入力情報をリスト化
    # if number1+1 and number2+1 and number3+1:
    #     number_list = [number1, number2, number3]
    # elif number1+1 and number2+1:
    #     number_list = [number1, number2]
    # elif number2+1 and number3+1:
    #     number_list = [number2, number3]
    # elif number1+1 and number3+1:
    #     number_list = [number1, number3]
    # elif number1+1:
    #     number_list = [number1]
    # elif number2+1:
    #     number_list = [number2]
    # elif number3+1:
    #     number_list = [number3]
    if 'number1' in locals() and 'number2' in locals() and 'number3' in locals():
        number_list = [number1, number2, number3]
    elif 'number1' in locals() and 'number2' in locals():
        number_list = [number1, number2]
    elif 'number2' in locals() and 'number3' in locals():
        number_list = [number2, number3]
    elif 'number1' in locals() and 'number3' in locals():
        number_list = [number1, number3]
    elif 'number1' in locals():
        number_list = [number1]
    elif 'number2' in locals():
        number_list = [number2]
    elif 'number3' in locals():
        number_list = [number3]
    print('***number_list')
    print(number_list)
    # デフォルトのユーザーのキャラとそのidをリストで取得
    print('***user_list session')
    print(request.session['user_list'])
    print('***user_list session type')
    print(type(request.session['user_list']))
    # user_json_list = request.session['user_list']
    # user_json_list = serializers.deserialize('json', request.session['user_list'])
    # user_gen = serializers.json.Deserializer(request.session['user_list'])
    user_gen = request.session['user_list']
    # print(user_json_list)

    chara_list = []

    for i in user_gen:
        print(i)
        user_dict = json.loads(i)
        print(user_dict['name'])
        # print(user_dict['hand'])
        user_obj = User()
        user_obj.name = user_dict['name']
        # user_obj.hand = user_dict['hand']
        # chara_hand_list.append(user_obj.hand)
        chara_list.append(user_obj)
    print('***chara_list')
    print(chara_list)
    user_hand_list = []
    # if 'index_number' in request.session:
    #     index_number = request.session['index_number']
    #     j = 0
    #     for i in index_number:
    #         chara_list[j].hand = number_list[i]
    #         user_hand_list.append(chara_list[i].hand)
    #         j += 1
    # else:
    #     for i in range(len(chara_list)):
    #         chara_list[i].hand = number_list[i]
    #         user_hand_list.append(chara_list[i].hand)

    # for i in range(len(chara_list)):
    #     chara_list[i].hand = number_list[i]
    #     user_hand_list.append(chara_list[i].hand)
    index_number = []
    print('***session number_index')
    print(request.session['number_index'])
    for i in request.session['number_index']:
        index_number.append(i-1)    
    j = 0
    for i in index_number:
        chara_list[j].hand = number_list[i]
        user_hand_list.append(chara_list[j].hand)
        j += 1
    print('***user_hand_list')
    print(user_hand_list)
    # セッションでユーザーのキャラのhand_list作成 セッションテスト
    # request.session['user_hand_list'] = user_hand_list
    player_hand_list = user_hand_list + pc_hand_list
    print('***player_hand_list')
    print(player_hand_list)
    player_list = chara_list + pc_chara_list
    print('***player_list')
    print(player_list)
    '''
    手ラベリング
    '''
    hand_type = ['ぐー', 'ちょき', 'ぱー']
    player_hand_type = []

    for i in range(len(player_list)):
        print('{}さんは {}'.format(player_list[i].name, hand_type[player_list[i].hand]))
        player_hand_type.append(player_list[i].name + ':' + hand_type[player_list[i].hand])
    
    hand_msg = ', '.join(player_hand_type)

    '''
    じゃんけん勝ち負け判定アルゴリズム
    '''
    winner_player_list = []
    if player_hand_list.count(0) != 0 and player_hand_list.count(1) != 0 and player_hand_list.count(2) != 0:
        print('あいこ')
        result_msg = 'あいこ'
        winner_player_list = player_list.copy()
    elif player_hand_list.count(0) == len(player_hand_list) or player_hand_list.count(1) == len(player_hand_list) or player_hand_list.count(2) == len(
            player_hand_list):
        print('あいこ')
        result_msg = 'あいこ'
        winner_player_list = player_list.copy()
    elif 0 in player_hand_list and 1 in player_hand_list:
        print(winners.list_pickup(player_hand_list, 0))
        result_list = []
        print('勝利者は、')
        for i in winners.list_pickup(player_hand_list, 0):
            print(player_list[i].name, end='さん ')
            result_list.append(player_list[i].name)
        print('\nです。')
        result_msg = '勝利者は' + ', '.join(result_list) + 'です。'
        for i in winners.list_pickup(player_hand_list, 0):
            winner_player_list.append(player_list[i])

    elif 1 in player_hand_list and 2 in player_hand_list:
        print(winners.list_pickup(player_hand_list, 1))
        result_list = []
        print('勝利者は、')
        for i in winners.list_pickup(player_hand_list, 1):
            print(player_list[i].name, end='さん ')
            result_list.append(player_list[i].name)
        print('\nです。。')
        result_msg = '勝利者は' + ', '.join(result_list) + 'です。'
        for i in winners.list_pickup(player_hand_list, 1):
            winner_player_list.append(player_list[i])

    elif 2 in player_hand_list and 0 in player_hand_list:
        print(winners.list_pickup(player_hand_list, 2))
        result_list = []
        print('勝利者は、')
        for i in winners.list_pickup(player_hand_list, 2):
            print(player_list[i].name, end='さん ')
            result_list.append(player_list[i].name)
        print('\nです。')
        result_msg = '勝利者は' + ', '.join(result_list) + 'です。'
        for i in winners.list_pickup(player_hand_list, 2):
            winner_player_list.append(player_list[i])

    '''
    winner_payer_listをwinner_charaとwinner_pcに分ける
    winner_charaとwinner_pcをそれぞれ、
    request.session['user_list']
    request.session['pc_list']
    に保存する
    '''
    winner_user_list = []
    winner_pc_list = []
    for i in winner_player_list:
        print(i)
        print(type(i))
        if i.is_user:
            winner_user_list.append(i)
        else:
            winner_pc_list.append(i)
    print(winner_user_list)
    print(winner_pc_list)
    # request.session['user_list'] = serializers.serialize('json', winner_user_list)
    # request.session['pc_list'] = serializers.serialize('json', winner_pc_list)
    temp_user_list = []
    for i in winner_user_list:
        user_obj = User()
        user_obj.name = i.name
        temp_user_list.append(json.dumps(user_obj.__dict__))
    
    print(temp_user_list)
    request.session['user_list'] = temp_user_list

    temp_pc_list = []
    for i in winner_pc_list:
        pc = PC()
        pc.name = i.name
        temp_pc_list.append(json.dumps(pc.__dict__))
    
    print(temp_pc_list)
    request.session['pc_list'] = temp_pc_list
            

    '''
    ユーザーの勝者キャラのchara_listにおけるindexを取得する①
    次の実行時の入力欄に反映する。
    でも次のchara_listは0,1と作成されてしまうので、次回実行時のその次に
    有効な入力欄の番号として採用できない。
    request.session['number_index']としてsessionを作成する。
    これはリスト。[0, 2]のように出力されるはず。
    ①で次回取得する番号が[1]だった場合、[0, 2]のうち、[2]が採用されるようにする。
    '''
    user_stable_gen = request.session['user_stable_list']
    # print(user_json_list)

    chara_stable_list =  []
    for i in user_stable_gen:
        print(i)
        user_dict = json.loads(i)
        # print(user_dict['name'])
        # print(user_dict['hand'])
        user_obj = User()
        user_obj.name = user_dict['name']
        # user_obj.hand = user_dict['hand']
        # chara_hand_list.append(user_obj.hand)
        chara_stable_list.append(user_obj)
    print(chara_stable_list)
    winner_name = []
    for i in winner_user_list:
        winner_name.append(i.name)
    print('***winner_name')
    print(winner_name)
    winner_pc_name = []
    for i in winner_pc_list:
        winner_pc_name.append(i.name)
    print('***winner_pc_name')
    print(winner_pc_name)
    stable_name = []
    for i in chara_stable_list:
        stable_name.append(i.name)
    print(stable_name)

    
    winner_index_list = []
    for i in winner_name:
        winner_index_list.append(stable_name.index(i)+1) # ！！！！←indexにプラス1してリストに格納している。
    print(winner_index_list)
    request.session['number_index'] = winner_index_list

    '''
    勝ち残りが一人だった場合、session終了させる
    -> 今後は、PC(pc_list)が0で、ユーザーが有り(user_list>0)であればという条件にする。
    '''

    if len(winner_pc_list) == 0 and len(winner_user_list) > 0:
        final_result_msg = 'ゲーム終了です。Nexusを守りました'
        reload_msg = 'ページをリロードしてください'
        del request.session['user_list']
        del request.session['pc_list']
        del request.session['number_index']
        del request.session['user_stable_list']
        user.matches += 1
        user.wins += 1
        matches = user.matches
        wins = user.wins
        user.wins_rate = wins / matches * 100
        user.save()

    elif len(winner_pc_list) > 0 and len(winner_user_list) == 0:
        final_result_msg = 'ゲーム終了です。Nexusを守れませんでした'
        reload_msg = 'ページをリロードしてください'
        del request.session['user_list']
        del request.session['pc_list']
        del request.session['number_index']
        del request.session['user_stable_list']
        user.matches += 1
        matches = user.matches
        wins = user.wins
        user.wins_rate = wins / matches * 100
        user.save()

    elif len(winner_player_list) == 1:
        print('ゲーム終了です。優勝者は{}さんでした！\nページをリロードしてください'.format(winner_player_list[0].name))
        final_result_msg = 'ゲーム終了です。優勝者は{}さんでした！\nページをリロードしてください'.format(winner_player_list[0].name)
        reload_msg = 'ページをリロードしてください'
        del request.session['user_list']
        del request.session['pc_list']
        del request.session['number_index']
        del request.session['user_stable_list']
    else:
        final_result_msg = ''
        reload_msg = ''


    '''
    勝ち抜きのテスト
    '''
    # # 勝ち抜いたキャラと仮定してwinner_listを作成
    # winner_list = [user.champions.get(id=7), user.champions.get(id=9)]
    # # 勝ち抜いたキャラがリストの中で何番目か？を知る為の情報を取得→次の段階でキャラの手を選別する為
    # winner_index_list = []
    # for i in winner_list:
    #     winner_index_list.append(chara_list.index(i))
    # print(winner_index_list)
    # for i in winner_index_list:
    #     user_hand_list[i] = number_list[i]
    # print(user_hand_list)
    # # セッションンテスト実行
    # if 'user_hand_list' in request.session:
    #     print(request.session['user_hand_list'])
    #     del request.session['user_hand_list']
    
    # player_list = request.session['player_list']
    # winner_name.append('Sona')
    print('***winner_name')
    print(winner_name)
    print(len(winner_name))
    print('***winner_pc_name')
    print(winner_pc_name)



    print('*' * 50)
    # hand_type = ['ぐー', 'ちょき', 'ぱー']
    # user_hand = hand_type[number1]
    # plus = 1000
    # minus = number1 - number2
    d = {
        # 'plus': plus,
        'result_msg': result_msg,
        'hand_msg': hand_msg,
        'final_result_msg': final_result_msg,
        'reload_msg': reload_msg,
        'winner_index_list': winner_index_list,
        'winner_name': winner_name,
        'winner_pc_name': winner_pc_name,
        # 'pc_hand': pc_hand,
        # 'user_hand': user_hand,
        # 'minus': minus,
    }
    return JsonResponse(d)