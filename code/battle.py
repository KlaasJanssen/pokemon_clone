import pygame, sys
from pokemon import Pokemon

class Battle():
    def __init__(pokemon1, pokemon2):
        pass

if __name__ == "__main__":
    screen_width = 500
    screen_height = 500
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    trainer_pokemon = pygame.sprite.Group()
    pokemon1 = Pokemon("wizard", 5, "front", screen)
    pokemon2 = Pokemon("wizard", 95, "back", screen)
    trainer_pokemon.add(pokemon1)
    trainer_pokemon.add(pokemon2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((240,240,240))
        trainer_pokemon.draw(screen)
        trainer_pokemon.update()
        pygame.display.update()
        clock.tick(60)
