from src.domain.post.post import Post

class PostRank:
    affinity: float = 1.0
    weight: float = 1.0
    time_decay: float = 0
    total_score: float = 0.0

    def __init__(self, post: Post):
        self.post = post
    
    def compute_total_score(self):
        self.total_score = self.affinity*self.weight*self.time_decay