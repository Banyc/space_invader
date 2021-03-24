
import game


class Environment(game.Game):
    def __init__(self, num_of_enemies=1):
        super(Environment, self).__init__(num_of_enemies=num_of_enemies)
        self.previous_score = 0

    def get_reward(self):
        game_over_reward = -100
        score_reward = 10
        reward = 0

        if self.is_game_over:
            reward += game_over_reward
        reward += (self.score_value - self.previous_score) * score_reward

        return reward

    def play_step(self, action):
        self.previous_score = self.score_value
        self.do_each_game_loop(action)
        return (self.get_state(), self.get_reward())

    def get_state(self):
        return [
            self.enemy_x[0],
            self.enemy_y[0],
            self.enemy_x_change[0],
            self.enemy_y_change[0],
            self.player_x,
            self.player_y,
            1 if self.bullet_state == "ready" else 0,
        ]
