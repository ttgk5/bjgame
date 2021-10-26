# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 21:13:10 2021

@author: k4toh
"""


import socket
import pickle
from time import sleep

from bjgame import CardDealer



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
            elif res == b'PLAY2':
                print("You are player 2")
            elif res == b'MATCH':
                print("Matching complate!")
            elif res == b'NEXTT':
                break
            else:
                print(res.decode("utf-8"))

        

        msg = s.recv(128)

        CardData = pickle.loads(msg)
        DCardData = [CardData[2], CardData[3]]
        PCardData = [CardData[0], CardData[1]]
        print("Dealer's Card")
        print(DCardData[0])
        print("Cards Dealt")
        print(PCardData)

        while 1:
                if(sum(PCardData) > 21):
                    print("You are busted!")
                    changeflg = "3"
                    ChangeData = [changeflg, None]
                    s.send(pickle.dumps(ChangeData))
                    break
                
                print("Do you wanna add card? Yes = 1 No = 2")
                print(PCardData)
                changeflg = input()

                if(changeflg == "1"):       #カード追加

                    ChangeData = [changeflg, 0]
                    s.send(pickle.dumps(ChangeData))
                    msg = s.recv(128)
                    PCardData = pickle.loads(msg)

                elif(changeflg == "2"):
                    ChangeData = [changeflg, None]
                    s.send(pickle.dumps(ChangeData))
                    break

                else:
                    print("invaid value")
                
        print("Your Cards")
        print(PCardData)

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
                print(DCardData)
            elif res == b'GOWIN':
                DCardData = s.recv(128)
                print("Dealer's cards")
                print(pickle.loads(DCardData))

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

    except Exception as e:
        print(e)
        continue