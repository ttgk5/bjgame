# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 21:13:10 2021

@author: k4toh
"""


import socket
import pickle
import sys
import threading
from time import sleep
import bj_gui as bjg

import bjgame
root = bjg.tk.Tk()
game = bjg.gui(master=root)

player_flag = 0
P1_flag = 0
P2_flag = 0
dealer_card_data = []
P1_card_data = []
P2_card_data = []
win = 0

#ゲーム変数初期化
def game_var_init():
    global P1_flag
    global P2_flag
    global dealer_card_data
    global P1_card_data
    global P2_card_data
    global player_flag

    player_flag = 0
    P1_flag = 0
    P2_flag = 0
    dealer_card_data = []
    P1_card_data = []
    P2_card_data = []
    win = 0


def game_thread():

    global P1_flag
    global P2_flag
    global player_flag
    global win

    #サーバーに接続要求

    while game.start_flag != 1:
        pass

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = "127.0.0.1"
        port = 55580

        s.connect((host, port))
    except Exception as e:
        print(e)

    print(s)

    #メインループ
    while (True):
        try:
            # サーバーからのレスポンス 5byteで受信 プレイヤーナンバー、マッチングなど
            while 1:
                
                res = s.recv(5)

                if res == b'START':
                    print("Welcome BLACKJACK game! please wait...")

                    game.start_click()
                    
                elif res == b'PLAY1':
                    print("You are player 1")
                    player_flag = 1
                    P1_flag = 1

                elif res == b'PLAY2':
                    print("You are player 2")
                    player_flag = 2
                    P2_flag = 1
                    

                elif res == b'MATCH':
                    print("Matching complate!")
                    break

                elif res == b'NEXTT':
                    break

                else:
                    print(res.decode("utf-8"))

            #マッチング完了後、データ受信準備完了のデータを送信
            sleep(0.5)
            s.send("READY".encode("utf-8"))
            game.match_phase(player_flag)

            #カードデータを受信
            msg = s.recv(256)
            CardData = pickle.loads(msg)

            dealer_card_data = [CardData[0], CardData[1]]
            P1_card_data = [CardData[2], CardData[3]]
            P2_card_data = [CardData[4], CardData[5]]


            #ディーラーのカードを一枚のみ見せる
            print("Dealer's Card")
            dbuf = bjgame.ShowCards(dealer_card_data)
            print(dbuf[0])

            #自分に配られたカードを見せる
            print("Cards Dealt")
            if player_flag == 1:
                print(bjgame.ShowCards(P1_card_data))
                PCardData = P1_card_data
                game.main_phase(dealer_card_data, PCardData, P2_card_data)
            elif player_flag == 2:
                print(bjgame.ShowCards(P2_card_data))
                PCardData = P2_card_data
                game.main_phase(dealer_card_data, P1_card_data, PCardData)
            

                
                            
            #カードを引くかどうかのループ、バーストするか追加で引かないと抜ける
            while 1:

                if(bjgame.CardSum_Class(PCardData) > 21):
                    print("You are busted!")
                    changeflg = "3"
                    ChangeData = [changeflg, None]
                    s.send(pickle.dumps(ChangeData))
                    break
                
                print("Do you wanna add card? Yes = 1 No = 2")
                print(bjgame.ShowCards(PCardData))
                print(game.draw_flag)

                buf = 0

                changeflg = game.draw_flag
 


                if(int(game.draw_flag) == 1 and int(game.stop_flag) == 0):       #カード追加
                    changeflg = game.draw_flag
                    ChangeData = [str(changeflg), 0]
                    s.send(pickle.dumps(ChangeData))
                    msg = s.recv(512)
                    PCardData = pickle.loads(msg)
                    if P1_flag == 1:
                        game.main_phase(dealer_card_data, PCardData, P2_card_data)
                    elif P2_flag == 1:
                        game.main_phase(dealer_card_data, P1_card_data, PCardData)
                    game.draw_flag = 0               

                if(int(game.stop_flag) == 1):
                    changeflg = "2"
                    ChangeData = [str(changeflg), None]
                    s.send(pickle.dumps(ChangeData))
                    break

                else:
                    print("invaid value")
                    print(changeflg, type(changeflg))
                    sleep(2)

            #最終的なカードを見せる
            print("Your Cards")
            print(bjgame.ShowCards(PCardData))

            #他プレイヤーの処理を待つ、5byte
            while 1:
                res = s.recv(5)
                if res == b'WAITN':
                    print("Waiting for others...")

                elif res == b'DONE!':
                    print("who wins...")
                    break
                else:
                    pass
                res = None
            
            #勝敗判定の表示のループ
            while 1:
                res = s.recv(5)

                if res == b'GOWIN':
                    all_card_data = s.recv(512)
                    all_card_data = pickle.loads(all_card_data)

                    dealer_card_data = all_card_data[2]
                    game.d_card_list = dealer_card_data

                    if player_flag == 1:
                        others_card_data = all_card_data[1]
                        game.p2_card_list = others_card_data
                    elif player_flag == 2:
                        others_card_data = all_card_data[0]
                        game.p1_card_list = others_card_data

                    print("Dealer's cards")
                    
                    print(bjgame.ShowCards(dealer_card_data))

                    sleep(0.5)
                    s.send("READY".encode("utf-8"))

                    win = s.recv(4)
                    if win == b'win!':
                        print("You Win!")
                        game.judge_phase(win)

                    elif win == b'lose':
                        print("You lose! ")
                        game.judge_phase(win)
                        
                    elif win == b'draw':
                        print("Draw!")
                        game.judge_phase(win)

                print("Other player's Cards")
                print(bjgame.ShowCards(others_card_data))     
                break

            #コンティニューのループ
            print("contunue?  yes or no")
            game.continue_phase()

            cont = game.continue_exit_flag

            while 1:
                cont = game.continue_exit_flag
                #print(cont, "contf")

                if int(cont) == 2:
                    sleep(0.5)
                    s.send("ENDGAMES".encode("utf-8"))
                    print("see you nex time!")
                    sys.exit()
                elif int(cont) == 1:
                    sleep(0.5)
                    s.send("CONTINUE".encode("utf-8"))
                    msg = 0
                    break
            cont = 0

            print("other player waitin...")
            res = s.recv(8)
            while 1:
                if res == b'CONTINUE':
                    game_var_init()
                    break
                elif res == b'ENDGAMES':
                    print("see you next time!")
                    game.quit()
                    sys.exit()
                else:
                    print(res.decode("utf-8"))
            
                

        except Exception as e:
            print(e)
            continue

def main():
    try:


        main_th = threading.Thread(target=game_thread)
        main_th.setDaemon(True)
        main_th.start()


        game.mainloop()

        main_th.join()


    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
