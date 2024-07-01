import pygame
from .settings import *
from .support import *

class settings_menu:
    def __init__(self, font, sounds):

        # general setup
        self.display_surface = pygame.display.get_surface()
        self.font = font
        self.index = 0
        # options
        self.width = 400
        self.space = 10
        self.padding = 8
        self.sounds = sounds
        self.go_back = False
        self.current_item = 0
        self.sliders = {}
        self.switches = {}
        self.arrows = {}
        self.functions = {
            "volume": self.volume_function,
            "ambience": self.ambience_function,
            "music": self.music_function,
            "muteifnotfocused": self.muteifnotfocused_function,
        }
        # entries
        self.options = ("Keybinds", "Audio", "Back")
        self.option_data = {
            0: {
                "Up": "UP ARROW",
                "Down": "DOWN ARROW",
                "Left": "LEFT ARROW",
                "Right": "RIGHT ARROW",
                "Use": "SPACE",
                "Cycle Tools": "Q",
                "Cycle Seeds": "E",
                "Plant Current Seed": "LCTRL",
            },
            1: {
                "Volume": {
                    "type": "slider",
                    "default": 50,
                    "function": self.functions["volume"]
                },
                "Ambience": {
                    "type": "switch",
                    "default": "On",
                    "function": self.functions["ambience"]
                },
                #"Sound Quality": {
                #    "type": "arrow",
                #    "values": [
                #        "Low",
                #        "Normal",
                #        "High",
                #        "Epic",
                #    ],
                #    "default": 0
                #},
                "Music": {
                    "type": "switch",
                    "default": "On",
                    "function": self.functions["music"]
                },
                "Mute if not focused": {
                    "type": "switch",
                    "default": "On",
                    "function": self.functions["muteifnotfocused"]
                },


            },
            2: {
                "Back": "Press Space to go back to the main menu!"
            },
        }
        self.setup()

    def setup(self):
        # create the text surfaces
        self.text_surfs = []
        self.total_height = 0

        for item in self.options:
            text_surf = self.font.render(item, False, 'Black')
            self.text_surfs.append(text_surf)
            self.total_height += text_surf.get_height() + (self.padding * 2)

        self.menu_top = SCREEN_HEIGHT / 20 + 100
        self.main_rect = pygame.Rect(SCREEN_WIDTH / 20 - self.width / 20, self.menu_top, self.width, self.total_height)

        # buy / sell text surface
    def input(self):
        event = pygame.event.get()
        for slider in self.sliders.values():
            if slider:
                slider.handle_event(event)   
        for switch in self.switches.values():
            if switch:
                switch.handle_event(event)
        for arrow in self.arrows.values():
            if arrow:
                arrow.handle_event(event)      

        keys = pygame.key.get_just_pressed()

        self.index = (self.index + int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])) % len(self.options)

        if keys[pygame.K_SPACE]:
            self.current_item = self.options[self.index]
            if 'Back' in self.current_item:
                self.go_back = True
                self.index = 0

    def show_entry(self, text_surf, top, index, text_index):
        # background
        bg_rect = pygame.Rect(self.main_rect.left, top, self.width, text_surf.get_height() + (self.padding * 2))
        pygame.draw.rect(self.display_surface, 'White', bg_rect, 0, 4)
        big_rect = pygame.Rect(SCREEN_WIDTH // 15 + self.width, (SCREEN_HEIGHT // 20 + self.total_height//2)+25, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.draw.rect(self.display_surface, 'White', big_rect, 0, 4)
        # text
        text_rect = text_surf.get_rect(midleft=(self.main_rect.left + (self.main_rect.width/2)-text_surf.get_width()/2, bg_rect.centery))
        big_text_surfs = {}
        if self.option_data[index]:
            for key, value in self.option_data[index].items():
                if isinstance(value, str):
                    text = f"{key}: {value}"
                    big_text_surf = self.font.render(text, False, 'Black')
                    big_text_surfs[key] = big_text_surf
                else:
                    if value["type"] == "slider":
                        if key in self.sliders:
                            slider = self.sliders[key]
                        else:
                            slider = Slider(big_rect.right - (big_rect.width/3), big_rect.height-(big_rect.height/2), big_rect.width/3, 10, 0, 100, value["default"], value["function"])
                            self.sliders[key] = slider
                        slider.draw(self.display_surface)
                        v = slider.get_value()
                        text = f"{key}: {round(v)}"
                        big_text_surf = self.font.render(text, False, 'Black')
                        big_text_surfs[key] = big_text_surf
                    elif value["type"] == "switch":
                        if key in self.switches:
                            switch = self.switches[key]
                        else: 
                            switch = Switch(big_rect.right - (big_rect.width/3), big_rect.height-(big_rect.height/10), 40, 20, 'Green', 'Red', self.sounds, value["function"])
                            if value["default"] == "On":
                                switch.is_on = True
                            else:
                                switch.is_on = False
                            self.switches[key] = switch
                        switch.draw(self.display_surface)
                        text = f"{key}"
                        big_text_surf = self.font.render(text, False, 'Black')
                        big_text_surfs[key] = big_text_surf
                    elif value["type"] == "arrow":
                        if key in self.arrows:
                            arrow = self.arrows[key]
                        else:
                            arrow = Arrow(big_rect.right - (big_rect.width/3), big_rect.height-(big_rect.height/10), big_rect.width/3, 10, list(value["values"]), self.sounds, value["function"])
                            self.arrows[key] = arrow
                        arrow.draw(self.display_surface)
                        text = f"{key}"
                        big_text_surf = self.font.render(text, False, 'Black')
                        big_text_surfs[key] = big_text_surf
        for i, (key, big_text_surf) in enumerate(big_text_surfs.items()):
            big_text_rect = big_text_surf.get_rect(topleft=(big_rect.left + 10, big_rect.top + 10 + i * 20))
            self.display_surface.blit(big_text_surf, big_text_rect)
            if key in self.sliders:
                self.sliders[key].rect.y = big_text_rect.top + 5
            if key in self.switches:
                self.switches[key].rect.y = big_text_rect.top + 5
            if key in self.arrows:
                self.arrows[key].rect.y = big_text_rect.top + 5
        self.display_surface.blit(text_surf, text_rect)
        # selected
        if index == text_index:
            pygame.draw.rect(self.display_surface, 'black', bg_rect, 4, 4)
            pygame.draw.rect(self.display_surface, 'white', big_rect, 4, 4)
    def main_menu_title(self):
        text_surf = self.font.render('Settings', False, 'Black')
        text_rect = text_surf.get_frect(midtop=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 20))

        pygame.draw.rect(self.display_surface, 'White', text_rect.inflate(10, 10), 0, 4)
        self.display_surface.blit(text_surf, text_rect)

    def update(self):
        self.input()
        self.main_menu_title()
        
        for text_index, text_surf in enumerate(self.text_surfs):
            top = self.main_rect.top + text_index * (text_surf.get_height() + (self.padding * 2) + self.space)
            self.show_entry(text_surf, top, self.index, text_index)

    def volume_function(self, value):
        self.sounds["music"].set_volume(value/1000)
        self.sounds["ambience"].set_volume(value/1000)
        for sound in self.sounds:
            if sound != "music" or sound != "ambience":
                self.sounds[sound].set_volume(value/100)

    def ambience_function(self, is_on):
        if not is_on:
            if self.sounds["ambience"].is_busy():
                self.sounds["ambience"].stop()
        elif is_on:
            if not self.sounds["ambience"].is_busy():
                self.sounds["ambience"].play(-1)

    def music_function(self, is_on):
        if not is_on:
            if self.sounds["music"].is_busy():
                self.sounds["music"].stop()
        elif is_on:
            if not self.sounds["music"].is_busy():
                self.sounds["music"].play(-1)

    def muteifnotfocused_function(self, is_on):
        return is_on
    
class Slider:
    def __init__(self, x, y, width, height, min_value, max_value, initial_value, function):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.clicking = False
        self.knob_radius = 10
        self.function = function

    def draw(self, surface):
        pygame.draw.rect(surface, (220, 185, 138), self.rect, 0, 4)
        pygame.draw.rect(surface, (243, 229, 194), self.rect.inflate(-4, -4), 0, 4)
        knob_x = self.rect.left + (self.rect.width - 10) * (self.value - self.min_value) / (self.max_value - self.min_value)
        pygame.draw.circle(surface, (232, 207, 166), (int(knob_x), self.rect.centery), self.knob_radius)

    def handle_event(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.clicking = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.clicking = False
            elif event.type == pygame.MOUSEMOTION and self.clicking:
                self.value = self.min_value + (self.max_value - self.min_value) * (event.pos[0] - self.rect.left) / (self.rect.width - 10)
                self.value = max(self.min_value, min(self.max_value, self.value))
                self.function(self.value)
    def get_value(self):
        return self.value

class Arrow:
    def __init__(self, x, y, width, height, items, sounds, function):
        self.rect = pygame.Rect(x, y, width, height + 10)
        self.items = items
        self.index = 0
        self.sounds = sounds
        self.arrow_width = 10
        self.arrow_height = 10
        self.font = import_font(20, 'font/LycheeSoda.ttf')
        self.clicking = False
        self.function = function

    def draw(self, surface):
        # Draw left arrow
        pygame.draw.polygon(surface, 'Black', [
            (self.rect.left, self.rect.top + self.arrow_height // 2 + 5),
            (self.rect.left + self.arrow_width, self.rect.top + 5),
            (self.rect.left + self.arrow_width, self.rect.top + self.arrow_height + 5)
        ])
        # Draw right arrow
        pygame.draw.polygon(surface, 'Black', [
            (self.rect.right - self.arrow_width, self.rect.top + 5),
            (self.rect.right, self.rect.top + self.arrow_height // 2 + 5),
            (self.rect.right - self.arrow_width, self.rect.top + self.arrow_height + 5)
        ])
        # Draw current index value
        text_surf = self.font.render(str(self.items[self.index]), False, 'Black')
        text_rect = text_surf.get_rect(center=(self.rect.centerx-5, self.rect.y + (text_surf.get_height()/2)))
        surface.blit(text_surf, text_rect)

    def handle_event(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.clicking = True
            if event.type == pygame.MOUSEBUTTONUP and self.clicking:
                self.clicking = False
                if self.rect.collidepoint(event.pos):
                    if event.pos[0] < self.rect.centerx:
                        self.index = max(0, self.index - 1)
                    else:
                        self.index = min(len(self.items) - 1, self.index + 1)
                    self.sounds['axe'].play()
                    self.function(self.index)

    def get_status(self):
        return self.items[self.index]

class Switch:
    def __init__(self, x, y, width, height, on_color, off_color, sounds, function):
        x += 170
        self.rect = pygame.Rect(x, y, width, height)
        self.on_color = on_color
        self.off_color = off_color
        self.sounds = sounds
        self.is_on = False
        self.clicking = False
        self.circle_radius = 10
        self.circle_x = x + 10
        self.function = function

    def draw(self, surface):
        # Draw background rectangle with rounded edges
        pygame.draw.rect(surface, (220, 185, 138), self.rect, 0, 20)
        # Draw circle
        if self.is_on:
            pygame.draw.circle(surface, self.on_color, (self.circle_x+20, self.rect.centery), self.circle_radius)
        else:
            pygame.draw.circle(surface, self.off_color, (self.circle_x, self.rect.centery), self.circle_radius)
    def handle_event(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.clicking = True
            if event.type == pygame.MOUSEBUTTONUP and self.clicking:
                self.clicking = False
                self.is_on = not self.is_on
                self.sounds['axe'].play()
                self.function(self.is_on)

    def get_status(self):
        return self.is_on