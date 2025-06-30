import pygame

class Player:
    def __init__(self, name, current_width, current_height):
        self.name = name
        
        # Position (center of screen)
        self.x = current_width // 2
        self.y = current_height // 2
        
        # Size
        self.width = 50
        self.height = 50
        
        # Movement speed
        self.speed = 5
        
    def update(self, keys_pressed, current_width, current_height):
        """Update player position based on key presses"""
        # Handle movement
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            self.x -= self.speed
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            self.x += self.speed
        if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
            self.y -= self.speed
        if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
            self.y += self.speed
            
        # Keep player on screen
        self.x = max(self.width // 2, min(current_width - self.width // 2, self.x))
        self.y = max(self.height // 2, min(current_height - self.height // 2, self.y))
        
    def draw(self, surface, text_font, BLUE, BLACK, WHITE):
        """Draw the player as a simple colored rectangle"""
        # Draw player body
        player_rect = pygame.Rect(
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.width,
            self.height
        )
        pygame.draw.rect(surface, BLUE, player_rect)
        pygame.draw.rect(surface, BLACK, player_rect, 2)  # Border
        
        # Draw player name above
        name_surface = text_font.render(self.name, True, WHITE)
        surface.blit(name_surface, (
            self.x - name_surface.get_width() // 2,
            self.y - self.height // 2 - name_surface.get_height() - 5
        ))