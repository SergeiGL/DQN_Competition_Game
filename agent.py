import numpy as np

class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.players_position = [0, 0, 0, 0, 0]
        self.players_score = [0, 0, 0, 0, 0]
        self.stage_rewards = [1, 2, 3]
        self.stage_capacity = [5, 3, 1]
        self.max_moves = 10

    def get_state(self):
        state = {
            'players_position': self.players_position,
            'players_score': self.players_score,
            'time_left': self.max_moves
        }
        return state

    def player_step(self, action=0, player_index=0):
        # actions: 0 - stay, 1 - up
        if action == 0:
            pass
        else:
            if self.players_position[player_index] != 2:
                my_stage = self.players_position[player_index] + 1
                on_stage_players = np.where(np.array(self.players_position) == my_stage)[0]
                # print('on_stage_players', on_stage_players, my_stage, self.stage_capacity[my_stage])
                if len(on_stage_players) > self.stage_capacity[my_stage]-1:
                    whom_to_push = np.random.choice(on_stage_players)
                    print('push', whom_to_push+1, ', I am', player_index+1)
                    self.players_position[whom_to_push] = 0
                self.players_position[player_index] += 1

    def step(self, actions_list):
        for i, action in enumerate(actions_list):
                self.player_step(action, player_index=i)
        
        #награда после того как все походили
        reward = [self.stage_rewards[self.players_position[i]] for i in range(len(self.players_position))]
        self.players_score =  np.array(self.players_score)+np.array(reward)
            
        self.max_moves -= 1
        is_game_end = False
        if self.max_moves == 0:
            is_game_end = True

        state = self.get_state()

        return state, reward, is_game_end

game = Game()

print(game.get_state())

while True:
    action = int(input('\t\t0- стоять или 1 - вверх\t'))
    actions_list = [action, np.random.randint(2),np.random.randint(2),np.random.randint(2),np.random.randint(2)]
    s, r, is_game_end = game.step(actions_list)
    print('\t','награда', r , '\t','состояние', s)
    if is_game_end == True:
        break