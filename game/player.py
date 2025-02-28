from ursina.prefabs.first_person_controller import FirstPersonController

def create_player():
    player = FirstPersonController(
        model='models/player.obj',
        scale=1,
        position=(0, 80, 0),
        collider='box',
    )
    return player
