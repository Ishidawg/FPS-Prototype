import random

from ursina import *
from game.entities import Bullet
from game.settings import close_fov, default_fov, speed, ammo as initial_ammo
from game.enemies import Enemy

game_objects = {
    'player': None,
    'ammo_label': None,
    'pistol': None,
    'middle_pistol': None,
    'health_bar': None
}

is_aiming = False
is_shooting = False
is_crouch = False

global_ammo = {'ammo': initial_ammo}

running_pos_pistol_both = Vec3(0, -100, 5)
default_pistol_rotation = Vec3(0, -90, 0)


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

    middle_weapon_model_recoil()
    right_weapon_model_recoil()

    global_ammo['ammo'] -= 1
    ammo_label = game_objects.get('ammo_label')
    if ammo_label:
        ammo_label.text = f"Ammo: {global_ammo['ammo']}"
    
    shooting_sound = Audio("sound/shoot.mp3")
    shooting_sound.volume = .2

def take_damage(amount):
    health_bar = game_objects.get('health_bar')
    if health_bar:
        health_bar.value -= amount
        health_bar.value = max(0, health_bar.value)
        if health_bar.value <= 0:
            application.quit()

def sprint_up():
    player = game_objects.get('player')
    player.speed = speed + 16


def apply_weapon_rotation():
    pistol = game_objects.get('pistol')
    middle_pistol = game_objects.get('middle_pistol')
    pistol.rotation = running_pos_pistol_both
    middle_pistol.rotation = running_pos_pistol_both

def crouch():
    player = game_objects.get('player')
    pistol = game_objects.get('pistol')
    middle_pistol = game_objects.get('middle_pistol')

    # pistol.always_on_top=True
    # middle_pistol.always_on_top=True

    if hasattr(player, 'camera_pivot'):
        player.camera_pivot.animate('y', 1.2, duration=0.4, curve=curve.in_out_expo)

def stand_up():
    player = game_objects.get('player')
    pistol = game_objects.get('pistol')
    middle_pistol = game_objects.get('middle_pistol')

    # pistol.always_on_top=False
    # middle_pistol.always_on_top=False

    if hasattr(player, 'camera_pivot'):
        player.camera_pivot.animate('y', 2.6, duration=0.4, curve=curve.in_out_expo)

def update_handler():
    global is_crouch
    player = game_objects.get('player')

    if held_keys.get('h'):
        take_damage(1)

    if held_keys.get('shift') and not is_aiming:
       sprint_up()

       if not is_shooting:
            apply_weapon_rotation()
    else:
        player.speed = speed
        reset_both_weapon_model_rotation()

    if held_keys.get('c'):
        if not is_crouch:
            crouch()
            is_crouch = True
    else:
        if is_crouch:
            stand_up()
            is_crouch = False

    # if held_keys.get('left mouse'):
    #     is_shooting = True
    #     reset_both_weapon_model_rotation()
    #     shoot()
    # else:
    #     is_shooting = False
    #     reset_both_weapon_model_position()

    # if held_keys.get('right mouse'):
    #     is_aiming = True
    #     pistol = game_objects.get('pistol')
    #     middle_pistol = game_objects.get('middle_pistol')
    #     if pistol and middle_pistol:
    #         pistol.visible = False
    #         middle_pistol.visible = True
    #     camera.animate('fov', close_fov, duration=0.15, curve=curve.in_out_expo)
    #     if player:
    #         player.cursor.visible = False
    # else:
    #     is_aiming = False
    #     pistol = game_objects.get('pistol')
    #     middle_pistol = game_objects.get('middle_pistol')
    #     if pistol and middle_pistol:
    #         pistol.visible = True
    #         middle_pistol.visible = False
    #     camera.animate('fov', default_fov, duration=0.15, curve=curve.in_out_expo)
    #     if player:
    #         player.cursor.visible = True


def recharge_weapon():
    pistol = game_objects.get('pistol')
    middle_pistol = game_objects.get('middle_pistol')
    
    reload_pos_pistol = Vec3(0.8, -1.2, 1.2)
    reload_pos_middle = Vec3(0.005, -1.4, 0.7)
    
    pistol.animate('position', reload_pos_pistol, duration=0.15, curve=curve.in_out_expo)
    middle_pistol.animate('position', reload_pos_middle, duration=0.15, curve=curve.in_out_expo)
    
    reloading_sound = Audio("sound/reloading.mp3")
    reloading_sound.volume = .2
    
    invoke(reset_both_weapon_model_position, delay=0.3)
    
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

def reset_both_weapon_model_position():
    middle_pistol = game_objects.get('middle_pistol')
    middle_pistol.position=(0.005, -1.2, 0.85)
    middle_pistol.rotation = default_pistol_rotation

    pistol = game_objects.get('pistol')
    pistol.position=(0.4, -1, 1)
    pistol.rotation = default_pistol_rotation

    
def reset_both_weapon_model_rotation():
    middle_pistol = game_objects.get('middle_pistol')
    middle_pistol.rotation = default_pistol_rotation

    pistol = game_objects.get('pistol')
    pistol.rotation = default_pistol_rotation

def spawn_enemy():
    enemy = Enemy(
        position=(random.randint(-20, 20), 50, random.randint(-20, 20)),
        speed=random.uniform(3, 10),
        health=30
    )

def enemy_spawn_loop():
    spawn_enemy()
    invoke(enemy_spawn_loop, delay=random.uniform(2, 5))

def input_handler(key):
    global is_aiming
    global is_shooting

    player = game_objects.get('player')

    if key == 'escape':
        application.quit()

    if key == 'r':
        if global_ammo['ammo'] < 50:
            recharge_weapon()

    if key == 'q':
        spawn_enemy()

    if key == 'left mouse down':
        is_shooting = True
        reset_both_weapon_model_rotation()
        shoot()
        
    if key == 'left mouse up':
        is_shooting = False
        reset_both_weapon_model_position()

    if key == 'right mouse down':
        is_aiming = True
        pistol = game_objects.get('pistol')
        middle_pistol = game_objects.get('middle_pistol')
        if pistol and middle_pistol:
            pistol.visible = False
            middle_pistol.visible = True
        camera.animate('fov', close_fov, duration=0.15, curve=curve.in_out_expo)
        if player:
            player.cursor.visible = False

    if key == 'right mouse up':
        is_aiming = False
        pistol = game_objects.get('pistol')
        middle_pistol = game_objects.get('middle_pistol')
        if pistol and middle_pistol:
            pistol.visible = True
            middle_pistol.visible = False
        camera.animate('fov', default_fov, duration=0.15, curve=curve.in_out_expo)
        if player:
            player.cursor.visible = True
