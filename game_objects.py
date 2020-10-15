import tiles

class GameObject:
    def __init__(self):
        self.sprite = None
        self.sprite_changed = False
        self.render_center_y = None
        self.render_center_x = None
        self.render_bottom = None
        self.tiles = []
        self.texture = None
        self.durability = 100
        self.resistances = {
            'piercing': 10,
            'crushing': 10,
            'cutting': 10,
            'fire': 10,
            'electric': 10,
            'temperature': 10,
        }