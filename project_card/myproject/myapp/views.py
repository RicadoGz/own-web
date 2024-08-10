from django.shortcuts import render,HttpResponse
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Card,Deck,Suite
import random
import json
#views.py
def index(request):
    # 仅返回 index.html，此视图不处理 POST 请求
    return render(request, 'game.html')
def game_view(request):
    if request.method=="POST":
        all_decks=request.POST.get("all_decks")
        if not all_decks or not all_decks.isdigit() or int(all_decks) not in range(1, 4):
            return HttpResponse("input wrong")
        all_decks = int(all_decks)
        n_user = request.POST.get('n_user')
        if not n_user.isdecimal():
            return HttpResponse("wrong input the nuber of user have to be numer")
        name = request.POST.get("name")
        #send the data from the request to the front
        context={
            'all_decks':all_decks,
            'name':name
        }
        return render(request,'draw_card.html',context)
    return render(request,'game.html')
def draw_card(all_decks):
    # delete the old data in the before
    all_decks=int(all_decks)
    Deck.objects.all().delete()
    Card.objects.all().delete()
    decks_info=[]
    for _ in range(all_decks):
        # creat the object for the cards
        deck = Deck.objects.create()
        deck_info = {'deck': deck.id, 'cards': []}
        for suite in Suite:
            for value in range(1,14):
                # suite.value the value methods is the spcial of the Enum
                # the value is not in the class is in the loop
                card = Card.objects.create(suite=suite.value,value=value)
                # based of the class Deck(models.Model) cards=models.ManyToManyField(Card) current = models.IntegerField(default=0)
                # this means the cards is the one to many obejct and cards <-->Deck can all one to more
                deck.cards.add(card)
                # this can from the str to call the suites = '♠♥♣♦'
                card_str = str(card)
                # the card.value is from the 34line 
                deck_info['cards'].append({'value': card.value, 'suite': suite.name, 'display': card_str})
                random.shuffle(deck_info['cards'])
                decks_info.append(deck_info)
            # 将 decks_info 和 name 添加到 context 中，并转换为 JSON 格式
    return decks_info
def start_game(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)  # 解析 JSON 数据 <!-- 这行添加了 -->
            all_decks = body.get("all_decks") 
            action=body.get("action","") # 从 JSON 数据中获取 all_decks <!-- 这行添加了 -->
            if not all_decks:
                return JsonResponse({"error": "all_decks parameter is missing"}, status=400)
            try:
                all_decks = int(all_decks)
            except ValueError:
                return JsonResponse({"error": "invalid value for all_decks"}, status=400)
            decks_info = draw_card(all_decks)
            drawn_cards = []
            card_count = 0
            while card_count < 8:
                for deck in decks_info:
                    if deck['cards']:
                        drawn_cards.append(deck['cards'].pop(0))
                        card_count += 1
                    if card_count == 8:
                        break
            return JsonResponse({"response": "game started", "drawn_cards": drawn_cards})
        except json.JSONDecodeError:  # 捕获 JSON 解析错误 <!-- 这行添加了 -->
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    if action =='goon':
        card=goon(request,decks_info)
        return JsonResponse({"response": "game started", "drawn_cards": card})
    elif request.method == "GET":
        return render(request, 'draw_card.html')
def goon(request,decks_info):
    c=0
    go=[]
    while c < 1:
        for i in decks_info:
            if i['cards']:
                go.append(i['cards'].pop[0])
                c +=1
            if c == 1:
                break








            
        



