#!/user/bin/env python3
#  -*- coding: utf-8 -*-
import sys

import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def update_screen(ai_settings, screen, stats, sb, ship, bullets, aliens, play_button):
    """更新屏幕上的图像，并切换到新屏幕上"""
    #每一次循环都重绘屏幕
    screen.fill(ai_settings.bg_color)
    # 重绘子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # 显示得分
    sb.show_score()

    #绘制按钮
    if not stats.game_active:
        play_button.draw_button()


    #让最近绘制的屏幕可见
    pygame.display.flip()

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb,
                 play_button, ship, aliens, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                              ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button,
                      ship, aliens, bullets, mouse_x, mouse_y):
    """点击按钮开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #隐藏光标
        pygame.mouse.set_visible(False)
        stats.reset_stats() #重置游戏统计信息
        stats.game_active = True
        #清空外星人和子弹
        aliens.empty()
        bullets.empty()
        #创建新外星人
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        ai_settings.initialize_dynamic_settings()
        #重置记分牌
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()


def update_bullets(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """更新子弹的位置，删除消失的子弹"""
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <=0:
            bullets.remove(bullet)
    #检查子弹是否击中外星人
    check_bullet_alien_collisions(ai_settings, stats, sb, screen, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """响应碰撞，删除子弹"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        #删除现有子弹并新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)

def fire_bullet(ai_settings, screen, ship, bullets):
    """发射子弹"""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人放在当行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def get_number_rows(ai_settings, ship_height, alien_height):
    """计算可以容纳外星人行数"""
    available_space_y = (ai_settings.screen_height
                          - (3*alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return  number_rows

def update_aliens(ai_settings, stats, sb, screen, bullets, aliens, ship):
    """更新外星人位置"""
    check_fleet_edges(ai_settings, aliens)
    check_aliens_bottom(ai_settings, stats, sb, screen, bullets, aliens, ship)
    aliens.update()
    #检测碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, bullets, aliens, ship)

def check_fleet_edges(ai_settings, aliens):
    """外星人到达边缘时"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """外星人下移，变向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, sb, screen, bullets, aliens, ship):
    """飞船撞到外星人"""
    if stats.ships_left > 0:
        stats.ships_left -= 1
        #清空列表
        aliens.empty()
        bullets.empty()
        #创建新外星人
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        #暂停
        sleep(0.5)
        #更新记分牌
        sb.prep_ships()
    else:
        stats.game_activa = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, sb, screen, bullets, aliens, ship):
    """检查外星人到达底部"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, sb, screen, bullets, aliens, ship)
            break

def check_high_score(stats, sb):
    """检查是否是最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
class GameStats():
    """跟踪游戏统计信息"""
    def __init__(self, ai_settings):
        """统计初始化信息"""
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False
        self.high_score = 0

    def reset_stats(self):
        """初始化在游戏运行中可以变化的统计信息"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1


