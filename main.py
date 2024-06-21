import random
import time
import pgzrun
from helper import *


class Enemy():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.image = img

    def get_info(self, text):
        print(f'{text}\nx = {self.x}\ny = {self.y}\nimage = {self.image}')


start_time = ''
WIDTH = 800
HEIGHT = 600
music_sounds = True
player = Actor('player')
enemy1 = Actor('enemy1')
enemy1.scale = 0
enm1 = Enemy(enemy1.pos[0], enemy1.pos[1], enemy1.image)
enm1.get_info('enemy1 info')
enemy2 = Actor('enemy2')
enemy2.scale = 0
enm2 = Enemy(enemy2.pos[0], enemy2.pos[1], enemy2.image)
enm2.get_info('enemy2 info')
enemy1_dead = False
enemy2_dead = False
speed = 1
player.pos = 400, 150
player.scale = 2.5
on_off_sounds = Actor('on_off', center=(130, 300))
on_off_sounds.scale = 0.2
start_button = Actor('play', center=(400, 300))
start_button.scale = 0.2
exit_button = Actor('exit_button', center=(670, 300))
exit_button.scale = 0.2
game_started = False
result = ''


def die_and_respawn():
    global enemy1_dead, enemy2_dead, speed
    speed -= 0.05
    if enemy1_dead:
        enemy1.image = 'enemy1'
        enemy1_dead = False
        enemy1.scale /= 2
        enemy1.pos = random.randint(1, 800), random.randint(1, 200)
        return
    if enemy2_dead:
        enemy2.image = 'enemy2'
        enemy2_dead = False
        enemy2.scale /= 2
        enemy2.pos = random.randint(1, 800), random.randint(1, 200)
        return


def follow_player():
    if game_started:
        if not enemy1_dead:
            enemy1.right = enemy1.right - 4 if enemy1.pos[0] > player.pos[0] else enemy1.right + 4
            enemy1.top = enemy1.top - 4 if enemy1.pos[1] > player.pos[1] else enemy1.top + 4
        if not enemy2_dead:
            enemy2.right = enemy2.right - 6 if enemy2.pos[0] > player.pos[0] else enemy2.right + 6
            enemy2.top = enemy2.top - 6 if enemy2.pos[1] > player.pos[1] else enemy2.top + 6

        clock.schedule(follow_player, 0.1 * speed)


def play_music():
    if music_sounds:
        sounds.mus.play(-1)


def draw():
    screen.fill((20, 0, 0))
    exit_button.draw()
    start_button.draw()
    on_off_sounds.draw()
    player.draw()
    enemy1.draw()
    enemy2.draw()
    screen.draw.text(result, center=(400, 500))


def update():
    global result
    if game_started:
        if keyboard.w:
            player.top -= 2
        if keyboard.a:
            player.right -= 2
        if keyboard.s:
            player.top += 2
        if keyboard.d:
            player.right += 2
        if (abs(enemy1.pos[0] - player.pos[0]) < 5 and abs(enemy1.pos[1] - player.pos[1]) < 5) or (
                abs(enemy2.pos[0] - player.pos[0]) < 5 and abs(enemy2.pos[1] - player.pos[1]) < 5):
            result = f'Вы проиграли\nВам удалось продержаться {int(time.time() - start_time)} секунд\nПрограмма будет завершена через 5 секунд'
            clock.schedule(exit, 5.0)


def on_mouse_down(pos):
    global music_sounds, game_started, enemy1_dead, enemy2_dead, start_time
    if on_off_sounds.collidepoint(pos):
        sounds.click.play()
        music_sounds = True if music_sounds == False else False
    if start_button.collidepoint(pos):
        sounds.click.play()
        exit_button.scale = 0
        start_button.scale = 0
        on_off_sounds.scale = 0
        game_started = True
        play_music()
        player.pos = 400, 300
        enemy1.scale = 2
        enemy1.pos = random.randint(600, 800), random.randint(1, 600)
        enemy2.scale = 2
        enemy2.pos = random.randint(1, 200), random.randint(1, 600)
        follow_player()
        start_time = time.time()
    if exit_button.collidepoint(pos):
        sounds.click.play()
        exit()
    if enemy1.collidepoint(pos) and not enemy1_dead:
        enemy1_dead = True
        enemy1.image = 'dead'
        sounds.switch.play()
        clock.schedule(die_and_respawn, 1.5)

    if enemy2.collidepoint(pos) and not enemy2_dead:
        enemy2_dead = True
        enemy2.image = 'dead'
        sounds.switch.play()
        clock.schedule(die_and_respawn, 3.0)


# start_game_menu()
pgzrun.go()
