from entity import Entity
from enemy import Enemy
import pygame
import random

class Button(Entity):
    def __init__(self, app, on_click, sprite="none", on_click_args= [], toggleable = False):
        super().__init__(app, sprite)
        self.on_click = on_click
        self.on_click_args = on_click_args
        self.surf = self.app.asset_loader.get(sprite)
        self.current_surf = self.surf[0]
        self.toggleable = toggleable
        self.active = False

    def draw(self, surface: pygame.Surface, camera_pos: pygame.Vector2):
        if self.active:
            self.current_surf = self.surf[1]
        else:
            self.current_surf = self.surf[0]
        surface.blit(self.current_surf, self.current_surf.get_rect(topleft = self.pos))
        
    def update(self):
        super().update()
        if not self.toggleable:
            self.active = False
        if self.current_surf.get_rect(topleft= self.pos).collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_just_released()[0]:
                self.on_click(*self.on_click_args)
                self.active = not self.active
                self.app.play_sound(random.choice(["click","click(1)","click(2)"]),0.1)
            if pygame.mouse.get_pressed()[0]:
                if self.toggleable == False:
                    self.active = True

class HUD(Entity):
    def __init__(self, app, player):
        super().__init__(app, sprite="")
        self.font = self.app.asset_loader.fonts.get("JetBrainsMonoNL-Medium")
        self.numbers = self.app.asset_loader.get("sheet_10_numbers")
        self.colon = self.app.asset_loader.get("colon")
        self.dash = self.app.asset_loader.get("char_dash")
        self.hud_image = self.app.asset_loader.get("assets_hud")
        self.health_image = self.app.asset_loader.get("full_health")
        self.xp_image = self.app.asset_loader.get("full_XP")
        self.pause_image = self.app.asset_loader.get("pause_menu")
        self.death_image = self.app.asset_loader.get("death_screen")
        self.level_menu = self.app.asset_loader.get("level_up_menu")
        
        pygame.mouse.set_visible(False)

        cutout_mask = pygame.mask.from_surface(self.health_image)
        self.cutout_image = cutout_mask.to_surface()
        self.cutout_image.set_colorkey('#FFFFFF')

        self.player = player
        self.previous_health = 0
        self.previous_xp = 1
        self.pos = self.player.pos

        self.clock = self.app.clock

        self.CENTER = pygame.Vector2(800, 450)
        self.HEALTH_TEXT_OFFSET = pygame.Vector2(65, 288)
        self.MAX_HEALTH_TEXT_OFFSET = pygame.Vector2(65, 32)
        self.HEALTH_BAR_OFFSET = pygame.Vector2(33, 33)
        self.XP_OFFSET = pygame.Vector2(544, 32)
        self.CHARGE_BAR_OFFSET = pygame.Vector2(800, 800)
        self.KILL_COUNT_OFFSET = pygame.Vector2(1440, 61)
        self.TIMER_OFFSET = pygame.Vector2(1440, 135)
        self.LEVEL_MENU_OFFSET = pygame.Vector2(576, 210)
        self.LEVEL_BUTTON_OFFSET = pygame.Vector2(320, 160)
        self.LEVEL_TEXT_OFFSET = pygame.Vector2(288, 160)
        self.LEVEL_BUTTON_STEP = 64
        self.DEATH_SCENE_TIMER_OFFSET = pygame.Vector2(512, 366)
        self.DEATH_SCENE_KILLS_OFFSET = pygame.Vector2(160, 366)
        self.DEATH_SCENE_ALIVE_OFFSET = pygame.Vector2(416, 240)
        self.PLAY_BUTTON_OFFSET = pygame.Vector2(512, 626)
        self.EXIT_BUTTON_OFFSET = pygame.Vector2(864, 626)

        self.target_health_pos = self.HEALTH_BAR_OFFSET
        self.target_xp_pos = self.XP_OFFSET 

        self.health_pos = pygame.Vector2(0, 1)
        self.xp_pos = pygame.Vector2(1, 0)

        self.level_available = False
        self.death_scene_made = False
        self.pause_scene_made = False

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
        self.health_pos = self.health_pos.smoothstep(self.target_health_pos, 0.15)

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
        self.xp_pos = self.xp_pos.smoothstep(self.target_xp_pos, 0.15) 

        surface.blit(self.new_xp_image, self.new_xp_image.get_rect(topleft = (self.pos + self.XP_OFFSET)))

        self.previous_xp = self.player.xp

    def draw_kill_count(self, surface: pygame.Surface):
        kill_count = self.make_text(str(self.player.total_kills))
        surface.blit(kill_count, kill_count.get_rect(midleft = (self.pos + self.KILL_COUNT_OFFSET)))
    
    def draw_time_played(self, surface: pygame.Surface):
        sec = self.app.timer // 60
        self.time_sec = sec % 60
        self.time_min = sec // 60
        if self.time_sec < 10:
            self.time_sec = f"0{self.time_sec}"
        if self.time_min < 10:
            self.time_min = f"0{self.time_min}"

        time_played = self.make_text(f"{self.time_min}:{self.time_sec}")
        
        surface.blit(time_played, time_played.get_rect(midleft = (self.pos + self.TIMER_OFFSET)))

    # def draw_cursor(self, surface: pygame.Surface):
    #     mouse_pos = pygame.mouse.get_pos()
    #     self.cursor_rect = self.cursor_image.get_rect(topleft= mouse_pos)
    #     if not pygame.mouse.get_pressed()[0]:
    #         surface.blit(self.cursor_image, self.cursor_rect)
    #     else:
    #         surface.blit(self.down_cursor ,self.cursor_rect)

    def draw_level_popup(self, surface: pygame.Surface, camera_pos: pygame.Vector2):
        surface.blit(self.new_level_menu, self.new_level_menu.get_rect(topleft= self.LEVEL_MENU_OFFSET))
        
        for child in self.children:
            child.draw(surface, camera_pos)
            child.update()

    def draw_charge_bar(self, surface):
        x_offset = self.CHARGE_BAR_OFFSET.x - (self.player.children[0].MAX_DRAW * 10 - 100) / 2
        pygame.draw.rect(surface, '#00C494', ((x_offset + self.pos.x, self.CHARGE_BAR_OFFSET.y + self.pos.y), (self.player.children[0].draw_timer * 10 - 100, 20)), border_radius= 5)
        pygame.draw.rect(surface, '#77888C', ((x_offset + self.pos.x, self.CHARGE_BAR_OFFSET.y + self.pos.y), (self.player.children[0].MAX_DRAW * 10 - 100, 20)), 5, 5)

    def draw_death_scene(self, surface, camera_pos):
        surface.blit(self.new_death_img, self.new_death_img.get_rect(center= self.CENTER))

        for child in self.children:
            child.draw(surface, camera_pos)
            child.update()

    def make_death_scene(self, surface):
        current_enemies = len(self.app.get_current_scene().enemy_manager.children)
        timer_text = self.make_text(f"{self.time_min}:{self.time_sec}", 1.5)
        kills_text = self.make_text(str(self.player.total_kills), 1.5)
        outnumbered_text = self.make_text(f"{current_enemies}-1", 4)

        self.new_death_img = self.death_image.copy()

        new_run_button = Button(self.app, self.app.reset, "sheet_2_play_button")
        new_run_button.pos = self.PLAY_BUTTON_OFFSET
        new_run_button.z_index = 100000
        exit_button = Button(self.app, self.quit_run, "sheet_2_exit_small_button")
        exit_button.pos = self.EXIT_BUTTON_OFFSET
        exit_button.z_index = 100000
        self.add_child(exit_button)
        self.add_child(new_run_button)

        self.new_death_img.blit(timer_text, timer_text.get_rect(midleft= self.DEATH_SCENE_TIMER_OFFSET))
        self.new_death_img.blit(kills_text, kills_text.get_rect(midleft= self.DEATH_SCENE_KILLS_OFFSET))
        self.new_death_img.blit(outnumbered_text, outnumbered_text.get_rect(center= self.DEATH_SCENE_ALIVE_OFFSET))

        self.death_scene_made = True

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
    
    def make_text(self, num: str, scale: int= 1) -> pygame.Surface:
        step = scale * 32
        surf = pygame.Surface((step * len(num), step))
        surf.set_colorkey('#000000')
        for i in range(0, len(num)):
            if num[i] == "-":
                image = pygame.transform.scale(self.dash, (image.width * scale, image.height * scale)).convert_alpha()
                surf.blit(image, (i * step, 0))
            elif num[i] == ":":
                image = pygame.transform.scale(self.colon, (image.width * scale, image.height * scale)).convert_alpha()
                surf.blit(image, (i * step, 0))
            else:
                image = self.numbers[int(num[i])]
                scaled_image = pygame.transform.scale(image, (image.width * scale, image.height * scale)).convert_alpha()
                surf.blit(scaled_image, (i * step, 0))
        return surf     

    def make_level_popup(self):
        self.app.play_sound("level_up", 0.03)
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
            self.add_child(buttons[i])

    def level_up(self, stat: str):
        self.player.level_up(stat)
        self.children = []
        self.level_available = False
        self.app.paused = False
    
    def draw_pause_popup(self, surface, camera_pos):
        rect = self.pause_image.get_rect()
        rect.center = (surface.width / 2, surface.height / 2)
        surface.blit(self.pause_image, rect.topleft)

        for child in self.children:
            child.draw(surface, camera_pos)
            child.update()

    def make_pause_popup(self, surface):
        play = Button(self.app, self.resume, "sheet_2_play_button")
        play.pos = pygame.Vector2(surface.width/2 - 3 * 32, surface.height/2 - 32)
        exit = Button(self.app, self.quit_run, "sheet_2_exit_small_button")
        exit.pos = pygame.Vector2(surface.width/2 - 3 * 32, surface.height/2 + 64)
        self.add_child(exit)
        self.add_child(play)
        self.pause_scene_made = True
    
    def resume(self):
        self.app.paused = False
        self.children = []
        self.pause_scene_made = False
    
    def quit_run(self):
        self.app.current_scene = "main_menu"

    def draw(self, surface: pygame.Surface, camera_pos: pygame.Vector2):
        if self.player.dead:
            if not self.death_scene_made:
                self.make_death_scene(surface)
            self.draw_death_scene(surface, camera_pos)
        else:
            self.pos = -self.get_relative_pos(surface, camera_pos)
            self.draw_xp(surface)
            self.draw_health(surface)
            if self.player.children[0].attributes["is_ranged"]:
                self.draw_charge_bar(surface)
            self.draw_kill_count(surface)
            self.draw_time_played(surface)
            self.draw_fps(surface)
            if self.level_available == True:
                self.app.paused = True
                self.draw_level_popup(surface, camera_pos)
            elif self.app.paused == True:
                if not self.pause_scene_made:
                    self.make_pause_popup(surface)
                self.draw_pause_popup(surface, camera_pos)
            surface.blit(self.hud_image, self.pos)

    def update(self):
        for child in self.children:
            child.update()