import pygame
from settings import *
from sprites import *
from file_handle import get_questions
from GUI import *
import json


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.questions = get_questions()
        self.flash_cards = []
        self.correct_questions = []
        self.create_cards()
        self.is_question = True

    def create_cards(self):
        ordered_flash_cards = []
        for number, card in enumerate(self.questions):
            ordered_flash_cards.append(FlashCard(number, card, self.screen))

        try:
            with open("cards.json", "r") as f:
                data = json.load(f)

            for number in data["card_order"]:
                card = next((card for card in ordered_flash_cards if card.number == number), None)
                if card:
                    self.flash_cards.append(card)

            for number in data["correct_order"]:
                card = next((card for card in ordered_flash_cards if card.number == number), None)
                if card:
                    self.correct_questions.append(card)

            print(data["card_order"] == [card.number for card in self.flash_cards])
            print(self.correct_questions)

        except FileNotFoundError:
            self.flash_cards = list(ordered_flash_cards)
            random.shuffle(self.flash_cards)

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        pass

    def draw(self):
        self.screen.fill(BGCOLOUR)
        self.flash_cards[-1].draw(self.screen)
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open("cards.json", "w") as f:
                    json.dump({"card_order": [card.number for card in self.flash_cards], "correct_order": [card.number for card in self.correct_questions]}, f)

                pygame.quit()
                quit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    if self.is_question:
                        self.flash_cards[-1].get_answer()
                        self.flash_cards[-1].show_answer = True
                        if self.flash_cards[-1].correct_answer:
                            if self.flash_cards[-1] not in self.correct_questions:
                                self.correct_questions.append(self.flash_cards[-1])
                        else:
                            if self.flash_cards[-1] in self.correct_questions:
                                self.correct_questions.remove(self.flash_cards[-1])
                        self.progress = f"{len(self.correct_questions)} / {len(self.flash_cards)}"
                        print(self.progress)
                    else:
                        self.place_card_back()
                        self.change_screen_size()

                    self.is_question = not self.is_question

                if event.button == 1:
                    self.flash_cards[-1].handle_events(event)

    def place_card_back(self):
        if self.flash_cards[-1].correct_answer:
            index = 0

        else:
            if len(self.flash_cards) > 50:
                index = random.randint(len(self.flash_cards) - len(self.flash_cards)//4, len(self.flash_cards)-4)

            else:
                index = random.randint(len(self.flash_cards)//2, len(self.flash_cards)-4)

        self.flash_cards[-1].show_answer = False
        self.flash_cards[-1].correct_answer = False
        self.flash_cards[-1].setup_choices()
        self.flash_cards.insert(index, self.flash_cards.pop())

    def change_screen_size(self):
        global WIDTH
        self.flash_cards[-1].options_wrap_width = WIDTH - 200
        self.flash_cards[-1].setup_choices()
        self.flash_cards[-1].question.wrap_width = WIDTH - 200

        if self.flash_cards[-1].choices_wrap[-1].y > HEIGHT:
            WIDTH = 1800
            self.flash_cards[-1].options_wrap_width = WIDTH-200
            self.flash_cards[-1].setup_choices()
            self.flash_cards[-1].question.wrap_width = WIDTH-200

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        WIDTH = 1300





game = Game()
game.run()
