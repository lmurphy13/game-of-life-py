#!/usr/bin/python3

import tkinter as tk
from tkinter import filedialog as fd
from tkinter import simpledialog as sd
import time

class Game:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Conway's Game of Life")
        self.window.geometry("500x600")
        self.window.maxsize(500, 600)
        #self.window.configure(bg="gray")
        self.window.configure(bg="#00559F")

        self.canvas_frame = tk.Frame(master=self.window, relief="sunken", borderwidth=5)
        self.canvas = tk.Canvas(master=self.canvas_frame, width=400, height=400)
        self.canvas.pack()

        self.menu_bar = tk.Menu(master=self.window)

        self.file_menu = tk.Menu(master=self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Import World", command=self.import_world)
        self.file_menu.add_command(label="Export World", command=self.export_world)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit)
        
        self.options_menu = tk.Menu(master=self.menu_bar, tearoff=0)
        
        
        self.bg_menu = tk.Menu(master=self.options_menu, tearoff=0)
        self.bg_menu.add_command(label="Blue")
        self.bg_menu.add_command(label="Red")
        self.bg_menu.add_command(label="Green")
        
        self.cell_menu = tk.Menu(master=self.options_menu, tearoff=0)
        self.cell_menu.add_command(label="Blue")
        self.cell_menu.add_command(label="Red")
        self.cell_menu.add_command(label="Green")
        
        
        self.options_menu.add_cascade(label="Background Color", menu=self.bg_menu)
        self.options_menu.add_cascade(label="Cell Color", menu=self.cell_menu)
        
        self.bg_menu = tk.Menu(master=self.options_menu, tearoff=0)
        self.bg_menu.add_command(label="Blue")
        self.bg_menu.add_command(label="Red")
        self.bg_menu.add_command(label="Green")
        
        

        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Options", menu=self.options_menu)

        self.grid_size = int(self.canvas.config()["width"][4])
        self.world = [[0 for i in range(0, self.grid_size, 10)] for j in range(0, self.grid_size, 10)]

        # to be used when importing from files and resetting
        self.old_world = self.world

        self.running = True

    def main(self):
        self.default_startup()

        self.draw_grid(self.canvas)
        self.draw_cells(self.canvas, self.world)

        button_frame = tk.Frame(master=self.window, relief="ridge", bg="gray", borderwidth=5)
        start_btn = tk.Button(master=button_frame, text="Start", fg="black", command=self.run, width=7)
        start_btn.grid(row=0, column=0)

        stop_btn = tk.Button(master=button_frame, text="Stop", fg="black", command=self.stop, width=7)
        stop_btn.grid(row=0, column=1)

        step_btn = tk.Button(master=button_frame, text="Step", fg="black", command=self.step, width=7)
        step_btn.grid(row=1, column=0)

        reset_btn = tk.Button(master=button_frame, text="Reset", fg="black", command=self.reset, width=7)
        reset_btn.grid(row=1, column=1)

        self.canvas_frame.pack(pady=15)
        button_frame.pack(pady=15)
        self.window.config(menu=self.menu_bar)
        
        self.canvas.bind('<Button-1>', self.click_cell)
        
        self.window.mainloop()
        
    def click_cell(self, event):
        x, y = event.x, event.y
        
        # resolve x, y to a cell
        grid_x = x // 10
        grid_y = y // 10
        
        state = self.world[grid_x][grid_y]
        if state == 0:
            self.world[grid_x][grid_y] = 1
        else:
            self.world[grid_x][grid_y] = 0
            
        self.draw_cells(self.canvas, self.world)

    def draw_grid(self, canvas):
        config = canvas.config()
        size = int(config["width"][4])

        for row in range(0, size, 10):
            canvas.create_line(0, row, size, row)

        for col in range(0, size, 10):
            canvas.create_line(col, 0, col, size)

    def draw_cells(self,canvas, world):
        size = len(world)

        x = 0
        y = 0
        for col in range(0, size):
            for row in range(0, size):
                if world[col][row] == 1:
                    canvas.create_rectangle(x, y, x+10, y+10, fill="black")
                else:
                    canvas.create_rectangle(x, y, x+10, y+10, fill="white")
                y += 10
            y = 0
            x += 10

    def calc_gen(self):
        new_world = self.make_copy(self.world)

        N = len(self.world)

        for i in range(len(self.world)):
            for j in range(len(self.world)):
                total = int(self.world[i][(j-1)%N] + self.world[i][(j+1)%N] +
                            self.world[(i-1)%N][j] + self.world[(i+1)%N][j] +
                            self.world[(i-1)%N][(j-1)%N] + self.world[(i-1)%N][(j+1)%N] +
                            self.world[(i+1)%N][(j-1)%N] + self.world[(i+1)%N][(j+1)%N])

                if self.world[i][j] == 1:
                    if ((total < 2) or (total > 3)):
                        new_world[i][j] = 0
                    elif total == 2 or total == 3:
                        new_world[i][j] = 1
                elif self.world[i][j] == 0:
                    if total == 3:
                        new_world[i][j] = 1
        self.world = new_world
        new_world = None

    def make_copy(self, lst):
       # lst_copy = [[0 for i in range(len(lst))] for j in range(len(lst))]
        lst_copy = [[0 for i in range(0, self.grid_size, 10)] for j in range(0, self.grid_size, 10)]
        for i in range(len(lst)):
            for j in range(len(lst[i])):
                lst_copy[i][j] = lst[i][j]
        return lst_copy
    
    
    def default_startup(self):
        # floater
        self.world[11][15] = 1
        self.world[12][16] = 1
        self.world[10][17] = 1
        self.world[11][17] = 1
        self.world[12][17] = 1

        # cross
        self.world[7][25] = 1
        self.world[6][26] = 1
        self.world[7][26] = 1
        self.world[8][26] = 1
        self.world[7][27] = 1

        # snowflake
        self.world[15][5] = 1
        self.world[15][6] = 1
        self.world[15][7] = 1
        self.world[15][8] = 1
        self.world[15][9] = 1

        self.world[16][5] = 1
        self.world[16][6] = 1
        self.world[16][7] = 1
        self.world[16][8] = 1
        self.world[16][9] = 1

        self.world[17][5] = 1
        self.world[17][6] = 1
        self.world[17][7] = 1
        self.world[17][8] = 1
        self.world[17][9] = 1

        self.world[18][5] = 1
        self.world[18][6] = 1
        self.world[18][7] = 1
        self.world[18][8] = 1
        self.world[18][9] = 1

        self.world[19][5] = 1
        self.world[19][6] = 1
        self.world[19][7] = 1
        self.world[19][8] = 1
        self.world[19][9] = 1

    ## Button callbacks
    
    def step(self):
        self.canvas.delete("all")
        self.draw_grid(self.canvas)
        self.calc_gen()
        self.draw_cells(self.canvas, self.world)

    def run(self):
        self.running = True
        while self.running:
            self.step()
            self.window.update()
            time.sleep(0.05)
        
    def stop(self):
        self.running = False

    def reset(self):
        self.world = [[0 for i in range(0, self.grid_size, 10)] for j in range(0, self.grid_size, 10)]

        self.draw_cells(self.canvas, self.world)

    def parse_world_from_file(self, filename):
        new_world = [[0 for i in range(0, self.grid_size, 10)] for j in range(0, self.grid_size, 10)]
        
        opening = False
        closing = False

        # Data point format is [COL,ROW,DAT]
        # columm, row, data
        with open(filename, "r") as in_file:
            for line in in_file:
                # split line into datum
                datum = line.split(",")
                # remove \n from third element
                datum[2] = datum[2][:len(datum[2])-1]
                
                col = int(datum[0])
                row = int(datum[1])
                data = int(datum[2])
                new_world[col][row] = data

        self.world = new_world
        self.canvas.delete("all")
        self.draw_grid(self.canvas)
        self.draw_cells(self.canvas, self.world)
        

    ## File menu methods
    def import_world(self):
        file_name = fd.askopenfilename()
        self.parse_world_from_file(file_name)
        

    def export_world(self):
        self.stop()
        file_name = fd.asksaveasfilename()
        
        with open(file_name, "w") as out_file:
            for i in range(len(self.world)):
                for j in range(len(self.world)):
                    out_file.write("{},{},{}\n".format(i,j,self.world[i][j]))

    def exit(self):
        self.stop()
        exit(0)     

game = Game()
game.main()
