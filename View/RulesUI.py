import sys
import pygame
import Colours
import Settings

pygame.init()


class RulesUI:
    """
    Class representing Rules view
    """

    # --- Art ---
    missing_texture = pygame.image.load("Art/missing-texture.png") # Placeholder texture (actual textures loaded later based on theme)
    # Buttons
    exit_icon = missing_texture
    # Background
    rules = missing_texture
    # Font
    title = pygame.font.SysFont('comicsansms', 50)
    font = pygame.font.SysFont('comicsansms', 18)

    def __init__(self, controller):

        # Theme
        self.theme = Settings.theme

        self.load_textures()

        # State
        self.is_running = False

        # Context
        self.screen = controller.screen
        self.controller = controller
        self.exit_icon_rect = self.exit_icon.get_rect()
        self.rules_rect = self.rules.get_rect()

    def main(self):
        self.event_handler()
        # Ticking
        self.controller.delta_time += self.controller.clock.tick() / 1000.0
        while self.controller.delta_time > 1 / Settings.max_tps:
            self.controller.delta_time -= 1 / Settings.max_tps
            self.update()
            self.render()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.controller.close_game()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.controller.change_view(self.controller.gameUI)
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.exit_icon_rect.collidepoint(pygame.mouse.get_pos()):
                    self.controller.change_view(self.controller.gameUI)

    def update(self):

        # Check for theme change
        if self.theme != Settings.theme:
            self.load_textures()
            self.theme = Settings.theme

        # Layout helper variables
        sw = self.screen.get_width()
        sh = self.screen.get_height()

        self.exit_icon_rect.bottomright = (sw - 20, sh - 20)
        self.rules_rect.center = (sw/2, sh/2)

    def render(self):
        # Clear screen
        if Settings.theme == "neon":
            self.screen.fill((3, 15, 56))
        elif Settings.theme == "paper":
            self.screen.fill((236, 214, 192))
        elif Settings.theme == "football":
            self.screen.fill((19, 7, 0))

        # Background
        self.screen.blit(self.rules, self.rules_rect)

        # Button
        self.screen.blit(self.exit_icon, self.exit_icon_rect)

        # Show new frame
        pygame.display.flip()

    def load_textures(self):
        # Path based on current theme
        path = "Art/" + Settings.theme

        # Load appropriate textures
        RulesUI.exit_icon = pygame.image.load(path+"/exit2.png")
        RulesUI.rules = pygame.image.load(path+"/game_rules.png")

