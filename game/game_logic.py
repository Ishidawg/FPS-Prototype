import random

from ursina import *
from game.entities import Bullet
from game.settings import close_fov, default_fov, ammo as initial_ammo

game_objects = {
    'player': None,
    'ammo_label': None,
    'pistol': None,
    'middle_pistol': None,
    'health_bar': None
}

global_ammo = {'ammo': initial_ammo}

def set_game_objects(player, ammo_label, pistol, middle_pistol, health_bar):
    game_objects['player'] = player
    game_objects['ammo_label'] = ammo_label
    game_objects['pistol'] = pistol
    game_objects['middle_pistol'] = middle_pistol
    game_objects['health_bar'] = health_bar

def shoot():
    if global_ammo['ammo'] <= 0:
        return

    offset = bullet_recoil()

    bullet = Bullet(
        position=camera.world_position + camera.forward * 2 + offset,
        direction=camera.forward,
    )
    shooting_sound = Audio("sound/shoot.mp3")
    shooting_sound.volume = .2

    middle_weapon_model_recoil()
    right_weapon_model_recoil()

    global_ammo['ammo'] -= 1
    ammo_label = game_objects.get('ammo_label')
    if ammo_label:
        ammo_label.text = f"Ammo: {global_ammo['ammo']}"

def take_damage(amount):
    health_bar = game_objects.get('health_bar')
    if health_bar:
        health_bar.value -= amount
        health_bar.value = max(0, health_bar.value)
        if health_bar.value <= 0:
            application.quit()

def update_handler():
    if held_keys.get('h'):
        take_damage(1)

def recharge_weapon():
    pistol = game_objects.get('pistol')
    middle_pistol = game_objects.get('middle_pistol')
    
    reload_pos_pistol = Vec3(0.8, -1.2, 1.2)
    reload_pos_middle = Vec3(0.005, -1.4, 0.7)
    
    pistol.animate('position', reload_pos_pistol, duration=0.15, curve=curve.in_out_expo)
    middle_pistol.animate('position', reload_pos_middle, duration=0.15, curve=curve.in_out_expo)
    
    invoke(reset_both_weapon_model, delay=0.3)
    
    global_ammo['ammo'] = 50
    ammo_label = game_objects.get('ammo_label')
    if ammo_label:
         ammo_label.text = f"Ammo: {global_ammo['ammo']}"

def bullet_recoil():
    random_x = round(random.uniform(-0.06, 0.06), 3)
    random_y = round(random.uniform(-0.08, 0.08), 3)
    random_z = round(random.uniform(-0.02, 0.02), 3)
    return Vec3(random_x, random_y, random_z)


def middle_weapon_model_recoil():
    random_x = round(random.uniform(-0.02 , 0.02), 3)
    random_y = round(random.uniform(-1.25 , -1.15), 3)
    random_z = round(random.uniform(0.70 , 0.90), 3)

    middle_pistol = game_objects.get('middle_pistol')
    middle_pistol.position=(random_x, random_y, random_z)
    
def right_weapon_model_recoil():
    random_x = round(random.uniform(0.38 , 0.42), 3)
    random_y = round(random.uniform(-0.96 , -1.04), 3)
    random_z = round(random.uniform(0.98 , 1.02), 3)

    pistol = game_objects.get('pistol')
    pistol.position=(random_x, random_y, random_z)

def reset_both_weapon_model():
    middle_pistol = game_objects.get('middle_pistol')
    middle_pistol.position=(0.005, -1.2, 0.85)


    pistol = game_objects.get('pistol')
    pistol.position=(0.4, -1, 1)

def input_handler(key):
    player = game_objects.get('player')
    if key == 'escape':
        application.quit()

    if key == 'r':
        recharge_weapon()

    if key == 'left mouse down':
        shoot()

    if key == 'left mouse up':
        reset_both_weapon_model()

    if key == 'right mouse down':
        pistol = game_objects.get('pistol')
        middle_pistol = game_objects.get('middle_pistol')
        if pistol and middle_pistol:
            pistol.visible = False
            middle_pistol.visible = True
        camera.animate('fov', close_fov, duration=0.15, curve=curve.in_out_expo)
        if player:
            player.cursor.visible = False

    if key == 'right mouse up':
        pistol = game_objects.get('pistol')
        middle_pistol = game_objects.get('middle_pistol')
        if pistol and middle_pistol:
            pistol.visible = True
            middle_pistol.visible = False
        camera.animate('fov', default_fov, duration=0.15, curve=curve.in_out_expo)
        if player:
            player.cursor.visible = True
