

from os import name
from tokenize import String
from turtle import title
import pygame
import pygame_menu
from data.CharacterDataManager import *
from data.StoreDataManager import *
from data.Defs import *
from data.Stage import Stage
from data.StageDataManager import *
from data.database_user import Database
from game.InfiniteGame import *
from pygame_menu.locals import ALIGN_RIGHT
from pygame_menu.utils import make_surface
from object.Character import *

# 캐릭터 선택 메뉴
class CharacterStoreMenu:
    image_widget: 'pygame_menu.widgets.Image'
    item_description_widget: 'pygame_menu.widgets.Label'

    def __init__(self, screen, character):
        # 화면 받고 화면 크기 값 받기
        self.screen = screen
        self.size = screen.get_size()
        self.character = character

        #menu_image = pygame_menu.baseimage.BaseImage(image_path='./Image/Login.png',drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)
        self.mytheme = pygame_menu.themes.THEME_ORANGE.copy()
        #mytheme.widget_font = pygame_menu.font.FONT_8BIT
        #mytheme.widget_background_color = (150, 213, 252) #버튼 가독성 올리기 위해서 버튼 배경색 설정 : 하늘색
        self.mytheme.title_font = pygame_menu.font.FONT_BEBAS
        self.mytheme.selection_color = (255,255,255) #선택됐을때 글씨색 설정
        self.mytheme.widget_font_color = (255,255,255) #글씨색 설정
        self.mytheme.title_background_color = (0,100,162)
        self.mytheme.title_font_color = (255,255,255)
        self.mytheme.widget_font = pygame_menu.font.FONT_BEBAS
        #self.mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_TITLE_ONLY_DIAGONAL
        self.mytheme.background_color = (0,0,0)

        self.menu = pygame_menu.Menu('Character Store', self.size[0], self.size[1],
                            theme=self.mytheme)


        #캐릭터 데이터를 json에서 불러온다
        #self.character_data = CharacterDataManager.load()

        self.show(self.character)
        self.menu.mainloop(self.screen,bgfun = self.check_resize)

    def to_menu(self):
            import menu.gameselectMenu
            game=menu.gameselectMenu.GameselectMenu(self.screen)

            while True:
                game.show(self.screen)
                pygame.display.flip()

    #메뉴 구성하고 보이기
    def show(self, character_info):  # 원래 character_info를 가져와서 직업에 따라 상점 구현하려고 함.
        self.character = character_info
        # front_image_path = [ Images.fire.value, Images.fire1.value, Images.fire2.value, Images.police.value, Images.police1.value,
        # Images.police2.value, Images.doctor.value, Images.doctor1.value, Images.doctor2.value]
        # self.character_data = CharacterDataManager.load()
        
        if self.character == "firefighter":
            front_image_path = [ Images.fire.value, Images.fire1.value, Images.fire2.value]
            self.character_data = StoreDataManager.load("fire")

            curs = Database().dct_db.cursor()
            self.id = User.user_id
            sql = "SELECT user_id, fchar1, fchar2, fchar3 FROM tusers2 WHERE user_id=%s" #user_id와 user_character열만 선택 -> 수정 필요
            curs.execute(sql,self.id) 
            data = curs.fetchone()  # fetchone 데이터베이스로부터 정보를 가져오는 과정 
            curs.close()

        if self.character == "police":
            front_image_path = [Images.police.value, Images.police1.value, Images.police2.value]
            self.character_data = StoreDataManager.load("police")  
    

            curs = Database().dct_db.cursor()
            self.id = User.user_id
            sql = "SELECT user_id, pchar1, pchar2, pchar3 FROM tusers2 WHERE user_id=%s" #user_id와 user_character열만 선택 -> 수정 필요
            curs.execute(sql,self.id) 
            data = curs.fetchone()  # fetchone 데이터베이스로부터 정보를 가져오는 과정 
            curs.close()

        if self.character == "doctor":
            front_image_path = [Images.doctor.value, Images.doctor1.value, Images.doctor2.value]
            self.character_data = StoreDataManager.load("doctor")

            curs = Database().dct_db.cursor()
            self.id = User.user_id
            sql = "SELECT user_id, dchar1, dchar2, dchar3 FROM tusers2 WHERE user_id=%s" #user_id와 user_character열만 선택 -> 수정 필요
            curs.execute(sql,self.id) 
            data = curs.fetchone()  # fetchone 데이터베이스로부터 정보를 가져오는 과정 
            curs.close()

        User.coin = Database().show_mycoin()
        self.menu.add.label("My coin : %d "%User.coin)
        #캐릭터 선택 메뉴 구성
        characters = []


        self.character_imgs = []
        self.character_imgs2 = []
        self.price = []
        # =====================================================================================================
        for idx in range(1,4): # 데이버 베이스 정보를 가져올 인덱스 설정
            print("인덱스 설정")
            char = data[idx] # 해당 인덱스에 저장된 값 (-1 또는 보유시 5로 설정)

            if(char == -1): # 보유하지 않다면 (기본캐릭터는 상점에 나오지 않음)
                default_image = pygame_menu.BaseImage(
                    image_path=front_image_path[idx-1] # 1~3까지 설정된  front_image_path 이미지 띄움
                ).scale(0.5, 0.5)
                characters.append((self.character_data[idx-1].name, idx-1))
                self.character_imgs.append(default_image.copy())
                
        if len(characters)==0:
                    self.menu.add.label("Nothing to buy.")
                    self.menu.add.button("    BACK    ",self.to_menu)

        else: # 구매할 아이템이 있을 경우
            for i in range(3): 
                    default_image = pygame_menu.BaseImage(
                    image_path=front_image_path[i]
                    ).scale(0.5, 0.5)
        
                    self.character_imgs2.append(default_image.copy())

            for i in range(0,3):
                self.price.append(User.price[i]) 
                
            self.character_selector = self.menu.add.selector(
                title='Character :\t',
                items=characters,
                onchange=self.on_selector_change
            )
            self.image_widget = self.menu.add.image(
                image_path=self.character_imgs[0],
                padding=(25, 0, 0, 0)  # top, right, bottom, left
            )
            

            self.item_description_widget = self.menu.add.label("")
            self.frame_v = self.menu.add.frame_v(350, 160, margin=(10, 0))
            # 각 캐릭터의 능력치 표시
            # self.power = self.frame_v.pack(self.menu.add.progress_bar(
            #     title="Power",
            #     default=int((self.character_data[0].missile_power/Default.character.value["max_stats"]["power"])*100),
            #     progress_text_enabled = False,
            #     box_progress_color = Color.RED.value
            # ), ALIGN_RIGHT)
            # self.fire_rate = self.frame_v.pack(self.menu.add.progress_bar(
            #     title="Fire Rate",
            #     default=int((Default.character.value["max_stats"]["fire_rate"]/self.character_data[0].org_fire_interval)*100),
            #     progress_text_enabled = False,
            #     box_progress_color =Color.BLUE.value
            # ), ALIGN_RIGHT)
            # self.velocity = self.frame_v.pack(self.menu.add.progress_bar(
            #     title="Mobility",
            #     default=int((self.character_data[0].org_velocity/Default.character.value["max_stats"]["mobility"])*100),
            #     progress_text_enabled = False,
            #     box_progress_color = Color.GREEN.value
            # ), ALIGN_RIGHT)

            # self.mytheme.widget_background_color = (150, 213, 252)
            #self.item_description_widget = self.show_price
            
            self.menu.add.button("Buy", self.buy_character(self.character))
            self.menu.add.vertical_margin(10)
            self.menu.add.button("    BACK    ",self.to_menu)
            self.lock(self.character)

            self.update_from_selection(int(self.character_selector.get_value()[0][1]))
            self.mytheme.widget_background_color = (0,0,0,0)
        


    def buy_character(self, character_info):
        character = character_info
        if character =="firefighter":
            curs = Database().dct_db.cursor()
            self.id = User.user_id
            sql = "SELECT user_id,fchar1, fchar2, fchar3, user_coin FROM tusers2 WHERE user_id=%s" #user_id와 user_character열만 선택
            curs.execute(sql,self.id) 
            data = curs.fetchone()  
            curs.close()
        if character =="police":
            curs = Database().dct_db.cursor()
            self.id = User.user_id
            sql = "SELECT user_id, pchar1, pchar2, pchar3, user_coin FROM tusers2 WHERE user_id=%s" #user_id와 user_character열만 선택
            curs.execute(sql,self.id) 
            data = curs.fetchone()  
            curs.close()
        if character =="doctor":
            curs = Database().dct_db.cursor()
            self.id = User.user_id
            sql = "SELECT user_id, dchar1, dchar2, dchar3, user_coin FROM tusers2 WHERE user_id=%s" #user_id와 user_character열만 선택
            curs.execute(sql,self.id) 
            data = curs.fetchone()  
            curs.close()
        
       
        # 캐릭터 셀릭터가 선택하고 있는 데이터를 get_value 로 가져와서, 그 중 Character 객체를 [0][1]로 접근하여 할당

        selected_idx = self.character_selector.get_value()[0][1]
        if(User.coin >= self.price[selected_idx]):
            User.buy_character = selected_idx
            database = Database()
            database.buy_char()
            User.coin = Database().show_mycoin()
            #self.show()
            self.item_description_widget.set_title(title = "Unlocked" )

        else:
            print("not enough money")
            import menu.CharacterBuy
            menu.CharacterBuy.CharacterBuy(self.screen,self.character_data[selected_idx].name).show()    

    #잠금 표시
    def lock(self, character_info):
        character = character_info
        if character== "firefighter":
            curs = Database().dct_db.cursor()
            self.id = User.user_id
            sql = "SELECT user_id, fchar1, fchar2, fchar3 FROM tusers2 WHERE user_id=%s" #user_id와 user_character열만 선택
            curs.execute(sql,self.id) 
            data = curs.fetchone()  
            curs.close()
        if character == "doctor":
            curs = Database().dct_db.cursor()
            self.id = User.user_id
            sql = "SELECT user_id, dchar1, dchar2, dchar3 FROM tusers2 WHERE user_id=%s" #user_id와 user_character열만 선택
            curs.execute(sql,self.id) 
            data = curs.fetchone()  
            curs.close()
        if character == "police":
            curs = Database().dct_db.cursor()
            self.id = User.user_id
            sql = "SELECT user_id, pchar1, pchar2, pchar3 FROM tusers2 WHERE user_id=%s" #user_id와 user_character열만 선택
            curs.execute(sql,self.id) 
            data = curs.fetchone()  
            curs.close()

        selected_idx = self.character_selector.get_value()[0][1]
        #self.item_description_widget.set_title(title = "Unlocked" if data[selected_idx] == True else "Locked")

        if(data[2] == 0):
            self.item_description_widget.set_title(title = "Locked")
        else:
            self.item_description_widget.set_title(title = "Unlocked" if data[selected_idx] == True else "Locked")
        
        if(data[3] == 0):
            self.item_description_widget.set_title(title = "Locked")
        else:
            self.item_description_widget.set_title(title = "Unlocked" if data[selected_idx] == True else "Locked")
        
        # if(data[4] == 0):
        #     self.item_description_widget.set_title(title = "Locked")
        # else:
        #     self.item_description_widget.set_title(title = "Unlocked" if data[selected_idx] == True else "Locked")
        
    


    


    # 화면 크기 조정 감지 및 비율 고정
    def check_resize(self):
        if (self.size != self.screen.get_size()): #현재 사이즈와 저장된 사이즈 비교 후 다르면 변경
            changed_screen_size = self.screen.get_size() #변경된 사이즈
            ratio_screen_size = (changed_screen_size[0],changed_screen_size[0]*783/720) #y를 x에 비례적으로 계산
            if(ratio_screen_size[0]<320): #최소 x길이 제한
                ratio_screen_size = (494,537)
            if(ratio_screen_size[1]>783): #최대 y길이 제한
                ratio_screen_size = (720,783)
            self.screen = pygame.display.set_mode(ratio_screen_size,
                                                    pygame.RESIZABLE)
            window_size = self.screen.get_size()
            new_w, new_h = 1 * window_size[0], 1 * window_size[1]
            self.menu.resize(new_w, new_h)
            self.size = window_size
            self.menu._current._widgets_surface = make_surface(0,0)
            print(f'New menu size: {self.menu.get_size()}')

    # 캐릭터 변경 시 실행
    def on_selector_change(self, selected, value: int) -> None:
        self.update_from_selection(value)

    # 캐릭터 선택 시 캐릭터 이미지 및 능력치 위젯 업데이트
    def update_from_selection(self, selected_value, **kwargs) -> None:
        #selected_idx = self.character_selector.get_value()[0][1]
        self.current = selected_value
        self.image_widget.set_image(self.character_imgs2[selected_value])
        # self.power.set_value(int((self.character_data[selected_value].missile_power/Default.character.value["max_stats"]["power"])*100))
        # self.fire_rate.set_value(int((Default.character.value["max_stats"]["fire_rate"]/self.character_data[selected_value].org_fire_interval)*100))
        # self.velocity.set_value(int((self.character_data[selected_value].org_velocity/Default.character.value["max_stats"]["mobility"])*100))
        self.item_description_widget.set_title(title = self.price[selected_value])