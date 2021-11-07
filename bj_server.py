"""
Created on Fri Oct 22 21:13:49 2021

@author: k4toh
cording in utf-8

ブラックジャック サーバー側プログラム
クライアント側からカード情報を受け取り、勝敗判定を行う
"""

import socket
import threading
import bjgame
import pickle
import sys
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

#ゲーム関連変数 Game_Var

card_sel_comp_flag = []
player_continue_flag = []
P1_burst_flag = 0
P2_burst_flag = 0
P1_continue_flag = None
P2_continue_flag = None
game_var_init_flag = []
game_end_flag = []
game_continue_flag = []
game_play_counter = 0
deck = bjgame.MakeDeck()

P1_card_data = bjgame.CardDealer(deck)
P2_card_data = bjgame.CardDealer(deck)
dealer_card_data  = bjgame.CardDealer(deck)

clients_card_data = [dealer_card_data]

def game_var_init():
    global card_sel_comp_flag
    global P1_burst_flag
    global P2_burst_flag
    global P1_continue_flag
    global P2_continue_flag
    global game_var_init_flag
    global deck
    global P1_card_data
    global P2_card_data 
    global dealer_card_data
    global game_end_flag
    global clients_card_data


    card_sel_comp_flag = []
    game_end_flag = []
    P1_burst_flag = 0
    P2_burst_flag = 0

    #P1_continue_flag = 0
    #P2_continue_flag = 0
    game_var_init_flag = []
    deck = bjgame.MakeDeck()
    P1_card_data = bjgame.CardDealer(deck)
    P2_card_data = bjgame.CardDealer(deck)
    dealer_card_data  = bjgame.CardDealer(deck)

    clients_card_data = [dealer_card_data, P1_card_data, P2_card_data]

def winner_judge(connection,pflag):
    global deck
    global dealer_card_data
    global P1_card_data
    global P2_card_data

    while 1:
        if(len(card_sel_comp_flag) == MAX_PLAYER):
            connection.send("DONE!".encode("utf-8"))
            break
        else:
            #print(card_sel_comp_flag)
            connection.send("WAITN".encode("utf-8"))
            sleep(2)
    """
    if (P1_burst_flag and P2_burst_flag):
        #print("dealer win")
        sleep(0.5)
        connection.send("SHOWD".encode("utf-8"))
    """
    
    sleep(0.5)
    connection.send("GOWIN".encode("utf-8"))
    d = bjgame.dealerCPU(deck, dealer_card_data, P2_card_data, P1_card_data)
    all_card_data = [P1_card_data, P2_card_data, d]
    sleep(0.1)

    connection.send(pickle.dumps(all_card_data))
    sleep(0.1)
    player_card = [P1_card_data, P2_card_data]
    result = bjgame.WinJudge(player_card, d)

    while 1:
        rdyflg = connection.recv(5)
        if rdyflg == b"READY":
            break
    if(pflag == 1):
        if result[pflag-1] == 0:
            sleep(0.3)
            connection.send("lose".encode("utf-8"))
            print("P%d lose" %(pflag))
        if result[pflag] == 1:
            sleep(0.3)
            connection.send("draw".encode("utf-8"))
            print("P%d draw" %(pflag))
        if result[pflag] == 2:
            sleep(0.3)
            connection.send("win!".encode("utf-8"))
            print("P%d win" %(pflag))

    elif(pflag == 2):
        if result[pflag-1] == 0:
            sleep(0.3)
            connection.send("lose".encode("utf-8"))
            print("P%d lose" %(pflag))
        if result[pflag-1] == 1:
            sleep(0.3)
            connection.send("draw".encode("utf-8"))
            print("P%d draw" %(pflag))
        if result[pflag-1] == 2:
            sleep(0.3)
            connection.send("win!".encode("utf-8"))
            print("P%d win" %(pflag))


def player_allocation(connection, address):
    #接続してきたプレイヤーの番号を割り振る
    cnt = 0
    for i in clients:
        cnt += 1
        if i == (connection, address):
            break
    
    return cnt

def player_main_thread(connection, address):
    global deck
    global card_sel_comp_flag
    global P1_continue_flag
    global P2_continue_flag
    global game_var_init_flag
    global game_continue_flag
    #global game_end_flag
    global P1_card_data
    global P2_card_data
    global P1_burst_flag
    global P2_burst_flag
    global game_play_counter

    contflg = 0

    try:
        while contflg == 0:
            #クライアント側から受信する
            # res = connection.recv(4096)

            #先に接続した方がP1
            pflag = player_allocation(connection, address)
            print(game_play_counter)

            if game_play_counter == 0:
                connection.send("START".encode("utf-8"))
                sleep(1)
                if pflag == 1:
                    connection.send("PLAY1".encode("utf-8"))
                    P1_continue_flag = None
                if pflag == 2:
                    P2_continue_flag = None
                    connection.send("PLAY2".encode("utf-8"))
            else:
                while 1:
                    if len(game_continue_flag) == MAX_PLAYER:
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
                    print("player_main_thread %d : Clients READY" % (pflag))
                    break
            
            DealCard = []
            game_continue_flag = []
            for i in clients_card_data:
                DealCard.extend(i)
            sleep(0.5)

            connection.send(pickle.dumps(DealCard))


            while 1:
                msg = connection.recv(128)
                ChangeData = pickle.loads(msg)

                if ChangeData[0] == "1":    #1枚追加
                    if pflag == 1:
                        P1_card_data = bjgame.CardDealer(deck, P1_card_data, 1)
                        sleep(0.2)
                        connection.send(pickle.dumps(P1_card_data))
                    else:
                        P1_card_data = bjgame.CardDealer(deck, P2_card_data, 1)
                        sleep(0.2)
                        connection.send(pickle.dumps(P2_card_data))                    

                elif ChangeData[0] == "2":  #交換なし
                    print("player_main_thread %d : no cards add"%(pflag))
                    break

                elif ChangeData[0] == "3":
                    if pflag == 1:
                        print("player_main_thread %d : Burst! "%(pflag))
                        P1_burst_flag = 1
                    else:
                        print("player_main_thread %d : Burst! "%(pflag))
                        P2_burst_flag = 1

                    break
                else:
                    connection.send("INVAL".encode("utf-8"))
            
            card_sel_comp_flag.append(1)

            #debug
            if pflag == 1:
                print("player_main_thread %d : Waiting for others ..."%(pflag))
            else:
                print("player_main_thread %d : Waiting for others ..."%(pflag))
            #~~

            winner_judge(connection,pflag)

            
            cont = connection.recv(8)
            while 1:
                if cont == b"CONTINUE":
                    if pflag == 1:
                        P1_continue_flag = 1
                        print("player_main_thread %d : Continue "%(pflag))
                        #print(P1_continue_flag)
                        sleep(0.5)
                        #connection.send("CONTINUE".encode("utf-8"))
                        break
                    elif pflag == 2:
                        P2_continue_flag = 1
                        print("player_main_thread %d : Continue "%(pflag))
                        #print(P2_continue_flag)
                        sleep(0.5)
                        #connection.send("CONTINUE".encode("utf-8"))
                        break

                elif cont == b"ENDGAMES":
                    if pflag == 1:
                        P1_continue_flag = 0
                        game_end_flag.append(1)
                        print("player_main_thread %d : P1 endgame"%(pflag))
                        #print(P1_continue_flag)
                        sleep(0.5)
                        #connection.send("CONTINUE".encode("utf-8"))
                        break
                    elif pflag == 2:
                        P2_continue_flag = 0
                        game_end_flag.append(1)
                        print("player_main_thread %d : P2 endgame"%(pflag))
                        #print(P2_continue_flag)
                        sleep(0.5)
                        #connection.send("CONTINUE".encode("utf-8"))
                        break

            print("player_main_thread %d : other player waitn..." % (pflag))
            while 1:
                if P1_continue_flag != None and P2_continue_flag != None:
                    if P1_continue_flag + P2_continue_flag == 2:
                        game_continue_flag.append(1)
                        game_var_init_flag.append(1)
                        connection.send("CONTINUE".encode("utf-8"))
                        sleep(1)
                        break

                if P1_continue_flag == 1 and P2_continue_flag == 0:
                    game_var_init_flag.append(1)
                    game_continue_flag.append(1)
                    if pflag == 1:
                        sleep(0.5)
                        connection.send("CONTINUE".encode("utf-8"))
                        sleep(1)
                        break
                    elif pflag == 2:
                        contflg = 1
                        break

                if P1_continue_flag == 0 and P2_continue_flag == 1:
                    game_var_init_flag.append(1)
                    game_continue_flag.append(1)
                    if pflag == 2:
                        sleep(0.5)
                        connection.send("CONTINUE".encode("utf-8"))
                        sleep(1)
                        break
                    elif pflag == 1:
                        contflg = 1
                        break
                if len(game_end_flag) == MAX_PLAYER:
                    contflg = 1
                    break

        
        print("player_main_thread %d : thread dead" % (pflag))

    except Exception as e:
        print("player_main_thread %d : " %(pflag) , end="")
        print(e)

    finally:
        clients.remove((connection, address))
        print(clients)

        connection.close()
    

def game_manager():
    global player_continue_flag
    global clients
    global game_play_counter
    global P1_continue_flag
    global P2_continue_flag
    global game_var_init_flag
    global game_continue_flag


    print("game_manager: Thread created")
    try:
        while 1:
            if len(game_var_init_flag) == MAX_PLAYER:
                print("game_manager: initialized")
                sleep(0.5)
                game_var_init()
                game_play_counter += 1
            if len(game_end_flag) == MAX_PLAYER:
                sleep(2)
                print("game_manager: initialized (because no players)")
                game_var_init()
                game_play_counter += 1

            if len(clients) == 0:
                game_continue_flag = [1,1]
            
    except Exception as e:
        print(e)

def comandline():
    while 1:
        if input() == "exit":
            sys.exit()
        else:
            print("comandline : invaild commands")


def player_acceptance():
    global clients

    #cmd = threading.Thread(target=comandline, daemon=True)

    #cmd.start()
    try:
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
                clients_card_data.extend([P1_card_data, P2_card_data])

            # スレッド作成
            """
            if(len(clients) == MAX_PLAYER):
                pflag = 2
                thread = threading.Thread(target=player_main_thread, args=(conn, addr, pflag), daemon=True)
            else:
                pflag = 1
            """
            thread = threading.Thread(target=player_main_thread, args=(conn, addr), daemon=True)
            # スレッドスタート
            thread.start()

    except Exception as e:
        print(e)

def main():
    print("BLACK JACK GAME SERVER STARTING....")
    acc_thread = threading.Thread(target=player_acceptance, daemon=True)
    game_manager_thread = threading.Thread(target=game_manager, daemon=True)

    acc_thread.start()
    game_manager_thread.start()

    comandline()





    

if __name__ == "__main__":
    main()
    
