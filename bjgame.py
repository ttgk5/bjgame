"""
blackjack game lib
author : t.katoh
"""

import random


def CardDealer(inputcards = None, Appendmode = None):
    cards = []
    if inputcards != None:
        cards = inputcards
    
    if Appendmode == None:
        cards.append(random.randint(1, 11))
        cards.append(random.randint(1, 11))
    else:
        cards.append(random.randint(1, 11))
    return cards

def dealerCPU(cards, P1, P2):
    while 1:
        if sum(cards) < 17:
            cards.append(random.randint(1, 11))
        elif sum(cards) >= 22:
            return cards
        else:
            break
    if (sum(cards) < sum(P1) or sum(cards) < sum(P2)):
        cards.append(random.randint(1, 11))

    return cards

def WinJudge(P1_cards, P2_cards, D_cards = [2,7]):       
    PlayerFlg = None      #1 = P1win   0 = P2win  None = draw
    DealerFlg = None      #1 = deler lost
    WinnerFlg = None      #1 = P1win   0 = P2win  2 = dealerwin  3 = P1, P2Win  None = draw 
    P1Cardsum = sum(P1_cards)
    P2Cardsum = sum(P2_cards)
    DCardsum = sum(D_cards)

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
    P1 = CardDealer()
    P2 = CardDealer()
    P1d = [10,10]
    P2d = [10,10]
    KeepCard = 0

    
    #card change division

    while 1:
        print("P1 Do you wanna change card(s)? 1card change = 1, 2cards change = 2, No card change = 0")
        print(P1)
        P1changeflg = input()

        if(P1changeflg == "1"):
            print("Please select keep card")
            KeepCard = input()
            P1 = CardDealer(KeepCard)
            break
        elif(P1changeflg == "2"):
            P1 = CardDealer()
            break
        elif(P1changeflg == "0"):
            pass
            break
        else:
            print("invaid value")

    print(P1)
    print(P2)
    a = WinJudge(P1, P2)
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


