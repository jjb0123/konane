from os import defpath
import game_rules, random
###########################################################################
# Explanation of the types:
# The board is represented by a row-major 2D list of characters, 0 indexed
# A point is a tuple of (int, int) representing (row, column)
# A move is a tuple of (point, point) representing (origin, destination)
# A jump is a move of length 2
###########################################################################

# I will treat these like constants even though they aren't
# Also, these values obviously are not real infinity, but close enough for this purpose
NEG_INF = -1000000000
POS_INF = 1000000000

class Player(object):
    """ This is the player interface that is consumed by the GameManager. """
    def __init__(self, symbol): self.symbol = symbol # 'x' or 'o'

    def __str__(self): return str(type(self))

    def selectInitialX(self, board): return (0, 0)
    def selectInitialO(self, board): pass

    def getMove(self, board): pass

    def h1(self, board):
        return -len(game_rules.getLegalMoves(board, 'o' if self.symbol == 'x' else 'x'))


# This class has been replaced with the code for a deterministic player.
class MinimaxPlayer(Player):
    def __init__(self, symbol, depth): super(MinimaxPlayer, self).__init__(symbol)
        
    # Leave these two functions alone.
    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    # Edit this one here. :)
    def getMove(self, board):
        symbol = self.symbol
        depth = self.depth
        return self.maximum_value(board, depth, symbol)[1]

    def maximum_value(self, board, depth, symbol):
        legalMoves = game_rules.getLegalMoves(board, symbol)
        if depth == 0:
            if len(legalMoves) == 0:
                return (self.h1(board,symbol), None)
        x = (NEG_INF, None)
        moves_length = len(legalMoves)
        for i in range(moves_length):
            next_Board = game_rules.makeMove(board, legalMoves[i])
            if symbol == 'x':
                value = self.minimum_value(next_Board, depth -1, 'o')[0]
            value = self.minimum_value(next_Board, depth - 1, 'x')[0]
            if x[0] < value:
                x = (value, legalMoves[i])
        return x
    
    #min value function will be the same but with positive infinity for lower bound of x 
    def minimum_value(self, board, depth, symbol):
        legalMoves = game_rules.getLegalMoves(board, symbol)
        if depth == 0:
            if len(legalMoves) == 0:
                return (self.h1(board,symbol), None)
        x = (POS_INF, None)
        moves_length = len(legalMoves)
        for i in range(moves_length):
            next_Board = game_rules.makeMove(board, legalMoves[i])
            if symbol == 'x':
                value = self.maximum_value(next_Board, depth -1, 'o')[0]
            value = self.maximum_value(next_Board, depth - 1, 'x')[0]
            if x[0] < value:
                x = (value, legalMoves[i])
        return x



# This class has been replaced with the code for a deterministic player.
class AlphaBetaPlayer(Player):
    def __init__(self, symbol, depth): super(AlphaBetaPlayer, self).__init__(symbol)

    # Leave these two functions alone.
    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    # Edit this one here. :)
    def getMove(self, board):
        return self.AlphaBetaSearch(board)[1]
    def AlphaBetaSearch(self, board):
        return self.maximum_value(board, NEG_INF, POS_INF, self.depth, self.symbol) 

    def maximum_value(self,board, x, y, depth, symbol):
        legalMoves = game_rules.getLegalMoves(board, symbol)
        z = (NEG_INF, None)
        if (depth ==0 or len(legalMoves) == 0):
            return (self.h1(board, symbol), None)
        
        for i in range(len(legalMoves)):
            next_Board =  game_rules.makeMove(board, legalMoves[i])
            if symbol == 'x':
                value = self.minimum_value(next_Board, x, y, depth-1, 'o')[0]
            value = self.minimum_value(next_Board, x, y, depth-1, 'x')[0]
            if z[0] < value:
                z = (value, legalMoves[i])
            if (z[0] >= y):
                return z 
            if (x < z[0]):
                x = z[0]
        return z
    def minimum_value(self,board, x, y, depth, symbol):
        legalMoves = game_rules.getLegalMoves(board, symbol)
        z = (POS_INF, None)
        if (depth ==0 or len(legalMoves) == 0):
            return (self.h1(board, symbol), None)
        
        for i in range(len(legalMoves)):
            next_Board =  game_rules.makeMove(board, legalMoves[i])
            if symbol == 'x':
                value = self.maximum_value(next_Board, x, y, depth-1, 'o')[0]
            value = self.maximum_value(next_Board, x, y, depth-1, 'x')[0]
            if z[0] > value:
                z = (value, legalMoves[i])
            if (z[0] <= x):
                return z 
            if (y > z[0]):
                y = z[0]
        return z

class RandomPlayer(Player):
    def __init__(self, symbol):
        super(RandomPlayer, self).__init__(symbol)

    def selectInitialX(self, board):
        validMoves = game_rules.getFirstMovesForX(board)
        return random.choice(list(validMoves))

    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return random.choice(list(validMoves))

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return random.choice(legalMoves)
        else: return None


class DeterministicPlayer(Player):
    def __init__(self, symbol): super(DeterministicPlayer, self).__init__(symbol)

    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return legalMoves[0]
        else: return None


class HumanPlayer(Player):
    def __init__(self, symbol): super(HumanPlayer, self).__init__(symbol)
    def selectInitialX(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')
    def selectInitialO(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')
    def getMove(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')


def makePlayer(playerType, symbol, depth=1):
    player = playerType[0].lower()
    if player   == 'h': return HumanPlayer(symbol)
    elif player == 'r': return RandomPlayer(symbol)
    elif player == 'm': return MinimaxPlayer(symbol, depth)
    elif player == 'a': return AlphaBetaPlayer(symbol, depth)
    elif player == 'd': return DeterministicPlayer(symbol)
    else: raise NotImplementedException('Unrecognized player type {}'.format(playerType))

def callMoveFunction(player, board):
    if game_rules.isInitialMove(board): return player.selectInitialX(board) if player.symbol == 'x' else player.selectInitialO(board)
    else: return player.getMove(board)
