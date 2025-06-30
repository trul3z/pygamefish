import pygame
import sys
import os

# Import from start_screen
from start_screen import (
    current_width, current_height, screen, clock, FPS, WHITE, BLACK, BLUE, 
    RED, GREEN, LIGHT_GREEN, LIGHT_BLUE, GRAY, text_font, button_font, scale_fonts,
    toggle_maximized, Button, maximized, MAX_WIDTH, MAX_HEIGHT, DEFAULT_WIDTH, DEFAULT_HEIGHT
)

# Import Player class from player module
from player import Player

class PauseMenu:
    def __init__(self):
        self.create_buttons()
        
    def create_buttons(self):
        """Create all buttons with correct positions"""
        # Create buttons for pause menu
        button_width = 0.25  # 25% of screen width
        button_height = 0.08  # 8% of screen height
        button_x = 0.5 - (button_width / 2)  # Centered horizontally
        
        # Resume button
        self.resume_button = Button(
            button_x, 0.4,  # x%, y%
            button_width, button_height,
            "Resume", GREEN, LIGHT_GREEN,
            self.resume_action
        )
        
        # Start Over button
        self.start_over_button = Button(
            button_x, 0.5,  # x%, y%
            button_width, button_height,
            "Start Over", BLUE, LIGHT_BLUE,
            self.start_over_action
        )
        
        # Quit button
        self.quit_button = Button(
            button_x, 0.6,  # x%, y%
            button_width, button_height,
            "Quit", RED, (255, 100, 100),
            self.quit_action
        )
        
        # Action results
        self.result = None
        
    def resume_action(self):
        self.result = "resume"
        
    def start_over_action(self):
        self.result = "start_over"
        
    def quit_action(self):
        self.result = "quit"
        
    def update_buttons(self):
        """Completely recreate buttons for new screen dimensions"""
        # This more thoroughly updates button positions for new screen sizes
        self.create_buttons()
        
    def handle_events(self, events):
        """Handle pause menu events"""
        mouse_pos = pygame.mouse.get_pos()
        
        # Check button hover states
        self.resume_button.check_hover(mouse_pos)
        self.start_over_button.check_hover(mouse_pos)
        self.quit_button.check_hover(mouse_pos)
        
        for event in events:
            # Handle button clicks
            self.resume_button.handle_event(event)
            self.start_over_button.handle_event(event)
            self.quit_button.handle_event(event)
            
            # REMOVE the ESC key handling here
            # We'll let the main game loop handle ESC
                
        return self.result
        
    def draw(self, surface):
        """Draw the pause menu"""
        # Semi-transparent overlay
        overlay = pygame.Surface((current_width, current_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Dark semi-transparent background
        surface.blit(overlay, (0, 0))
        
        # Draw title
        title_text = button_font.render("PAUSED", True, WHITE)
        title_rect = title_text.get_rect(center=(current_width // 2, current_height * 0.3))
        surface.blit(title_text, title_rect)
        
        # Draw buttons
        self.resume_button.draw(surface)
        self.start_over_button.draw(surface)
        self.quit_button.draw(surface)

def run_game(player_name):
    """Main game function that runs when Start Game is pressed"""
    # Make variables global 
    global screen, current_width, current_height, maximized
    
    # Set initial window size based on maximized state
    if maximized:
        current_width = MAX_WIDTH
        current_height = MAX_HEIGHT
    else:
        current_width = DEFAULT_WIDTH
        current_height = DEFAULT_HEIGHT
        
    # Recreate the screen with the right dimensions
    screen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)
    pygame.display.set_caption("fishgame.")
    
    # Create the player - pass screen dimensions
    player = Player(player_name, current_width, current_height)
    
    # Pause menu
    pause_menu = PauseMenu()
    paused = False
    
    # Add a key tracking variable to detect NEW keypresses
    last_keys = pygame.key.get_pressed()

    # Main game loop
    running = True
    while running:
        # Get current keyboard state
        current_keys = pygame.key.get_pressed()
        
        # Get events
        events = pygame.event.get()
        
        # Process quit event
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE and not fullscreen:
                # Calculate player's relative position before resizing
                player_rel_x = player.x / current_width
                player_rel_y = player.y / current_height
                
                # Only handle manual resizing in windowed mode
                current_width, current_height = event.size
                screen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)
                
                # Update prev_width and prev_height for proper fullscreen exit
                prev_width = current_width
                prev_height = current_height
                
                # Scale everything for new size
                scale_fonts(current_width, current_height)
                pause_menu.update_buttons()
                
                # Reposition player using relative coordinates
                player.x = int(player_rel_x * current_width)
                player.y = int(player_rel_y * current_height)
        
        # Handle ESC key - check for NEW press (was up, now down)
        if current_keys[pygame.K_ESCAPE] and not last_keys[pygame.K_ESCAPE]:
            if not paused:
                # Only pause if not already paused
                paused = True
                pause_menu.result = None
        
        # Handle F11 key - check for NEW press
        if current_keys[pygame.K_F11] and not last_keys[pygame.K_F11]:
            # F11 toggles true fullscreen
            fullscreen = not fullscreen
            
            if fullscreen:
                # Store current window size before going fullscreen
                prev_width = current_width
                prev_height = current_height
                
                # Calculate player's relative position before changing screen size
                player_rel_x = player.x / current_width
                player_rel_y = player.y / current_height
                
                # Switch to true fullscreen
                screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                
                # Get the new dimensions
                current_width, current_height = screen.get_size()
            else:
                # Calculate player's relative position before changing screen size
                player_rel_x = player.x / current_width
                player_rel_y = player.y / current_height
                
                # Switch back to windowed mode
                if maximized:
                    current_width = MAX_WIDTH
                    current_height = MAX_HEIGHT
                else:
                    current_width = DEFAULT_WIDTH
                    current_height = DEFAULT_HEIGHT
                
                screen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)
            
            # Scale fonts for new screen size
            scale_fonts(current_width, current_height)
            
            # Update pause menu buttons
            pause_menu.update_buttons()
            
            # Reposition player using relative coordinates
            player.x = int(player_rel_x * current_width)
            player.y = int(player_rel_y * current_height)
            
        # FIRST: Clear the screen
        screen.fill(background_color)
        
        # SECOND: Get input and update player when not paused
        if not paused:
            player.update(current_keys, current_width, current_height)  # Use current_keys instead of getting them again
        
        # THIRD: Draw the player
        player.draw(screen, text_font, BLUE, BLACK, WHITE)
        
        # FOURTH: Draw instructions
        instructions = [
            "Use WASD or Arrow Keys to move",
            "ESC: Pause menu",
            "F11: Toggle fullscreen"
        ]
        
        for i, instruction in enumerate(instructions):
            text_surface = text_font.render(instruction, True, WHITE)
            screen.blit(text_surface, (20, 20 + i * 30))
        
        # FIFTH: Draw pause menu on top if paused
        if paused:
            result = pause_menu.handle_events(events)
            pause_menu.draw(screen)
            
            # Handle pause menu results
            if result == "resume":
                paused = False
                pause_menu.result = None
            elif result == "start_over":
                # Return to start screen
                return True
            elif result == "quit":
                pygame.quit()
                sys.exit()
        
        # FINALLY: Update display
        pygame.display.flip()
        
        # Store current keys for next frame
        last_keys = current_keys
        
        # Cap framerate
        clock.tick(FPS)
    
    # Return to main menu
    return True