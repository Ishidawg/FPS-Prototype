from ursina import *

class Enemy(Entity):
    def __init__(self, position=(0,0,0), speed=1, health=30, **kwargs):
        super().__init__(
            model='cube',
            color=color.red,
            position=position,
            collider='box',
            **kwargs
        )
        self.speed = speed
        self.max_health = health
        self.health = health

        self.health_bar_bg = Entity(
            parent=self,
            model='quad',
            scale=(1, 0.1),
            position=(0, 1.4, 0),
            color=color.gray,
            billboard=True,
            # origin_x=-0.5
        )

        self.health_bar = Entity(
            parent=self.health_bar_bg,
            model='quad',
            scale=(1, 1),
            # origin_x=-0.5,
            color=color.green,
            billboard=True
        )

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

        self.health_bar.scale_x = self.health / self.max_health
        if self.health <= 0:
            destroy(self)

    def update(self):
        self.rotation_y += 20 * time.dt
