import pygame
import sys
import random
import os
import math
import shutil
from PIL import Image, ImageSequence # We'll use Pillow to process the GIF
from PIL.Image import Resampling

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()

# Get monitor info
info = pygame.display.Info()
MONITOR_WIDTH = info.current_w
MONITOR_HEIGHT = info.current_h

# Game constants - default windowed size
DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 600
FPS = 60

# Maximized window will be slightly smaller than full monitor size to account for taskbar and borders
MAX_WIDTH = MONITOR_WIDTH - 80
MAX_HEIGHT = MONITOR_HEIGHT - 80

# Track window state - start maximized by default
maximized = True
current_width = MAX_WIDTH
current_height = MAX_HEIGHT

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 100, 255)
GREEN = (0, 128, 0)
LIGHT_GREEN = (100, 255, 100)
GRAY = (150, 150, 150)
LIGHT_GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Audio settings
music_volume = 0.1  # 50% volume by default
sfx_volume = 0.7   # 70% volume by default for SFX

# Create the screen (initially maximized but still a regular window)
screen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)
pygame.display.set_caption("fishgame.")
clock = pygame.time.Clock()

# Create asset directories if they don't exist
if not os.path.exists('assets'):
    os.makedirs('assets')
if not os.path.exists('assets/music'):
    os.makedirs('assets/music')
if not os.path.exists('assets/sounds'):
    os.makedirs('assets/sounds')
if not os.path.exists('assets/images'):
    os.makedirs('assets/images')
if not os.path.exists('assets/fonts'):
    os.makedirs('assets/fonts')
if not os.path.exists('assets/animations'):
    os.makedirs('assets/animations')

# Check if maintheme.mp3 exists in root, if so, move it to assets/music
if os.path.exists('maintheme.mp3') and not os.path.exists('assets/music/maintheme.mp3'):
    shutil.move('maintheme.mp3', 'assets/music/maintheme.mp3')

# Check if mainmenu.gif exists in root, if so, move it to assets/animations
if os.path.exists('mainmenu.gif') and not os.path.exists('assets/animations/mainmenu.gif'):
    shutil.move('mainmenu.gif', 'assets/animations/mainmenu.gif')

# Music file path
main_theme_path = 'assets/music/maintheme.mp3'

pop_drip_sound = None
digi_plink_sound = None
click_04_sound = None
start_game_sound = None

# Check if pop_drip.wav exists in root, if so, move it to assets/sounds
if os.path.exists('pop_drip.wav') and not os.path.exists('assets/sounds/pop_drip.wav'):
    shutil.move('pop_drip.wav', 'assets/sounds/pop_drip.wav')

# Check if digi_plink.wav exists in root, if so, move it to assets/sounds  
if os.path.exists('digi_plink.wav') and not os.path.exists('assets/sounds/digi_plink.wav'):
    shutil.move('digi_plink.wav', 'assets/sounds/digi_plink.wav')

# Check if click_04.wav exists in root, if so, move it to assets/sounds
if os.path.exists('click_04.wav') and not os.path.exists('assets/sounds/click_04.wav'):
    shutil.move('click_04.wav', 'assets/sounds/click_04.wav')
    shutil.move('click_04.wav', 'assets/sounds/click_04.wav')

if os.path.exists('start_game.wav') and not os.path.exists('assets/sounds/start_game.wav'):
    shutil.move('start_game.wav', 'assets/sounds/start_game.wav')

# Load sound effects
if os.path.exists('assets/sounds/pop_drip.wav'):
    pop_drip_sound = pygame.mixer.Sound('assets/sounds/pop_drip.wav')
    pop_drip_sound.set_volume(0.5 * sfx_volume) 
else:
    print("Warning: pop_drip.wav not found. Bubble sounds will not play.")

if os.path.exists('assets/sounds/digi_plink.wav'):
    digi_plink_sound = pygame.mixer.Sound('assets/sounds/digi_plink.wav')
    digi_plink_sound.set_volume(0.5 * sfx_volume) 
else:
    print("Warning: digi_plink.wav not found. Button sounds will not play.")

if os.path.exists('assets/sounds/click_04.wav'):
    click_04_sound = pygame.mixer.Sound('assets/sounds/click_04.wav')
    click_04_sound.set_volume(0.7 * sfx_volume)  # Slightly louder for button clicks
else:
    print("Warning: click_04.wav not found. Random name button click sound will not play.")
if os.path.exists('assets/sounds/start_game.wav'):
    start_game_sound = pygame.mixer.Sound('assets/sounds/start_game.wav')
    start_game_sound.set_volume(0.8 * sfx_volume)  # Slightly louder for game start
else:
    print("Warning: start_game.wav not found. Start game button sound will not play.")

# Start the music if file exists
if os.path.exists(main_theme_path):
    pygame.mixer.music.load(main_theme_path)
    pygame.mixer.music.set_volume(music_volume)
    pygame.mixer.music.play(-1)  # Loop indefinitely
else:
    print(f"Warning: {main_theme_path} not found. Music will not play.")

# Font sizes (will be scaled based on resolution)
TITLE_SIZE = 64
BUTTON_SIZE = 36
TEXT_SIZE = 28
INPUT_SIZE = 32

# Fonts - these will be recreated when resolution changes
title_font = pygame.font.Font(None, TITLE_SIZE)
button_font = pygame.font.Font(None, BUTTON_SIZE)
text_font = pygame.font.Font(None, TEXT_SIZE)
input_font = pygame.font.Font(None, INPUT_SIZE)

# Scale fonts for initial screen size
def scale_fonts(width, height):
    """Scale font sizes based on screen resolution"""
    global title_font, button_font, text_font, input_font
    
    # Calculate scale factor (using the smaller dimension)
    scale_factor = min(width / DEFAULT_WIDTH, height / DEFAULT_HEIGHT)
    
    # Scale font sizes, but ensure minimum sizes
    title_size = max(32, int(TITLE_SIZE * scale_factor))
    button_size = max(18, int(BUTTON_SIZE * scale_factor))
    text_size = max(14, int(TEXT_SIZE * scale_factor))
    input_size = max(16, int(INPUT_SIZE * scale_factor))
    
    # Create new fonts with scaled sizes
    title_font = pygame.font.Font(None, title_size)
    button_font = pygame.font.Font(None, button_size)
    text_font = pygame.font.Font(None, text_size)
    input_font = pygame.font.Font(None, input_size)

# Initialize fonts for the current screen size
scale_fonts(current_width, current_height)

class AnimatedGIF:
    def __init__(self, gif_path, scale_factor=1.0):
        self.frames = []
        self.current_frame = 0
        self.frame_delay = 0
        self.last_update_time = 0
        self.scale_factor = scale_factor
        self.load_gif(gif_path)
        
    def load_gif(self, gif_path):
        """Load frames from a GIF file"""
        if not os.path.exists(gif_path):
            print(f"Warning: GIF file not found: {gif_path}")
            return
            
        try:
            # Open the GIF file
            gif = Image.open(gif_path)
            
            # Get all frames
            for frame in ImageSequence.Iterator(gif):
                # Convert frame to RGBA mode (for transparency)
                frame_rgba = frame.convert("RGBA")
                
                # Scale the frame if needed
                if self.scale_factor != 1.0:
                    new_size = (
                        int(frame_rgba.width * self.scale_factor), 
                        int(frame_rgba.height * self.scale_factor)
                    )
                    frame_rgba = frame_rgba.resize(new_size, Resampling.LANCZOS)
                
                # Convert PIL image to pygame surface
                frame_data = frame_rgba.tobytes()
                frame_size = frame_rgba.size
                pygame_frame = pygame.image.fromstring(
                    frame_data, frame_size, "RGBA"
                )
                
                # Store the frame
                self.frames.append(pygame_frame)
                
            # Get the frame delay time (in milliseconds)
            # Default to 100ms if not specified
            self.frame_delay = gif.info.get('duration', 100)
            
            # Initialize the last update time
            self.last_update_time = pygame.time.get_ticks()
            
            print(f"Successfully loaded GIF with {len(self.frames)} frames")
            
        except Exception as e:
            print(f"Error loading GIF: {e}")
            
    def update(self):
        """Update the animation frame"""
        if not self.frames:
            return
            
        current_time = pygame.time.get_ticks()
        
        # Check if it's time to advance to the next frame
        if current_time - self.last_update_time > self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update_time = current_time
            
    def draw(self, surface, position):
        """Draw the current frame at the specified position"""
        if not self.frames:
            return
            
        # Center the frame horizontally
        frame = self.frames[self.current_frame]
        x = position[0] - frame.get_width() // 2
        y = position[1]
        
        # Draw the frame
        surface.blit(frame, (x, y))
        
    def get_size(self):
        """Get the size of the current frame"""
        if not self.frames:
            return (0, 0)
        return self.frames[self.current_frame].get_size()

# First and last name lists from main.py
first_names = [
    "Fisher", "Marina", "River", "Brook", "Sailor", "Pike", "Fresno", "Prophet", "Philip", "Kodak", "Sebastian", "Biscuit",
    "Bass", "Finn", "Rod", "Reel", "Anchor", "Tide", "Storm", "Wave", "Current", "Pirate",
    "Depth", "Coral", "Pearl", "Shell", "Drift", "Harbor", "Bay", "Coast", "Barnacle", "Sarge", "Colonel", "Major", "General", "Admiral", "Lieutenant", "Captain", "First Mate",
    "Reef", "Marlin", "Tuna", "Cod", "Salmon", "Trout", "Carp", "Minnow", "Clitoris", "Maximus", "Octopus", "Squid", "Dolphin", "Seal", "Turtle", "Starfish", "Jellyfish", "Diddy",
    "Whale", "Shark", "Ray", "Eel", "Crab", "Lobster", "Shrimp", "Kelp","Cthulu","Stinky","Big","Fishy","Bubbles","Splash","Gills","Finley","Hook","Reelina","Tidal","Nautical","Muhammad","Jesus","Lil", "Truck", "Big Back", "Ford", "Tyler", "Bubba", "Koda", "Marco", "Duke", "Gilligan", "Dick", "Philly", "Sarah", "Flounder"
]

last_names = [
    "Angler", "Caster", "Fisher", "Netsman", "Hooker", "Baiter", "Reeler", "Driftwood", "Leaf",
    "Sailor", "Mariner", "Seaman", "Captain", "Navigator", "Helmsman", "White", "Black",
    "Tidewatcher", "Stormrider", "Wavebreaker", "Deepdiver", "Surfcaster",
    "Linecaster", "Rodmaster", "Baitlord", "Catchall", "Bigfish", "Longline", "Booty",
    "Sinker", "Floater", "Dragnetter", "Spearman", "Harpoon", "Tackle", "Maximus", "Squarepants",
    "Lighthouse", "Portside", "Starboard", "Windward", "Leeward", "Offshore","Cthulu","Jackson","Texas", "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Martinez", "Davis", "Rodriguez", "Wilson", "Anderson", "Thomas", "Moore", "Martin", "Lee", "Perez", "Big Back", "Buster", "Military", "Taylor", "Chimichanga"
]

def generate_random_name():
    """Generate a random fish-themed name using first and last name components"""
    first = random.choice(first_names)
    last = random.choice(last_names)
    return f"{first} {last}"

def toggle_maximized():
    """Toggle between maximized window and smaller window"""
    global screen, maximized, current_width, current_height
    
    if maximized:
        # Switch to smaller window
        current_width = DEFAULT_WIDTH
        current_height = DEFAULT_HEIGHT
        screen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)
    else:
        # Switch to maximized window (still resizable)
        current_width = MAX_WIDTH
        current_height = MAX_HEIGHT
        screen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)
    
    # Update the maximized flag
    maximized = not maximized
    
    # Scale fonts for new resolution
    scale_fonts(current_width, current_height)

def set_music_volume(volume):
    """Set the music volume (0.0 to 1.0)"""
    global music_volume
    music_volume = max(0.0, min(1.0, volume))  # Clamp between 0 and 1
    pygame.mixer.music.set_volume(music_volume)

def set_sfx_volume(volume):
    """Set the SFX volume (0.0 to 1.0)"""
    global sfx_volume
    sfx_volume = max(0.0, min(1.0, volume))  # Clamp between 0 and 1
    
    # Update all sound effect volumes
    if pop_drip_sound:
        pop_drip_sound.set_volume(0.5 * sfx_volume)
    if digi_plink_sound:
        digi_plink_sound.set_volume(0.5 * sfx_volume)
    if click_04_sound:
        click_04_sound.set_volume(0.7 * sfx_volume)
    if start_game_sound:
        start_game_sound.set_volume(0.7 * sfx_volume)

class Button:
    def __init__(self, x_percent, y_percent, width_percent, height_percent, text, color, hover_color, action=None):
        # Store percentages for resizing
        self.x_percent = x_percent
        self.y_percent = y_percent
        self.width_percent = width_percent
        self.height_percent = height_percent
        
        # Calculate actual rectangle based on current screen size
        self.update_rect()
        
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.is_hovered = False
        self.was_hovered = False  # Track previous hover state for sound
        
    def update_rect(self):
        """Update the button rectangle based on current screen dimensions"""
        x = int(current_width * self.x_percent)
        y = int(current_height * self.y_percent)
        width = int(current_width * self.width_percent)
        height = int(current_height * self.height_percent)
        self.rect = pygame.Rect(x, y, width, height)
        
    def draw(self, surface):
        # Draw button with hover effect
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)  # Border
        
        # Draw text
        text_surf = button_font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, mouse_pos):
        # Store previous hover state
        self.was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Play hover sound when mouse enters button (not when leaving)
        if self.is_hovered and not self.was_hovered and digi_plink_sound:
            digi_plink_sound.play()
        
        return self.is_hovered
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            # No sound here anymore - sound plays on hover instead
            if self.action:
                self.action()
            return True
        return False

class Slider:
    def __init__(self, x_percent, y_percent, width_percent, height_percent, min_value, max_value, initial_value, label):
        # Store percentages for resizing
        self.x_percent = x_percent
        self.y_percent = y_percent
        self.width_percent = width_percent
        self.height_percent = height_percent
        
        # Value range
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.label = label
        
        # Calculate actual rectangle based on current screen size
        self.update_rect()
        
        # Handle interaction
        self.active = False
        
    def update_rect(self):
        """Update the slider rectangle based on current screen dimensions"""
        x = int(current_width * self.x_percent)
        y = int(current_height * self.y_percent)
        width = int(current_width * self.width_percent)
        height = int(current_height * self.height_percent)
        self.rect = pygame.Rect(x, y, width, height)
        self.handle_radius = int(height * 1.5)
        
        # Calculate handle position based on current value
        value_percent = (self.value - self.min_value) / (self.max_value - self.min_value)
        self.handle_x = self.rect.x + int(value_percent * self.rect.width)
        
    def draw(self, surface):
        # Draw slider track
        track_rect = pygame.Rect(
            self.rect.x, 
            self.rect.y + self.rect.height // 2 - 2, 
            self.rect.width, 
            4
        )
        pygame.draw.rect(surface, GRAY, track_rect)
        
        # Draw filled part of the track
        filled_width = self.handle_x - self.rect.x
        filled_rect = pygame.Rect(
            self.rect.x, 
            self.rect.y + self.rect.height // 2 - 2, 
            filled_width, 
            4
        )
        pygame.draw.rect(surface, BLUE, filled_rect)
        
        # Draw handle
        pygame.draw.circle(
            surface, 
            LIGHT_BLUE if self.active else BLUE, 
            (self.handle_x, self.rect.y + self.rect.height // 2), 
            self.handle_radius
        )
        pygame.draw.circle(
            surface, 
            BLACK, 
            (self.handle_x, self.rect.y + self.rect.height // 2), 
            self.handle_radius, 
            2
        )
        
        # Draw label
        label_text = text_font.render(f"{self.label}: {int(self.value * 100)}%", True, WHITE)
        surface.blit(label_text, (self.rect.x, self.rect.y - label_text.get_height() - 5))
        
    def check_hover(self, mouse_pos):
        # Check if mouse is over the handle
        handle_rect = pygame.Rect(
            self.handle_x - self.handle_radius,
            self.rect.y + self.rect.height // 2 - self.handle_radius,
            self.handle_radius * 2,
            self.handle_radius * 2
        )
        
        # Store previous hover state if it doesn't exist
        if not hasattr(self, 'was_hovered'):
            self.was_hovered = False
        
        # Check current hover state
        is_currently_hovered = handle_rect.collidepoint(mouse_pos)
        
        # Play hover sound when mouse enters slider handle
        if is_currently_hovered and not self.was_hovered and digi_plink_sound:
            digi_plink_sound.play()
        
        # Update hover state
        self.was_hovered = is_currently_hovered
        
        return is_currently_hovered
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if mouse is over the handle
            if self.check_hover(event.pos):
                self.active = True
                return True
            
            # Check if click is on the track
            if self.rect.collidepoint(event.pos):
                # Set handle position directly to click position
                self.set_handle_position(event.pos[0])
                self.active = True
                return True
                
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.active:
                self.active = False
                return True
                
        elif event.type == pygame.MOUSEMOTION and self.active:
            # Update handle position based on mouse movement
            self.set_handle_position(event.pos[0])
            return True
            
        return False
    
    def set_handle_position(self, x_pos):
        # Constrain x position to track bounds
        x_pos = max(self.rect.x, min(self.rect.right, x_pos))
        
        # Update handle position
        self.handle_x = x_pos
        
        # Calculate and update value based on position
        value_percent = (self.handle_x - self.rect.x) / self.rect.width
        self.value = self.min_value + value_percent * (self.max_value - self.min_value)
        
        # Apply the value based on slider type
        if self.label == "Music Volume":
            set_music_volume(self.value)
        elif self.label == "SFX Volume":
            set_sfx_volume(self.value)

class InputBox:
    def __init__(self, x_percent, y_percent, width_percent, height_percent, text=''):
        # Store percentages for resizing
        self.x_percent = x_percent
        self.y_percent = y_percent
        self.width_percent = width_percent
        self.height_percent = height_percent
        
        # Calculate actual rectangle based on current screen size
        self.update_rect()
        
        self.color_inactive = GRAY
        self.color_active = LIGHT_BLUE
        self.color = self.color_inactive
        self.text = text
        self.active = False
        self.max_length = 30  # Prevent extremely long names
        
    def update_rect(self):
        """Update the input box rectangle based on current screen dimensions"""
        x = int(current_width * self.x_percent)
        y = int(current_height * self.y_percent)
        width = int(current_width * self.width_percent)
        height = int(current_height * self.height_percent)
        self.rect = pygame.Rect(x, y, width, height)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state if clicked
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_inactive
            return self.active
            
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    # Return the current text when Enter is pressed
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    # Remove last character when Backspace is pressed
                    self.text = self.text[:-1]
                else:
                    # Add typed character if it doesn't make the name too long
                    if len(self.text) < self.max_length:
                        self.text += event.unicode
        return False
    
    def draw(self, surface):
        # Draw the input box
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)  # Border
        
        # Render and center the text
        text_surf = input_font.render(self.text, True, BLACK)
        
        # Create a temporary rect for text positioning
        text_rect = text_surf.get_rect()
        text_rect.center = self.rect.center
        
        # Blit the text surface
        surface.blit(text_surf, text_rect)
        
        # Draw a blinking cursor when active
        if self.active and pygame.time.get_ticks() % 1000 < 500:
            # Calculate cursor position based on text width
            cursor_x = text_rect.centerx + text_surf.get_width() // 2 + 2
            cursor_y = text_rect.centery
            pygame.draw.line(surface, BLACK, 
                            (cursor_x, cursor_y - 10), 
                            (cursor_x, cursor_y + 10), 2)

class StartScreen:
    def __init__(self):
        self.current_name = generate_random_name()
        self.custom_input = ""  # Track custom user input
        self.use_custom_name = False  # Flag to track which name to use
        
        # Load the animated GIF
        self.logo_animation = AnimatedGIF('assets/animations/mainmenu.gif', scale_factor=10.0)
        
        # Create input box (x%, y%, width%, height%)
        self.input_box = InputBox(0.5 - 0.1875, 0.52, 0.4, 0.1, "")
        
        # Create buttons (x%, y%, width%, height%)
        self.regenerate_button = Button(
            0.5 - 0.25 - 0.0125, 0.68, 
            0.25, 0.08, 
            "Random Name", BLUE, LIGHT_BLUE,
            self.regenerate_name
        )
        
        self.start_button = Button(
            0.5 + 0.0125, 0.68, 
            0.25, 0.08, 
            "Start Game", GREEN, LIGHT_GREEN,
            self.start_game
        )
        
        # Create volume sliders
        self.music_slider = Slider(
            0.1, 0.85,  # x%, y%
            0.35, 0.03,  # width%, height%
            0.0, 1.0,   # min, max values
            music_volume, "Music Volume"  # initial value and label
    )

        self.sfx_slider = Slider(
            0.55, 0.85,  # x%, y%
            0.35, 0.03,  # width%, height%
            0.0, 1.0,   # min, max values
            sfx_volume, "SFX Volume"  # initial value and label
    )
        
        # Background elements
        self.bubbles = []
        self.initialize_bubbles()
        
        # Toggle flag for name source
        self.using_random_name = True
        
    def initialize_bubbles(self):
        """Create bubbles scaled to screen size with physics properties"""
        self.bubbles = []
        bubble_count = int(30 * (current_width * current_height) / (DEFAULT_WIDTH * DEFAULT_HEIGHT))
        
        for _ in range(bubble_count):
            self.bubbles.append({
                'x': random.randint(0, current_width),
                'y': random.randint(0, current_height),
                'size': random.randint(8, 25),
                'speed': random.uniform(0.3, 1.5),
                'vel_x': 0.0,  # Horizontal velocity for cursor interaction
                'vel_y': 0.0,  # Vertical velocity for cursor interaction
                'original_speed': random.uniform(0.3, 1.5),  # Store original upward speed
                'alpha': random.randint(80, 150),  # Individual transparency
                'wobble': random.uniform(0, 6.28),  # For slight horizontal wobble
                'wobble_speed': random.uniform(0.02, 0.05)
            })
    
    def update_ui_elements(self):
        """Update UI elements after resolution change"""
        self.input_box.update_rect()
        self.regenerate_button.update_rect()
        self.start_button.update_rect()
        self.music_slider.update_rect()
        self.sfx_slider.update_rect()
        self.initialize_bubbles()
        
    def regenerate_name(self):
        if click_04_sound:
            click_04_sound.play()
        self.current_name = generate_random_name()
        self.using_random_name = True
        
    def start_game(self):
        # Play the start game sound
        if start_game_sound:
            start_game_sound.play()
        
        # Determine which name to use
        player_name = self.current_name if self.using_random_name else self.input_box.text
        
        # Make sure we have a valid name
        if not player_name.strip():
            player_name = generate_random_name()  # Fallback to random if empty
            
        print(f"Starting game with character name: {player_name}")
        
        # Launch the game with the player name
        try:
            # First check if the game module exists
            import game
            # Run the game
            game.run_game(player_name)
            # When game.py returns, we'll be back in the main menu
        except ImportError as e:
            print(f"Error loading game module: {e}")
            print("Make sure game.py exists in the same directory as start_screen.py")
        
    def update(self):
        # Get mouse position for cursor interaction
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Track if any bubble was affected for sound playing
        bubble_affected = False

        # Update bubble positions with cursor interaction
        for bubble in self.bubbles:
            # Calculate distance from cursor to bubble
            dx = bubble['x'] - mouse_x
            dy = bubble['y'] - mouse_y
            distance = (dx * dx + dy * dy) ** 0.5
            
            # Interaction radius based on bubble size
            interaction_radius = bubble['size'] * 3
            
            if distance < interaction_radius and distance > 0:
                # Calculate repulsion force (bubbles move away from cursor)
                force_strength = (interaction_radius - distance) / interaction_radius
                force_strength = min(force_strength * 8, 15)  # Limit max force
                
                # Normalize direction vector
                dx_norm = dx / distance
                dy_norm = dy / distance
                
                # Apply force
                bubble['vel_x'] += dx_norm * force_strength * 0.3
                bubble['vel_y'] += dy_norm * force_strength * 0.3

                    # Mark that a bubble was affected if force is significant
                if force_strength > 2:
                    bubble_affected = True
            
            # Apply some damping to velocities
            bubble['vel_x'] *= 0.95
            bubble['vel_y'] *= 0.95
            
            # Add slight horizontal wobble for natural movement
            bubble['wobble'] += bubble['wobble_speed']
            wobble_offset = math.sin(bubble['wobble']) * 0.5
            
            # Update position with original upward movement + interaction forces + wobble
            bubble['x'] += bubble['vel_x'] + wobble_offset
            bubble['y'] += bubble['vel_y'] - bubble['original_speed']
            
            # Keep bubbles on screen horizontally
            if bubble['x'] < -bubble['size']:
                bubble['x'] = current_width + bubble['size']
            elif bubble['x'] > current_width + bubble['size']:
                bubble['x'] = -bubble['size']
                
            # Reset bubble when it goes off top
            if bubble['y'] < -bubble['size']:
                bubble['y'] = current_height + bubble['size']
                bubble['x'] = random.randint(0, current_width)
                bubble['vel_x'] = 0
                bubble['vel_y'] = 0
                
        # Play bubble sound if any bubble was significantly affected
        # Add a cooldown to prevent sound spam
        current_time = pygame.time.get_ticks()
        if not hasattr(self, 'last_bubble_sound_time'):
            self.last_bubble_sound_time = 0
        
        if bubble_affected and pop_drip_sound and (current_time - self.last_bubble_sound_time > 150):
            pop_drip_sound.play()
            self.last_bubble_sound_time = current_time

        # Update the GIF animation
        self.logo_animation.update()
        
    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        
        # Check button hover states
        self.regenerate_button.check_hover(mouse_pos)
        self.start_button.check_hover(mouse_pos)
        self.music_slider.check_hover(mouse_pos)
        self.sfx_slider.check_hover(mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # ESC always exits the game
                    return False
                elif event.key == pygame.K_F11:
                    # F11 toggles between maximized and normal window
                    toggle_maximized()
                    self.update_ui_elements()

            
            # Handle window resize events
            elif event.type == pygame.VIDEORESIZE:
                global current_width, current_height, screen
                current_width, current_height = event.size
                screen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)
                scale_fonts(current_width, current_height)
                self.update_ui_elements()
            
            # Handle volume slider events
            self.music_slider.handle_event(event)
            self.sfx_slider.handle_event(event)
            
            # Handle input box events
            input_result = self.input_box.handle_event(event)
            
            # If the input box was clicked or content changed
            if input_result is not False:
                # If text was entered (Enter pressed)
                if isinstance(input_result, str) and input_result:
                    self.using_random_name = False
                # If box was clicked
                elif input_result is True:
                    self.using_random_name = False
            
            # Handle button clicks
            if self.regenerate_button.handle_event(event):
                self.using_random_name = True
                
            if self.start_button.handle_event(event):
                pass  # Action is handled by the button
                
        return True
              
    def draw(self):
        # Fill background
        screen.fill((20, 60, 100))  # Deep blue background
        
        # Draw bubbles with enhanced visuals
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        for bubble in self.bubbles:
            # Calculate distance from cursor for visual effects
            dx = bubble['x'] - mouse_x
            dy = bubble['y'] - mouse_y
            distance = (dx * dx + dy * dy) ** 0.5
            interaction_radius = bubble['size'] * 3
            
            # Change bubble appearance based on cursor proximity
            if distance < interaction_radius:
                # Bubble is near cursor - make it brighter and more opaque
                proximity_factor = 1 - (distance / interaction_radius)
                alpha = min(255, int(bubble['alpha'] + proximity_factor * 100))
                color = (
                    min(255, int(200 + proximity_factor * 55)),
                    min(255, int(220 + proximity_factor * 35)),
                    255
                )
            else:
                # Normal bubble appearance
                alpha = bubble['alpha']
                color = (200, 220, 255)
            
            # Create a surface for the bubble with transparency
            bubble_surface = pygame.Surface((bubble['size'] * 2, bubble['size'] * 2), pygame.SRCALPHA)
            
            # Draw outer bubble (main bubble)
            pygame.draw.circle(
                bubble_surface,
                (*color, alpha),
                (bubble['size'], bubble['size']),
                bubble['size']
            )
            
            # Draw inner highlight for 3D effect
            highlight_size = max(2, bubble['size'] // 3)
            highlight_offset = bubble['size'] // 4
            pygame.draw.circle(
                bubble_surface,
                (255, 255, 255, min(100, alpha // 2)),
                (bubble['size'] - highlight_offset, bubble['size'] - highlight_offset),
                highlight_size
            )
            
            # Blit the bubble surface to the screen
            screen.blit(
                bubble_surface,
                (int(bubble['x'] - bubble['size']), int(bubble['y'] - bubble['size']))
            )
        
        # Draw animated logo above title
        logo_y = int(current_height * 0.03)  # Position above the title
        self.logo_animation.draw(screen, (current_width // 2, logo_y))
        
        # Draw title
        scaled_title_font = pygame.font.Font(None, int(title_font.get_height() * 3))  # 50% bigger
        title_text = scaled_title_font.render("fishgame.", True, WHITE)
        screen.blit(title_text, (current_width // 2 - title_text.get_width() // 2, int(current_height * 0.27)))
        
        # Draw character name prompt
        prompt_text = text_font.render("Your name:", True, WHITE)
        screen.blit(prompt_text, (current_width // 2 - prompt_text.get_width() // 2, int(current_height * 0.47)))
        
        # Draw input box or current random name based on mode
        if self.using_random_name:
            # Draw character name box for random name
            name_box_rect = pygame.Rect(
                int(current_width * (0.5 - 0.1875)),
                int(current_height * 0.52),
                int(current_width * 0.375),
                int(current_height * 0.1)
            )
            pygame.draw.rect(screen, GRAY, name_box_rect)
            pygame.draw.rect(screen, BLACK, name_box_rect, 2)
            
            # Draw random name
            name_text = button_font.render(self.current_name, True, BLACK)
            screen.blit(name_text, (current_width // 2 - name_text.get_width() // 2, int(current_height * 0.53 + name_text.get_height() * 0.5)))
            
            # Draw click to edit hint
            hint_text = text_font.render("(Click to edit)", True, WHITE)
            screen.blit(hint_text, (current_width // 2 - hint_text.get_width() // 2, int(current_height * 0.62)))
        else:
            # Draw the input box for custom name
            self.input_box.draw(screen)
               
        # Draw buttons
        self.regenerate_button.draw(screen)
        self.start_button.draw(screen)
        
        # Draw volume sliders
        self.music_slider.draw(screen)
        self.sfx_slider.draw(screen)
        
        # Draw controls info
        controls_text = text_font.render("F11: Toggle size | ESC: Exit", True, WHITE)
        screen.blit(controls_text, (current_width // 2 - controls_text.get_width() // 2, int(current_height * 0.92)))

def main():
    # Make sure Pillow is installed
    try:
        import PIL
    except ImportError:
        print("Pillow library is required for GIF animations.")
        print("Please install it using: pip install Pillow")
        pygame.quit()
        sys.exit()
    
    start_screen = StartScreen()
    running = True
    
    while running:
        # Handle events
        running = start_screen.handle_events()
        
        # Update
        start_screen.update()
        
        # Draw
        start_screen.draw()
        
        # Update display
        pygame.display.flip()
        
        # Cap framerate
        clock.tick(FPS)
    
    # Cleanup
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()