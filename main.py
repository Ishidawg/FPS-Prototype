from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.health_bar import HealthBar

app = Ursina(
    title='FPS Prototype'
)

window.borderless = False
window.exit_button.visible = False
window.fps_counter.visible = False
window.entity_counter.visible = False
window.collider_counter.visible = False
window.cog_menu.visible = False
window.cog_button.visible = False

ammo = 10

ammo_label = Text(
    text=f"Ammo: {ammo}",
    position=(.2, .425, 0)
)

sky_box = Sky(
    texture="sky_sunset",
    scale= 2
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

player = FirstPersonController(
    position=(0, 80, 0)
)   

health_bar = HealthBar(
    bar_color=color.lime.tint(-.25),
    roundness=0,
    max_value=100,
    value=100,
    scale=(.5, .05)
)

pistol = Entity(
    parent=camera,
    model="models/pistol.obj",
    scale=0.65,
    position=(0.4, -1, 1),
    rotation=(0, -90, 0)

)

middle_pistol = Entity(
    parent=camera,
    model="models/pistol.obj",
    scale=0.85,
    position=(0.005, -1.2, .85),
    rotation=(0, -90, 0),
    visible=False
)

close_fov = 80
default_fov = 100

class Bullet(Entity):
    def __init__(self, position, direction):
        super().__init__(
            model='models/bullet.obj',
            scale=0.75,
            position=position,
            collider='mesh'
        )
        self.direction = direction

    def update(self):
        self.position += self.direction * 80 * time.dt
        if distance(self.position, player.position) > 20:
            destroy(self)

def shoot():
    global ammo

    bullet = Bullet(
        position=camera.world_position + camera.forward * 2,
        direction=camera.forward,
    )

    shooting_sound = Audio("sound/shoot.mp3")
    shooting_sound.volume = .2

    ammo = ammo - 1
    ammo_label.text = f"Ammo: {ammo}"

def take_damage(amount):
    health_bar.value -= amount
    health_bar.value = max(0, health_bar.value)

    if health_bar.value <= 0:
        application.quit()

def update():
    if held_keys['h']:
        take_damage(1)

def input(key):
    if key == 'escape':
        application.quit()

    if key == 'left mouse down':
        if ammo > 0:
            shoot()

    if key == 'right mouse down':
        pistol.visible = False
        middle_pistol.visible = True
        camera.animate('fov', close_fov, duration=0.15, curve=curve.in_out_expo)
        player.cursor.visible = False

    if key == 'right mouse up':
        pistol.visible = True
        middle_pistol.visible = False
        camera.animate('fov', default_fov, duration=0.15, curve=curve.in_out_expo)
        player.cursor.visible = True


app.run()
