import os.path

import pygame
import random
from settings import *
from GUI import *


class FlashCard:
    def __init__(self, number, card, screen, active=False, show_answer=False):
        self.number = number
        self.card = card
        self.screen = screen
        self.x, self.y = 50, 50
        self.options_wrap_width = WIDTH-200
        self.active = active
        self.show_answer = show_answer
        self.question = TextWrap(card[0], self.x, self.y, wrap_width=WIDTH-200)
        self.choices = card[1]
        self.randomize_choices = self.choices.copy()

        self.question_type = card[2]
        self.image_path = card[4]
        if self.image_path != "":
            # print(self.image_path)
            self.image = pygame.image.load(os.path.join("images", self.image_path))
        self.explanation = TextWrap(card[5], self.x, 400, wrap_width=WIDTH-200)
        self.correct_answer = False
        self.setup_choices()

    def __repr__(self):
        return str(self.number)

    def setup_choices(self):
        random.shuffle(self.randomize_choices)
        self.choices_text_wrap()
        if self.question_type == "single":
            self.answer = self.choices[int(self.card[3]) - 1]
        else:
            self.answer = []
            temp = self.card[3].split(",")
            for index in temp:
                self.answer.append(self.choices[int(index) - 1])

    def choices_text_wrap(self):
        self.choices_wrap = []
        for i, choice in enumerate(self.randomize_choices):
            if i == 0:

                if self.image_path == "":
                    self.choices_wrap.append(TextWrap(choice, self.x,
                                                      self.y + self.question.wrap_text.get_height() + 30,
                                                      wrap_width=self.options_wrap_width))
                elif self.image.get_height() < 250:
                    self.choices_wrap.append(TextWrap(choice, self.x,
                                                      self.y + self.question.wrap_text.get_height() + 50 + self.image.get_height(),
                                                      wrap_width=self.options_wrap_width))
                else:
                    self.choices_wrap.append(TextWrap(choice, self.x,
                                                      self.y + self.question.wrap_text.get_height() + 30,
                                                      wrap_width=self.options_wrap_width - self.image.get_width() - 50))

            else:
                previous_choice = self.choices_wrap[i - 1]
                if self.image_path == "":
                    self.choices_wrap.append(
                        TextWrap(choice, self.x, previous_choice.y + previous_choice.wrap_text.get_height() + 30,
                                 wrap_width=self.options_wrap_width))

                elif self.image.get_height() < 250:
                    self.choices_wrap.append(
                        TextWrap(choice, self.x, previous_choice.y + previous_choice.wrap_text.get_height() + 30,
                                 wrap_width=self.options_wrap_width))

                else:
                    self.choices_wrap.append(
                        TextWrap(choice, self.x, previous_choice.y + previous_choice.wrap_text.get_height() + 30,
                                 wrap_width=self.options_wrap_width - self.image.get_width() - 50))

        if self.question_type == "single":
            self.options_single = RadioButton(self.screen, self.choices_wrap, 0, 0)
        else:
            self.options_multiple = []
            for choice in self.choices_wrap:
                self.options_multiple.append(
                    CheckBox(self.screen, choice.x, choice.y, choice.text, choice, right_text=True))

    def draw(self, screen):
        # show the question
        if not self.show_answer:
            if self.image_path != "":
                if self.image.get_height() < 250:
                    screen.blit(self.image,  (self.x, self.y + self.question.wrap_text.get_height() + 20))
                else:
                    screen.blit(self.image, (self.x + self.choices_wrap[-1].wrap_width + 70, self.y + self.question.wrap_text.get_height() + 20))
            self.question.draw(screen)
            if self.question_type == "single":
                self.options_single.draw()
            else:
                for option in self.options_multiple:
                    option.draw()

        # show answer
        else:
            self.text.draw(screen)
            if self.question_type == "single":
                self.answer_text.draw(screen)
                self.explanation.y = self.answer_text.y + self.answer_text.render_text.get_height() + 50
            else:
                for a in self.answer_text:
                    a.draw(screen)
                self.explanation.y = self.answer_text[-1].y + self.answer_text[-1].render_text.get_height() + 50

            self.explanation.draw(screen)

    def get_answer(self):
        if self.question_type == "single":
            self.correct_answer = self.options_single.get() == self.answer

        else:
            options_values = []
            for option in self.options_multiple:
                if option.get():
                    options_values.append(option.text)
            self.correct_answer = self.check_multiple_answer(options_values)

        if self.correct_answer:
            self.text = Text(f"CORRECT!     Answer:", self.x, self.y, font_colour=WHITE)
        else:
            self.text = Text(f"INCORRECT!   Answer:", self.x, self.y, font_colour=WHITE)
        self.explanation_text = Text("Explanation", self.x, 460, font_colour=WHITE)

        if self.question_type == "single":
            self.answer_text = TextWrap(self.answer, 50, self.y + self.text.font_render.get_height() + 30,
                                        wrap_width=1000)
        else:
            self.answer_text = []
            for i, option in enumerate(self.answer):
                if i == 0:
                    self.answer_text.append(
                        TextWrap(option, 50, self.y + self.text.font_render.get_height() + 30, wrap_width=1000))
                else:
                    previous_answer = self.answer_text[i - 1]
                    self.answer_text.append(
                        TextWrap(option, 50, previous_answer.y + previous_answer.wrap_text.get_height() + 30, wrap_width=1000))

    def check_multiple_answer(self, user_answer):
        if len(user_answer) == len(self.answer):
            for a in user_answer:
                if a not in self.answer:
                    return False
            return True
        return False

    def handle_events(self, event):
        if self.question_type == "single":
            self.options_single.is_clicked(event)
        else:
            for option in self.options_multiple:
                option.is_clicked(event)
