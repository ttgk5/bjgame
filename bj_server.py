"""
Created on Fri Oct 22 21:13:49 2021

@author: k4toh
cording in utf-8

ブラックジャック サーバー側プログラム
クライアント側からカード情報を受け取り、勝敗判定を行う
"""

import socket
import select
import threading
import random
import bjgame
import pickle
from time import sleep

MAX_PLAYER = 2
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 接続待ちするサーバのホスト名とポート番号を指定
host = "127.0.0.1"
port = 55580
argument = (host, port)
sock.bind(argument)
# MAX_PLAYER まで接続を許可
sock.listen(MAX_PLAYER)
clients = []

#ゲーム関連変数
ConFlg = 0
doneflg = []
continueflg = []
P1Burstflg = 0
P2Burstflg = 0
P1Continueflg = 0
P2Continueflg = 0
Playcount = 0
deck = bjgame.MakeDeck()
P1CardData = bjgame.CardDealer(deck)
P2CardData = bjgame.CardDealer(deck)
DCardData  = bjgame.CardDealer(deck)

clientscard = [DCardData]

def GameInit():
    global doneflg
    global P1Burstflg
    global P2Burstflg
    global P1Continueflg
    global P2Continueflg
    global deck
    global P1CardData 
    global P2CardData 
    global DCardData


    doneflg = []
    P1Burstflg = 0
    P2Burstflg = 0
    P1Continueflg = 0
    P2Continueflg = 0
    deck = bjgame.MakeDeck()
    P1CardData = bjgame.CardDealer(deck)
    P2CardData = bjgame.CardDealer(deck)
    DCardData  = bjgame.CardDealer(deck)

    clientscard = [DCardData]

def Win_Procedure(connection):
    global deck
    global DCardData
    global P1CardData
    global P2CardData

    while 1:
        if(len(doneflg) == MAX_PLAYER):
            connection.send("DONE!".encode("utf-8"))
            break
        else:
            #print(doneflg)
            connection.send("WAITN".encode("utf-8"))
            sleep(2)

    if (P1Burstflg and P2Burstflg):
        print("dealer win")
        sleep(0.5)
        connection.send("SHOWD".encode("utf-8"))

    else:
        sleep(0.5)
        connection.send("GOWIN".encode("utf-8"))
        d = bjgame.dealerCPU(deck, DCardData, P2CardData, P1CardData)
        sleep(0.1)
        connection.send(pickle.dumps(d))
        sleep(0.1)
        winner = bjgame.WinJudge(P1CardData, P2CardData, d)


        if(winner == 1):
            sleep(0.3)
            connection.send("P1W".encode("utf-8"))
            print("P1 win")
        elif(winner == 0):
            sleep(0.3)
            connection.send("P2W".encode("utf-8"))
            print("P2 win")
        elif(winner == 2):
            sleep(0.3)
            connection.send("DLW".encode("utf-8"))
            print("dealer win")
        elif(winner == 3):
            sleep(0.3)
            connection.send("P12".encode("utf-8"))
            print("p1 p2 win (dealer lost) ")
        else:
            sleep(0.3)
            connection.send("DRW".encode("utf-8"))
            print("draw")


def PlayerThread(connection, address, pflag):
    global deck
    global doneflg
    global P1Continueflg
    global P2Continueflg
    global P1CardData
    global P2CardData
    global P1Burstflg
    global P2Burstflg
    global Playcount

    try:
        while 1:
            #クライアント側から受信する
            # res = connection.recv(4096)

            #先に接続した方がP1
            P1Flg = 0
            cnt = 0

            if Playcount == 0:
                connection.send("START".encode("utf-8"))
                sleep(1)
                if pflag == 1:
                    connection.send("PLAY1".encode("utf-8"))
                if pflag == 2:
                    connection.send("PLAY2".encode("utf-8"))
            else:
                sleep(1)
                if pflag == 1:
                    connection.send("PLAY1".encode("utf-8"))
                if pflag == 2:
                    connection.send("PLAY2".encode("utf-8"))

            while 1:               
                if ConFlg == 1:
                    connection.send("MATCH".encode("utf-8"))
                    connection.send("NEXTT".encode("utf-8"))
                    break
                    
                
            
            #ディーラーのカードとプレイヤーのカードデータ
            DealCard = []
            for i in clientscard:
                DealCard.extend(i)

            connection.send(pickle.dumps(DealCard))


            while 1:
                msg = connection.recv(128)
                ChangeData = pickle.loads(msg)

                if ChangeData[0] == "1":    #1枚追加
                    if pflag == 1:
                        P1CardData = bjgame.CardDealer(deck, P1CardData, 1)
                        sleep(0.2)
                        connection.send(pickle.dumps(P1CardData))
                    else:
                        P1CardData = bjgame.CardDealer(deck, P2CardData, 1)
                        sleep(0.2)
                        connection.send(pickle.dumps(P2CardData))                    

                elif ChangeData[0] == "2":  #交換なし
                    print("no card add")
                    break

                elif ChangeData[0] == "3":
                    if pflag == 1:
                        print("P1 burst")
                        P1Burstflg = 1
                    else:
                        print("P2 burst")
                        P2Burstflg = 1

                    break
                else:
                    connection.send("INVAL".encode("utf-8"))
            
            doneflg.append(1)

            #debug
            if pflag == 1:
                print("1 Waiting for others...")
            else:
                print("2 Waiting for others...")
            #~~

            Win_Procedure(connection)

            
            cont = connection.recv(8)
            if cont == "CONTINUE":
                if pflag == 1:
                    P1Continueflg = 1
                    print(P1Continueflg)
                elif pflag == 2:
                    P2Continueflg = 1
                    print(P2Continueflg)
                sleep(0.5)
                
            elif cont == "ENDGAMES":
                break

    except Exception as e:
        print(e)

def gamemanager():
    global continueflg
    global clients
    global Playcount
    global P1Continueflg
    global P2Continueflg
    cnt = 0

    print("made thread")
    try:
        while 1:
            if P1Continueflg == 1:
                print("p1cont")
            if P2Continueflg == 1:
                print("p2cont")
            if P1Continueflg + P2Continueflg == MAX_PLAYER:
                print("initialized")
                GameInit()
                Playcount = 1 + Playcount
    except Exception as e:
        print(e)



def main():
    global ConFlg
    global clients

    th = threading.Thread(target=gamemanager, daemon=True)
    th.start()
    while True:
        try:
            # 接続要求を受信
            conn, addr = sock.accept()

        except KeyboardInterrupt:
            sock.close()
            exit()
            break

        # アドレス確認
        print("[アクセス元アドレス]=>{}".format(addr[0]))
        print("[アクセス元ポート]=>{}".format(addr[1]))
        print("\r\n")
        # 待受中にアクセスしてきたクライアントを追加
        clients.append((conn, addr))
        if(len(clients) == 2):
            ConFlg = 1
            clientscard.extend([P1CardData, P2CardData])

        # スレッド作成
        if(len(clients) == 2):
            pflag = 2
            thread = threading.Thread(target=PlayerThread, args=(conn, addr, pflag), daemon=True)
        else:
            pflag = 1
            thread = threading.Thread(target=PlayerThread, args=(conn, addr, pflag), daemon=True)
        # スレッドスタート
        thread.start()




    

if __name__ == "__main__":
    main()
    
