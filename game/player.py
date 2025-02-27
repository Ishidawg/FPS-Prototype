from ursina.prefabs.first_person_controller import FirstPersonController

def create_player():
    player = FirstPersonController(
        position=(0, 80, 0)
    )
    return player
