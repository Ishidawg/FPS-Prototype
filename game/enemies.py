from ursina import *

class Enemy(Entity):
    def __init__(self, position=(0,0,0), speed=1, health=30, **kwargs):
        super().__init__(
            model='models/enemy.obj',
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
            # origin_x=0.5,
            # x=-0.5,
        )

        self.health_bar = Entity(
            parent=self.health_bar_bg,
            model='quad',
            scale=(1, 1),
            # origin_x=0.5,
            # x=-0.5,
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
        from game.game_logic import game_objects
        from game.entities import Bullet

        player = game_objects.get('player')

        # Prevents enemies from dive down the ground

        hit_info = raycast(self.position, direction=(0, -1, 0), distance=2, ignore=[self])
        self.gravity = 9.8 # Like earth

        if not hit_info.hit:
            self.position = self.position + Vec3(0, -self.gravity * time.dt, 0) # Floatig down
        else:
            self.y = hit_info.world_point.y + 0.39

        if player:
            self.look_at(player.position)
            self.position = self.position + self.forward * self.speed * time.dt

            # Need to revise IF I WILL leave this feature
            bullets = [e for e in scene.entities if isinstance(e, Bullet)]

            for bullet in bullets:
                if distance(self.position, bullet.position) < 5:


                    # Explain this shit:
                    # - 30% chance of dogde on full life
                    # - 50% change of dogde on half life (3 ??)
                    # - 0% of change when it almost dying

                    chance_to_dodge = 0.3 * (self.health / self.max_health)

                    if random.random() < chance_to_dodge:
                        self.dodge()
                    
                    # if random.random() < 0.3:  # Divided by 100, need to tweak this later on!
                    #     self.dodge()

            if self.intersects(player).hit:
                from game.game_logic import take_damage
                take_damage(10)
                destroy(self)

        # self.rotation_y += 20 * time.dt  ANTIGO!

    def dodge(self):
        side = random.choice([-1, 1])
        dodge_pos = self.position + self.right * side * 2
        self.animate_position(dodge_pos, duration=0.2, curve=curve.linear)
