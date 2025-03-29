import random
import sys
import os
import pygame
from pygame.locals import *

FPS = 60
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
ACHIEVEMENTS = []
DIFFICULTY = 'Medium'  # Default difficulty level
PLAYER_SKIN = 'bird.png'  # Default bird skin

# Corrected asset path
ASSET_PATH = r"C:\Users\HP\Desktop\Others\Flappy-Bird\\"

PLAYER = ASSET_PATH + PLAYER_SKIN
BACKGROUND = ASSET_PATH + 'background.png'
PIPE = ASSET_PATH + 'pipe.png'

def check_assets():
    print("Checking files...")
    for filename in ['message.png', 'background.png', 'bird.png', 'pipe.png', 'base.png']:
        full_path = ASSET_PATH + filename
        exists = os.path.exists(full_path)
        print(f"Checking: {full_path} - Exists: {exists}")
        if not exists:
            print(f"ERROR: {filename} is missing! The game may not run correctly.")

def saveHighScore(score):
    """
    Save the score to the highscore file and keep only the top 10 scores.
    """
    try:
        with open("highscore.txt", "r") as file:
            scores = [int(line.strip()) for line in file.readlines()]
    except FileNotFoundError:
        scores = []

    scores.append(score)
    scores = sorted(scores, reverse=True)[:10]  # Keep only the top 10 scores

    with open("highscore.txt", "w") as file:
        for s in scores:
            file.write(f"{s}\n")

def getHighScores():
    """
    Retrieve the top 10 high scores from the file.
    """
    try:
        with open("highscore.txt", "r") as file:
            return [int(line.strip()) for line in file.readlines()]
    except FileNotFoundError:
        return []

def mainMenu():
    """
    Display the main menu with options to Start Game, View Scores, or Quit.
    """
    font = pygame.font.Font(None, 36)
    while True:
        SCREEN.fill((0, 0, 0))  # Black background
        title_text = font.render("Flappy Bird", True, (255, 255, 255))
        start_text = font.render("1. Start Game", True, (255, 255, 255))
        scores_text = font.render("2. View Scores", True, (255, 255, 255))
        quit_text = font.render("3. Quit", True, (255, 255, 255))

        SCREEN.blit(title_text, (SCREENWIDTH // 2 - title_text.get_width() // 2, 50))
        SCREEN.blit(start_text, (50, 150))
        SCREEN.blit(scores_text, (50, 200))
        SCREEN.blit(quit_text, (50, 250))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_1:  # Start Game
                    return "start"
                elif event.key == K_2:  # View Scores
                    return "scores"
                elif event.key == K_3:  # Quit
                    pygame.quit()
                    sys.exit()

def selectDifficulty():
    """
    Allow the player to select a difficulty level.
    """
    global DIFFICULTY
    font = pygame.font.Font(None, 36)
    while True:
        SCREEN.fill((0, 0, 0))  # Black background
        title_text = font.render("Select Difficulty", True, (255, 255, 255))
        easy_text = font.render("1. Easy", True, (255, 255, 255))
        medium_text = font.render("2. Medium", True, (255, 255, 255))
        hard_text = font.render("3. Hard", True, (255, 255, 255))
        impossible_text = font.render("4. Impossible", True, (255, 255, 255))

        SCREEN.blit(title_text, (SCREENWIDTH // 2 - title_text.get_width() // 2, 50))
        SCREEN.blit(easy_text, (50, 150))
        SCREEN.blit(medium_text, (50, 200))
        SCREEN.blit(hard_text, (50, 250))
        SCREEN.blit(impossible_text, (50, 300))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_1:
                    DIFFICULTY = "Easy"
                    return
                elif event.key == K_2:
                    DIFFICULTY = "Medium"
                    return
                elif event.key == K_3:
                    DIFFICULTY = "Hard"
                    return
                elif event.key == K_4:
                    DIFFICULTY = "Impossible"
                    return

def viewScores():
    """
    Display the top 10 high scores.
    """
    scores = getHighScores()
    font = pygame.font.Font(None, 36)
    while True:
        SCREEN.fill((0, 0, 0))  # Black background
        title_text = font.render("High Scores", True, (255, 255, 255))
        SCREEN.blit(title_text, (SCREENWIDTH // 2 - title_text.get_width() // 2, 50))

        y_offset = 100
        for i, score in enumerate(scores):
            score_text = font.render(f"{i + 1}. {score}", True, (255, 255, 255))
            SCREEN.blit(score_text, (50, y_offset))
            y_offset += 40

        back_text = font.render("Press ESC to go back", True, (255, 255, 255))
        SCREEN.blit(back_text, (50, SCREENHEIGHT - 50))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return

def gameOverScreen(score):
    """
    Display the game over screen with the current score and high score.
    """
    high_score = max(getHighScores() + [0])  # Get the highest score or 0 if no scores exist
    font = pygame.font.Font(None, 36)
    while True:
        SCREEN.fill((0, 0, 0))  # Black background
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        current_score_text = font.render(f"Your Score: {score}", True, (255, 255, 255))
        high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
        restart_text = font.render("Press SPACE to restart", True, (255, 255, 255))

        SCREEN.blit(game_over_text, (SCREENWIDTH // 2 - game_over_text.get_width() // 2, 50))
        SCREEN.blit(current_score_text, (50, 150))
        SCREEN.blit(high_score_text, (50, 200))
        SCREEN.blit(restart_text, (50, 300))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                return

def getRandomPipe(pipeGap=150):
    """
    Generate positions of two pipes (one upper and one lower) for blitting on the screen.
    Returns a list of two dictionaries containing x and y positions of the pipes.
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT / 3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + pipeGap  # Use dynamic pipeGap
    return [
        {'x': pipeX, 'y': -y1},  # Upper pipe
        {'x': pipeX, 'y': y2}    # Lower pipe
    ]

def isCollide(playerx, playery, upperPipes, lowerPipes):
    """
    Check if the player collides with any pipe or the ground.
    """
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and
                abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y'] and
                abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            return True

    if playery > GROUNDY - GAME_SPRITES['player'].get_height():
        return True

    return False

def mainGame():
    """
    Main game loop.
    """
    global ACHIEVEMENTS
    score = 0
    playerx = int(SCREENWIDTH / 5)
    playery = int(SCREENWIDTH / 2)
    basex = 0

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
    ]
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
    ]

    # Adjust parameters based on difficulty
    if DIFFICULTY == 'Easy':
        pipeVelX = -2  # Slower pipes
        pipeGap = 200  # Larger gap
        gravity = 0.8  # Reduced gravity
    elif DIFFICULTY == 'Medium':
        pipeVelX = -5
        pipeGap = 150
        gravity = 1
    elif DIFFICULTY == 'Hard':
        pipeVelX = -7
        pipeGap = 120
        gravity = 1.2
    elif DIFFICULTY == 'Impossible':
        pipeVelX = -9
        pipeGap = 100
        gravity = 1.5

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = gravity
    playerFlapAccv = -8
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        if crashTest:
            saveHighScore(score)
            gameOverScreen(score)
            return

        playerMidPos = playerx + GAME_SPRITES['player'].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()

                # Add achievements
                if score == 10:
                    ACHIEVEMENTS.append("Scored 10 Points!")
                elif score == 20:
                    ACHIEVEMENTS.append("Scored 20 Points!")

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe(pipeGap)  # Pass pipeGap dynamically
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')

    check_assets()

    try:
        GAME_SPRITES['message'] = pygame.image.load(ASSET_PATH + 'message.png').convert_alpha()
        GAME_SPRITES['background'] = pygame.image.load(ASSET_PATH + 'background.png').convert()
        GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
        GAME_SPRITES['base'] = pygame.image.load(ASSET_PATH + 'base.png').convert_alpha()
        GAME_SPRITES['pipe'] = (
            pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
            pygame.image.load(PIPE).convert_alpha()
        )
        GAME_SOUNDS['wing'] = pygame.mixer.Sound(ASSET_PATH + 'wing.wav')
        GAME_SOUNDS['point'] = pygame.mixer.Sound(ASSET_PATH + 'point.wav')
        GAME_SOUNDS['hit'] = pygame.mixer.Sound(ASSET_PATH + 'hit.wav')
    except Exception as e:
        print("Error loading sprites or sounds:", e)
        sys.exit()

    while True:
        menu_choice = mainMenu()
        if menu_choice == "start":
            selectDifficulty()
            mainGame()
        elif menu_choice == "scores":
            viewScores()