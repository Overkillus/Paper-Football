import sys
import pygame
import Settings

pygame.init()


class LobbyUI:
    """
    Class representing Lobby view
    """

    # Art
    exitIcon = pygame.image.load('Art/exit2.png')

    def __init__(self, controller):
        # State
        self.is_running = False

        # Context
        self.screen = controller.screen
        self.controller = controller

        # Exit
        self.exit_button = self.exitIcon.get_rect()


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
                self.controller.change_view(self.controller.menuUI)
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                # Back button
                if self.exit_button.collidepoint(mouse_pos):
                    self.controller.change_view(self.controller.menuUI)


    def update(self):
        # Exit
        self.exit_button.topleft = (20, 20)


    def render(self):
        sw = self.screen.get_width()
        sh = self.screen.get_height()

        # Clear screen
        self.screen.fill((255, 182, 193))

        # Exit Icon
        self.screen.blit(self.exitIcon, self.exit_button)

        pygame.display.flip()