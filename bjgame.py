"""
blackjack game lib
author : t.katoh
"""

import random

suit = ["SPADE", "HEART", "DIAMD", "CLOVE"]
number = ['a', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

deck = []

class TrumpCard:
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number
        

def MakeDeck():
    deck = []
    for i in suit:
        for j in number:
            b = TrumpCard(i, j)
            deck.append(b)
        random.shuffle(deck)
    return deck

def ShowCards(cards):
    i = 0
    cardnums = []
    for i in range(len(cards)):
        #print(cards[i].number, end=" ")
        cardnums.append(cards[i].number)
        
    return cardnums

def CardDealer(deck, inputcards = None, Appendmode = None):     
    #引数は引いてくるデッキ、手札に追加したい場合は手札、Appendmodeは1にする 単純に2まい引く時は引数はdeckのみ

    cards = []
    
    #inputcardsがあったら引数をcardsに保存する
    if inputcards != None:
        cards = inputcards
    
    if Appendmode == None:
        for k in range(2):
            cards.append(deck.pop())
    else:
        cards.append(deck.pop())
    return cards

def CardSum_Class(cards): #引数はTrumpCard class 返り値はint
    buffer = []

    i = 0
    for i in range(len(cards)):
        buffer.append(cards[i].number)
    buffer.sort()
    
    Csum = 0
    for j in buffer:
        if (j == "J" or j == "Q" or j == "K"):
            #print("kjq")
            Csum = 10 + Csum
        elif j == "a":
            #print("ace")
            if Csum <= 10 :
                #print("a = 11")
                Csum = 11 + Csum
            else:
                #print("a = 1")
                Csum = 1 + Csum
        else:
            #print("suuji")
            Csum = int(j) + Csum 
    
    return Csum

def CardSum(cardlist): #引数はlist 返り値はint
    Csum = 0
    for i in cardlist:
        if (i == "J" or i == "Q" or i == "K"):
            Csum = 10 + Csum
        elif i == "a":
            #print("ace")
            if Csum <= 10 :
                #print("a = 11")
                Csum = 11 + Csum
            else:
                #print("a = 1")
                Csum = 1 + Csum
        else:
            #print("suuji")
            Csum = int(i) + Csum         
    
def SplitCard(cards): #引数はTrumpCard class 返り値はlist
    buffer = []
    cardlist = []
    
    i = 0
    j = 0
    for i in range(len(cards)):
        buffer.append(cards[i].number)
    
    for j in buffer:
        if (j == "J" or j == "Q" or j == "K"):
            #print("kjq")
            cardlist.append("10")
        elif j == "a":
            #print("ace")
            cardlist.append("a")
        else:
            #print("suuji")
            cardlist.append(str(j))
        
    return cardlist
              
def dealerCPU(deck, cards, P1, P2):
    while 1:
        if CardSum_Class(cards) < 17:
            cards = CardDealer(deck, cards, 1)
        elif CardSum_Class(cards) >= 22:
            return cards
        else:
            break
    if (CardSum_Class(cards) < CardSum_Class(P1) or CardSum_Class(cards) < CardSum_Class(P2)):
        cards = CardDealer(deck, cards, 1)

    return cards

def index_Multi(List,liter):
    #Listはリスト本体・literは検索したい文字
    index_L = []
    for val in range(0,len(List)):
        if liter == List[val]:
            index_L.append(val)
    return index_L


def WinJudge(Clients_card, D_cards):
    
    players = len(Clients_card)
    
    #プレイヤーのカード管理情報は配列で管理,インデックスが若い順にp1, p2 ...    
    player_card_sum = []
    #負け = 0 勝ち = 2 引き分け = 1
    player_winjudge_flag = [0 for i in range(players)]
    #バーストした場合は1が立つ
    player_burst_flag = []
    
    DCardsum = CardSum_Class(D_cards)
    
    
    for i in range(players):
        cardsum_buffer = CardSum_Class(Clients_card[i])
        player_card_sum.append(cardsum_buffer)
        
        
        if player_card_sum[i] > 21:
            player_burst_flag.append(1)
            player_card_sum[i] = 0
        else:
            player_burst_flag.append(0)
        
        if DCardsum < player_card_sum[i]:
            player_winjudge_flag[i] = 2
        
        elif DCardsum == player_card_sum[i]:
            player_winjudge_flag[i] = 1
        
        if DCardsum > 21:
            player_winjudge_flag[i] = 2
        
            
    
    return player_winjudge_flag
        


def main():
    global deck
    MakeDeck(deck)
    P1 = CardDealer(deck)
    P2 = CardDealer(deck)
    PD = CardDealer(deck)
    P1d = [10,10]
    P2d = [10,10]
    KeepCard = 0
    

    
    #card change division

    while 1:
        print("P1 Do you need card(s)? Need = 1,  No card change = 0")
        print(ShowCards(P1))
        P1changeflg = input()

        if(P1changeflg == "1"):

            P1 = CardDealer(deck, P1, 1)
            break
        elif(P1changeflg == "2"):
            break
        elif(P1changeflg == "0"):
            pass
            break
        else:
            print("invaid value")

    print(ShowCards(P1))
    print(ShowCards(P2))
    print(ShowCards(PD))
    a = WinJudge(P1, P2, PD)
    #a = WinJudge(P1d, P2d)

    if(a == 1):
        print("P1 win")
    elif(a == 0):
        print("P2 win")
    elif(a == 2):
        print("dealer win")
    elif(a == 3):
        print("p1 p2 win (dealer lost) ")
    else:
        print("draw")
if __name__ == "__main__":
    #main()
    pass
    