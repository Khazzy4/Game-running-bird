from email.mime import image
from tracemalloc import start
from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '400')


from binhex import LINELEN
from calendar import c
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line  
from kivy.properties import Clock
from numpy import Infinity, spacing
from kivy.graphics.vertex_instructions import Quad
from kivy.graphics.vertex_instructions import Triangle 
from kivy.uix.relativelayout import RelativeLayout
import random
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.core.audio import SoundLoader
from tkinter import *

Builder.load_file("menu.kv")


class MainWidget(RelativeLayout):
    
    menu_widget = ObjectProperty()
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    V_NB_LINES = 6      
    V_LINES_SPACING = .14
    vertical_lines = []

    H_NB_LINES = 44
    H_LINES_SPACING = .24
    horizontal_lines = []
    
    SPEED = 1.8
    current_offset_y = 0
    current_y_loop = 0

    SPEED_X = 1.1
    current_speed_x = 0
    current_offset_x = 0

    NB_TILES = 11       
    tiles = []
    tiles_coordinates = []

    SHIP_WIDTH = .1
    SHIP_HEIGHT = 0.035
    SHIP_BASE_Y = 0.04
    ship = None
    ship_coordinates = [(0, 0), (0, 0), (0, 0)]

    state_game_over = False
    state_game_has_started = False

    menu_title = StringProperty("RUNNING BIRD")
    menu_button_title = StringProperty("START")
    score_txt = StringProperty()
    score12_txt = StringProperty() 

    sound_begin = None
    sound_begin = None
    sound_music1 = None
    sound_music2 = None
    sound_press = None
    sound_game_over = None
    
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
       # print("INIT W:" + str(self.width) + "H:" + str(self.height))   
        self.init_audio()
        self.init_vertical_lines() 
        self.init_horizontal_lines() 
        self.init_tiles()
        self.init_ship()
        self.pre_fill_tiles_coordinates()
        self.generate_tiles_coordinates()
        
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def init_audio(self):
        self.sound_begin = SoundLoader.load("Sweet.mp3")
        self.sound_music1 = SoundLoader.load("Dogs.mp3")
        self.sound_music2 = SoundLoader.load("Selva.mp3")
        self.sound_press = SoundLoader.load("ClickSound.mp3")
        self.sound_game_over = SoundLoader.load("GameOver.mp3")

        self.sound_begin.volume = .1

    def reset_game(self):    
        self.current_offset_y = 0
        self.current_y_loop = 0

        self.current_speed_x = 0
        self.current_offset_x = 0


        
        self.tiles_coordinates = []
        self.pre_fill_tiles_coordinates()
        self.generate_tiles_coordinates()

        self.state_game_over = False
    
    def on_parent(self, widget, parent):
       # print("ON PARENT W:" + str(self.width) + "H:" + str(self.height))
        pass

    def on_size (self, *args):
        #print("ON SIZE W:" + str(self.width) + "H:" + str(self.height))
        #self.perspective_point_x = self.width/2
       # self.perspective_point_y = self.height * 0.75
        #self.update_vertical_lines()
        #self.update_horizontal_lines()
        pass

    def on_perspective_point_x(self, widget, value):
       # print("PX:" + str(value))
       pass
    
    def on_perspective_point_y(self, widget, value):
      #  print("PY:" + str(value))
      pass

    def init_ship(self):
        with self.canvas:
            Color (0,0,0)
            self.ship = Triangle()
        

    def update_ship(self):
        center_x = self.width /2
        base_y = self.SHIP_BASE_Y * self.height
        ship_half_width = self.SHIP_WIDTH * self.width / 2
        ship_height = self.SHIP_HEIGHT * self.height

        self.ship_coordinates[0] = (center_x-ship_half_width, base_y)
        self.ship_coordinates[1] = (center_x, base_y + ship_height)
        self.ship_coordinates[2] = (center_x+ship_half_width, base_y)

        x1, y1 = self.transform(*self.ship_coordinates[0])
        x2, y2 = self.transform(*self.ship_coordinates[1]) 
        x3, y3 = self.transform(*self.ship_coordinates[2])                
        
        self.ship.points = [x1, y1, x2, y2, x3, y3]
    
    def check_ship_collision(self):
        for i in range (0, len(self.tiles_coordinates)):
            ti_x, ti_y = self.tiles_coordinates[i]
            if ti_y > self.current_y_loop + 1:
                return False

            if self.check_ship_collision_with_tile(ti_x, ti_y):
                return True
        return False
    
    def check_ship_collision_with_tile(self, ti_x, ti_y):
        xmin, ymin = self.get_tile_coordinates(ti_x, ti_y)
        xmax, ymax = self.get_tile_coordinates(ti_x+1, ti_y+1)
        for i in range(0, 3):
            px, py = self.ship_coordinates[i]
            if xmin <= px <= xmax and ymin <= py <= ymax:
                return True
        return False

    
    def init_tiles(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.NB_TILES):

                self.tiles.append(Quad())
                self.sound_begin.play() 


    def pre_fill_tiles_coordinates(self):
        for i in range(0, 10):
            self.tiles_coordinates.append((0, i))

    def generate_tiles_coordinates(self):
        last_x = 0   
        last_y = 0  
        
        for i in range(len(self.tiles_coordinates)-1, -1, -1):
            if self.tiles_coordinates[i][1] < self.current_y_loop:
                del self.tiles_coordinates[i]
    
        if len(self.tiles_coordinates) > 0:
            last_coordinates = self.tiles_coordinates[-1]
            last_x = last_coordinates[0] 
            last_y = last_coordinates[1] + 1
        
        print("foo1")




        for i in range(len(self.tiles_coordinates), self.NB_TILES):
            
            r = random.randint(0, 2)
            start_index = -int(self.V_NB_LINES/2 ) + 1
            end_index = start_index+self.V_NB_LINES -1
            if last_x <= start_index:
                r = 1
            if last_x >= end_index - 1:
                r = 2
            
            self.tiles_coordinates.append((last_x, last_y))   
            if r == 1:
                last_x += 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1 
                self.tiles_coordinates.append((last_x, last_y))

            if r == 2:
                last_x -= 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1 
                self.tiles_coordinates.append((last_x, last_y))

        print("foo2")



    def init_vertical_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            #self.line = Line(points = [100, 0, 100, 100])
            for i in range(0, self.V_NB_LINES):
                self.vertical_lines.append(Line())  

    def get_line_x_from_index(self,index):
        central_line_x=self.perspective_point_x
        spacing=self.V_LINES_SPACING*self.width
        offset=index +3
        line_x = central_line_x + offset*spacing + self.current_offset_x
        return line_x

    def get_line_y_from_index(self,index):
        spacing_y = self.H_LINES_SPACING*self.height
        line_y= index*spacing_y-self.current_offset_y
        return line_y

    def get_tile_coordinates(self, ti_x, ti_y):
        ti_y = ti_y - self.current_y_loop
        x = self.get_line_x_from_index(ti_x)
        y = self.get_line_y_from_index(ti_y)
        return x, y
    
    def update_tiles(self):
        for i in range(0, self.NB_TILES):
            tile = self.tiles[i]
            tile_coordinates = self.tiles_coordinates[i]
            xmin, ymin = self.get_tile_coordinates(tile_coordinates[0], tile_coordinates[1])
            xmax, ymax = self.get_tile_coordinates(tile_coordinates[0]+1, tile_coordinates[1]+1)

            
            x1, y1 = self.transform(xmin, ymin)
            x2, y2 = self.transform(xmin, ymax)
            x3, y3 = self.transform(xmax, ymax)
            x4, y4 = self.transform(xmax, ymin)
        
            tile.points = [x1, y1, x2, y2, x3, y3, x4, y4]

    def update_vertical_lines(self):
        central_line_x = int(self.width)
        spacing = self.V_LINES_SPACING * self.width
        offset = -int(self.V_NB_LINES/2) + 0.5
        
        start_index = -int(self.V_NB_LINES/2 ) + 1
        for i in range(start_index, start_index+self.V_NB_LINES):
            line_x = self.get_line_x_from_index(i)                            
            
            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)
            self.vertical_lines[i].points = [x1, y1, x2, y2]
            offset += 1


    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.H_NB_LINES):
                self.horizontal_lines.append(Line())


    def update_horizontal_lines(self):
        start_index = -int(self.V_NB_LINES/2 ) + 1
        end_index = start_index+self.V_NB_LINES-1
       
        xmin = self.get_line_x_from_index(start_index)
        xmax = self.get_line_x_from_index(end_index)
        spacing_y = self.H_LINES_SPACING*self.height
    
        for i in range(0,self.H_NB_LINES):
            line_y = i*spacing_y-self.current_offset_y
            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)
            self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def transform(self, x, y):
        #return self.transform_perspective(x, y)
        return self.transform_2D(x, y)
    
    def transform_2D(self, x, y):
        return int(x), int(y)

    def transform_perspective(self, x, y):
        tr_y = y * self.perspective_point_y / self.height
        if tr_y > self.perspective_point_y:
            tr_y = self.perspective_point_y 
    
    
        
        diff_x = x-self.perspective_point_x
        diff_y = self.perspective_point_y-tr_y
        proportion_y = diff_y / self.perspective_point_y 
        
        tr_x = self.perspective_point_x + diff_x*proportion_y
        
        
        return int(tr_x), int(tr_y)
    
    def on_touch_down(self, touch):
        
        
        if not self.state_game_over and self.state_game_has_started:
        
            if touch.x < self.width/2:
                #print("<-")
                self.current_speed_x = self.SPEED_X
                

            else:
                print(">-")
                self.current_speed_x = -self.SPEED_X
        return super(RelativeLayout,self).on_touch_down(touch)
    
    
    def on_touch_up(self, touch):
        #print("UP")
        self.current_speed_x = 0


    def update(self, dt):
        time_factor = dt*60
        self.update_vertical_lines()
        self.update_horizontal_lines()  
        self.update_tiles()
        self.update_ship()

        if not self.state_game_over and self.state_game_has_started:
            speed_y = self.SPEED * self.height / 100
            self.current_offset_y += speed_y*time_factor 

        
            spacing_y = self.H_LINES_SPACING * self.height
            while self.current_offset_y >= spacing_y:
                self.current_offset_y -= spacing_y
                self.current_y_loop += 1
                self.score12_txt = "SCORE"
                self.score_txt = str(self.current_y_loop)
                self.generate_tiles_coordinates()
                print("loop: " + str(self.current_y_loop))

            speed_x = self.current_speed_x * self.width / 100
            self.current_offset_x += speed_x*time_factor 

        if not self.check_ship_collision() and not self.state_game_over:
            self.state_game_over = True
            self.menu_title = "GAME OVER"
            self.menu_widget.opacity = 1
            self.sound_music1.stop()

            print("GAME OVER")

    def on_menu_button_pressed(self):
        print("BUTTON")
        self.sound_music1.play() 
        self.reset_game()
        self.sound_begin.stop()
        self.state_game_has_started = True
        self.menu_widget.opacity = 0
       

class GalaxyApp(App):
    pass


GalaxyApp().run()