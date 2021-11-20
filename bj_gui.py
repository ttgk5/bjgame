import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import sys
from time import sleep, time

import bjgame

#ゲーム関連imgパス
img_cards = [
    [
        "./img/S_1.png",
        "./img/S_2.png",
        "./img/S_3.png",
        "./img/S_4.png",
        "./img/S_5.png",
        "./img/S_6.png",
        "./img/S_7.png",
        "./img/S_8.png",
        "./img/S_9.png",
        "./img/S_10.png",
        "./img/S_11.png",
        "./img/S_12.png",
        "./img/S_13.png",
    ],
    [
        "./img/H_1.png",
        "./img/H_2.png",
        "./img/H_3.png",
        "./img/H_4.png",
        "./img/H_5.png",
        "./img/H_6.png",
        "./img/H_7.png",
        "./img/H_8.png",
        "./img/H_9.png",
        "./img/H_10.png",
        "./img/H_11.png",
        "./img/H_12.png",
        "./img/H_13.png",
    ],
    [
        "./img/D_1.png",
        "./img/D_2.png",
        "./img/D_3.png",
        "./img/D_4.png",
        "./img/D_5.png",
        "./img/D_6.png",
        "./img/D_7.png",
        "./img/D_8.png",
        "./img/D_9.png",
        "./img/D_10.png",
        "./img/D_11.png",
        "./img/D_12.png",
        "./img/D_13.png",
    ],
    [
        "./img/C_1.png",
        "./img/C_2.png",
        "./img/C_3.png",
        "./img/C_4.png",
        "./img/C_5.png",
        "./img/C_6.png",
        "./img/C_7.png",
        "./img/C_8.png",
        "./img/C_9.png",
        "./img/C_10.png",
        "./img/C_11.png",
        "./img/C_12.png",
        "./img/C_13.png",
    ]
]

bg = "./img/backgraund.png"
logo = "./img/logo.png"
start = "./img/START.png"
waiting_match = "./img/waiting_match.png"
match = "./img/maching.png"
p1 = "./img/Player1.png"
p2 = "./img/Player2.png"
sb = "./img/scoreborad.png"
win = "./img/win.png"
lose = "./img/lose.png"
draw = "./img/draw.png"
btn_d = "./img/DRAW_button.png"
btn_s = "./img/STOP.png"
waiting = "./img/waiting.png"
conti =  "./img/CONTINUE.png"
ex = "./img/EXIT.png"
bc = "./img/card.png"




class gui(tk.Frame):
    
    start_flag = 0
    draw_flag = 0
    stop_flag = 0
    player_flag = 0
    btn_flag = 0
    continue_exit_flag = 0

    d_card_list = []
    p1_card_list = []
    p2_card_list = []
    d_img_list = []
    p1_img_list = []
    p2_img_list = []
    
    p1_path = None
    p2_path = None



    def __init__(self,master):
        super().__init__(master)
        self.pack()
        master.geometry("600x400")
        master.title("Black Jack")
        master.resizable(False, False)
        self.canvas = tk.Canvas(master, width=600, height=400)
        self.bg_img = tk.PhotoImage(file = bg)
        self.canvas.create_image(300, 200, image = self.bg_img)
        self.set_phase()
        self.canvas.pack()



    def reset(self):
        self.start_flag = 0
        self.stop_flag = 0
        self.drawflag = 0
        self.player_flag = 0
        self.btn_flag = 0
        self.continue_exit_flag = 0
        self.d_card_list = []
        self.p1_card_list = []
        self.p2_card_list = []
        self.d_img_list = []
        self.p1_img_list = []
        self.p2_img_list = []



    def set_phase(self):
        self.logo_img = tk.PhotoImage(file = logo)
        self.canvas.create_image(300, 200, image = self.logo_img, tag = 't1')
        self.startbtn_img = Image.open(start)
        self.startbtn_img = self.startbtn_img.resize((70, 70))
        self.startbtn_img = ImageTk.PhotoImage(self.startbtn_img)
        self.start_btn = ttk.Button(image=self.startbtn_img, compound="none", command=self.start_click)
        self.start_btn.place(x=270,y=270)




    def start_click(self):
        self.start_flag = 1
        self.waiting_match_img = tk.PhotoImage(file = waiting_match)
        self.canvas.create_image(300, 200, image = self.waiting_match_img, tag = 't2')
        self.canvas.pack()
        self.start_btn.destroy()
        
    

    def match_phase(self, player):
        self.canvas.delete('t1')
        self.canvas.delete('t2')
        self.match_img = tk.PhotoImage(file = match)
        self.p1_img = tk.PhotoImage(file = p1)
        self.p2_img = tk.PhotoImage(file = p2)
        self.player_flag = player
        self.canvas.create_image(300, 200, image = self.match_img, tag = 't3')
        if self.player_flag == 1:
            self.canvas.create_image(300, 200, image = self.p1_img, tag = 't4')
            sleep(1)
        elif self.player_flag == 2:
            self.canvas.create_image(300, 200, image = self.p2_img, tag = 't5')
            sleep(1)



    def main_phase(self, d_cards, p1_cards, p2_cards):
        self.d_card_list = d_cards
        self.p1_card_list = p1_cards
        self.p2_card_list = p2_cards
        self.canvas.delete('t3')
        self.canvas.delete('t4')
        self.canvas.delete('t5')
        if self.btn_flag == 0:
            self.sb_img = tk.PhotoImage(file = sb)
            self.canvas.create_image(300, 200, image = self.sb_img, tag = 't6')
            self.make_mainbutton()
        self.card_show()
        self.canvas.pack()
        


    def make_mainbutton(self):
        self.draw_btn_img = Image.open(btn_d)
        self.draw_btn_img = self.draw_btn_img.resize((55, 55))
        self.draw_btn_img = ImageTk.PhotoImage(self.draw_btn_img)
        self.draw_btn = ttk.Button(image=self.draw_btn_img, compound="none", command=self.draw_click)
        self.draw_btn.place(x=200,y=167)
        self.stop_btn_img = Image.open(btn_s)
        self.stop_btn_img = self.stop_btn_img.resize((55, 55))
        self.stop_btn_img = ImageTk.PhotoImage(self.stop_btn_img)
        self.stop_btn = ttk.Button(image=self.stop_btn_img, compound="none", command=self.stop_click)
        self.stop_btn.place(x=340,y=167)
        self.btn_flag = 1
        


    def draw_click(self):
        self.draw_flag = 1



    def stop_click(self):
        self.draw_btn.destroy()
        self.stop_btn.destroy()
        self.stop_flag = 1
        self.waiting_img = tk.PhotoImage(file = waiting)
        self.canvas.create_image(300, 200, image = self.waiting_img, tag = 't7')
        self.canvas.pack()
    
        


    def judge_phase(self, judge):
        sleep(0.5)
        self.canvas.delete('t7')
        self.show_all()
        if judge == b'win!':
            self.win_img = tk.PhotoImage(file = win)
            self.canvas.create_image(300, 190, image = self.win_img, tag = 't8')
        elif judge == b'lose':
            self.lose_img = tk.PhotoImage(file = lose)
            self.canvas.create_image(300, 190, image = self.lose_img, tag = 't9')
        elif judge == b'draw':
            self.draw_img = tk.PhotoImage(file = draw)
            self.canvas.create_image(300, 190, image = self.draw_img, tag = 't10')
        self.canvas.pack()
        
    

    def continue_phase(self):
        self.continue_img = Image.open(conti)
        self.continue_img = self.continue_img.resize((50, 50))
        self.continue_img = ImageTk.PhotoImage(self.continue_img)
        self.continue_btn = tk.Button(image=self.continue_img, compound="none", command=self.continue_click)
        self.continue_btn.place(x=220,y=310)
        
        self.exit_img = Image.open(ex)
        self.exit_img = self.exit_img.resize((50, 50))
        self.exit_img = ImageTk.PhotoImage(self.exit_img)
        self.exit_btn = tk.Button(image=self.exit_img, compound="none", command=self.exit_click)
        self.exit_btn.place(x=320,y=310)



    def continue_click(self):

        self.continue_exit_flag = 1
        self.continue_btn.destroy()
        self.exit_btn.destroy()
        self.canvas.destroy()
        self.reset()
        self.canvas = tk.Canvas(self, width=600, height=400)
        self.bg_img = tk.PhotoImage(file = bg)
        self.canvas.create_image(300, 200, image = self.bg_img)
        
        self.set_phase()
        self.canvas.pack()
        self.start_click()




    def exit_click(self):
        self.continue_exit_flag = 2
        #self.destroy()
        self.quit()

            

    #ディーラーのカード１枚と自分のカードを表、それ以外を裏で表示
    def card_show(self):
        self.dealer_show(self.d_card_list)
        if self.player_flag == 1:
            self.p1_show(self.p1_card_list, 1)
            self.p2_show(self.p2_card_list)
        elif self.player_flag == 2:
            self.p1_show(self.p1_card_list)
            self.p2_show(self.p2_card_list, 1)



    #すべてのカードを表示
    def show_all(self):
        self.dealer_show(self.d_card_list, 1)
        self.p1_show(self.p1_card_list, 1)
        self.p2_show(self.p2_card_list, 1)



    #ディーラーのカードを表示
    #game_flagがNoneならカードを1枚だけ表示
    #そうでないならすべて表示
    def dealer_show(self, cards, show_flag = None):
        self.canvas.delete('l0')
        self.d_img_list = []
        if show_flag == None:
            d_path = cardPath(cards, 1)
            self.canvas.create_text(300, 58, text="??", font=("MSゴシック", "20"), tag='l0')
        elif show_flag != None:
            d_path = cardPath(cards)
            sum = bjgame.CardSum_Class(cards)
            if sum > 21 :
                self.canvas.create_text(310, 58, text='busted!', font=("MSゴシック", "20"), tag='l0')
                self.stop_click()
            else:
                self.canvas.create_text(300, 58, text=str(sum), font=("MSゴシック", "20"), tag='l0')
        for i in range(len(d_path)):
            img = Image.open(d_path[i])
            img = img.resize((50, 65))
            img = ImageTk.PhotoImage(img)
            self.d_img_list.append(img)
            self.canvas.create_image(245+(i*60), 90, image=self.d_img_list[i], anchor=tk.NW)
        
    #Player1のカードを表示
    #show_flagがNoneならカードをすべて裏
    #そうでないならすべて表示
    def p1_show(self, cards, show_flag = None):
        self.canvas.delete('l1')
        self.p1_img_list = []
        p1_path = []
        if show_flag != None:
            p1_path = cardPath(cards)
            sum = bjgame.CardSum_Class(cards)
            if sum > 21 :
                self.canvas.create_text(170, 360, text='busted!', font=("MSゴシック", "20"), tag='l1')
                self.stop_click()
            else:
                self.canvas.create_text(160, 360, text=str(sum), font=("MSゴシック", "20"), tag='l1')

        elif show_flag == None:
            p1_path = backOnlyPath(len(cards))
            self.canvas.create_text(160, 360, text="??", font=("MSゴシック", "20"), tag='l1')

        for i in range(len(cards)):
            if show_flag != None:
                img = Image.open(p1_path[i])
            elif show_flag == None:
                img = Image.open(p1_path[i])

            img = img.resize((50, 65))
            img = ImageTk.PhotoImage(img)
            self.p1_img_list.append(img)
            self.canvas.create_image(50+(i*60), 235, image=self.p1_img_list[i], anchor=tk.NW)


    #Player2のカードを表示
    #show_flagがNoneならカードをすべて裏
    #そうでないならすべて表示
    def p2_show(self, cards, show_flag = None):
        self.canvas.delete('l2')
        self.p2_img_list = []
        p2_path = []
        if show_flag != None:
            p2_path = cardPath(cards)
            sum = bjgame.CardSum_Class(cards)
            if sum > 21 :
                self.canvas.create_text(470, 360, text='busted!', font=("MSゴシック", "20"), tag='l2')
                self.stop_click()
            else:
                self.canvas.create_text(460, 360, text=str(sum), font=("MSゴシック", "20"), tag='l2')
        elif show_flag == None:
            p2_path = backOnlyPath(len(cards))
            self.canvas.create_text(460, 360, text="??", font=("MSゴシック", "20"), tag='l2')

        for i in range(len(cards)):
            if show_flag != None:
                img = Image.open(p2_path[i])
            elif show_flag == None:
                img = Image.open(p2_path[i])

            img = Image.open(p2_path[i])
            img = img.resize((50, 65))
            img = ImageTk.PhotoImage(img)
            self.p2_img_list.append(img)
            self.canvas.create_image(490-(i*60), 235, image=self.p2_img_list[i], anchor=tk.NW)


        

#カードと表示枚数を受けとり、imgのパスを返す
#表示枚数以外のカードは裏面で返す
#引数はTrumpCard class, int　返り値はlist
def cardPath(cards, sheets = None):
    cardimg = []
    if sheets == None:
        for i in range(len(cards)):
            if cards[i].suit == "SPADE":
                mark = 0
            elif cards[i].suit == "HEART":
                mark = 1
            elif cards[i].suit == "DIAMD":
                mark = 2
            elif cards[i].suit == "CLOVE":
                mark = 3
            num = cards[i].number
            if num == 'a':
                num = 1
            elif num == 'J':
                num = 11
            elif num == 'Q':
                num = 12
            elif num == 'K':
                num = 13
            cardimg.append(img_cards[int(mark)][int(num)-1])
    elif sheets != None:
        for i in range(sheets):
            if cards[i].suit == "SPADE":
                mark = 0
            elif cards[i].suit == "HEART":
                mark = 1
            elif cards[i].suit == "DIAMD":
                mark = 2
            elif cards[i].suit == "CLOVE":
                mark = 3
            num = cards[i].number
            if num == 'a':
                num = 1
            elif num == 'J':
                num = 11
            elif num == 'Q':
                num = 12
            elif num == 'K':
                num = 13
            cardimg.append(img_cards[int(mark)][int(num)-1])
        for i in range(len(cards) - sheets):
            cardimg.append(bc)
    return cardimg

#表示枚数を受けとり、imgのパスを返す
#表示枚数のカードを裏面で返す
#引数はint　返り値はlist
def backOnlyPath(sheets):
    cardimg = []
    for i in range(sheets):
        cardimg.append(bc)
    return cardimg


def main():
    
    root = tk.Tk()
    game = gui(master=root)
    game.start_click()
    game.match_phase(1)
    
    deck = bjgame.MakeDeck()
    dealer = bjgame.CardDealer(deck)
    P1 = bjgame.CardDealer(deck)
    P2 = bjgame.CardDealer(deck)
    #game.main_phase(dealer, P1, P2)
    #P1 = bjgame.CardDealer(deck, P1, 1)
    #P2 = bjgame.CardDealer(deck, P2, 1)

    
    
    game.main_phase(dealer, P1, P2)
    game.stop_click()
    #game.judge_phase(b'win!')
    game.continue_phase()
    

    game.mainloop()


if __name__ == "__main__":
    main()
    