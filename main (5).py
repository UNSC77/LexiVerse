
import pygame
import sys
from transformers import pipeline, AutoTokenizer, set_seed
import torch
import random
import string

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("LexiVerse")
# Set up the font
font = pygame.font.Font(None, 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 255, 0)
PURPLE = (147, 0, 211)

# Fonts
font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def main():
    # Set up AI model
    set_seed(42)
    print("Initializing model...")
    tokenizer = AutoTokenizer.from_pretrained('gpt2', pad_token_id=50256)
    generator = pipeline('text-generation', model='gpt2', tokenizer=tokenizer, device=-1)
    print("Model initialized!")

    if torch.backends.cuda.is_built():
        torch.backends.cuda.matmul.allow_tf32 = True

    # Game state variables
    input_text = ""
    favorite_words = []
    current_word = ""
    new_word = ""
    state = "input"  # States: "input", "learning"
    
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if state == "input":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and input_text:
                        favorite_words = [word.strip() for word in input_text.split(",")]
                        state = "learning"
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode
            
            elif state == "learning":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if favorite_words:
                        current_word = favorite_words.pop(0)
                        # Generate new word
                        letters = string.ascii_lowercase + 'äöüßáéíóúñ'
                        vowels = 'aeiouäöüáéíóú'
                        consonants = ''.join(c for c in letters if c not in vowels)
                        
                        word_length = random.randint(4, 8)
                        start_letter = random.choice([c for c in letters if c != current_word[0].lower()])
                        new_word = start_letter
                        
                        for i in range(word_length - 1):
                            if i % 2 == 0:
                                new_word += random.choice(vowels)
                            else:
                                new_word += random.choice(consonants)
                    else:
                        state = "input"
                        input_text = ""
                        current_word = ""
                        new_word = ""

        # Drawing
        screen.fill(BLACK)
        
        if state == "input":
            draw_text("Language Learning Game", font_large, BLUE, WINDOW_WIDTH//2, 100)
            draw_text("Enter your favorite words (separated by commas):", font_medium, WHITE, WINDOW_WIDTH//2, 200)
            draw_text(input_text + "|", font_medium, GREEN, WINDOW_WIDTH//2, 250)
            draw_text("Press Enter when ready", font_small, WHITE, WINDOW_WIDTH//2, 350)
        
        elif state == "learning":
            draw_text("Language Learning Game", font_large, BLUE, WINDOW_WIDTH//2, 100)
            if current_word:
                draw_text(f"Original Word: {current_word}", font_medium, WHITE, WINDOW_WIDTH//2, 200)
                draw_text(f"New Word: {new_word}", font_medium, PURPLE, WINDOW_WIDTH//2, 250)
            draw_text(f"Words remaining: {len(favorite_words)}", font_small, WHITE, WINDOW_WIDTH//2, 350)
            draw_text("Press SPACE for next word", font_small, WHITE, WINDOW_WIDTH//2, 400)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
