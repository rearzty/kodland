import random
import time
import pgzrun
from helper import *

class Enemy():
    current_scale = 0
    def __init__(self, actor, dead, enemy_speed, imgs: list):
        self.actor = actor
        self.dead = dead
        self.enemy_speed = enemy_speed
        self.imgs = imgs
        self.chosen = imgs[0]
        self.timer = 0
    def spawn(self):
        self.actor.pos = random.randint(600, 800), random.randint(1, 600)
    def create(self):
        self.actor.draw()
    def walk(self):
        self.change_img(self.imgs[0] if self.actor.image == self.imgs[1] else self.imgs[1])
        self.change_scale(self.current_scale)
        self.actor.right = self.actor.right - self.enemy_speed if self.actor.pos[0] > player.pos[0] else self.actor.right + self.enemy_speed
        self.actor.top = self.actor.top - self.enemy_speed if self.actor.pos[1] > player.pos[1] else self.actor.top + self.enemy_speed
    def respawn(self):
        self.actor.image = self.imgs[0]
        self.dead = False
        self.change_scale(self.current_scale / 2 if (self.current_scale / 2) >= 0.5 else 0.5)
        self.actor.pos = random.randint(1, 800), random.randint(1, 200)
    def get_pos(self):
        return [self.actor.pos[0], self.actor.pos[1]]
    def change_scale(self, value):
        self.actor.scale = value
        self.current_scale = value
    def change_img(self, value):
        self.actor.image = value


start_time = ''
WIDTH = 800
HEIGHT = 600
music_sounds = True
player = Actor('player')
enemy1 = Actor('enemy1')
enm1 = Enemy(enemy1, dead=False, enemy_speed=4, imgs=['enemy1', 'enemy1_'])
enemy2 = Actor('enemy2')
enm2 = Enemy(enemy2, dead=False, enemy_speed=6, imgs=['enemy2', 'enemy2_'])
speed = 1
enm1.change_scale(0)
enm2.change_scale(0)
player_timer = 0
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
    global speed
    speed -= 0.05
    if enm1.dead:
        enm1.respawn()
        return
    if enm2.dead:
        enm2.respawn()
        return


def follow_player():
    if game_started:
        if not enm1.dead:
            enm1.walk()
        if not enm2.dead:
            enm2.walk()

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
    enm1.create()
    enm2.create()
    screen.draw.text(result, center=(400, 500))

def player_moving():
    global player_timer
    if keyboard.w or keyboard.a or keyboard.s or keyboard.d:
        if player_timer == 10:
            player.image = 'player' if player.image == 'player_' else 'player_'
            player.scale = 2.5
            player_timer = 0
        player_timer+=1
def update():
    global result
    if game_started:
        player_moving()
        if keyboard.w:
            player.top -= 2
        if keyboard.a:
            player.right -= 2
        if keyboard.s:
            player.top += 2
        if keyboard.d:
            player.right += 2
        if (abs(enm1.get_pos()[0] - player.pos[0]) < 5 and abs(enm1.get_pos()[1] - player.pos[1]) < 5) or (
                abs(enm2.get_pos()[0] - player.pos[0]) < 5 and abs(enm2.get_pos()[1] - player.pos[1]) < 5):
            result = f'Вы проиграли\nВам удалось продержаться {int(time.time() - start_time)} секунд\nПрограмма будет завершена через 5 секунд'
            clock.schedule(exit, 5.0)


def on_mouse_down(pos):
    global music_sounds, game_started, start_time
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
        enm1.change_scale(2)
        enm1.spawn()
        enm2.change_scale(2)
        enm2.spawn()
        follow_player()
        start_time = time.time()
    if exit_button.collidepoint(pos):
        sounds.click.play()
        exit()
    if enemy1.collidepoint(pos) and not enm1.dead:
        enm1.dead = True
        enm1.change_img('dead')
        sounds.switch.play()
        clock.schedule(die_and_respawn, 1.5)

    if enemy2.collidepoint(pos) and not enm2.dead:
        enm2.dead = True
        enm2.change_img('dead')
        sounds.switch.play()
        clock.schedule(die_and_respawn, 3.0)


pgzrun.go()
