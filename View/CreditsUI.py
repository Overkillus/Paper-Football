import pygame
import Settings




pygame.init()


class CreditsUI:
    """
    Class representing Credits view
    """

    # Art
    title = pygame.font.SysFont('comicsansms', 50)
    font = pygame.font.SysFont('comicsansms', 18)
    exit_icon = pygame.image.load("Art/Neon/exit2.png")
    next_icon = pygame.transform.flip(exit_icon, True, False)
    credits1 = pygame.image.load("Art/Neon/credits1_screen.png")
    credits2 = pygame.image.load("Art/Neon/credits2_screen.png")

    def __init__(self, controller):
        # State
        self.is_running = False
        self.credits_page = 1

        # Context
        self.screen = controller.screen
        self.controller = controller
        self.exit_icon_rect = self.exit_icon.get_rect()
        self.next_icon_rect = self.next_icon.get_rect()
        self.credits_rect = self.credits1.get_rect()

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
                if self.exit_icon_rect.collidepoint(pygame.mouse.get_pos()):
                    if self.credits_page > 1:
                        self.credits_page -= 1
                    else:
                        self.controller.change_view(self.controller.menuUI)
                if self.next_icon_rect.collidepoint(pygame.mouse.get_pos()):
                    if self.credits_page < 2:
                        self.credits_page += 1

    def update(self):
        # Layout helper variables
        sw = self.screen.get_width()
        sh = self.screen.get_height()

        self.exit_icon_rect.topleft = (20, 20)
        self.next_icon_rect.topright = (sw-20, 20)
        self.credits_rect.center = (sw/2, sh/2)

    def render(self):
        # Clear screen
        self.screen.fill((3, 15, 56))

        # Credits Screen
        if self.credits_page == 1:
            self.screen.blit(self.credits1, self.credits_rect)
        elif self.credits_page ==2:
            self.screen.blit(self.credits2, self.credits_rect)

        # Button
        self.screen.blit(self.exit_icon, self.exit_icon_rect)
        self.screen.blit(self.next_icon, self.next_icon_rect)

        # Show new frame
        pygame.display.flip()
