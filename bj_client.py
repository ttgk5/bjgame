# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 21:13:10 2021

@author: k4toh
"""


import socket
import pickle
import sys
from time import sleep

import bjgame

P1_flag = 0
P2_flag = 0
dealer_card_data = []
P1_card_data = []
P2_card_data = []

def game_var_init():
    global P1_flag
    global P2_flag
    global dealer_card_data
    global P1_card_data
    global P2_card_data

    P1_flag = 0
    P2_flag = 0
    dealer_card_data = []
    P1_card_data = []
    P2_card_data = []


def main():

    global P1_flag
    global P2_flag

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = "127.0.0.1"
        port = 55580

        s.connect((host, port))
    except Exception as e:
        print(e)

    print(s)


    while (True):
        try:
            print("\n")
            # サーバーからのレスポンス
            while 1:
                
                res = s.recv(5)

                if res == b'START':
                    print("Welcome BLACKJACK game! please wait...")
                elif res == b'PLAY1':
                    print("You are player 1")
                    P1_flag = 1
                elif res == b'PLAY2':
                    print("You are player 2")
                    P2_flag = 1
                elif res == b'MATCH':
                    print("Matching complate!")
                    break
                elif res == b'NEXTT':
                    break
                else:
                    print(res.decode("utf-8"))

            sleep(0.5)
            s.send("READY".encode("utf-8"))

            msg = s.recv(256)

            CardData = pickle.loads(msg)

            dealer_card_data = [CardData[0], CardData[1]]
            P1_card_data = [CardData[2], CardData[3]]
            P2_card_data = [CardData[4], CardData[5]]

            print("Dealer's Card")
            dbuf = bjgame.ShowCards(dealer_card_data)
            print(dbuf[0])

            print("Cards Dealt")
            if P1_flag == 1:
                print(bjgame.ShowCards(P1_card_data))
                PCardData = P1_card_data
            elif P2_flag == 1:
                print(bjgame.ShowCards(P2_card_data))
                PCardData = P2_card_data

            while 1:
                    if(bjgame.CardSum_Class(PCardData) > 21):
                        print("You are busted!")
                        changeflg = "3"
                        ChangeData = [changeflg, None]
                        s.send(pickle.dumps(ChangeData))
                        break
                    
                    print("Do you wanna add card? Yes = 1 No = 2")
                    print(bjgame.ShowCards(PCardData))
                    changeflg = input()

                    if(changeflg == "1"):       #カード追加

                        ChangeData = [changeflg, 0]
                        s.send(pickle.dumps(ChangeData))
                        msg = s.recv(256)
                        PCardData = pickle.loads(msg)

                    elif(changeflg == "2"):
                        ChangeData = [changeflg, None]
                        s.send(pickle.dumps(ChangeData))
                        break

                    else:
                        print("invaid value")
                    
            print("Your Cards")
            print(bjgame.ShowCards(PCardData))

            waitcnt = 0

            while 1:
                res = s.recv(5)
                if res == b'WAITN':
                    print("Waiting for others...")
                    waitcnt =+ 1

                elif res == b'DONE!':
                    print("who wins...")
                    break
                else:
                    pass
                res = None
            
            while 1:
                res = s.recv(5)
                if res == b'SHOWD':
                    print("Dealer win!")
                    print(dealer_card_data)
                elif res == b'GOWIN':
                    dealer_card_data = s.recv(256)
                    print("Dealer's cards")
                    
                    print(bjgame.ShowCards(pickle.loads(dealer_card_data)))

                    win = s.recv(3)
                    if win == b'P1W':
                        print("P1 win!")

                    elif win == b'P2W':
                        print("P2 win! ")
                        
                    elif win == b'P12':
                        print("P1 P2 win!")
                        
                    elif win == b'DLW':
                        print("Dealer win!")
                        
                    elif win == b'DRW':
                        print("Draw!")
                break

            print("contunue?  yes or no")
            while 1:
                cont = input()
                if cont == "no":
                    sleep(0.5)
                    s.send("ENDGAMES".encode("utf-8"))
                    print("see you nex time!")
                    sys.exit()
                elif cont == "yes":
                    sleep(0.5)
                    s.send("CONTINUE".encode("utf-8"))
                    msg = 0
                    break
            
            print("other player waitin...")
            res = s.recv(8)
            while 1:
                if res == b'CONTINUE':
                    game_var_init()
                    break
                elif res == b'ENDGAMES':
                    print("see you next time!")
                    sys.exit()
                else:
                    print(res.decode("utf-8"))
                

        except Exception as e:
            print(e)
            continue


if __name__ == "__main__":
    main()
    