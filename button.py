#!/user/bin/env python3
#  -*- coding: utf-8 -*-
import  pygame.font

class Button():
    def __init__(self, ai_settings, screen, msg):
        """初始按钮属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        #设置按钮大小
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        #创建按钮rect对象
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        #按钮标签只创建一次
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """将msg渲染成图像并使其在按钮上"""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """绘制用颜色填充的按钮，绘制文本"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)