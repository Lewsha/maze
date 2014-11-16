__author__ = 'Lewsha'

from tkinter import *
from tkinter.filedialog import *
import codecs
import copy


class modidied_button(Frame):  # Класс для new_maze(), позволяющий менять цвет у конкретной кнопки,
                                # когда у нее нет собственного имени
    def __init__(self, dad=None):
        Frame.__init__(self, dad)
        self.li = ["black", "grey"]
        self.frame = Frame(maze_frame)
        self.x = 0
        self.y = 0
        self.frame.grid(row=0, column=0)
        self.frame.bind("<Button-1>", lambda _: self.button_click())

    def button_click(self):
        self.frame.configure(bg=self.li[0])
        self.li[0], self.li[1] = self.li[1], self.li[0]


def building_maze_txt(string):  # Функция построения строкового представления лабиринта
    string = string[:string.find('end') - 1]
    tmp_maze = string.split('\n')
    maze = list()
    for i in range(0, len(tmp_maze)):
        maze.append(list())
        maze[i] = tmp_maze[i].split()
    for i in range(0, len(maze)):
        for j in range(0, len(maze[i])):
            maze[i][j] = int(maze[i][j])
    return maze


def adjacency_table(maze):  # Функция построения таблицы смежности
    squares_count = ((len(maze) + 1) // 2) ** 2
    a = (len(maze) + 1) // 2
    adj_table = list()
    k = 0
    while k < squares_count:
        for i in range(0, len(maze), 2):
            for j in range(0, len((maze[i])), 2):
                adj_table.append(list())
                if k - a > 0:
                    if maze[i - 1][j] == 0:
                        adj_table[k].append(k - a)
                if (k // a) == (k - 1) // a:
                    if maze[i][j - 1] == 0:
                        adj_table[k].append(k - 1)
                if (k // a) == (k + 1) // a:
                    if maze[i][j + 1] == 0:
                        adj_table[k].append(k + 1)
                if (k + a) < squares_count:
                    if maze[i + 1][j] == 0:
                        adj_table[k].append(k + a)
                k += 1
    return adj_table


def bfs_bomb(start, end, bomb_count, maze, adj_table):  # modified bfs
                                                        # algorithm enumerates all possible ways using bombs
    if start[0] == end[0]:
        return 'The begin is the end!'
    else:
        a = (len(maze) + 1) // 2
        bomb_result = list()
        result = dict()
        for k in range(0, bomb_count + 1):
            bombs = k
            adj = copy.deepcopy(adj_table)
            level = {start[0]: 0}
            bomb_parent = {start[0]: None}
            ways_bomb_count = {start[0]: bombs}
            i = 1
            frontier = [start[0]]
            heap = list()
            heap.append(start[0])
            while end[0] not in heap and frontier and bombs >= 0:
                next = []
                for u in frontier:
                    for v in adj[u]:
                        ways_bomb_count[v] = ways_bomb_count[u]
                    for v in adj[u]:
                        if v not in level and v not in heap:
                            heap.append(v)
                            level[v] = i
                            bomb_parent[v] = u
                            next.append(v)
                for u in frontier:
                    if (u - a > 0) and ((u - a) not in adj[u]) and (ways_bomb_count[u] > 0):
                        if u - a not in heap or (ways_bomb_count[u] - 1) > ways_bomb_count[u - a]:
                            adj[u].append(u - a)
                            ways_bomb_count[u - a] = ways_bomb_count[u] - 1
                            level[u - a] = i
                            bomb_parent[u - a] = u
                            next.append(u - a)
                            heap.append(u - a)
                    if ((u // a) == (u - 1) // a) and ((u - 1) not in adj[u]) and (ways_bomb_count[u] > 0):
                        if u - 1 not in heap or (ways_bomb_count[u] - 1) > ways_bomb_count[u - 1]:
                            adj[u].append(u - 1)
                            ways_bomb_count[u - 1] = ways_bomb_count[u] - 1
                            level[u - 1] = i
                            bomb_parent[u - 1] = u
                            next.append(u - 1)
                            heap.append(u - 1)
                    if ((u // a) == (u + 1) // a) and (u + 1 not in adj[u]) and (ways_bomb_count[u] > 0):
                        if u + 1 not in heap or (ways_bomb_count[u] - 1) > ways_bomb_count[u + 1]:
                            adj[u].append(u + 1)
                            ways_bomb_count[u + 1] = ways_bomb_count[u] - 1
                            level[u + 1] = i
                            bomb_parent[u + 1] = u
                            next.append(u + 1)
                            heap.append(u + 1)
                    if ((u + a) < a ** 2) and (u + a not in adj[u]) and (ways_bomb_count[u] > 0):
                        if u + 10 not in heap or (ways_bomb_count[u] - 1) > ways_bomb_count[u + a]:
                            adj[u].append(u + 10)
                            ways_bomb_count[u + a] = ways_bomb_count[u] - 1
                            level[u + a] = i
                            bomb_parent[u + a] = u
                            next.append(u + a)
                            heap.append(u + a)
                frontier = next
                i += 1
            bomb_result.append(list())
            bomb_result[k].append(end[0])
            j = end[0]
            if end[0] in heap:
                while start[0] not in bomb_result[k]:
                    bomb_result[k].append(bomb_parent[j])
                    j = bomb_parent[j]
                bomb_result[k].reverse()
            else:
                bomb_result[k].append('No way!')
        for num in range(0, len(bomb_result)):
            if bomb_result[num][1] == 'No way!':
                result[num] = 'No way!'
            else:
                result[num] = bomb_result[num]
        if type(result) is str:
            print(result)
        else:
            i = 0
            for j in result:
                if result[j] == 'No way!':
                    i += 1
            if i == len(result):
                return 'No way for all count of bombs!'
            else:
                min_length = [bomb_count, maze + maze]
                min_bombs = [bomb_count, maze]
                for i in range(0, len(result)):
                    if result[i] != 'No way!':
                        if i <= min_bombs[0]:
                            min_bombs = [i, result[i]]
                        if len(result[i]) < len(min_length[1]):
                            min_length = [i, result[i]]
                return min_length, min_bombs


def help():
    win = Toplevel(root)
    win.title("Help")
    try:
        file = codecs.open("readme.txt", 'r', "utf_8_sig")
        text = file.read()
        lab = Text(win)
        lab.insert(1.0, text)
        lab.pack()
    except Exception:
        print()


def about():
    win = Toplevel(root)
    win.title("Help")
    win.minsize(200, 100)
    win.maxsize(200, 100)
    try:
        file = codecs.open("about.txt", 'r', "utf_8_sig")
        text = file.read()
        lab = Text(win)
        lab.insert(1.0, text)
        lab.pack()
    except Exception:
        print()


def open_maze():  #Функция для открытия и построения лабиринта из имеющегося файла лабиринта(отрисовка в painting)
    root.maxsize(200, 200)
    button_frame.grid_remove()
    maze_frame.grid_remove()

    def f_button(event):
        if choice.get() == 1:
            painting(result[0], txt_maze, start, end)
            label.destroy()
            rbutton1.destroy()
            rbutton2.destroy()
            fbutton.destroy()
            button_frame.grid_remove()
        elif choice.get() == 2:
            painting(result[1], txt_maze, start, end)
            label.destroy()
            rbutton1.destroy()
            rbutton2.destroy()
            fbutton.destroy()
            button_frame.grid_remove()
        else:
            win = Toplevel(root)
            win.minsize(250, 50)
            win.maxsize(250, 50)
            win.title("Error!")
            message = Text(win)
            message.insert(1.0, "Выберите режим работы \n программы!")
            message.pack()

    op = askopenfile()
    try:
        op = op.name
        file = open(op, 'r')
        text = file.read()
        file.close()
        if text[-19:] == "This is a maze file":
            txt_maze = building_maze_txt(text)
            info = text[text.find('end') + 4:].split('\n')
            bomb_count = int(info[0])
            start = info[1].split()
            end = info[2].split()
            for i in range(0, len(start)):
                start[i] = int(start[i])
                end[i] = int(end[i])
            adj_table = adjacency_table(txt_maze)
            result = bfs_bomb(start, end, bomb_count, txt_maze, adj_table)
            if type(result) is str:
                win = Toplevel(root)
                win.title("Message")
                win.minsize(250, 100)
                win.maxsize(250, 100)
                message = Text(win)
                message.insert(1.0, result)
                message.pack()
                print(result)
            else:
                choice = IntVar()
                button_frame.grid(row=0, column=0)
                label = Label(button_frame, text="Выберите режим \n поиска пути")
                rbutton1 = Radiobutton(button_frame, text='Кратчайший путь', variable=choice, value=1)
                rbutton2 = Radiobutton(button_frame, text='Наименьший \n расход бомб', variable=choice, value=2)
                fbutton = Button(button_frame, text='Выбрать')
                fbutton.bind("<Button-1>", f_button)
                label.pack()
                rbutton1.pack()
                rbutton2.pack()
                fbutton.pack()
        else:
            win = Toplevel(root)
            win.minsize(250, 50)
            win.maxsize(250, 50)
            win.title("Error!")
            message = Text(win)
            message.insert(1.0, "Это не файл лабиринта.\nВыберите нужный файл")
            message.pack()
    except Exception as ex:
        print(ex.args)


def new_maze():  # Функция для создания нового лабиринта
    def choice(event):
        def click(event):
            def final(event):
                if mode.get() < 5:
                    lab7.destroy()
                    rbutton1.destroy()
                    rbutton2.destroy()
                    for i in range(1, len(result[mode.get()][1]) - 1):
                        button_maze[result[mode.get()][1][i] // size * 2][result[mode.get()][1][i] % size * 2].\
                            configure(bg="yellow")
            start = [scale1_x.get() + scale1_y.get() * size]
            end = [scale2_x.get() + scale2_y.get() * size]
            print(scale1_x.get(), scale1_y.get(), scale2_x.get(), scale2_y.get())
            button_maze[scale1_y.get() * 2][scale1_x.get() * 2].configure(bg='red')
            button_maze[scale2_y.get() * 2][scale2_x.get() * 2].configure(bg='green')
            bomb_count = scale_bomb.get()
            button_creat.destroy()
            lab2.destroy()
            lab3.destroy()
            lab4.destroy()
            lab5.destroy()
            scale1_x.destroy()
            scale1_y.destroy()
            scale2_x.destroy()
            scale2_y.destroy()
            scale_bomb.destroy()
            lab6.destroy()
            button_save = Button(root, text='Сохранить')
            button_save.grid(row=5, column=1)
            for i in range(0, size * 2 - 1):
                for j in range(0, size * 2 - 1):
                    if i % 2 == 0:
                        if j % 2 == 0:
                            color = button_maze[i][j]['bg']
                            button_maze[i][j] = Frame(maze_frame, width=x, height=x, bg=color)
                            button_maze[i][j].grid(row=i, column=j)
                            if color == 'black':
                                maze[i][j] = 1
                        else:
                            color = button_maze[i][j].frame['bg']
                            button_maze[i][j] = Frame(maze_frame, width=y, height=x, bg=color)
                            button_maze[i][j].grid(row=i, column=j)
                            if color == 'black':
                                maze[i][j] = 1
                    else:
                        if j % 2 == 0:
                            color = button_maze[i][j].frame['bg']
                            button_maze[i][j] = Frame(maze_frame, width=x, height=y, bg=color)
                            button_maze[i][j].grid(row=i, column=j)
                            if color == 'black':
                                maze[i][j] = 1
                        else:
                            color = button_maze[i][j]['bg']
                            button_maze[i][j] = Frame(maze_frame, width=y, height=y, bg=color)
                            button_maze[i][j].grid(row=i, column=j)
                            if color == 'black':
                                maze[i][j] = 1
            adj_table = adjacency_table(maze)
            result = bfs_bomb(start, end, bomb_count, maze, adj_table)
            lab7 = Label(root, text='Выберите режим работы')
            lab7.grid(row=1, column=0, columnspan=2)
            mode = IntVar()
            mode.set(5)
            rbutton1 = Radiobutton(root, text='Кратчайший путь', variable=mode, value=0)
            rbutton2 = Radiobutton(root, text='Наименьший \n расход бомб', variable=mode, value=1)
            rbutton1.grid(row=2, column=0)
            rbutton2.grid(row=2, column=1)
            button_show = Button(root, text="Показать")
            button_show.grid(row=3, column=0, columnspan=2)
            button_show.bind("<1>", final)

        if scale.get() > 0:
            size = scale.get()
            lab1.destroy()
            button_choise.destroy()
            scale.destroy()
            lab2 = Label(root, text="Выберите начальную позицию")
            lab3 = Label(root, text="Выберите конечную позицию")
            lab2.grid(row=0, column=0)
            lab3.grid(row=0, column=2)
            lab4 = Label(root, text='x')
            lab5 = Label(root, text='y')
            lab4.grid(row=1, column=1)
            lab5.grid(row=2, column=1)
            scale1_x = Scale(root, orient=HORIZONTAL, length=200, from_=0, to=size - 1, tickinterval=1, resolution=1)
            scale1_x.grid(row=1, column=0)
            scale1_y = Scale(root, orient=HORIZONTAL, length=200, from_=0, to=size - 1, tickinterval=1, resolution=1)
            scale1_y.grid(row=2, column=0)
            scale2_x = Scale(root, orient=HORIZONTAL, length=200, from_=0, to=size - 1, tickinterval=1, resolution=1)
            scale2_x.grid(row=1, column=2)
            scale2_y = Scale(root, orient=HORIZONTAL, length=200, from_=0, to=size - 1, tickinterval=1, resolution=1)
            scale2_y.grid(row=2, column=2)
            lab6 = Label(root, text='Количество бомб')
            lab6.grid(row=3, column=0)
            scale_bomb = Scale(root, orient=HORIZONTAL, length=200, from_=0, to=10, tickinterval=1, resolution=1)
            scale_bomb.grid(row=3, column=2)
            maze_frame.grid(row=4, column=0, columnspan=3)
            maze = list()
            button_maze = list()
            x = 0
            y = 0
            if size < 11:
                x = 50
                y = 10
            else:
                x = 30
                y = 10

            for i in range(0, size * 2 - 1):
                maze.append(list())
                button_maze.append(list())
                for j in range(0, size * 2 - 1):
                    button_maze[i].append(modidied_button(maze_frame))
                    button_maze[i][j].frame.grid(row=i, column=j)
                    button_maze[i][j].x = size * i + j
                    maze[i].append(0)
                    button_maze[i][j].y = 0
                    button_maze[i][j].frame.configure(width=x, height=x, bg='grey')
                    if i % 2 == 0:
                        if j % 2 == 0:
                            button_maze[i][j] = Frame(maze_frame, width=x, height=x)
                            button_maze[i][j].grid(row=i, column=j)

                        else:
                            button_maze[i][j].frame.configure(width=y, height=x)
                    else:
                        if j % 2 == 0:
                            button_maze[i][j].frame.configure(width=x, height=y)
                        else:
                            button_maze[i][j].frame.grid_remove()
                            button_maze[i][j] = Frame(maze_frame, width=y, height=y)
                            button_maze[i][j].grid(row=i, column=j)
                            button_maze[i][j].configure(bg='black')
            button_creat = Button(root, text='Создать')
            button_creat.grid(row=5, column=0, columnspan=3)
            button_creat.bind("<1>", click)

        else:
            win = Toplevel(root)
            win.minsize(250, 50)
            win.maxsize(250, 50)
            win.title("Error!")
            message = Text(win)
            message.insert(1.0, "Выберите \n значение!")
            message.pack()
    maze_frame.grid_remove()
    lab1 = Label(root, text="Выберите размер стороны лабиринта")
    lab1.grid(row=0, column=0, columnspan=2)
    scale = Scale(root, orient=HORIZONTAL, length=400, from_=0, to=10, tickinterval=1, resolution=1)
    scale.grid(row=1, column=0, columnspan=2)
    button_choise = Button(root, text='Создать')
    button_choise.grid(row=4, column=0, columnspan=2)
    button_choise.bind("<Button-1>", choice)
    size = IntVar()


def save_maze():
    win = Toplevel(root)
    win.title("Сохранить текущий лабиринт")
    lab = Label(win, text="Test")
    lab.pack()


def exit():
    root.destroy()


def painting(result, maze, start, end):  # Функция для отрисовки лабиринта, полученного из open_maze
    maze_frame.grid_remove()
    maze_frame.grid()
    frame_list = list()
    x = 0
    y = 0
    if len(maze) < 40:
        x = 50
        y = 5
    else:
        x = 25
        y = 2
    for i in range(0, len(maze)):
        frame_list.append(list())
        for j in range(0, len(maze)):
            if i % 2 == 0:
                if j % 2 == 0:
                    frame_list[i].append(Frame(maze_frame, width=x, height=x))
                    frame_list[i][j].grid(row=i, column=j)
                else:
                    frame_list[i].append(Frame(maze_frame, width=y, height=x))
                    frame_list[i][j].grid(row=i, column=j)
            else:
                if j % 2 == 0:
                    frame_list[i].append(Frame(maze_frame, width=x, height=y))
                    frame_list[i][j].grid(row=i, column=j)
                else:
                    frame_list[i].append(Frame(maze_frame, width=y, height=y))
                    frame_list[i][j].grid(row=i, column=j)

    squares_count = ((len(maze) + 1) // 2) ** 2
    a = (len(maze) + 1) // 2
    k = 0
    for i in range(0, len(maze), 2):
        for j in range(0, len(maze[i]), 2):
            if i != len(maze) - 1 and j != len(maze[i]) - 1:
                frame_list[i + 1][j + 1].configure(bg='black')
            if k - a > 0:
                if maze[i - 1][j] == 1:
                    frame_list[i - 1][j].configure(bg='black')
            if (k // a) == (k - 1) // a:
                if maze[i][j - 1] == 1:
                    frame_list[i][j - 1].configure(bg='black')
            if (k // a) == (k + 1) // a:
                if maze[i][j + 1] == 1:
                    frame_list[i][j + 1].configure(bg='black')
            if (k + a) < squares_count:
                if maze[i + 1][j] == 1:
                    frame_list[i + 1][j].configure(bg='black')
            k += 1
    for i in result[1]:
        frame_list[i // a * 2][i % a * 2].configure(bg='yellow')
    frame_list[start[2] * 2][start[1] * 2].configure(bg='red')
    frame_list[end[2] * 2][end[1] * 2].configure(bg='green')
    root.maxsize(a * x + (a - 1) * y, a * x + (a - 1) * y)


root = Tk()  # Главное окно
root.title("Maze")
root.minsize(100, 100)

menu = Menu(root)  # создается объект Меню на главном окне
root.config(menu=menu)  # окно конфигурируется с указанием меню для него
fm = Menu(menu)  # создается пункт меню с размещением на основном меню (m)
menu.add_cascade(label="File", menu=fm)  # пункту располагается на основном меню (m)
fm.add_command(label="Open maze", command=open_maze)  # формируется список команд пункта меню
fm.add_command(label="New maze", command=new_maze)
fm.add_command(label="Save current maze", command=save_maze)
fm.add_command(label="Exit", command=exit)
hm = Menu(menu)  # второй пункт меню
menu.add_cascade(label="Help", menu=hm)
hm.add_command(label="Help", command=help)
hm.add_command(label="About", command=about)


maze_frame = Frame(root,  width=200, height=200)
maze_frame.grid(row=2, column=0, columnspan=2)
button_frame = Frame(root, width=200, height=500, bd=20)

root.mainloop()
