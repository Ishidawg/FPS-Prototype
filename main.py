from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.health_bar import HealthBar

# Importing packages
from game.settings import ammo, close_fov, default_fov
from game.player import create_player
from game.entities import create_entities
from game.game_logic import set_game_objects, update_handler, input_handler
from game.enemies import Enemy

app = Ursina(title='FPS Prototype')

# Window settings, I dont like that default dev options...
window.borderless = False
window.exit_button.visible = False
window.fps_counter.visible = False
window.entity_counter.visible = False
window.collider_counter.visible = False
window.cog_menu.visible = False
window.cog_button.visible = False


# Creating a solid base, label, ground, lights and shit...
ammo_label = Text(
    text=f"Ammo: {ammo}",
    position=(.2, .425, 0)
)

sky_box = Sky(
    texture="sky_sunset",
    scale=2
)

ground = Entity(
    model="models/ground.obj",
    texture="grass",
    double_sided=True,
    position=(10, 0, 0),
    rotation=(0, 0, 0),
    scale=2,
    collider="mesh"
)

ambient_light = AmbientLight(
    parent=scene,
    color=color.rgb(252, 221, 136) * 0.006
)

directional_light = DirectionalLight(
    parent=scene,
    color=color.rgb(252, 180, 136) * 0.010
)
directional_light.look_at(Vec3(10, -10, 10))

point_light = PointLight(
    parent=camera.ui, 
    position=(0, 0, -12), 
    color=color.rgb(255, 60, 0) * 0.020
)

# Calls the function to create a player, from: game/player.py
player = create_player()

enemy1 = Enemy(position=(5, 50, 5), speed=1, health=30)

health_bar = HealthBar(
    bar_color=color.lime.tint(-.25),
    roundness=0,
    max_value=100,
    value=100,
    scale=(.5, .05)
)

pistol, middle_pistol = create_entities()

set_game_objects(
    player=player,
    ammo_label=ammo_label,
    pistol=pistol,
    middle_pistol=middle_pistol,
    health_bar=health_bar
)

def update():
    update_handler()

def input(key):
    input_handler(key)

app.run()
