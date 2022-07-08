from random import randint
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

DIFFICULTY = {
            "easy":(8,8,10),
            "medium":(16,16,40),
            "hard":(30,24,99)}
BOMB = "b"

class Game:
    def __init__(self, frame: object, diff: str = "medium"):
        self.size_x, self.size_y, self.bombs = DIFFICULTY[diff]
        self.button_pressed = set()
        self.field = self.create_field(frame)

        self.place_bombs(self.bombs)
        

    def create_field(self, frame: object) -> list:
        """Create a Matrix with Button Class instances"""
        return [[MsButton(frame, x, y, game_obj=self)
                            for x in range(self.size_x)]
                                for y in range(self.size_y)]
        

    def place_bombs(self, bomb_count: int) -> None:
        """Places the bombs in the field and set the numbers near the bombs"""
        while bomb_count > 0:
            x,y = randint(0,self.size_x-1), randint(0,self.size_y-1)
            if self.field[y][x].text == BOMB:
                continue
            self.field[y][x].text = BOMB
            bomb_count -= 1
            for j in (-1,0,1):
                for i in (-1,0,1):
                    if 0 <= y+j < self.size_y and 0 <= x+i < self.size_x:
                        if self.field[y+j][x+i].text != "b":
                            self.field[y+j][x+i].text += 1

    def button_press(self, coord_xy: tuple):
        """Handle pressed button"""
        x,y = coord_xy
        if (x,y) in self.button_pressed:
            return
        b = self.field[y][x]
        if b.text == BOMB:
            self.game_over()
        elif b.text:
            b["text"] = str(b.text)
            b["style"]="{}.TButton".format(b.text)
            b.state(['disabled'])
            self.button_pressed.add((x,y))
        else:
            b.state(['disabled'])
            self.button_pressed.add((x,y))
            k = (-1,0,1)
            for j in k:
                for i in k:
                    if 0 <= y+j < self.size_y and 0 <= x+i < self.size_x:
                        self.button_press((x+i,y+j))
        self.check_win()


    def check_win(self):
        """check if player wins"""
        if len(self.button_pressed) == self.size_x*self.size_y-self.bombs:
            messagebox.showinfo(message='Y O U  W O N')


    def game_over(self):
        """Massage if player hit a bomb"""
        messagebox.showinfo(message="B O O M !\nG A M E  O V E R")


class MsButton(ttk.Button):
    def __init__(self, frame, xpos: int, ypos: int, game_obj: object) -> object:
        super().__init__(master=frame, command=lambda j=(xpos, ypos): game_obj.button_press(j), width=3)
        self.text = 0
        self.bind('<ButtonPress-3>', lambda e: self.state(["pressed"]))
        self.grid(row=ypos,column=xpos)


class UserInterface:
    def __init__(self,root: object):
        self.gameframe = tk.Frame(root)
        self.difficulty = tk.StringVar(value = "medium")
        self.start_game()
        self.menubar_func(root)
        self.gameframe.grid()
        

    def start_game(self) -> object:
        for widget in self.gameframe.winfo_children():
            widget.destroy()
        return Game(self.gameframe, self.difficulty.get())

    def menubar_func(self, root: object):
        root.option_add('*tearOff', False)
        menubar = tk.Menu(root)
        root['menu'] = menubar
        menu_file = tk.Menu(menubar)
        menu_edit = tk.Menu(menubar)
        menubar.add_cascade(menu=menu_file, label='File')
        menubar.add_cascade(menu=menu_edit, label='Edit')
        menu_edit.add_radiobutton(label='easy', variable=self.difficulty, value="easy")
        menu_edit.add_radiobutton(label='medium', variable=self.difficulty, value="medium")
        menu_edit.add_radiobutton(label='hard', variable=self.difficulty, value="hard")
        menu_file.add_command(label='Restart', command=lambda: self.start_game())
        menu_file.add_command(label='Exit', command=lambda: root.quit())


def main():
    root = tk.Tk()
    root.title("TK Minesweeper")
    UserInterface(root)
    style = ttk.Style()

  
    style.configure("1.TButton", foreground = 'green')
    style.configure("2.TButton", foreground = "blue")
    style.configure("3.TButton", foreground = "red")

    style.map("1.TButton",foreground=[("disabled", "green")])
    style.map("2.TButton",foreground=[("disabled", "blue")])
    style.map("3.TButton",foreground=[("disabled", "red")])


    root.mainloop()


if __name__ == "__main__":
    main()
