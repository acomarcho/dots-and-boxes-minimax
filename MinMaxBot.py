from Bot import Bot
from GameAction import GameAction
from GameState import GameState
import copy
import random

class MinMaxBot(Bot):
    def __init__(self, depth_limit = 5):
        self.depth_limit = depth_limit

    def get_action(self, state: GameState) -> GameAction:
        return self.minimax({"state": state, "action": None}, 1, -10000, 10000, True)['action']

    def minimax(self, state, depth, alpha, beta, agent_turn):
        if depth == self.depth_limit or self.terminal_state(state['state']):
            return {"state": state['state'], "action": None}

        if agent_turn:
            # Agen ingin memaksimalkan poinnya
            best = -10000
            best_state = None
            states = self.generatePossibleStates(state['state'])
            for s in states:
                next_turn = not agent_turn
                # Untuk tiap state, evaluasi menggunakan minmax
                if self.evaluate(s['state']) > self.evaluate(state['state']):
                    # Berhasil menambah kotak -- next_turn adalah turn agent lagi
                    next_turn = True
                return_state = self.minimax(s, depth + 1, alpha, beta, next_turn)
                state_score = self.evaluate(return_state['state'])
                if state_score > best:
                    best = state_score
                    best_state = s
                if best >= beta:
                    break
                alpha = max(alpha, best)
            return best_state
        else:
            # Lawan ingin memaksimalkan poinnya
            best = 10000
            best_state = None
            states = self.generatePossibleStates(state['state'])
            for s in states:
                next_turn = not agent_turn
                # Untuk setiap state, evaluasi menggunakan minmax
                if self.evaluate(s['state']) < self.evaluate(state['state']):
                    # Berhasil menambah kotak -- next_turn adalah turn lawan lagi
                    next_turn = False
                return_state = self.minimax(s, depth + 1, alpha, beta, next_turn)
                state_score = self.evaluate(return_state['state'])
                if state_score < best:
                    best = state_score
                    best_state = s
                if best <= alpha:
                    break
                beta = min(beta, best)
            return best_state


    def generatePossibleStates(self, state: GameState):
        result = []
        for i in range(len(state.row_status)):
            for j in range(len(state.row_status[0])):
                if (state.row_status[i][j] == 0):
                    board_status_copy = copy.deepcopy(state.board_status)
                    row_status_copy = copy.deepcopy(state.row_status)
                    col_status_copy = copy.deepcopy(state.col_status)
                    if (i == 0):
                        # If row 0
                        board_status_copy[i][j] = abs(board_status_copy[i][j]) + 1
                    elif (i == len(state.row_status) - 1):
                        # If last row
                        board_status_copy[i - 1][j] = abs(board_status_copy[i - 1][j]) + 1
                    else:
                        board_status_copy[i][j] = abs(board_status_copy[i][j]) + 1
                        board_status_copy[i - 1][j] = abs(board_status_copy[i - 1][j]) + 1
                    row_status_copy[i][j] = 1

                    newState = GameState(board_status_copy, row_status_copy, col_status_copy, True)
                    newAction = GameAction('row', (j, i))
                    result.append({
                        "state": newState,
                        "action": newAction
                    })

                # print(f'Running row_status search for {j},{i}')
        
        for i in range(len(state.col_status)):
            for j in range(len(state.col_status[0])):
                if (state.col_status[i][j] == 0):
                    board_status_copy = copy.deepcopy(state.board_status)
                    row_status_copy = copy.deepcopy(state.row_status)
                    col_status_copy = copy.deepcopy(state.col_status)
                    if (j == 0):
                        # If col 0
                        board_status_copy[i][j] = abs(board_status_copy[i][j]) + 1
                    elif (j == len(state.col_status[0]) - 1):
                        # If last col
                        board_status_copy[i][j - 1] = abs(board_status_copy[i][j - 1]) + 1
                    else:
                        board_status_copy[i][j] = abs(board_status_copy[i][j]) + 1
                        board_status_copy[i][j - 1] = abs(board_status_copy[i][j - 1]) + 1
                    col_status_copy[i][j] = 1

                    newState = GameState(board_status_copy, row_status_copy, col_status_copy, True)
                    newAction = GameAction('col', (j, i))
                    result.append({
                        "state": newState,
                        "action": newAction
                    })

                # print(f'Running col_status search for {j},{i}')

        random.shuffle(result)
        return result

    def evaluate(self, state: GameState):
        score = 0
        for i in range(len(state.board_status)):
            for j in range(len(state.board_status[0])):
                if (state.board_status[i][j] == 4):
                    score += 4
                elif (state.board_status[i][j] == 3):
                    score -= 1
                elif (state.board_status[i][j] == -3):
                    score += 1
                elif (state.board_status[i][j] == -4):
                    score -= 4

        return score

    def terminal_state(self, state):
        square_count = 0
        for i in range(len(state.board_status)):
            for j in range(len(state.board_status[0])):
                if (abs(state.board_status[i][j]) == 4):
                    square_count += 1

        return square_count == 9