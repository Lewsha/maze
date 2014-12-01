__author__ = 'Lewsha'

from tkinter import *
from tkinter.filedialog import *
import copy


#Класс для new_maze(), позволяющий менять цвет у конкретной кнопки,
#когда у нее нет собственного имени
class modidied_button(Frame):
    def __init__(self, dad=None):
        Frame.__init__(self, dad)
        self.li = ["black", "grey"]
        self.frame = Frame(frame_maze)
        self.x = 0
        self.y = 0
        self.frame.grid(row=0, column=0)
        self.frame.bind("<Button-1>", lambda _: self.button_click())

    def button_click(self):  # Метод для смены цвета
        self.frame.configure(bg=self.li[0])
        self.li[0], self.li[1] = self.li[1], self.li[0]


#Функция построения строкового представления лабиринта
def building_maze_txt(string):
    string = string[:string.find('end') - 1]  # Отрезаем кусок строки с лабиринтом
    tmp_maze = string.split('\n')
    maze = [x.split() for x in tmp_maze]  # Создание лабиринта
    for i in range(len(maze)):  # Перегон в int'ы
        maze[i] = [int(x) for x in maze[i]]
    return maze


#Функция построения таблицы смежности
def adjacency_table(maze):
    size = (len(maze) + 1) // 2  # Размер стороны лабиринта
    squares_count = size ** 2  # Количество клеток лабиринта
    adj_table = list()
    k = 0
    while k < squares_count:
        for i in range(0, len(maze), 2):
            for j in range(0, len((maze[i])), 2):
                adj_table.append(list())
                if k - size > 0:
                    if maze[i - 1][j] == 0:
                        adj_table[k].append(k - size)
                if k // size == (k - 1) // size:
                    if maze[i][j - 1] == 0:
                        adj_table[k].append(k - 1)
                if k // size == (k + 1) // size:
                    if maze[i][j + 1] == 0:
                        adj_table[k].append(k + 1)
                if k + size < squares_count:
                    if maze[i + 1][j] == 0:
                        adj_table[k].append(k + size)
                k += 1
    return adj_table


#Модифицированный поиск в ширину, подфункция bfs_bomb
def bfs(k, size, start, end, adj_table):
    adj = copy.deepcopy(adj_table)
    level = {start: 0}  # Уровень каждой клетки
    bomb_parent = {start: None}  # Отец каждой клетки
    ways_bomb_count = {start: k}  # Количество бомб каждой клетки
    level_num = 1  # Текущий уровень
    frontier = [start]  # Рассматриваемые на данный момент клетки
    heap = list()  # Куча для просмотренных клеток
    heap.append(start)
    while end not in heap and frontier:  # Пока не достигли конца и есть что смотреть
        next_level = []  # будущий фронт
        for u in frontier:  # Смотрим "фронтовые" клетки
            for v in adj[u]:  # Во "фронтовых" клетках смотрим детей
                ways_bomb_count[v] = ways_bomb_count[u]  # Клетка наследует бомбы от предка
                if v not in level and v not in heap:  # Если ребенок не в куче...
                    heap.append(v)  # Добавляем его в кучу
                    level[v] = level_num  # устанавлиаем уровень
                    bomb_parent[v] = u  # отмечаем предка
                    next_level.append(v)  # добавляем в будущий фронт
        for u in frontier:  # добавление клеток, которые находятся за стенками
            if (u - size > 0) and ((u - size) not in adj[u]) and (ways_bomb_count[u] > 0):
                if u - size not in heap or (ways_bomb_count[u] - 1) > ways_bomb_count[u - size]:
                    adj[u].append(u - size)
                    ways_bomb_count[u - size] = ways_bomb_count[u] - 1
                    level[u - size] = level_num
                    bomb_parent[u - size] = u
                    next_level.append(u - size)
                    heap.append(u - size)
            if ((u // size) == (u - 1) // size) and ((u - 1) not in adj[u]) and (ways_bomb_count[u] > 0):
                if u - 1 not in heap or (ways_bomb_count[u] - 1) > ways_bomb_count[u - 1]:
                    adj[u].append(u - 1)
                    ways_bomb_count[u - 1] = ways_bomb_count[u] - 1
                    level[u - 1] = level_num
                    bomb_parent[u - 1] = u
                    next_level.append(u - 1)
                    heap.append(u - 1)
            if ((u // size) == (u + 1) // size) and (u + 1 not in adj[u]) and (ways_bomb_count[u] > 0):
                if u + 1 not in heap or (ways_bomb_count[u] - 1) > ways_bomb_count[u + 1]:
                    adj[u].append(u + 1)
                    ways_bomb_count[u + 1] = ways_bomb_count[u] - 1
                    level[u + 1] = level_num
                    bomb_parent[u + 1] = u
                    next_level.append(u + 1)
                    heap.append(u + 1)
            if ((u + size) < size ** 2) and (u + size not in adj[u]) and (ways_bomb_count[u] > 0):
                if u + 10 not in heap or (ways_bomb_count[u] - 1) > ways_bomb_count[u + size]:
                    adj[u].append(u + 10)
                    ways_bomb_count[u + size] = ways_bomb_count[u] - 1
                    level[u + size] = level_num
                    bomb_parent[u + size] = u
                    next_level.append(u + size)
                    heap.append(u + size)
        frontier = next_level
        level_num += 1
    bomb_result = list()
    bomb_result.append(end)
    j = end
    if end in heap:  # Если конец в куче, создаем путь
        while start not in bomb_result:
            bomb_result.append(bomb_parent[j])
            j = bomb_parent[j]
        bomb_result.reverse()
    else:  # Иначе - отмечаем, что нет пути
        bomb_result.append('No way!')
    return bomb_result


#Функция, использующая модифицированный bfs и обрабатывающая результаты
def bfs_bomb(start, end, bomb_count, maze, adj_table):
    if start == end:
        return [None, 'The begin is the end!']
    else:
        size = (len(maze) + 1) // 2  # Размер стороны лабиринта
        bomb_result = list()  # Массив путей
        result = dict()  # Словарь путей
        for k in range(bomb_count + 1):  # Просчет кратчайшего пути для каждого количества бомб
            bomb_result.append(bfs(k, size, start, end, adj_table))
        for num in range(len(bomb_result)):  # Переводим результаты в словарь
            if bomb_result[num][1] == 'No way!':
                result[num] = 'No way!'
            else:
                result[num] = bomb_result[num]
        i = 0  # Определяем, есть ли вообще путь в лабиринте при нашем числе бомб
        for j in result:
            if result[j] == 'No way!':
                i += 1
        if i == len(result):
            return [None, 'No way for all count of bombs!']
        else:  # Если пути есть, то определяем, какой из них самый короткий, а какой - самый экономичный
            min_length = [bomb_count, maze + maze]
            min_bombs = [bomb_count, maze]
            for i in range(len(result)):
                if result[i] != 'No way!':
                    if i <= min_bombs[0]:
                        min_bombs = [i, result[i]]
                    if len(result[i]) < len(min_length[1]):
                        min_length = [i, result[i]]
            return min_length, min_bombs


#Функция для открытия и построения лабиринта из имеющегося файла лабиринта(отрисовка в painting)
def open_maze():
    root.maxsize(200, 200)
    maze_frame.grid_remove()
    frame_maze.grid_remove()
    new_maze_frame.grid_remove()
    open_maze_frame.grid_remove()
    open_maze_frame.grid()

    def f_button(event):
        if choice.get() == 1:  # Если мы хотим увидеть минимальный путь,...
            painting(result[0], txt_maze, start, end)  # отрисовываем по самому короткому пути
            label.destroy()  # Удаляем ненужные элементы
            rbutton1.destroy()
            rbutton2.destroy()
            fbutton.destroy()
            button_frame.destroy()
        elif choice.get() == 2:  # Если мы хотим увидеть экономичный путь,...
            painting(result[1], txt_maze, start, end)  # отрисовываем экономичный путь
            label.destroy()
            rbutton1.destroy()
            rbutton2.destroy()
            fbutton.destroy()
            button_frame.destroy()
        else:  # Выводим сообщение, если ничего не выбрано
            win = Toplevel(root)
            win.minsize(250, 50)
            win.maxsize(250, 50)
            win.title("Error!")
            message = Text(win)
            message.insert(1.0, "Выберите режим работы \n программы!")
            message.pack()

    op = askopenfile()  # Диалог для выбора файла
    try:
        op = op.name
        file = open(op, 'r')  # Пробуем открыть
        text = file.read()
        file.close()
        if text[-19:] == "This is a maze file":  # Если это файл лабиринта, вытаскиваем всю нужную информацию
            txt_maze = building_maze_txt(text)  # Строковок представление лабиринта
            info = text[text.find('end') + 4:].split('\n')
            bomb_count = int(info[0])  # Количество бомб
            start = int(info[1])  # Точка входа
            end = int(info[2])  # Точка выхода
            adj_table = adjacency_table(txt_maze)  # Таблица смежности
            result = bfs_bomb(start, end, bomb_count, txt_maze, adj_table)  # Результат поиска пути
            if result[0] is None:  # Если нет пути или начало равно концу
                win = Toplevel(root)
                win.title("Message")
                win.minsize(250, 100)
                win.maxsize(250, 100)
                message = Text(win)
                message.insert(1.0, result[1])
                message.pack()
            else:
                choice = IntVar()  # Флаг
                button_frame = Frame(open_maze_frame, width=200, height=500, bd=20)  # Фрейм для кнопок
                button_frame.grid(row=0, column=0)
                label = Label(button_frame, text="Выберите режим \n поиска пути")
                rbutton1 = Radiobutton(button_frame, text='Кратчайший путь', variable=choice, value=1)  # Кнопки выбора
                rbutton2 = Radiobutton(button_frame, text='Наименьший \n расход бомб', variable=choice, value=2)
                fbutton = Button(button_frame, text='Выбрать')  # Кнопка для продолжения
                fbutton.bind("<Button-1>", f_button)
                label.pack()
                rbutton1.pack()
                rbutton2.pack()
                fbutton.pack()
        else:  # Выводим сообщение, если это не файл лабиринта
            win = Toplevel(root)
            win.minsize(250, 50)
            win.maxsize(250, 50)
            win.title("Error!")
            message = Text(win)
            message.insert(1.0, "Это не файл лабиринта.\nВыберите нужный файл")
            message.pack()
    except Exception as ex:
        print(ex.args)


#Дочерняя функция building_control для построения управляемого поля лабиринта
def building_field(size):
    x = 40
    y = 10
    maze = list()
    button_maze = list()
    for i in range(size * 2 - 1):
        maze.append(list())
        button_maze.append(list())
        for j in range(size * 2 - 1):
            button_maze[i].append(modidied_button(frame_maze))
            button_maze[i][j].frame.grid(row=i, column=j)
            button_maze[i][j].x = size * i + j
            maze[i].append(0)
            button_maze[i][j].y = 0
            button_maze[i][j].frame.configure(width=x, height=x, bg='grey')
            if i % 2 == 0:
                if j % 2 == 0:
                    button_maze[i][j] = Frame(frame_maze, width=x, height=x)
                    button_maze[i][j].grid(row=i, column=j)

                else:
                    button_maze[i][j].frame.configure(width=y, height=x)
            else:
                if j % 2 == 0:
                    button_maze[i][j].frame.configure(width=x, height=y)
                else:
                    button_maze[i][j].frame.grid_remove()
                    button_maze[i][j] = Frame(frame_maze, width=y, height=y)
                    button_maze[i][j].grid(row=i, column=j)
                    button_maze[i][j].configure(bg='black')
    return maze, button_maze


#Дочерняя функци building_control для превращения построенного лабиринта в неизменяемый
def fixation(maze, button_maze, size):
    x = 40
    y = 10
    for i in range(size * 2 - 1):
        for j in range(size * 2 - 1):
            if i % 2 == 0:
                if j % 2 == 0:
                    color = button_maze[i][j]['bg']
                    button_maze[i][j] = Frame(frame_maze, width=x, height=x, bg=color)
                    button_maze[i][j].grid(row=i, column=j)
                    if color == 'black':
                        maze[i][j] = 1
                else:
                    color = button_maze[i][j].frame['bg']
                    button_maze[i][j] = Frame(frame_maze, width=y, height=x, bg=color)
                    button_maze[i][j].grid(row=i, column=j)
                    if color == 'black':
                        maze[i][j] = 1
            else:
                if j % 2 == 0:
                    color = button_maze[i][j].frame['bg']
                    button_maze[i][j] = Frame(frame_maze, width=x, height=y, bg=color)
                    button_maze[i][j].grid(row=i, column=j)
                    if color == 'black':
                        maze[i][j] = 1
                else:
                    color = button_maze[i][j]['bg']
                    button_maze[i][j] = Frame(frame_maze, width=y, height=y, bg=color)
                    button_maze[i][j].grid(row=i, column=j)
                    if color == 'black':
                        maze[i][j] = 1
    return maze


#Дочерняя функция building control для сохранения построенного лабиринта
def save_maze(maze, start, end, bomb_count):
    save = asksaveasfile()  # Диалог для выбора имени и распложения
    try:
        save = save.name
        file = open(save, 'w')  # Непосредственно запись
        for i in range(len(maze)):
            for j in range(len(maze[i])):
                file.write(str(maze[i][j]))
                if j < len(maze[i]) - 1:
                    file.write(' ')
            file.write('\n')
        file.write('end' + '\n')
        file.write(str(bomb_count) + '\n')
        file.write(str(start) + '\n')
        file.write(str(end) + '\n')
        file.write('This is a maze file')
    except Exception as ex:
        print(ex.args)


#Дочерняя функция new_maze, которая выводит большую часть кода в отдельные функции
def building_control(size):
    def click(event):
        def paint(event):
            def final(event):
                save_maze(maze, start, end, bomb_count)
                button_save.destroy()
            if mode.get() < 5:
                lab7.destroy()
                rbutton1.destroy()
                rbutton2.destroy()
                for i in range(1, len(result[mode.get()][1]) - 1):
                    button_maze[result[mode.get()][1][i] // size * 2][result[mode.get()][1][i] % size * 2].\
                        configure(bg="yellow")
                button_save = Button(new_maze_frame, text='Сохранить')
                button_save.grid(row=5, column=1)
                button_save.bind("<1>", final)
            button_show.destroy()
        start = scale1_x.get() + scale1_y.get() * size
        end = scale2_x.get() + scale2_y.get() * size
        button_maze[scale1_y.get() * 2][scale1_x.get() * 2].configure(bg='red')
        button_maze[scale2_y.get() * 2][scale2_x.get() * 2].configure(bg='green')
        bomb_count = scale_bomb.get()
        button_create.destroy()
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
        fix_maze = fixation(maze, button_maze, size)
        adj_table = adjacency_table(fix_maze)
        result = bfs_bomb(start, end, bomb_count, fix_maze, adj_table)
        if result[0] is None:
            window = Toplevel(root)
            window.title("Message")
            window.minsize(250, 100)
            window.maxsize(250, 100)
            message = Text(window)
            message.insert(1.0, result[0])
            message.pack()
        else:
            lab7 = Label(new_maze_frame, text='Выберите режим работы')
            lab7.grid(row=1, column=0, columnspan=2)
            mode = IntVar()
            mode.set(5)
            rbutton1 = Radiobutton(new_maze_frame, text='Кратчайший путь', variable=mode, value=0)
            rbutton2 = Radiobutton(new_maze_frame, text='Наименьший \n расход бомб', variable=mode, value=1)
            rbutton1.grid(row=2, column=0)
            rbutton2.grid(row=2, column=1)
            button_show = Button(new_maze_frame, text="Показать")
            button_show.grid(row=3, column=0, columnspan=3)
            button_show.bind("<1>", paint)

    if size > 0:
        lab2 = Label(new_maze_frame, text="Выберите начальную позицию")
        lab3 = Label(new_maze_frame, text="Выберите конечную позицию")
        lab2.grid(row=0, column=0)
        lab3.grid(row=0, column=2)
        lab4 = Label(new_maze_frame, text='x')
        lab5 = Label(new_maze_frame, text='y')
        lab4.grid(row=1, column=1)
        lab5.grid(row=2, column=1)
        scale1_x = Scale(new_maze_frame, orient=HORIZONTAL, length=200, from_=0, to=size - 1, tickinterval=1, resolution=1)
        scale1_x.grid(row=1, column=0)
        scale1_y = Scale(new_maze_frame, orient=HORIZONTAL, length=200, from_=0, to=size - 1, tickinterval=1, resolution=1)
        scale1_y.grid(row=2, column=0)
        scale2_x = Scale(new_maze_frame, orient=HORIZONTAL, length=200, from_=0, to=size - 1, tickinterval=1, resolution=1)
        scale2_x.grid(row=1, column=2)
        scale2_y = Scale(new_maze_frame, orient=HORIZONTAL, length=200, from_=0, to=size - 1, tickinterval=1, resolution=1)
        scale2_y.grid(row=2, column=2)
        lab6 = Label(new_maze_frame, text='Количество бомб')
        lab6.grid(row=3, column=0)
        scale_bomb = Scale(new_maze_frame, orient=HORIZONTAL, length=200, from_=0, to=10, tickinterval=1, resolution=1)
        scale_bomb.grid(row=3, column=2)
        frame_maze.grid(row=4, column=0, columnspan=3)

        maze = building_field(size)[0]
        button_maze = building_field(size)[1]
        button_create = Button(new_maze_frame, text='Создать')
        button_create.grid(row=5, column=0, columnspan=3)
        button_create.bind("<1>", click)
    else:
        win = Toplevel(root)
        win.minsize(250, 50)
        win.maxsize(250, 50)
        win.title("Error!")
        message = Text(win)
        message.insert(1.0, "Выберите \n значение!")
        message.pack()


#Функция для создания нового лабиринта
def new_maze():
    root.maxsize(1000, 1000)
    maze_frame.grid_remove()
    frame_maze.grid_remove()
    new_maze_frame.grid_remove()
    open_maze_frame.grid_remove()
    new_maze_frame.grid()

    def choice(event):
        building_control(scale.get())
        lab1.destroy()
        button_choice.destroy()
        scale.destroy()
    lab1 = Label(new_maze_frame, text="Выберите размер стороны лабиринта")
    lab1.grid(row=0, column=0, columnspan=2)
    scale = Scale(new_maze_frame, orient=HORIZONTAL, length=400, from_=0, to=10, tickinterval=1, resolution=1)
    scale.grid(row=1, column=0, columnspan=2)
    button_choice = Button(new_maze_frame, text='Создать')
    button_choice.grid(row=4, column=0, columnspan=2)
    button_choice.bind("<Button-1>", choice)


#Вывод помощи
def print_help():
    win = Toplevel(root)  # Создание допокна
    win.title("Help")  # Его заголовок
    try:
        file = open("readme.txt", 'r')  # Файл помощи
        text = file.read()
        lab = Text(win)
        lab.insert(1.0, text)
        lab.pack()
    except Exception as ex:
        print(ex.args)


#Вывод инфы
def about():
    win = Toplevel(root)  # Создание допокна
    win.title("About")  # Заголовок
    win.minsize(250, 100)  # Фиксированный размер
    win.maxsize(250, 100)
    try:
        file = open("about.txt", 'r')  # Файл с инфой
        text = file.read()
        lab = Text(win)
        lab.insert(1.0, text)
        lab.pack()
    except Exception as ex:
        print(ex.args)


#Выход...
def exit():
    root.destroy()


#Функция для отрисовки лабиринта, полученного из open_maze
def painting(result, maze, start, end):
    frame_maze.grid_remove()
    maze_frame.grid(row=0, column=0)  # Пакуем
    frame_list = list()  # Лист для лабиринта

    if len(maze) < 40:  # Выбираем размер клеток
        x = 50
        y = 5
    else:
        x = 25
        y = 2

    for i in range(len(maze)):  # Создаем отрисовку
        frame_list.append(list())
        for j in range(len(maze)):
            if i % 2 == 0:  # Если строка клеток
                if j % 2 == 0:  # Если клетка
                    frame_list[i].append(Frame(maze_frame, width=x, height=x))
                    frame_list[i][j].grid(row=i, column=j)
                else:  # Если стенка
                    frame_list[i].append(Frame(maze_frame, width=y, height=x))
                    frame_list[i][j].grid(row=i, column=j)
            else:  # Если строка стенок
                if j % 2 == 0:  # Если стенка
                    frame_list[i].append(Frame(maze_frame, width=x, height=y))
                    frame_list[i][j].grid(row=i, column=j)
                else:  # Если "столбик"
                    frame_list[i].append(Frame(maze_frame, width=y, height=y))
                    frame_list[i][j].grid(row=i, column=j)

    size = (len(maze) + 1) // 2  # Размер стороны лабиринта
    squares_count = size ** 2  # Количество клеток
    k = 0  # Счетчик отрисованных клеток
    for i in range(0, len(maze), 2):
        for j in range(0, len(maze[i]), 2):
            if i != len(maze) - 1 and j != len(maze[i]) - 1:
                frame_list[i + 1][j + 1].configure(bg='black')  # "Красим" "столбики"
            if k - size > 0:
                if maze[i - 1][j] == 1:
                    frame_list[i - 1][j].configure(bg='black')  # "Красим" стенку выше клетки
            if (k // size) == (k - 1) // size:
                if maze[i][j - 1] == 1:
                    frame_list[i][j - 1].configure(bg='black')  # "Красим" стенку слева от клетки
            if (k // size) == (k + 1) // size:
                if maze[i][j + 1] == 1:
                    frame_list[i][j + 1].configure(bg='black')  # "Красим" стенку справа от клетки
            if (k + size) < squares_count:
                if maze[i + 1][j] == 1:
                    frame_list[i + 1][j].configure(bg='black')  # "Красим" стенку выше клетки
            k += 1
    for i in result[1]:
        frame_list[i // size * 2][i % size * 2].configure(bg='yellow')  # Раскрашиваем путь
    frame_list[start // size * 2][start % size * 2].configure(bg='red')  # Обозначаем начало
    frame_list[end // size * 2][end % size * 2].configure(bg='green')  # Обозначаем конец
    root.maxsize(size * x + (size - 1) * y, size * x + (size - 1) * y)  # Закрепляем размер окна


root = Tk()  # Главное окно
root.title("Maze")  # Заголовок окна
root.minsize(100, 100)  # Минимально допустимый размер

menu = Menu(root)  # создается объект Меню на главном окне
root.config(menu=menu)  # окно конфигурируется с указанием меню для него
fm = Menu(menu)  # создается пункт меню с размещением на основном меню (m)
menu.add_cascade(label="File", menu=fm)  # пункту располагается на основном меню (m)
fm.add_command(label="Open maze", command=open_maze)  # формируется список команд пункта меню
fm.add_command(label="New maze", command=new_maze)
fm.add_command(label="Exit", command=exit)
hm = Menu(menu)  # второй пункт меню
menu.add_cascade(label="Help", menu=hm)
hm.add_command(label="Help", command=print_help)
hm.add_command(label="About", command=about)


new_maze_frame = Frame(root)  # Фреймы для отрисовки элементов
open_maze_frame = Frame(root)
maze_frame = Frame(open_maze_frame,  width=200, height=200)  # Фрейм для отрисовки из файла
frame_maze = Frame(new_maze_frame,  width=200, height=200)  # Фрейм для рисования

root.mainloop()
