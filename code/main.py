import pygame
from random import randint

class Pokemon(pygame.sprite.Sprite):
    def __init__(self, name, level, face, screen):
        super().__init__()
        self.screen = screen
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.pokemon = name
        self.image = pygame.image.load(f'../graphics/{name}_{face}.png').convert_alpha()
        self.health_box_surf = pygame.image.load('../graphics/info_display_box.png').convert_alpha()
        self.face = face

        if face == "front":
            self.rect = self.image.get_rect(topright = (self.screen_width - 40, 20))
            self.health_box_rect = self.health_box_surf.get_rect(topleft = (40, 40))
        else:
            self.rect = self.image.get_rect(bottomleft = (40, self.screen_height - 20))
            self.health_box_rect = self.health_box_surf.get_rect(bottomright = (self.screen_width - 40, self.screen_height - 40))
        self.level = level

        # Pokemon data import
        f = open('../data/pokemon_data.txt', "r")
        for line in f.readlines():
            if line[0:len(name)] == name:
                data = line.strip('\n').split('\t')
                self.base_hp = int(data[1])
                self.base_atk = int(data[2])
                self.base_def = int(data[3])
                self.base_sp_atk = int(data[4])
                self.base_sp_def = int(data[5])
                self.base_speed = int(data[6])
                break
        f.close()

        # Pokemon IV values
        self.hp_IV = randint(0,31)
        self.atk_IV = randint(0,31)
        self.def_IV = randint(0,31)
        self.sp_atk_IV = randint(0,31)
        self.sp_def_IV = randint(0,31)
        self.speed_IV = randint(0,31)

        # Pokemon stat calculation for specific level
        self.hp = int(((2 * self.base_hp + self.hp_IV) * self.level) / 100 + self.level + 10)
        self.atk = int(((2 * self.base_atk + self.atk_IV) * self.level) / 100 + 5)
        self.defense = int(((2 * self.base_def + self.def_IV) * self.level) / 100 + 5)
        self.sp_atk = int(((2 * self.base_sp_atk + self.sp_atk_IV) * self.level) / 100 + 5)
        self.sp_def = int(((2 * self.base_sp_def + self.sp_def_IV) * self.level) / 100 + 5)
        self.speed = int(((2 * self.base_speed + self.speed_IV) * self.level) / 100 + 5)

        # HP box information
        self.hp_box_x_pos = 43
        self.hp_box_y_pos = 63
        self.hp_rect = pygame.Rect(self.hp_box_x_pos, self.hp_box_y_pos,135,7)
        self.current_hp = self.hp
        self.target_hp = self.hp
        self.font = pygame.font.Font('../fonts/VCR_OSD_MONO.ttf', 18)

        self.name_surf = self.font.render(self.pokemon.capitalize(), True, (0,0,0))
        self.name_rect = self.name_surf.get_rect(topleft = (18,18))

        self.level_surf = self.font.render(f"Lv{self.level}", True, (0,0,0))
        self.level_rect = self.level_surf.get_rect(topright = (178, 18))

        print(self.hp)

    def update(self):
        self.display_health_box()
        self.get_damaged(10)
        self.get_healed(1)


    def level_up(self):
        self.level += 1
        self.hp = int(((2 * self.base_hp + self.hp_IV) * self.level) / 100 + self.level + 10)
        self.atk = int(((2 * self.base_atk + self.atk_IV) * self.level) / 100 + 5)
        self.defense = int(((2 * self.base_def + self.def_IV) * self.level) / 100 + 5)
        self.sp_atk = int(((2 * self.base_sp_atk + self.sp_atk_IV) * self.level) / 100 + 5)
        self.sp_def = int(((2 * self.base_sp_def + self.sp_def_IV) * self.level) / 100 + 5)
        self.speed = int(((2 * self.base_speed + self.speed_IV) * self.level) / 100 + 5)

    def display_health_box(self):
        if self.target_hp > self.current_hp:
            self.current_hp += self.hp * 0.02
            if self.target_hp < self.current_hp: self.current_hp = self.target_hp
        elif self.target_hp < self.current_hp:
            self.current_hp -= self.hp * 0.02
            if self.target_hp > self.current_hp: self.current_hp = self.target_hp

        self.health_box_surf = pygame.image.load('../graphics/info_display_box.png').convert_alpha()
        if self.face == "front":
            self.health_box_rect = self.health_box_surf.get_rect(topleft = (40, 40))
        else:
            self.health_box_rect = self.health_box_surf.get_rect(bottomright = (self.screen_width - 40, self.screen_height - 40))

        if self.current_hp / self.hp > 0.5:
            health_color = (0,255,0)
        elif self.current_hp / self.hp > 0.2:
            health_color = (255,155,0)
        else:
            health_color = (255,0,0)

        if self.face == "back":
            self.health_text_surf = self.font.render(f"{int(self.current_hp)}/{self.hp}", True, (0,0,0))
            self.health_text_rect = self.health_text_surf.get_rect(topright = (178,74))
            self.health_box_surf.blit(self.health_text_surf, self.health_text_rect)

        health_width = int(self.current_hp / self.hp * 135)
        self.hp_rect = pygame.Rect(self.hp_box_x_pos, self.hp_box_y_pos,health_width,7)
        pygame.draw.rect(self.health_box_surf, health_color, self.hp_rect)
        self.health_box_surf.blit(self.name_surf, self.name_rect)
        self.health_box_surf.blit(self.level_surf, self.level_rect)
        self.screen.blit(self.health_box_surf, self.health_box_rect)

    def get_damaged(self, amount):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.target_hp -= amount
            if self.target_hp <= 0: self.target_hp = 0


    def get_healed(self, amount):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.target_hp += amount
            if self.target_hp >= self.hp: self.target_hp = self.hp
