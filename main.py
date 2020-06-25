import numpy as np
import PySimpleGUI as sg
import tkinter
import random
BOX_SIZE = 15
class GameOfLife:
    def __init__(self, Cells=35):
        self.Cells = Cells
        self.old_grid = np.zeros(Cells * Cells, dtype='i').reshape(Cells, Cells)
        self.new_grid = np.zeros(Cells * Cells, dtype='i').reshape(Cells, Cells)
        self.color = 'white'
    
        for i in range(0, self.Cells):
            for j in range(0, self.Cells):
                self.old_grid[i][j] = 0
        self.init_graphics()
        self.manual_board_setup()

    def live_neighbours(self, i , j):
        s = 0
        for x in [i - 1, i, i + 1]:
            for y in [j - 1, j, j + 1]:
                if (x == i and y == j):
                    continue
                if (x != self.Cells and y != self.Cells):
                    s += self.old_grid[x][y]
                elif (x == self.Cells and y != self.Cells):
                    s += self.old_grid[0][y]
                elif (x != self.Cells and y == self.Cells):
                    s += self.old_grid[x][0]
                else:
                    s += self.old_grid[0][0]
        return s

    def play(self):
        self.generation = 1
        while self.generation:
            for i in range(self.Cells):
                for j in range(self.Cells):
                    live = self.live_neighbours(i, j)
                    if (self.old_grid[i][j] == 1 and live < 2):
                        self.new_grid[i][j] = 0
                    elif (self.old_grid[i][j] == 1 and (live == 2 or live ==3)):
                        self.new_grid[i][j] = 1
                    elif (self.old_grid[i][j] == 1 and live > 3):
                        self.new_grid[i][j] = 0
                    elif (self.old_grid[i][j] == 0 and live == 3):
                        self.new_grid[i][j] = 1
    
            self.old_grid = self.new_grid.copy()
            self.draw_board()
            self.generation +=1
            

    def init_graphics(self):
        self.graph = sg.Graph((600, 600), (0, 0), (450, 450),
            key='-GRAPH-', change_submits=True, drag_submits=False, background_color='black')

        layout = [
            [sg.Text('Game of Life', font='Any 15'),
            sg.Text('Click below to place cells', key='-GEN-', size=(30, 1), font='ANY 15')],
            [self.graph],
            [sg.Button('Start', key='-TOGGLE-'),
            sg.Button('Clear', key='-CLEAR-'),
            sg.Button('Random', key='-RANDOM-'),
            sg.Combo(['blue','red'], key='-COLOR-', default_value='white'),
            sg.Text(' Delay (ms)'),
            sg.Slider((0,800), 100,orientation='h',key='-SLIDER-', enable_events=True, size=(15, 15)),
            sg.Text('',size=(3,1), key='-SPEED-'),
            sg.Button('About',key='-ABOUT-'),
            sg.Button('Exit', key='-EXIT-')]     
        ]

        self.window = sg.Window('John Conways Game of Life', layout, finalize=True)
        event, values = self.window.read(timeout=0)
        self.delay = values['-SLIDER-']
        self.window['-SPEED-'].update(values['-SLIDER-'])

    def draw_board(self):
        BOX_SIZE = 15
        self.graph.erase()
        for i in range(self.Cells):
            for j in range(self.Cells):
                if self.old_grid[i][j]:
                    self.graph.draw_rectangle((i * BOX_SIZE, j * BOX_SIZE),(i * BOX_SIZE + BOX_SIZE, j * (BOX_SIZE) + BOX_SIZE),line_color='grey',fill_color=self.color)
        event, values =  self.window.read(timeout=self.delay)
        if event == '-ABOUT-':
            sg.popup('Any live cell with two or three live neighbours survives. Any dead cell with three live neighbours becomes a live cell. All other live cells die in the next generation. Similarly, all other dead cells stay dead.',title='Rules')
        if event in (None, '-EXIT-'):
            self.window.close()
            exit()
        if event in (None, '-TOGGLE-'):
            self.window['-TOGGLE-'].update(text='Start')
            self.manual_board_setup()
        self.delay = values['-SLIDER-']
        self.window['-SPEED-'].update(values['-SLIDER-'])
        self.window['-GEN-'].update('Generation {}'.format(self.generation))

    def manual_board_setup(self):
        ids = []
        for i in range(self.Cells):
            ids.append([])
            for j in range(self.Cells):
                ids[i].append(0)
        while True:
            event, values = self.window.read()
            self.color = values['-COLOR-']
            if event is None or event == '-TOGGLE-' or event == '-EXIT-':
                break
            if event == '-ABOUT-':
                sg.popup('Any live cell with two or three live neighbours survives. Any dead cell with three live neighbours becomes a live cell. All other live cells die in the next generation. Similarly, all other dead cells stay dead.',title='Rules')
            
            self.window['-SPEED-'].update(values['-SLIDER-'])
            mouse = values['-GRAPH-']
            if event == '-CLEAR-':
                self.graph.erase()
            if event == '-RANDOM-':
                self.graph.erase()
                for i in range(self.Cells):
                    for j in range(self.Cells):
                        self.old_grid[i][j] = random.randint(0,1)
                        if self.old_grid[i][j] == 1:
                            self.graph.draw_rectangle((i * BOX_SIZE, j * BOX_SIZE),(i * BOX_SIZE + BOX_SIZE, j * (BOX_SIZE) + BOX_SIZE),line_color='grey',fill_color=self.color)
            if event == '-GRAPH-':
                if mouse == (None, None):
                    continue
                box_x = mouse[0] // BOX_SIZE
                box_y = mouse[1] // BOX_SIZE
                if self.old_grid[box_x][box_y] == 1:
                    id_val = ids[box_x][box_y]
                    self.graph.delete_figure(id_val)
                    self.old_grid[box_x][box_y] = 0
                else:
                    id_val = self.graph.draw_rectangle((box_x * BOX_SIZE, box_y * BOX_SIZE),(box_x * BOX_SIZE + BOX_SIZE, box_y * (BOX_SIZE) + BOX_SIZE),line_color='grey',fill_color=self.color)
                    ids[box_x][box_y] = id_val
                    self.old_grid[box_x][box_y] = 1

        if event is None or event == '-EXIT-':
            self.window.close()
        else:
            self.window['-TOGGLE-'].update(text='Stop')


game = GameOfLife(Cells=35)
game.play()
game.window.close()