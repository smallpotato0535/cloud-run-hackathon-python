class Player:
    def __init__(self, url, x, y, dir, wasHit, score) -> None:
        self.url = url
        self.x = x
        self.y = y
        self.dir = dir
        self.wasHit = wasHit
        self.score = score

    