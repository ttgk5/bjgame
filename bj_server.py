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
P1Continueflg = None
P2Continueflg = None
initflg = []
endflg = []
gameendflg = []
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
    global initflg
    global deck
    global P1CardData 
    global P2CardData 
    global DCardData
    global endflg
    global ConFlg
    global clientscard


    doneflg = []
    endflg = []
    P1Burstflg = 0
    P2Burstflg = 0
    ConFlg = 0
    #P1Continueflg = 0
    #P2Continueflg = 0
    initflg = []
    deck = bjgame.MakeDeck()
    P1CardData = bjgame.CardDealer(deck)
    P2CardData = bjgame.CardDealer(deck)
    DCardData  = bjgame.CardDealer(deck)

    clientscard = [DCardData, P1CardData, P2CardData]

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
        #print("dealer win")
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

def Player_Allocation(connection, address):
    #接続してきたプレイヤーの番号を割り振る
    cnt = 0
    for i in clients:
        cnt += 1
        if i == (connection, address):
            break
    
    return cnt

def PlayerThread(connection, address):
    global deck
    global doneflg
    global P1Continueflg
    global P2Continueflg
    global initflg
    global gameendflg
    #global endflg
    global P1CardData
    global P2CardData
    global P1Burstflg
    global P2Burstflg
    global Playcount

    contflg = 0

    try:
        while contflg == 0:
            #クライアント側から受信する
            # res = connection.recv(4096)

            #先に接続した方がP1
            pflag = Player_Allocation(connection, address)
            print(Playcount)

            if Playcount == 0:
                connection.send("START".encode("utf-8"))
                sleep(1)
                if pflag == 1:
                    connection.send("PLAY1".encode("utf-8"))
                    P1Continueflg = None
                if pflag == 2:
                    P2Continueflg = None
                    connection.send("PLAY2".encode("utf-8"))
            else:
                while 1:
                    if len(gameendflg) == MAX_PLAYER:
                        break
                if pflag == 1:
                    connection.send("PLAY1".encode("utf-8"))
                    sleep(0.5)
                if pflag == 2:
                    connection.send("PLAY2".encode("utf-8"))
                    sleep(0.5)

            while 1:               
                if len(clients) == MAX_PLAYER:
                    connection.send("MATCH".encode("utf-8"))
                    sleep(0.5)
                    """
                    connection.send("NEXTT".encode("utf-8"))
                    sleep(0.5)
                    """
                    break
                    
                
            
            #ディーラーのカードとプレイヤーのカードデータ

            rdyflg = connection.recv(5)
            while 1:
                if rdyflg == b'READY':
                    print("PlayerThread %d : Clients READY" % (pflag))
                    break
            
            DealCard = []
            gameendflg = []
            for i in clientscard:
                DealCard.extend(i)
            sleep(0.5)

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
                    print("PlayerThread %d : no cards add"%(pflag))
                    break

                elif ChangeData[0] == "3":
                    if pflag == 1:
                        print("PlayerThread %d : Burst! "%(pflag))
                        P1Burstflg = 1
                    else:
                        print("PlayerThread %d : Burst! "%(pflag))
                        P2Burstflg = 1

                    break
                else:
                    connection.send("INVAL".encode("utf-8"))
            
            doneflg.append(1)

            #debug
            if pflag == 1:
                print("PlayerThread %d : Waiting for others ..."%(pflag))
            else:
                print("PlayerThread %d : Waiting for others ..."%(pflag))
            #~~

            Win_Procedure(connection)

            
            cont = connection.recv(8)
            while 1:
                if cont == b"CONTINUE":
                    if pflag == 1:
                        P1Continueflg = 1
                        print("PlayerThread %d : Continue "%(pflag))
                        #print(P1Continueflg)
                        sleep(0.5)
                        #connection.send("CONTINUE".encode("utf-8"))
                        break
                    elif pflag == 2:
                        P2Continueflg = 1
                        print("PlayerThread %d : Continue "%(pflag))
                        #print(P2Continueflg)
                        sleep(0.5)
                        #connection.send("CONTINUE".encode("utf-8"))
                        break

                elif cont == b"ENDGAMES":
                    if pflag == 1:
                        P1Continueflg = 0
                        endflg.append(1)
                        print("PlayerThread %d : P1 endgame"%(pflag))
                        #print(P1Continueflg)
                        sleep(0.5)
                        #connection.send("CONTINUE".encode("utf-8"))
                        break
                    elif pflag == 2:
                        P2Continueflg = 0
                        endflg.append(1)
                        print("PlayerThread %d : P2 endgame"%(pflag))
                        #print(P2Continueflg)
                        sleep(0.5)
                        #connection.send("CONTINUE".encode("utf-8"))
                        break

            print("PlayerThread %d : other player waitn..." % (pflag))
            while 1:
                if P1Continueflg != None and P2Continueflg != None:
                    if P1Continueflg + P2Continueflg == 2:
                        gameendflg.append(1)
                        initflg.append(1)
                        connection.send("CONTINUE".encode("utf-8"))
                        sleep(1)
                        break

                if P1Continueflg == 1 and P2Continueflg == 0:
                    initflg.append(1)
                    gameendflg.append(1)
                    if pflag == 1:
                        sleep(0.5)
                        connection.send("CONTINUE".encode("utf-8"))
                        sleep(1)
                        break
                    elif pflag == 2:
                        contflg = 1
                        break

                if P1Continueflg == 0 and P2Continueflg == 1:
                    initflg.append(1)
                    gameendflg.append(1)
                    if pflag == 2:
                        sleep(0.5)
                        connection.send("CONTINUE".encode("utf-8"))
                        sleep(1)
                        break
                    elif pflag == 1:
                        contflg = 1
                        break
                if len(endflg) == MAX_PLAYER:
                    contflg = 1
                    break

        
        print("PlayerThread %d : thread dead" % (pflag))
    except Exception as e:
        print(e)

    finally:
        clients.remove((connection, address))
        print(clients)

        connection.close()
    

def gamemanager():
    global continueflg
    global clients
    global Playcount
    global P1Continueflg
    global P2Continueflg
    global initflg
    global gameendflg
    cnt = 0

    print("gamemanager: Thread created")
    try:
        while 1:
            if len(initflg) == MAX_PLAYER:
                print("gamemanager: initialized")
                GameInit()
                Playcount += 1
            if len(endflg) == MAX_PLAYER:
                sleep(2)
                print("gamemanager: initialized (because no players)")
                GameInit()
                Playcount += 1

            if len(clients) == 0:
                gameendflg = [1,1]
            
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
        if(len(clients) == MAX_PLAYER):
            ConFlg = 1
            clientscard.extend([P1CardData, P2CardData])

        # スレッド作成
        """
        if(len(clients) == MAX_PLAYER):
            pflag = 2
            thread = threading.Thread(target=PlayerThread, args=(conn, addr, pflag), daemon=True)
        else:
            pflag = 1
        """
        thread = threading.Thread(target=PlayerThread, args=(conn, addr), daemon=True)
        # スレッドスタート
        thread.start()




    

if __name__ == "__main__":
    main()
    
