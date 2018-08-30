#!/user/bin/env python3
#  -*- coding: utf-8 -*-
import sys

import pygame

from setting import Settings
from ship import Ship
from alien import Alien
from pygame.sprite import Group
import game_function as gf
from game_function import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    #初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    pygame.display.set_caption("白马探花")
    stats = GameStats(ai_settings)

    #创建一艘飞船
    ship = Ship(ai_settings, screen )

    #创建外星人
    alien = Alien(ai_settings, screen)

    #创建一个用于存储子弹的编组
    bullets = Group()
    aliens = Group()

    #创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)

    #创建按钮
    play_button = Button(ai_settings, screen, "PLAY")

    #创建记分牌
    sb = Scoreboard(ai_settings, screen, stats)

    #开始游戏的主循环
    while True:
        #监视键盘和鼠标事件
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
                        bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, stats, sb, screen, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, sb, screen, bullets, aliens, ship)

        gf.update_screen(ai_settings, screen, stats, sb, ship, bullets,
                         aliens, play_button)

run_game()
