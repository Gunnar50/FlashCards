import pygame
import time


def wrap_text(text, font, width, colour):
    """Wrap text to fit inside a given width when rendered.
    :param text: The text to be wrapped.
    :param font: The font the text will be rendered in.
    :param width: The width to wrap to.
    """
    text_lines = text.replace('\t', '    ').split('\n')
    if width is None or width == 0:
        return text_lines

    wrapped_lines = []
    for line in text_lines:
        line = line.rstrip() + ' '
        if line == ' ':
            wrapped_lines.append(line)
            continue

        # Get the leftmost space ignoring leading whitespace
        start = len(line) - len(line.lstrip())
        start = line.index(' ', start)
        while start + 1 < len(line):
            # Get the next potential splitting point
            next = line.index(' ', start + 1)
            if font.size(line[:next])[0] <= width:
                start = next
            else:
                wrapped_lines.append(line[:start])
                line = line[start + 1:]
                start = line.index(' ')
        line = line[:-1]
        if line:
            wrapped_lines.append(line)

    return render_text_list(wrapped_lines, font, colour)


def render_text_list(lines, font, colour=(255, 255, 255)):
    """Draw multiline text to a single surface with a transparent background.
    Draw multiple lines of text in the given font onto a single surface
    with no background colour, and return the result.
    :param lines: The lines of text to render.
    :param font: The font to render in.
    :param colour: The colour to render the font in, default is white.
    """
    rendered = [font.render(line, True, colour).convert_alpha()
                for line in lines]

    line_height = font.get_linesize()
    width = max(line.get_width() for line in rendered)
    tops = [int(round(i * line_height)) for i in range(len(rendered))]
    height = tops[-1] + font.get_height()

    surface = pygame.Surface((width, height)).convert_alpha()
    surface.fill((0, 0, 0, 0))
    for y, line in zip(tops, rendered):
        surface.blit(line, (0, y))

    return surface


class Text:
    def __init__(self, text, x, y, font="Consolas", font_size=22, font_colour=(0, 0, 0)):
        """
        Output text in the screen.

        :param screen: The display (pygame.display)
        :param text: The text to output
        :param x: The x position
        :param y: The y position
        :param font: The font family, which defaults to Consolas
        :param font_size: The font size, which defaults to 24px
        :param font_colour: The font color in r, g, b format, which defaults to white
        """
        self.x, self.y = x, y
        self.text = text
        self.font = font
        self.font_size = font_size
        self.font_colour = font_colour
        self.draw_font()

    def draw_font(self):
        self.font_render = pygame.font.SysFont(self.font, self.font_size)
        self.render_text = self.font_render.render(self.text, True, self.font_colour)

    def draw(self, screen):
        screen.blit(self.render_text, (self.x, self.y))


class TextWrap:
    def __init__(self, text, x, y, font="Consolas", font_size=22, font_colour=(255, 255, 255), wrap_width=800):
        """
        Output text in the screen.

        :param screen: The display (pygame.display)
        :param text: The text to output
        :param x: The x position
        :param y: The y position
        :param font: The font family, which defaults to Consolas
        :param font_size: The font size, which defaults to 24px
        :param font_colour: The font color in r, g, b format, which defaults to white
        """
        self.x, self.y = x, y
        self.text = text
        self.font = font
        self.font_size = font_size
        self.font_colour = font_colour
        self.wrap_width = wrap_width
        self.draw_font()
        self.wrap_text = wrap_text(self.text, self.font_render, self.wrap_width, self.font_colour)

    def draw_font(self):
        self.font_render = pygame.font.SysFont(self.font, self.font_size)
        self.render_text = self.font_render.render(self.text, True, self.font_colour)

    def draw(self, screen):
        screen.blit(self.wrap_text, (self.x, self.y))


class TextField:
    def __init__(self, screen, x, y, box_size=20, font="Consolas", font_size=20, font_colour=(255, 255, 255),
                 box_height=12, placeholder="", required=False):
        """
        Text Field - to get input from the user

        :param screen: The display (pygame.display)
        :param x: x position
        :param y: y position
        :param box_size: The box size in characters, defaults to 20
        :param font: The font family, which defaults to Consolas
        :param font_size: The font size, which defaults to 20px
        :param font_colour: The font color in r, g, b format, which defaults to white
        :param box_height: The box height, this is only to add more spacing between the characters and the box
        :param placeholder:
        :param required:
        """
        # box_size in character
        self.timer = 0
        self.screen = screen
        self.height = box_height
        self.x, self.y = x, y
        self.font = font
        self.font_size = font_size
        self.font_colour = font_colour
        self.text = ""
        self.active = False
        self.colour = (255, 255, 255)
        self.box_size = box_size
        self.character = "a"
        self.character_render = pygame.font.SysFont(self.font, self.font_size) \
            .render(self.character, True, self.font_colour)
        self.width = self.box_size * self.character_render.get_width()
        self.placeholder = placeholder
        self.required = required
        self.empty = False
        self.draw_font()

    def draw_font(self):
        self.sys_font = pygame.font.SysFont(self.font, self.font_size)

    def draw(self):
        if self.active:
            self.colour = (255, 255, 255)
        elif self.empty:
            self.colour = (200, 50, 50)
        else:
            self.colour = (100, 100, 100)

        if self.text != "":
            self.empty = False
            self.text_render = self.sys_font.render(self.text, True, self.font_colour)
        else:
            self.text_render = self.sys_font.render(self.placeholder, True, (100, 100, 100))

        self.input_rect = pygame.Rect(self.x, self.y, self.width + 2 * self.character_render.get_width(),
                                      self.text_render.get_height() + self.height)

        pygame.draw.rect(self.screen, self.colour, self.input_rect, 2)

        self.screen.blit(self.text_render, (self.x + 5, self.y + 8))

        # blinking bar
        if self.active:
            if self.timer > 30:
                self.bar = pygame.draw.line(self.screen, (255, 255, 255),
                                            (max(15, (5 + self.x + (
                                                self.text_render.get_width() if self.text != "" else 0))), 5 + self.y),
                                            (max(15, (5 + self.x + (
                                                self.text_render.get_width() if self.text != "" else 0))),
                                             8 + self.y + self.character_render.get_height()), 2)
                if self.timer == 60:
                    self.timer = 0
            self.timer += 1

    def is_clicked(self, event):
        pygame.key.set_repeat(500, 80)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) < self.box_size:
                        self.text += event.unicode

    def get(self):
        if self.required and self.text == "":
            self.empty = True
        else:
            return self.text


class Button:
    def __init__(self, screen, x, y, width, height, text, command=None, button_colour=(50, 50, 50),
                 button_outline_colour=None,
                 font="Consolas", font_size=22, font_colour=(255, 255, 255)):
        self.screen = screen
        self.x, self.y = x, y
        self.button_colour, self.button_outline_colour = button_colour, button_outline_colour
        self.width, self.height = width, height
        self.text = text
        self.font = font
        self.font_size = font_size
        self.font_colour = font_colour
        self.command = command
        self.draw_font()

    def draw_font(self):
        font = pygame.font.SysFont(self.font, self.font_size)
        self.render_text = font.render(self.text, True, self.font_colour)
        self.draw_x = self.x + (self.width / 2 - self.render_text.get_width() / 2)
        self.draw_y = self.y + (self.height / 2 - self.render_text.get_height() / 2)

    def draw(self):
        if self.button_outline_colour is not None:
            pygame.draw.rect(self.screen, self.button_outline_colour,
                             (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
        pygame.draw.rect(self.screen, self.button_colour, (self.x, self.y, self.width, self.height), 0)

        self.screen.blit(self.render_text, (self.draw_x, self.draw_y))

    def is_clicked(self, event):
        mx, my = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.x <= mx <= self.x + self.width and self.y <= my <= self.y + self.height:
                if self.command is not None:
                    self.command()

    def hover(self, event):
        mx, my = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEMOTION:
            return self.x <= mx <= self.x + self.width and self.y <= my <= self.y + self.height


class Tab:
    def __init__(self, screen, x, y, width, height, options, selected_colour=(50, 10, 200),
                 button_colour=(100, 100, 100), bgcolour=(255, 255, 255), outline_colour=(0, 0, 0),
                 font_size=24, font_colour=(0, 0, 0), font="Consolas"):
        self.screen = screen
        self.options = options
        self.x, self.y = x, y
        self.width, self.height = width / len(options), height
        self.button_colour, self.bgcolour, self.outline_colour = button_colour, bgcolour, outline_colour
        self.selected_colour = selected_colour
        self.font, self.font_size, self.font_colour = font, font_size, font_colour
        self.tabs_list = []
        self.draw_text()

    def draw_text(self):
        for i, text in enumerate(self.options):
            tab = Button(self.screen, self.x + (self.width * i), self.y, self.width, self.height, text,
                         button_colour=self.button_colour, button_outline_colour=self.outline_colour, font=self.font,
                         font_size=self.font_size, font_colour=self.font_colour)
            self.tabs_list.append(tab)
        self.tabs_list[0].button_colour = self.selected_colour

    def draw(self):
        for tab in self.tabs_list:
            tab.draw()

    def is_clicked(self, event):
        mx, my = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for tab in self.tabs_list:
                if tab.x <= mx <= tab.x + tab.width and tab.y <= my <= tab.y + tab.height:
                    tab.button_colour = self.selected_colour
                    for t in self.tabs_list:
                        if t != tab:
                            t.button_colour = self.button_colour

    def get(self):
        for tab in self.tabs_list:
            if tab.button_colour == self.selected_colour:
                return tab.text


class ToggleButton:
    def __init__(self, screen, x, y, width, height, text_left, text_right, round_border=10, text="",
                 button_colour=(0, 0, 0),
                 bgcolour=(255, 255, 255), outline_colour=(0, 0, 0), toggle=True):
        self.screen = screen
        self.colour, self.outline = button_colour, outline_colour
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.text = text
        self.text_left, self.text_right = text_left, text_right
        self.bgcolour = bgcolour
        self.toggle = toggle
        self.round_border = round_border

    def draw(self):
        pygame.draw.rect(self.screen, self.outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0,
                         self.round_border + 1)
        pygame.draw.rect(self.screen, self.bgcolour, (self.x, self.y, self.width, self.height), 0, self.round_border)
        font = pygame.font.SysFont("Consolas", 15)
        if self.toggle:
            pygame.draw.rect(self.screen, self.colour, (self.x, self.y, self.width / 2, self.height), 0,
                             border_top_left_radius=self.round_border, border_bottom_left_radius=self.round_border)
            text_left = font.render(self.text_left, True, self.bgcolour)
            text_right = font.render(self.text_right, True, self.outline)
        else:
            pygame.draw.rect(self.screen, self.colour, (self.x + self.width / 2, self.y, self.width / 2, self.height),
                             0,
                             border_top_right_radius=self.round_border, border_bottom_right_radius=self.round_border)
            text_left = font.render(self.text_left, True, self.outline)
            text_right = font.render(self.text_right, True, self.bgcolour)

        draw_x_left = self.x + (self.width / 2 - text_left.get_width() / 2) / 3
        draw_y_left = self.y + (self.height / 2 - text_left.get_height() / 2)
        draw_x_right = self.x + (self.width / 2 - text_right.get_width() / 2) + (
                self.width / 2 - text_right.get_width() / 2) / 1.6
        draw_y_right = self.y + (self.height / 2 - text_right.get_height() / 2)
        self.screen.blit(text_left, (draw_x_left, draw_y_left))
        self.screen.blit(text_right, (draw_x_right, draw_y_right))

    def is_clicked(self, event):
        mx, my = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.x <= mx <= self.x + self.width and self.y <= my <= self.y + self.height:
                self.toggle = not self.toggle

    def get(self):
        return self.toggle


class CheckBox:
    def __init__(self, screen, x, y, text="", text_wrap_object=None, size=30, checked=False, right_text=False,
                 box_colour=(255, 255, 255),
                 selected_colour=None, box_outline=(0, 0, 0), check_colour=(0, 0, 0),
                 font="Consolas", font_size=20, font_colour=(0, 0, 0)):
        self.screen = screen
        self.x, self.y = x, y
        self.text_wrap_obj = text_wrap_object
        self.text = text
        self.checked = checked
        self.right_text = right_text
        self.box_size = size
        self.spacing = 20
        self.box_colour = box_colour
        self.box_outline = box_outline
        self.check_colour = check_colour
        self.font = font
        self.font_size = font_size
        self.font_colour = font_colour
        self.selected_colour = selected_colour
        self.radio = False
        self.draw_font()

    def draw_font(self):
        font = pygame.font.SysFont(self.font, self.font_size)
        self.render_text = font.render(self.text, True, self.font_colour)
        self.draw_y = self.y + (self.box_size / 2) - (self.render_text.get_height() / 2)
        if self.right_text:
            self.draw_x = self.x + self.box_size + self.spacing
        else:
            self.draw_x = self.x - (self.render_text.get_width()) - self.spacing

    def draw(self):
        if not self.radio:
            # checkbox
            pygame.draw.rect(self.screen, self.box_outline,
                             (self.x - 3, self.y - 3, self.box_size + 6, self.box_size + 6))
            pygame.draw.rect(self.screen, self.box_colour, (self.x, self.y, self.box_size, self.box_size))
            if self.checked:
                # draw tick for checkbox
                if self.selected_colour is not None:
                    pygame.draw.rect(self.screen, self.selected_colour, (self.x, self.y, self.box_size, self.box_size))
                pygame.draw.line(self.screen, self.box_colour if self.selected_colour is not None else self.box_outline,
                                 (self.x + self.box_size / 4, self.y + self.box_size / 2),
                                 (self.x + (self.box_size / 2) - self.box_size / 10, self.y + 3 * (self.box_size / 4)),
                                 3)
                pygame.draw.line(self.screen, self.box_colour if self.selected_colour is not None else self.box_outline,
                                 (self.x + (self.box_size / 2) - self.box_size / 10, self.y + 3 * (self.box_size / 4)),
                                 (self.x + 3 * (self.box_size / 4), self.y + self.box_size / 4), 3)
        else:
            # radio button
            pygame.draw.circle(self.screen, self.box_outline,
                               (self.x + (self.box_size / 2), self.y + (self.box_size / 2)), (self.box_size / 2) + 3)
            pygame.draw.circle(self.screen, self.box_colour if self.selected_colour is None else self.selected_colour,
                               (self.x + (self.box_size / 2), self.y + (self.box_size / 2)), self.box_size / 2)
            if self.checked:
                # draw circle for radio button
                pygame.draw.circle(self.screen,
                                   self.box_colour if self.selected_colour is not None else self.box_outline,
                                   (self.x + (self.box_size / 2), self.y + (self.box_size / 2)),
                                   (self.box_size / 2) - 2)

        if self.text_wrap_obj is not None:
            self.screen.blit(self.text_wrap_obj.wrap_text, (self.draw_x, self.draw_y))
        else:
            self.screen.blit(self.render_text, (self.draw_x, self.draw_y))

    def is_clicked_2(self, event):
        mx, my = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.x <= mx <= self.x + self.box_size and self.y <= my <= self.y + self.box_size:
                self.checked = not self.checked

    def is_clicked(self, event):
        mx, my = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.text_wrap_obj is not None:
                if self.right_text:
                    if self.x <= mx <= self.x + self.box_size + self.text_wrap_obj.wrap_text.get_width() + self.spacing and self.y <= my <= self.y + self.box_size:
                        self.checked = not self.checked
                else:
                    if self.x - self.text_wrap_obj.wrap_text.get_width() - self.spacing <= mx <= self.x + self.box_size and self.y <= my <= self.y + self.box_size:
                        self.checked = not self.checked

            else:
                if self.x <= mx <= self.x + self.box_size and self.y <= my <= self.y + self.box_size:
                    self.checked = not self.checked

    def get(self):
        return self.checked


class RadioButton:
    def __init__(self, screen, options, x, y, size=20, gap=50, right_text=True, wrap_text=True,
                 box_colour=(255, 255, 255),
                 selected_colour=None, box_outline=(0, 0, 0), check_colour=(0, 0, 0),
                 font="Consolas", font_size=20, font_colour=(0, 0, 0)):
        # options is a list with the options as strings
        self.screen = screen
        self.options = options
        self.x, self.y = x, y
        self.right_text = right_text
        self.wrap_text = wrap_text
        self.box_size = size
        self.gap = gap
        self.box_colour = box_colour
        self.selected_colour = selected_colour
        self.box_outline = box_outline
        self.check_colour = check_colour
        self.font = font
        self.font_size = font_size
        self.font_colour = font_colour
        self.radio_button_list = []
        self.create_options()

    def create_options(self):
        for i, option in enumerate(self.options):
            radio = CheckBox(self.screen, option.x, option.y, text=option.text, text_wrap_object=option,
                             size=self.box_size,
                             right_text=self.right_text,
                             box_colour=self.box_colour, selected_colour=self.selected_colour,
                             box_outline=self.box_outline,
                             check_colour=self.check_colour, font=self.font, font_size=self.font_size,
                             font_colour=self.font_colour)
            radio.radio = True
            self.radio_button_list.append(radio)
        self.radio_button_list[0].checked = True

    def draw(self):
        for box in self.radio_button_list:
            box.draw()

    def is_clicked_2(self, event):
        mx, my = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.radio_button_list:
                if button.x <= mx <= button.x + button.box_size and button.y <= my <= button.y + button.box_size:
                    button.checked = True
                    for box in self.radio_button_list:
                        if box != button:
                            box.checked = False

    def is_clicked(self, event):
        mx, my = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.radio_button_list:
                if self.wrap_text:
                    if self.right_text:
                        if button.x <= mx <= button.x + button.box_size + button.text_wrap_obj.wrap_text.get_width() + button.spacing and button.y <= my <= button.y + button.box_size:
                            button.checked = True
                            for box in self.radio_button_list:
                                if box != button:
                                    box.checked = False
                    else:
                        if button.x - button.text_wrap_obj.wrap_text.get_width() - button.spacing <= mx <= button.x + button.box_size and button.y <= my <= button.y + button.box_size:
                            button.checked = True
                            for box in self.radio_button_list:
                                if box != button:
                                    box.checked = False
                else:
                    if button.x <= mx <= button.x + button.box_size and button.y <= my <= button.y + button.box_size:
                        button.checked = True
                        for box in self.radio_button_list:
                            if box != button:
                                box.checked = False

    def get(self):
        for button in self.radio_button_list:
            if button.checked:
                return button.text


class DropDown:
    def __init__(self, screen, x, y, options=None, box_colour=(255, 255, 255), hover_colour=(150, 150, 150),
                 box_outline_colour=(0, 0, 0),
                 box_outline_width=3,
                 font="Consolas", font_size=20, font_colour=(0, 0, 0), default_text="Select an Option"):
        self.screen = screen
        self.x, self.y = x, y
        self.options = [] if options is None else options
        self.box_colour, self.box_outline_colour = box_colour, box_outline_colour
        self.font, self.font_size, self.font_colour = font, font_size, font_colour
        self.opened = False
        self.default_text = default_text
        self.outline_width = box_outline_width
        self.hover_colour = hover_colour
        self.selected = False
        self.draw_font()
        self.create_options()
        self.get_value = ""

    def draw_font(self):
        self.sys_font = pygame.font.SysFont(self.font, self.font_size)
        self.render_text = self.sys_font.render(self.default_text, True, self.font_colour)
        self.box_width = self.render_text.get_width() + 10
        self.box_height = self.render_text.get_height() + 10
        self.draw_x = self.x + (self.box_width / 2 - self.render_text.get_width() / 2)
        self.draw_y = self.y + (self.box_height / 2 - self.render_text.get_height() / 2)

    def create_options(self):
        self.options_rect = []
        self.render_options = []
        for i, option in enumerate(self.options):
            self.options_rect.append([self.box_colour,
                                      pygame.Rect(self.x, self.y + self.box_height + (self.box_height * i),
                                                  self.box_width, self.box_height)])
            self.render_options.append(self.sys_font.render(option, True, self.font_colour))

    def draw(self):
        # box
        if self.opened:
            if len(self.options) > 0:
                for rect, render in zip(self.options_rect, self.render_options):
                    pygame.draw.rect(self.screen, rect[0], rect[1])
                    self.screen.blit(render, (
                        self.draw_x, rect[1].y + (self.box_height / 2 - self.render_text.get_height() / 2)))
            else:
                pygame.draw.rect(self.screen, self.box_colour,
                                 (self.x, self.y + self.box_height, self.box_width, self.box_height))

        # unopened box
        pygame.draw.rect(self.screen, self.box_outline_colour,
                         (self.x - self.outline_width, self.y - self.outline_width,
                          self.box_width + (2 * self.outline_width), self.box_height + (2 * self.outline_width)))
        pygame.draw.rect(self.screen, self.box_colour, (self.x, self.y, self.box_width, self.box_height))

        if not self.selected:
            self.screen.blit(self.render_text, (self.draw_x, self.draw_y))
        else:
            self.screen.blit(self.render, (self.draw_x, self.draw_y))

    def is_clicked(self, event):
        mx, my = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.opened:
                self.opened = False
                for rect, i, render in zip(self.options_rect, range(len(self.render_options)), self.render_options):
                    if rect[1].x <= mx <= rect[1].x + self.box_width and rect[1].y <= my <= rect[1].y + self.box_height:
                        self.selected = True
                        self.render = render
                        self.get_value = self.options[i]

            elif self.x <= mx <= self.x + self.box_width and self.y <= my <= self.y + self.box_height:
                self.opened = not self.opened

        if event.type == pygame.MOUSEMOTION:
            for rect in self.options_rect:
                if rect[1].x <= mx <= rect[1].x + self.box_width and rect[1].y <= my <= rect[1].y + self.box_height:
                    rect[0] = self.hover_colour
                else:
                    rect[0] = self.box_colour

    def get(self):
        return self.get_value


class Drag:
    def __init__(self, x, y, width, text):
        self.x, self.y = x, y
        self.width, self.height = width
        self.text = text


class Drop(Drag):
    def __init__(self, x, y, width, text):
        Drag.__init__(self, x, y, width, text)


class DragDrop:
    def __init__(self, width, height, x, y, options, font="Consolas", font_size=20, font_colour=(0, 0, 0)):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.surface = pygame.Surface((width, height))
        self.options = options  # list of 2 lists
        self.margin = 50
        self.font_family = font
        self.font_size = font_size
        self.font_colour = font_colour
        self.drag_options = []
        self.drop_options = []
        self.create_options()

    def create_options(self):
        for drag in self.options[0]:
            self.drag_options.append(Drag(self.x, self.y, (self.width/2) - self.margin*2))

    def draw_font(self):
        font = pygame.font.SysFont(self.font_family, self.font_size)
        self.render_text = font.render(self.text, True, self.font_colour)
        self.draw_y = self.y + (self.box_size / 2) - (self.render_text.get_height() / 2)
        if self.right_text:
            self.draw_x = self.x + self.box_size + self.spacing
        else:
            self.draw_x = self.x - (self.render_text.get_width()) - self.spacing































