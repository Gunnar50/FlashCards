import os.path
import random

import pydantic
import pygame

import gui
import settings


class Card(pydantic.BaseModel):
  question: str
  options: list[str]
  answers: list[int]
  image_path: str | None = None
  explanation: str | None = None


class FlashCard:
  def __init__(self, card: Card, index: int, screen: pygame.Surface):
    self.index = index
    self.card = card
    self.screen = screen
    self.x, self.y = 50, 50
    self.options_wrap_width = settings.WIDTH - 200
    self.show_answer = False
    self.question = gui.TextWrap(
      card.question, self.x, self.y, wrap_width=settings.WIDTH - 200
    )
    self.options = card.options
    self.randomize_choices = self.options.copy()

    self.image_path = card.image_path
    if self.image_path is not None:
      self.image = pygame.image.load(os.path.join('images', self.image_path))

    self.explanation: gui.TextWrap | None
    if card.explanation is not None:
      self.explanation = gui.TextWrap(
        card.explanation, self.x, 400, wrap_width=settings.WIDTH - 200
      )
    else:
      self.explanation = None

    self.is_correct_answer = False
    self.setup_options()

  def __repr__(self):
    return str(self.index)

  def setup_options(self):
    random.shuffle(self.randomize_choices)
    self.answers: list[str] = []
    for index in self.card.answers:
      self.answers.append(self.options[int(index) - 1])
    self.choices_text_wrap()

  def choices_text_wrap(self):
    self.choices_wrap = []
    for index, choice in enumerate(self.randomize_choices):
      if index == 0:
        if self.image_path is None:
          self.choices_wrap.append(
            gui.TextWrap(
              choice,
              self.x,
              self.y + self.question.wrap_text.get_height() + 30,
              wrap_width=self.options_wrap_width,
            )
          )
        elif self.image.get_height() < 250:
          self.choices_wrap.append(
            gui.TextWrap(
              choice,
              self.x,
              self.y
              + self.question.wrap_text.get_height()
              + 50
              + self.image.get_height(),
              wrap_width=self.options_wrap_width,
            )
          )
        else:
          self.choices_wrap.append(
            gui.TextWrap(
              choice,
              self.x,
              self.y + self.question.wrap_text.get_height() + 30,
              wrap_width=self.options_wrap_width - self.image.get_width() - 50,
            )
          )

      else:
        previous_choice = self.choices_wrap[index - 1]
        if self.image_path is None:
          self.choices_wrap.append(
            gui.TextWrap(
              choice,
              self.x,
              previous_choice.y + previous_choice.wrap_text.get_height() + 30,
              wrap_width=self.options_wrap_width,
            )
          )

        elif self.image.get_height() < 250:
          self.choices_wrap.append(
            gui.TextWrap(
              choice,
              self.x,
              previous_choice.y + previous_choice.wrap_text.get_height() + 30,
              wrap_width=self.options_wrap_width,
            )
          )

        else:
          self.choices_wrap.append(
            gui.TextWrap(
              choice,
              self.x,
              previous_choice.y + previous_choice.wrap_text.get_height() + 30,
              wrap_width=self.options_wrap_width - self.image.get_width() - 50,
            )
          )

    self.ui_options: list[gui.CheckBox | gui.RadioButton] = []
    if len(self.answers) == 1:
      self.ui_options = [
        gui.RadioButton(
          self.screen,
          self.choices_wrap,
          0,
          0,
        )
      ]
    else:
      # TODO: Update checkboxes to create the checkboxes within the object, like radio buttons are
      for choice_wrap in self.choices_wrap:
        self.ui_options.append(
          gui.CheckBox(
            self.screen,
            choice_wrap.x,
            choice_wrap.y,
            choice_wrap.text,
            choice_wrap,
            right_text=True,
          )
        )

  def draw(self, screen):
    # show the question
    if not self.show_answer:
      if self.image_path is not None:
        if self.image.get_height() < 250:
          screen.blit(
            self.image,
            (self.x, self.y + self.question.wrap_text.get_height() + 20),
          )
        else:
          screen.blit(
            self.image,
            (
              self.x + self.choices_wrap[-1].wrap_width + 70,
              self.y + self.question.wrap_text.get_height() + 20,
            ),
          )
      self.question.draw(screen)
      for option in self.ui_options:
        option.draw()

    # show answer
    else:
      self.text.draw(screen)
      for answer in self.answer_text:
        answer.draw(screen)
      if self.explanation is not None:
        self.explanation.y = (
          self.answer_text[-1].y
          + self.answer_text[-1].render_text.get_height()
          + 50
        )
        self.explanation.draw(screen)

  def get_answer(self) -> None:
    options_values = []
    for option in self.ui_options:
      if isinstance(option, gui.CheckBox):
        if option.get():
          options_values.append(option.text)
      else:
        if text := option.get():
          options_values.append(text)

    self.is_correct_answer = self.check_answer(options_values)

    if self.is_correct_answer:
      self.text = gui.Text(
        'CORRECT!     Answer:', self.x, self.y, font_colour=settings.WHITE
      )
    else:
      self.text = gui.Text(
        'INCORRECT!   Answer:', self.x, self.y, font_colour=settings.WHITE
      )
    self.explanation_text = gui.Text(
      'Explanation', self.x, 460, font_colour=settings.WHITE
    )

    self.answer_text: list[gui.TextWrap] = []
    for index, answer in enumerate(self.answers):
      if index == 0:
        self.answer_text.append(
          gui.TextWrap(
            answer,
            50,
            self.y + self.text.font_render.get_height() + 30,
            wrap_width=1000,
          )
        )
      else:
        previous_answer = self.answer_text[index - 1]
        self.answer_text.append(
          gui.TextWrap(
            answer,
            50,
            previous_answer.y + previous_answer.wrap_text.get_height() + 30,
            wrap_width=1000,
          )
        )

  def check_answer(self, user_answer: list[str]) -> bool:
    if len(user_answer) != len(self.answers):
      return False

    for answer in user_answer:
      if answer not in self.answers:
        return False
    return True

  def handle_events(self, event) -> None:
    for option in self.ui_options:
      option.is_clicked(event)
