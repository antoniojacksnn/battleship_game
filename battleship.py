import pygame
import random

# Constants
BOARD_SIZE = 8
CELL_SIZE = 50
NUM_SHIPS = 5
WINDOW_WIDTH = (BOARD_SIZE * 2 + 3) * CELL_SIZE
WINDOW_HEIGHT = (BOARD_SIZE + 1) * CELL_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

# Initialize pygame
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Battleship Game")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont(None, 24)
small_font = pygame.font.SysFont(None, 20)

# Create the game boards
player_board = [['O'] * BOARD_SIZE for _ in range(BOARD_SIZE)]
computer_board = [['O'] * BOARD_SIZE for _ in range(BOARD_SIZE)]

# Place the ships randomly on the boards
player_ships = []
computer_ships = []
for _ in range(NUM_SHIPS):
    while True:
        ship_row = random.randint(0, BOARD_SIZE - 1)
        ship_col = random.randint(0, BOARD_SIZE - 1)
        if (ship_row, ship_col) not in player_ships:
            player_ships.append((ship_row, ship_col))
            break

    while True:
        ship_row = random.randint(0, BOARD_SIZE - 1)
        ship_col = random.randint(0, BOARD_SIZE - 1)
        if (ship_row, ship_col) not in computer_ships and (ship_row, ship_col) not in player_ships:
            computer_ships.append((ship_row, ship_col))
            break

# Game variables
player_turn = True
game_over = False
player_hits = 0
computer_hits = 0

# Helper function to convert board coordinates to screen coordinates
def convert_coordinates(row, col, is_player):
    x_offset = 0 if is_player else BOARD_SIZE + 2
    x = col * CELL_SIZE + (x_offset + 1) * CELL_SIZE
    y = row * CELL_SIZE + CELL_SIZE
    return x, y

# Game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.MOUSEBUTTONDOWN and player_turn:
            if event.button == 1:  # Left mouse button
                # Get the clicked cell position
                click_x, click_y = event.pos
                col = (click_x - CELL_SIZE) // CELL_SIZE
                row = (click_y - CELL_SIZE) // CELL_SIZE

                # Check if the player has already guessed the cell
                if player_board[row][col] != 'O':
                    continue

                # Check the player's guess
                if (row, col) in computer_ships:
                    player_board[row][col] = "X"
                    player_hits += 1
                    if player_hits == NUM_SHIPS:
                        game_over = True
                else:
                    player_board[row][col] = "M"

                player_turn = False

    if not player_turn and not game_over:
        # Computer's turn
        while not player_turn:
            row = random.randint(0, BOARD_SIZE - 1)
            col = random.randint(0, BOARD_SIZE - 1)

            if computer_board[row][col] == 'O':
                if (row, col) in player_ships:
                    computer_board[row][col] = "X"
                    computer_hits += 1
                    if computer_hits == NUM_SHIPS:
                        game_over = True
                else:
                    computer_board[row][col] = "M"

                player_turn = True

    # Draw the game boards
    window.fill(WHITE)

    # Draw player's board
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            x, y = convert_coordinates(row, col, True)
            pygame.draw.rect(window, LIGHT_GRAY, (x, y, CELL_SIZE, CELL_SIZE))

            if player_board[row][col] == "X":
                pygame.draw.circle(window, RED, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 4)
            elif player_board[row][col] == "M":
                pygame.draw.line(window, RED, (x, y), (x + CELL_SIZE, y + CELL_SIZE))
                pygame.draw.line(window, RED, (x + CELL_SIZE, y), (x, y + CELL_SIZE))

            if player_turn and player_board[row][col] == 'O':
                pygame.draw.circle(window, BLACK, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), 2)

    # Draw computer's board
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            x, y = convert_coordinates(row, col, False)
            pygame.draw.rect(window, LIGHT_GRAY, (x, y, CELL_SIZE, CELL_SIZE))

            if computer_board[row][col] == "X":
                pygame.draw.circle(window, RED, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 4)
            elif computer_board[row][col] == "M":
                pygame.draw.line(window, RED, (x, y), (x + CELL_SIZE, y + CELL_SIZE))
                pygame.draw.line(window, RED, (x + CELL_SIZE, y), (x, y + CELL_SIZE))

            if not player_turn and computer_board[row][col] == 'O':
                pygame.draw.circle(window, BLACK, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), 2)

    # Draw player's hits count
    player_hits_text = small_font.render(f"Hits: {player_hits}", True, BLACK)
    window.blit(player_hits_text, (CELL_SIZE, WINDOW_HEIGHT - CELL_SIZE))

    # Draw computer's hits count
    computer_hits_text = small_font.render(f"Hits: {computer_hits}", True, BLACK)
    window.blit(computer_hits_text, (CELL_SIZE + BOARD_SIZE * CELL_SIZE + CELL_SIZE, WINDOW_HEIGHT - CELL_SIZE))

    # Draw text
    player_text = font.render("Player", True, BLACK)
    window.blit(player_text, (CELL_SIZE, 10))
    computer_text = font.render("Computer", True, BLACK)
    window.blit(computer_text, (CELL_SIZE + BOARD_SIZE * CELL_SIZE + CELL_SIZE, 10))

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Show the game result
result_text = font.render("Player wins!" if player_hits == NUM_SHIPS else "Computer wins!", True, BLACK)
window.blit(result_text, (CELL_SIZE + (BOARD_SIZE * CELL_SIZE - result_text.get_width()) // 2,
                          CELL_SIZE + (BOARD_SIZE * CELL_SIZE - result_text.get_height()) // 2))
pygame.display.flip()

# Game over loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
