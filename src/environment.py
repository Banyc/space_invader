
import game


class Environment(game.Game):
    def __init__(self, is_render, num_of_enemies=1):
        super(Environment, self).__init__(is_render=is_render, num_of_enemies=num_of_enemies)
        self.previous_score = 0
        self.previous_bullet_state = "ready"

    def get_reward(self):
        game_over_reward = -20
        score_reward = 30
        shotting_reward = -10
        reward = 0

        if self.is_game_over:
            reward += game_over_reward
        reward += (self.score_value - self.previous_score) * score_reward
        if self.bullet_state == "fire" and self.previous_bullet_state == "ready":
            reward += shotting_reward
        return reward

    def play_step(self, action):
        self.previous_score = self.score_value
        self.do_each_game_loop(action)
        return (self.get_state(), self.get_reward())

    def get_state(self):
        return [
            self.enemy_x[0] / 800,
            self.enemy_y[0] / 600,
            self.enemy_x_change[0] / self.enemy_speed,
            # self.enemy_y_change[0] / 16,
            self.player_x / 800,
            self.player_y / 600,
            1 if self.bullet_state == "ready" else 0,
        ]

    def get_action_space(self):
        return range(4)
