import pygame
import random
import time
import cv2
import pygame.freetype

# Initialize Pygame
pygame.init()

# Screen dimensions (16:9 aspect ratio)
SCREEN_WIDTH, SCREEN_HEIGHT = 1475, 830
GRID_SIZE = 10
GRID_X_OFFSET = 20  # Space on the left
PANEL_X_OFFSET = GRID_X_OFFSET  # Match left grid offset
GRID_HEIGHT = SCREEN_HEIGHT - 20  # Leave equal spacing on top and bottom

PANEL_HEIGHT = GRID_HEIGHT
# CELL_SIZE = GRID_HEIGHT // GRID_SIZE  # Cell size based on grid height
CELL_SPACING = 5  # Space between cells
CELL_SIZE = (GRID_HEIGHT - (GRID_SIZE - 1) * CELL_SPACING) // GRID_SIZE
# Dynamically calculate vertical offset to center the grid
total_grid_height = GRID_SIZE * (CELL_SIZE + CELL_SPACING) - CELL_SPACING
GRID_Y_OFFSET = (SCREEN_HEIGHT - total_grid_height) // 2
GRID_WIDTH = (CELL_SIZE + CELL_SPACING) * GRID_SIZE  # Adjusted ratio for narrower grid
PANEL_WIDTH = SCREEN_WIDTH - GRID_WIDTH - GRID_X_OFFSET * 3  # Adjust for equal offset


# Font settings
CHAT_GRID_FONT = pygame.font.Font("font/GideonRoman-Regular.ttf", 17)
CHAT_FONT = pygame.font.Font("font/GideonRoman-Regular.ttf", 17)
GRID_FONT = pygame.font.Font("font/GentiumPlus-Bold.ttf", 21)
TIMER_FONT = pygame.font.Font("font/GentiumPlus-Bold.ttf", 21)


# Colors
TRANSPARENT = (0, 0, 0, 3)
WHITE = (255, 255, 255, 3)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
VIOLET = (97, 4, 161)

GRID_COLOR = (21, 21, 21, 1)
GRID_FONT_COLOR = (255, 255, 255, 3)
CHAT_COLOR = (97, 4, 161, 17)
CHAT_FONT_COLOR = (255, 255, 255, 3)

# Colors associated with each player
PLAYER_COLORS = {
    "Eros": (13, 32, 62),        #Blue
    "Psyche": (204, 162, 42),    # Gold
    "Ares": (128, 0, 32),        # Burgundy
    "Aphrodite": (255, 215, 0),  # Gold
    "Eos": (255, 165, 0),        # Orange
    "Zeus": (255, 215, 0),       # Gold
    "Hera": (80, 200, 120),      # Emerald
    "Semele": (255, 192, 203),   # Pink
    "Io": (15, 82, 186),         # Sapphire Blue
    "Medusa": (3, 48, 41),       # Green
    "Hedone": (97, 4, 161),       # Violet
}


def apply_rounded_mask(image, radius=CELL_SIZE // 5):
    mask = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, CELL_SIZE, CELL_SIZE), border_radius=10)
    rounded_image = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
    rounded_image.blit(image, (0, 0))
    rounded_image.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    return rounded_image


PLAYER_IMAGES = []

MEDUSA_IMAGE = "char/medusa.png"
HEDONE_IMAGE = "char/hedone.png"

MEDUSA_IMAGES = [
    pygame.image.load(f"char/medusa/medusa{i}.png") for i in range(1, 11)
]
HEDONE_IMAGES = [
    pygame.image.load(f"char/hedone/hedone{i}.png") for i in range(1, 11)
]

MEDUSA_IMAGES = [
    pygame.transform.smoothscale(image, (CELL_SIZE, CELL_SIZE))
    for image in MEDUSA_IMAGES
]
HEDONE_IMAGES = [
    pygame.transform.smoothscale(image, (CELL_SIZE, CELL_SIZE))
    for image in HEDONE_IMAGES
]

MEDUSA_BACKGROUNDS = [
    pygame.image.load(f"char/medusa/medusa{i}.png") for i in range(1, 11)
]
HEDONE_BACKGROUNDS = [
    pygame.image.load(f"char/hedone/hedone{i}.png") for i in range(1, 11)
]
MEDUSA_BACKGROUNDS = [
    pygame.transform.smoothscale(img, (int(GRID_WIDTH), GRID_HEIGHT)) for img in MEDUSA_BACKGROUNDS
]
HEDONE_BACKGROUNDS = [
    pygame.transform.smoothscale(img, (int(GRID_WIDTH), GRID_HEIGHT)) for img in HEDONE_BACKGROUNDS
]

MEDUSA_IMAGES = [
    apply_rounded_mask(pygame.transform.smoothscale(image, (CELL_SIZE, CELL_SIZE)))
    for image in MEDUSA_IMAGES
]
HEDONE_IMAGES = [
    apply_rounded_mask(pygame.transform.smoothscale(image, (CELL_SIZE, CELL_SIZE)))
    for image in HEDONE_IMAGES
]



# Load single intro image
INTRO_IMAGE = pygame.transform.smoothscale(pygame.image.load("char/io.png"), (int(SCREEN_WIDTH), SCREEN_HEIGHT))

INTRO_VIDEO_PATH = "char/intro/intro.mp4"


def play_intro_video():
    cap = cv2.VideoCapture(INTRO_VIDEO_PATH)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_height, frame_width = frame.shape[:2]
        aspect_ratio = 16 / 9
        if frame_width / frame_height > aspect_ratio:
            # Wider than 16:9, fit by height
            new_height = SCREEN_HEIGHT
            new_width = int(new_height * aspect_ratio)
        else:
            # Taller than 16:9, fit by width
            new_width = SCREEN_WIDTH
            new_height = int(new_width / aspect_ratio)

        frame = cv2.resize(frame, (new_width, new_height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

        # Center the frame on the screen
        x_offset = (SCREEN_WIDTH - new_width) // 2
        y_offset = (SCREEN_HEIGHT - new_height) // 2
        screen.fill(GRID_COLOR)  # Clear the screen
        screen.blit(frame_surface, (x_offset, y_offset))
        pygame.display.flip()

        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def load_player_images(num_players):
    def load_high_quality_image(path):
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.smoothscale(image, (CELL_SIZE, CELL_SIZE))
    if num_players == 2:
        return [
            load_high_quality_image("char/eros.png"),
            load_high_quality_image("char/psyche.png")
        ]
    elif num_players == 3:
        return [
            load_high_quality_image("char/ares.png"),
            load_high_quality_image("char/aphrodite.png"),
            load_high_quality_image("char/eos.png")
        ]
    elif num_players == 4:
        return [
            load_high_quality_image("char/zeus.png"),
            load_high_quality_image("char/hera.png"),
            load_high_quality_image("char/semele.png"),
            load_high_quality_image("char/io.png")
        ]

    return []



# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Himeros and Philotes")

# Chat panel setup
chat_panel = []


def update_chat(action_message, player_index=None):
    global chat_scroll_offset

    if player_index is None:
        image_path = HEDONE_IMAGE
        player_name = "Hedone"
    elif player_index == 500:
        image_path = MEDUSA_IMAGE
        player_name = "Medusa"
    else:
        image_path = None
        player_name = players[player_index]

    if image_path:
        chat_image = pygame.image.load(image_path).convert_alpha()
        chat_image = apply_rounded_mask(pygame.transform.smoothscale(chat_image, (CELL_SIZE, CELL_SIZE)))
        chat_image = pygame.transform.smoothscale(chat_image, (35, 35))
    else:
        chat_image = pygame.transform.smoothscale(PLAYER_IMAGES[player_index], (CELL_SIZE, CELL_SIZE))
        chat_image = apply_rounded_mask(chat_image)
        chat_image = pygame.transform.smoothscale(chat_image, (35, 35))

    # Wrap the text for the chat bubble
    wrapped_lines = wrap_text(action_message, CHAT_FONT, PANEL_WIDTH - 110)  # Adjust width for padding

    # Use the player color for the chat bubble
    player_color = PLAYER_COLORS.get(player_name, CHAT_FONT_COLOR)  # Default to font color if not found
    chat_panel.append((player_name, player_color, wrapped_lines, chat_image))

    # Calculate the total height of chat content
    total_height = sum(len(message[2]) * (CHAT_FONT.get_height() + 5) + 20 for message in chat_panel)  # Add space between bubbles

    # Trim messages if the total height exceeds the chat panel height
    visible_height = SCREEN_HEIGHT - (GRID_Y_OFFSET + 70 + 100)  # Adjusted visible height
    while total_height > visible_height:
        chat_panel.pop(0)
        total_height = sum(len(message[2]) * (CHAT_FONT.get_height() + 5) + 20 for message in chat_panel)

    # Auto-scroll to the bottom
    max_offset = max(0, total_height - visible_height)
    chat_scroll_offset = max_offset


# Chat scrolling offset
chat_scroll_offset = 0
max_chat_lines = 15  # Maximum lines that fit in the visible chat area


def draw_right_panel(countdown_time, input_value, chat_scroll_offset):
    panel_x = GRID_WIDTH + GRID_X_OFFSET * 2
    panel_width = PANEL_WIDTH

    # Draw timer
    remaining_time = max(0, int(countdown_time - time.time()))
    minutes = remaining_time // 60
    seconds = remaining_time % 60
    timer_text = TIMER_FONT.render(f"{minutes:02}:{seconds:02}", True, CHAT_FONT_COLOR)
    timer_rect = pygame.Rect(panel_x + 10, GRID_Y_OFFSET, panel_width - 20, CELL_SIZE)

    # Transparent background for the timer
    timer_surface = pygame.Surface((timer_rect.width, timer_rect.height), pygame.SRCALPHA)
    timer_surface.fill(CHAT_COLOR)  # CHAT_COLOR = (97, 4, 161, 29)
    screen.blit(timer_surface, timer_rect.topleft)

    pygame.draw.rect(screen, VIOLET, timer_rect, 2, border_radius=10)  # Outline
    screen.blit(timer_text, (timer_rect.x + 10, timer_rect.y + 10))

    # Chat surface for scrolling
    chat_y_offset = GRID_Y_OFFSET + 81
    chat_rect_outline = pygame.Rect(
        panel_x + 10,
        chat_y_offset,
        panel_width - 20,
        SCREEN_HEIGHT - chat_y_offset - 15
    )
    pygame.draw.rect(screen, VIOLET, chat_rect_outline, 2, border_radius=10)

    chat_rect = pygame.Rect(
        chat_rect_outline.x + 5,
        chat_rect_outline.y + 15,
        chat_rect_outline.width - 10,
        chat_rect_outline.height - 10
    )

    # Transparent chat surface
    chat_surface = pygame.Surface((chat_rect.width, chat_rect.height), pygame.SRCALPHA)
    chat_surface.fill(CHAT_COLOR)

    # Adjusted chat surface height
    total_chat_height = sum(
        len(message[2]) * (CHAT_FONT.get_height() + 3) + 10
        for message in chat_panel
    )
    chat_content_surface = pygame.Surface(
        (chat_rect.width, max(total_chat_height, chat_rect.height)),
        pygame.SRCALPHA
    )

    max_text_width = chat_rect.width - 83
    y_position = 5

    for player_name, player_color, wrapped_lines, chat_image in chat_panel:
        bubble_height = len(wrapped_lines) * (CHAT_FONT.get_height() + 3) + 10
        bubble_rect = pygame.Rect(55, y_position, max_text_width, bubble_height)

        # Fill the bubble with the player's color
        pygame.draw.rect(chat_content_surface, player_color, bubble_rect, border_radius=10)
        pygame.draw.rect(chat_content_surface, CHAT_FONT_COLOR, bubble_rect, 1, border_radius=10)  # Border

        # Render the text lines
        for i, line in enumerate(wrapped_lines):
            rendered_text = CHAT_FONT.render(line, True, CHAT_FONT_COLOR)
            chat_content_surface.blit(rendered_text, (bubble_rect.x + 10, y_position + 5 + i * (CHAT_FONT.get_height() + 3)))

        image_x = bubble_rect.x - 45
        image_y = y_position + bubble_height - 37
        chat_content_surface.blit(chat_image, (image_x, image_y))

        y_position += bubble_rect.height + 15

    # Blit chat content with scrolling
    chat_surface.blit(chat_content_surface, (0, -chat_scroll_offset))
    screen.blit(chat_surface, chat_rect.topleft)

    # Draw dice panel
    # dice_panel_rect = pygame.Rect(panel_x + 10, SCREEN_HEIGHT - 63, panel_width - 20, 50)
    # dice_panel_surface = pygame.Surface((dice_panel_rect.width, dice_panel_rect.height), pygame.SRCALPHA)
    # dice_panel_surface.fill(CHAT_COLOR)
    # screen.blit(dice_panel_surface, dice_panel_rect.topleft)
    #
    # pygame.draw.rect(screen, VIOLET, dice_panel_rect, 1, border_radius=10)
    # input_text = CHAT_FONT.render(f"Enter Dice Value (1-6): {input_value}", True, CHAT_FONT_COLOR)
    # screen.blit(input_text, (dice_panel_rect.x + 10, dice_panel_rect.y + 10))

    return total_chat_height


def wrap_text(text, font, max_width):
    """Wrap text to fit within a specified width."""
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.render(test_line, True, CHAT_FONT_COLOR).get_width() > max_width:
            lines.append(current_line)
            current_line = word
        else:
            current_line = test_line

    if current_line:
        lines.append(current_line)

    return lines


def handle_chat_scroll(event, total_chat_height):
    global chat_scroll_offset
    if event.type == pygame.MOUSEWHEEL:
        chat_scroll_offset -= event.y * 20  # Scroll speed
        chat_scroll_offset = max(0, chat_scroll_offset)  # Prevent scrolling above the first message

        # Calculate maximum scroll offset
        visible_height = SCREEN_HEIGHT - (GRID_Y_OFFSET + 65 + 100)  # Chat panel height
        max_offset = max(0, total_chat_height - visible_height)  # Include bottom padding
        chat_scroll_offset = min(chat_scroll_offset, max_offset)  # Prevent scrolling below the last message


# Create the board
def draw_board(action_positions, snake_tiles={}, ladder_tiles={}):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if row % 2 == 0:  # Even rows go right to left
                position = (GRID_SIZE * (GRID_SIZE - row - 1)) + (GRID_SIZE - col - 1) + 1
            else:  # Odd rows go left to right
                position = (GRID_SIZE * (GRID_SIZE - row - 1)) + col + 1

            rect_x = GRID_X_OFFSET + col * (CELL_SIZE + CELL_SPACING)
            rect_y = GRID_Y_OFFSET + row * (CELL_SIZE + CELL_SPACING)
            rect = pygame.Rect(rect_x, rect_y, CELL_SIZE, CELL_SIZE)

            # Check if the tile should display a Medusa or Hedone image
            if position in snake_tiles:
                screen.blit(snake_tiles[position], rect.topleft)
            elif position in ladder_tiles:
                screen.blit(ladder_tiles[position], rect.topleft)



            overlay = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            overlay.fill(CHAT_COLOR)
            pygame.draw.rect(screen, VIOLET, rect, 2, border_radius=10)
            screen.blit(overlay, rect.topleft)
            # pygame.draw.rect(screen, GRID_FONT_COLOR, rect, 1, border_radius=10)
            #pygame.draw.rect(screen, (97, 4, 161), rect, border_radius=10)

            # Render the number in the center of the cell
            text = GRID_FONT.render(str(position), True, GRID_FONT_COLOR)
            text_rect = text.get_rect(center=(rect_x + CELL_SIZE // 2, rect_y + CELL_SIZE // 2))
            screen.blit(text, text_rect)




# Generate snakes and ladders
def generate_snakes_and_ladders():
    snakes = {}
    ladders = {}
    snake_medusa_mapping = {}
    ladder_hedone_mapping = {}
    snake_background_mapping = {}
    ladder_background_mapping = {}

    for level_index, level_start in enumerate(range(1, 101, 10)):
        level_end = level_start + 9

        # Generate one snake per level
        while True:
            start = random.randint(level_start + 1, level_end)
            end = random.randint(level_start, start - 1)
            if start - end <= 5 and start not in snakes and start not in ladders and end > level_start:
                snakes[start] = end
                break

        # Assign the corresponding Medusa image to the snake
        snake_medusa_mapping[start] = MEDUSA_IMAGES[level_index % 10]
        snake_background_mapping[start] = MEDUSA_BACKGROUNDS[level_index % 10]


        # Generate one ladder per level
        while True:
            start = random.randint(level_start, level_end - 1)
            end = random.randint(start + 1, level_end)
            if end - start <= 5 and start not in ladders and start not in snakes:
                ladders[start] = end
                break

        # Assign the corresponding Hedone image to the ladder
        ladder_hedone_mapping[start] = HEDONE_IMAGES[level_index % 10]
        ladder_background_mapping[start] = HEDONE_BACKGROUNDS[level_index % 10]

    return snakes, ladders, snake_medusa_mapping, ladder_hedone_mapping, snake_background_mapping, ladder_background_mapping

snakes, ladders, snake_medusa_mapping, ladder_hedone_mapping, snake_bg_mapping, ladder_bg_mapping = generate_snakes_and_ladders()

# Draw snakes and ladders using custom styles
def draw_snakes_and_ladders():
    pass
    # for start, end in snakes.items():
    #     start_pos = get_coordinates(start)
    #     end_pos = get_coordinates(end)
    #
    #     # Create curvy wavy effect for snakes
    #     num_segments = 10  # Number of segments for the curve
    #     x_diff = (end_pos[0] - start_pos[0]) / num_segments
    #     y_diff = (end_pos[1] - start_pos[1]) / num_segments
    #     points = []
    #     for i in range(num_segments + 1):
    #         x = start_pos[0] + i * x_diff + CELL_SIZE // 6 * (-1)**i
    #         y = start_pos[1] + i * y_diff
    #         points.append((x + CELL_SIZE // 2, y + CELL_SIZE // 2))  # Center-align the wave
    #
    #     # Snakes are now invisible
    #     pygame.draw.lines(screen, TRANSPARENT, False, points, 8)
    #
    # for start, end in ladders.items():
    #     start_pos = get_coordinates(start)
    #     end_pos = get_coordinates(end)
    #     # Ladders are now invisible
    #     pygame.draw.line(screen, TRANSPARENT, (start_pos[0] + CELL_SIZE // 2, start_pos[1] + CELL_SIZE // 2),
    #                      (end_pos[0] + CELL_SIZE // 2, end_pos[1] + CELL_SIZE // 2), 5)  # Draw the wavy snake
    #
    # for start, end in ladders.items():
    #     start_pos = get_coordinates(start)
    #     end_pos = get_coordinates(end)
    #     pygame.draw.line(screen, GOLD, (start_pos[0] + CELL_SIZE // 2, start_pos[1] + CELL_SIZE // 2),
    #                      (end_pos[0] + CELL_SIZE // 2, end_pos[1] + CELL_SIZE // 2), 5)  # Shiny golden ladder

# Convert board index to screen coordinates
def get_coordinates(position):
    position -= 1
    row = position // GRID_SIZE
    if row % 2 == 0:  # Even rows go right to left
        col = position % GRID_SIZE
    else:  # Odd rows go left to right
        col = GRID_SIZE - 1 - (position % GRID_SIZE)

    x = GRID_X_OFFSET + col * (CELL_SIZE + CELL_SPACING)
    y = GRID_Y_OFFSET + (GRID_SIZE - 1 - row) * (CELL_SIZE + CELL_SPACING)
    return x, y



# Smooth movement animation
def animate_movement(start, end, player_index, background_override=None):
    step = 1 if end > start else -1

    for position in range(start, end + step, step):
        if background_override:
            screen.blit(background_override, (0, 0))  # Draw override background
        else:
            screen.fill(GRID_COLOR)  # Clear screen to white

        # Redraw the board and elements
        draw_board(action_positions, snake_tiles, ladder_tiles)
        draw_snakes_and_ladders()
        draw_players()

        # Redraw the right panel
        total_chat_height = sum(
            len(message[2]) * (CHAT_FONT.get_height() + 3) + 10
            for message in chat_panel
        )
        draw_right_panel(countdown_end, "", chat_scroll_offset)

        # Draw the moving player with color outline
        x, y = get_coordinates(position)
        player_color = PLAYER_COLORS.get(players[player_index], GRID_FONT_COLOR)
        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, player_color, rect, border_radius=10)  # Fill with player's color

        # Draw the player image
        player_image = pygame.transform.smoothscale(PLAYER_IMAGES[player_index], (CELL_SIZE - 10, CELL_SIZE - 10))
        image_x = x + (CELL_SIZE - player_image.get_width()) // 2
        image_y = y + (CELL_SIZE - player_image.get_height()) // 2
        screen.blit(player_image, (image_x, image_y))

        # Render everything
        pygame.display.flip()
        time.sleep(0.2)


# Load actions
def load_actions():
    actions = {
        "L1": ["Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas pharetra maximus eros, non efficitur justo scelerisque id. Phasellus arcu nisi, dignissim eu lorem quis, faucibus facilisis mauris. Suspendisse potenti. Donec ultricies consectetur orci at feugiat. Proin finibus porttitor tellus in viverra."],
        "L2": ["Action for L2"],
        "L3": ["Action for L3"],
        "L4": ["Action for L4"],
        "L5": ["Action for L5"],
        "L6": ["Action for L6"],
        "L7": ["Action for L7"],
        "L8": ["Action for L8"],
        "L9": ["Action for L9"],
        "L10": ["Action for L10"]
    }
    return actions

actions = load_actions()

def get_action(position):
    if 1 <= position <= 10:
        return random.choice(actions["L1"])
    elif 11 <= position <= 20:
        return random.choice(actions["L2"])
    elif 21 <= position <= 30:
        return random.choice(actions["L3"])
    elif 31 <= position <= 40:
        return random.choice(actions["L4"])
    elif 41 <= position <= 50:
        return random.choice(actions["L5"])
    elif 51 <= position <= 60:
        return random.choice(actions["L6"])
    elif 61 <= position <= 70:
        return random.choice(actions["L7"])
    elif 71 <= position <= 80:
        return random.choice(actions["L8"])
    elif 81 <= position <= 90:
        return random.choice(actions["L9"])
    elif 91 <= position <= 100:
        return random.choice(actions["L10"])
    else:
        return "No Action"

# Initialize players
def initialize_players():
    global PLAYER_IMAGES
    while True:
        try:
            num_players = int(input("Enter the number of players (2-4): "))
            if num_players == 2:
                player_names = ["Eros", "Psyche"]
                update_chat("Welcome Eros and Psyche!")
                PLAYER_IMAGES = [
                    apply_rounded_mask(image) for image in load_player_images(2)
                ]
            elif num_players == 3:
                player_names = ["Ares", "Aphrodite", "Eos"]
                update_chat("Welcome Ares, Aphrodite, and Eos!")
                PLAYER_IMAGES = [
                    apply_rounded_mask(image) for image in load_player_images(2)
                ]
            elif num_players == 4:
                player_names = ["Zeus", "Hera", "Semele", "Io"]
                update_chat("Welcome Zeus, Hera, Semele, and Io!")
                PLAYER_IMAGES = [
                    apply_rounded_mask(image) for image in load_player_images(2)
                ]
            else:
                print("Invalid number of players. Please choose between 2 and 4.")
                continue

            # Show start image for 5 seconds
            # screen.blit(INTRO_IMAGE, (0, 0))
            # pygame.display.flip()
            # time.sleep(9)

            play_intro_video()

            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    player_positions = [1 for _ in range(num_players)]
    return player_names, player_positions

players, player_positions = initialize_players()
current_player_idx = 0



def get_dice_value():
    global countdown_end
    input_value = ""
    scroll_offset = 0  # Ensure the chat panel scroll offset is passed

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.unicode.isdigit() and 1 <= int(event.unicode) <= 6:
                    return int(event.unicode)  # Immediately return the value once a valid number is pressed
                elif event.key == pygame.K_BACKSPACE:
                    input_value = input_value[:-1]

            # Scroll events
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    scroll_offset = max(0, scroll_offset - 20)
                elif event.button == 5:  # Scroll down
                    total_chat_height = sum(
                        len(wrapped_lines) * (CHAT_FONT.get_height() + 10) + 10
                        for _, _, wrapped_lines, _ in chat_panel  # Updated unpacking to match structure
                    )
                    chat_panel_height = SCREEN_HEIGHT - (GRID_Y_OFFSET + 70 + 100)
                    scroll_offset = min(scroll_offset + 20, max(0, total_chat_height - chat_panel_height))

        screen.fill(GRID_COLOR)  # Clear screen to white
        draw_board(action_positions, snake_tiles, ladder_tiles)
        draw_snakes_and_ladders()
        draw_players()
        draw_right_panel(countdown_end, input_value, scroll_offset)
        pygame.display.flip()



# Draw players
def draw_players():
    for i, position in enumerate(player_positions):
        x, y = get_coordinates(position)

        # Fetch player's color
        player_color = PLAYER_COLORS.get(players[i], GRID_FONT_COLOR)  # Default to grid font color if not found

        # Draw a rounded rectangle filled with the player's color
        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, player_color, rect, border_radius=10)  # Fill with player's color

        # Draw the player image on top of the colored cell
        player_image = pygame.transform.smoothscale(PLAYER_IMAGES[i], (CELL_SIZE - 10, CELL_SIZE - 10))  # Slightly smaller
        image_x = x + (CELL_SIZE - player_image.get_width()) // 2
        image_y = y + (CELL_SIZE - player_image.get_height()) // 2
        screen.blit(player_image, (image_x, image_y))


# Main game loop
running = True
winner = None
action_positions = {}
snake_tiles = {}
ladder_tiles = {}
countdown_end = time.time()
scroll_offset = 0

while running:
    screen.fill(GRID_COLOR)  # Clear screen to white
    draw_board(action_positions, snake_tiles, ladder_tiles)
    draw_snakes_and_ladders()
    draw_players()
    draw_right_panel(countdown_end, "", scroll_offset)

    total_chat_height = draw_right_panel(countdown_end, "", chat_scroll_offset)

    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         running = False
    #     elif event.type == pygame.MOUSEBUTTONDOWN:
    #         if event.button == 4:  # Scroll up
    #             scroll_offset = max(0, scroll_offset - 20)
    #         elif event.button == 5:  # Scroll down
    #             # Limit scroll offset to not exceed total chat height
    #             total_chat_height = sum(
    #                 len(wrapped_lines) * (CHAT_FONT.get_height() + 10) + 10
    #                 for _, wrapped_lines in chat_panel
    #             )
    #             chat_panel_height = int(SCREEN_HEIGHT * 0.9) - int(SCREEN_HEIGHT * 0.1) - 70
    #             scroll_offset = min(scroll_offset + 20, max(0, total_chat_height - chat_panel_height))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEWHEEL:
            # Handle scrolling of the chat
            handle_chat_scroll(event, total_chat_height)



    if not winner:
        dice_value = get_dice_value()
        current_player = players[current_player_idx % len(players)]
        # update_chat(f"{current_player} rolled a {dice_value}!")

        # Logic for rolling 6s
        six_count = 0
        turn_total = 0

        while True:
            if dice_value == 6:
                six_count += 1
                if six_count == 3:
                    update_chat(f"{current_player} rolled three 6s! Turn skipped.")
                    break
                else:
                    update_chat(f"{current_player} rolled a 6! Another chance!")
                dice_value = get_dice_value()
            else:
                turn_total += 6 * six_count + dice_value
                new_pos = player_positions[current_player_idx] + turn_total

                if new_pos > 100:
                    update_chat("Roll exceeds 100! Stay in place.")
                else:
                    if new_pos in snakes:
                        animate_movement(player_positions[current_player_idx], new_pos, current_player_idx)
                        animate_movement(new_pos, snakes[new_pos], current_player_idx, snake_bg_mapping[new_pos])
                        update_chat(f"{current_player} encountered Medusa's wrath! You now need to get Spanked!", 500)
                        snake_tiles[new_pos] = snake_medusa_mapping[new_pos]
                        player_positions[current_player_idx] = snakes[new_pos]
                        countdown_end = time.time() + player_positions[current_player_idx] * 2
                    elif new_pos in ladders:
                        animate_movement(player_positions[current_player_idx], new_pos, current_player_idx)
                        animate_movement(new_pos, ladders[new_pos], current_player_idx, ladder_bg_mapping[new_pos])
                        update_chat(f"{current_player} is embraced by Hedone’s delight! You may now experience a delightful action of your choosing!")
                        ladder_tiles[new_pos] = ladder_hedone_mapping[new_pos]
                        player_positions[current_player_idx] = ladders[new_pos]
                        countdown_end = time.time() + player_positions[current_player_idx] * 2
                    else:
                        animate_movement(player_positions[current_player_idx], new_pos, current_player_idx)
                        player_positions[current_player_idx] = new_pos
                        countdown_end = time.time() + player_positions[current_player_idx] * 2

                    action = get_action(player_positions[current_player_idx])
                    update_chat(action, current_player_idx)

                    if player_positions[current_player_idx] == 100:
                        winner = current_player
                        update_chat(f"{winner} wins the game! Congratulations!")

                break

        current_player_idx = (current_player_idx + 1) % len(players)

    pygame.display.flip()

pygame.quit()
