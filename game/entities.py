from ursina import *

from game.enemies import Enemy

class Bullet(Entity):
    def __init__(self, position, direction):
        super().__init__(
            model='models/bullet.obj',
            scale=0.75,
            position=position,
            collider='sphere'
        )
        self.direction = direction

    def update(self):
        from game.game_logic import game_objects
        self.position += self.direction * 80 * time.dt

        hit_info = self.intersects()

        if hit_info.hit:
            if hasattr(hit_info.entity, 'take_damage'):
                hit_info.entity.take_damage(10)
            destroy(self)
            return

        player = game_objects.get('player')
        if player and distance(self.position, player.position) > 20:
            destroy(self)

def create_entities():
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
        position=(0.005, -1.2, 0.85),
        rotation=(0, -90, 0),
        visible=False
    )
    return pistol, middle_pistol
