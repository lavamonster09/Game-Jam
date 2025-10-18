from entity import Entity
from enemy import Enemy
import pygame

class Button(Entity):
    def __init__(self, app, on_click, sprite="none", on_click_args= []):
        super().__init__(app, sprite)
        self.on_click = on_click
        self.on_click_args = on_click_args
        self.surf = self.app.asset_loader.get(sprite)
        self.current_surf = self.surf[0]

    def draw(self, surface: pygame.Surface, camera_pos: pygame.Vector2):
        surface.blit(self.current_surf, self.current_surf.get_rect(topleft = self.pos))
        
    def update(self):
        super().update()
        self.current_surf = self.surf[0]
        if self.current_surf.get_rect(topleft= self.pos).collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_just_released()[0]:
                self.on_click(*self.on_click_args)
            if pygame.mouse.get_pressed()[0]:
                self.current_surf = self.surf[1]

class HUD(Entity):
    def __init__(self, app, player):
        super().__init__(app, sprite="")
        self.font = self.app.asset_loader.fonts.get("JetBrainsMonoNL-Medium")
        self.numbers = self.app.asset_loader.get("sheet_10_numbers")
        self.colon = self.app.asset_loader.get("colon")
        self.hud_image = self.app.asset_loader.get("assets_hud")
        self.health_image = self.app.asset_loader.get("full_health")
        self.xp_image = self.app.asset_loader.get("full_XP")
        self.cursor_image = self.app.asset_loader.get("CURSOR2")
        self.down_cursor = self.app.asset_loader.get("CURSOR2_down") 
        self.level_menu = self.app.asset_loader.get("level_up_menu")
        
        pygame.mouse.set_visible(False)

        cutout_mask = pygame.mask.from_surface(self.health_image)
        self.cutout_image = cutout_mask.to_surface()
        self.cutout_image.set_colorkey('#FFFFFF')

        self.player = player
        self.previous_health = 0
        self.previous_xp = -1
        self.pos = self.player.pos

        self.clock = self.app.clock

        self.HEALTH_TEXT_OFFSET = pygame.Vector2(65, 288)
        self.MAX_HEALTH_TEXT_OFFSET = pygame.Vector2(65, 32)
        self.HEALTH_BAR_OFFSET = pygame.Vector2(33, 33)
        self.XP_OFFSET = pygame.Vector2(544, 32)
        self.KILL_COUNT_OFFSET = pygame.Vector2(1440, 61)
        self.TIMER_OFFSET = pygame.Vector2(1440, 135)
        self.LEVEL_MENU_OFFSET = pygame.Vector2(576, 210)
        self.LEVEL_BUTTON_OFFSET = pygame.Vector2(320, 160)
        self.LEVEL_TEXT_OFFSET = pygame.Vector2(288, 160)
        self.LEVEL_BUTTON_STEP = 64

        self.target_health_pos = self.HEALTH_BAR_OFFSET
        self.target_xp_pos = self.XP_OFFSET 

        self.health_pos = pygame.Vector2(0, 1)
        self.xp_pos = pygame.Vector2(1, 0)

        self.level_available = False

    def get_relative_pos(self, surface: pygame.Surface, camera_pos: pygame.Vector2) -> pygame.Vector2:
        relative_pos = self.player.pos - camera_pos
        return relative_pos
    
    def draw_fps(self, surface: pygame.Surface):
        self.fps_text = self.font.render(str(round(self.clock.get_fps())), True, '#00A494')
        self.fps_rect = self.fps_text.get_rect(bottomright = (1600, 900))
        surface.blit(self.fps_text, self.fps_rect)

    def draw_health(self, surface: pygame.Surface):
        if self.previous_health != self.player.health:
            self.target_health_pos = self.get_missing_health()
            self.current_health_text = self.make_text(str(self.player.health))
            self.max_health_text = self.make_text(str(self.player.max_health))
        self.cutout_health()
        if self.target_health_pos != pygame.Vector2(0,0):
            self.health_pos = self.health_pos.slerp(self.target_health_pos, 0.05)

        self.current_health_rect = self.current_health_text.get_rect(midtop= (self.pos + self.HEALTH_TEXT_OFFSET))
        self.max_health_rect = self.max_health_text.get_rect(midbottom= (self.pos + self.MAX_HEALTH_TEXT_OFFSET))

        surface.blit(self.new_health_image, self.pos + self.health_pos + self.HEALTH_BAR_OFFSET)
        surface.blit(self.current_health_text, self.current_health_rect)
        surface.blit(self.max_health_text, self.max_health_rect)

        self.previous_health = self.player.health

    def draw_xp(self, surface: pygame.Surface):
        if self.previous_xp != self.player.xp:
            self.target_xp_pos = self.get_missing_xp()
            if self.player.xp == self.player.max_xp:
                self.level_available = True
                self.make_level_popup()
        self.cutout_xp()
        if self.target_xp_pos == pygame.Vector2(0,0):
            self.target_xp_pos = pygame.Vector2(0.001,0)
        self.xp_pos = self.xp_pos.slerp(self.target_xp_pos, 0.05) 

        surface.blit(self.new_xp_image, self.new_xp_image.get_rect(topleft = (self.pos + self.XP_OFFSET)))

        self.previous_xp = self.player.xp

    def draw_kill_count(self, surface: pygame.Surface):
        kill_count = self.make_text(str(self.player.total_kills))
        surface.blit(kill_count, kill_count.get_rect(midleft = (self.pos + self.KILL_COUNT_OFFSET)))
    
    def draw_time_played(self, surface: pygame.Surface):
        sec = self.app.timer // 60
        time_sec = sec % 60
        time_min = sec // 60
        if time_sec < 10:
            time_sec = f"0{time_sec}"
        if time_min < 10:
            time_min = f"0{time_min}"

        time_played = self.make_text(f"{time_min}:{time_sec}")
        
        surface.blit(time_played, time_played.get_rect(midleft = (self.pos + self.TIMER_OFFSET)))

    def draw_cursor(self, surface: pygame.Surface):
        mouse_pos = pygame.mouse.get_pos()
        self.cursor_rect = self.cursor_image.get_rect(topleft= mouse_pos)
        if not pygame.mouse.get_pressed()[0]:
            surface.blit(self.cursor_image, self.cursor_rect)
        else:
            surface.blit(self.down_cursor ,self.cursor_rect)

    def draw_level_popup(self, surface: pygame.Surface, camera_pos: pygame.Vector2):
        surface.blit(self.new_level_menu, self.new_level_menu.get_rect(topleft= self.LEVEL_MENU_OFFSET))
        
        for child in self.children:
            child.draw(surface, camera_pos)
            child.update()

    def cutout_health(self):
        size = self.health_image.size
        rect_size = (size[0], self.health_pos.y)
        rect_cutout = pygame.Surface(rect_size)
        rect_cutout.fill('#000000')
        self.new_health_image = self.health_image.copy()
        self.new_health_image.blit(self.cutout_image, self.cutout_image.get_rect(topleft= -self.health_pos))
        self.new_health_image.blit(rect_cutout, rect_cutout.get_rect(bottomright= size))
        self.new_health_image.set_colorkey('#000000')

    def cutout_xp(self):
        bar_size = self.xp_image.get_size()
        cutout_size = (self.xp_pos.x, bar_size[1])
        cutout_surf = pygame.Surface(cutout_size)
        cutout_surf.fill('#000000')
        self.new_xp_image = self.xp_image.copy()
        self.new_xp_image.blit(cutout_surf, cutout_surf.get_rect(bottomright= bar_size))
        self.new_xp_image.set_colorkey('#000000')

    def get_missing_health(self) -> pygame.Vector2:
        percent_health_missing = 1 - self.player.health / self.player.max_health
        img_height = self.health_image.get_height() - 64
        health_pos = pygame.Vector2(0, img_height * percent_health_missing)
        return health_pos
    
    def get_missing_xp(self) -> pygame.Vector2:
        percent_missing_xp = 1 - self.player.xp / self.player.max_xp
        bar_size = self.xp_image.get_width() 
        xp_pos = pygame.Vector2(bar_size * percent_missing_xp, 0)
        return xp_pos
    
    def make_text(self, num: str) -> pygame.Surface:
        surf = pygame.Surface((32 * len(num), 32))
        surf.set_colorkey('#000000')
        for i in range(0, len(num)):
            if num[i] == ":":
                surf.blit(self.colon, (i * 32, 0))
            else:
                surf.blit(self.numbers[int(num[i])], (i * 32, 0))
        return surf     

    def make_level_popup(self):
        self.new_level_menu = self.level_menu.copy()
        buttons = [
            Button(self.app, self.level_up, "sheet_2_level_up_button", ["Strength"]),
            Button(self.app, self.level_up, "sheet_2_level_up_button", ["Dexterity"]),
            Button(self.app, self.level_up,  "sheet_2_level_up_button", ["Vigor"]),
            Button(self.app, self.level_up,  "sheet_2_level_up_button", ["Endurance"])
        ]

    
        levels = list(self.player.levels.values())
        for i in range(len(levels)):
            surf = self.make_text(str(levels[i]))
            self.new_level_menu.blit(surf, surf.get_rect(topright= (self.LEVEL_TEXT_OFFSET) + (0, i * 64)))

        for i in range(0, 4):
            buttons[i].pos = self.LEVEL_MENU_OFFSET + (self.LEVEL_BUTTON_OFFSET.x, self.LEVEL_BUTTON_OFFSET.y + i * self.LEVEL_BUTTON_STEP)
            print(buttons[i].pos)
            self.add_child(buttons[i])

    def level_up(self, stat: str):
        self.player.level_up(stat)
        self.level_available = False
        self.app.paused = False
        for child in self.children:
            self.remove_child(child)

    def draw(self, surface: pygame.Surface, camera_pos: pygame.Vector2):
        self.pos = self.get_relative_pos(surface, camera_pos)
        self.draw_xp(surface)
        self.draw_health(surface)
        self.draw_kill_count(surface)
        self.draw_time_played(surface)
        self.draw_fps(surface)
        if self.level_available == True:
            self.app.paused = True
            self.draw_level_popup(surface, camera_pos)
        surface.blit(self.hud_image, self.pos)
        self.draw_cursor(surface)

    def update(self):
        for child in self.children:
            child.update()