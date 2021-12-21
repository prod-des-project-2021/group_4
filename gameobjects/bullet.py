from .gameobject import GameObject

class Bullet(GameObject):
    def __init__(self, sprite):
        super().__init__(sprite)
        self.speed = 8
        self.owner = 0

    def update(self):
        self.position += self.direction * self.speed
