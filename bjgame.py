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

def WinJudge(P1_cards, P2_cards, D_cards = [2,7]):       
    PlayerFlg = None      #1 = P1win   0 = P2win  None = draw
    DealerFlg = None      #1 = deler lost
    WinnerFlg = None      #1 = P1win   0 = P2win  2 = dealerwin  3 = P1, P2Win  None = draw 
    P1Cardsum = CardSum_Class(P1_cards)
    P2Cardsum = CardSum_Class(P2_cards)
    DCardsum = CardSum_Class(D_cards)

    P1Judge = 21 - P1Cardsum
    P2Judge = 21 - P2Cardsum
    DJudge  = 21 - DCardsum

    if (P1Cardsum > 21):    #P1 burst
        PlayerFlg = 0
    elif (P2Cardsum > 21):  #P2 burst
        PlayerFlg = 1
    elif (DCardsum > 21):
        DealerFlg = 1
        return 3
    
    if(PlayerFlg == None):
        if(P1Judge < P2Judge):  
            if(P1Judge < DJudge):
                WinnerFlg = 1
            elif(DJudge < P1Judge):
                WinnerFlg = 2
            else:
                WinnerFlg = None
                

        elif(P2Judge < P1Judge):
            if(P2Judge < DJudge):
                WinnerFlg = 0

            elif(DJudge < P2Judge):
                WinnerFlg = 2
            else:
                WinnerFlg = None
                
        else:
            if(P1Judge < DJudge):
                WinnerFlg = 3
            else:
                WinnerFlg = 2

    return WinnerFlg


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
    main()


