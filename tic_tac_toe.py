from abc import ABC, abstractmethod
from builtins import NotImplementedError
from math import inf
from typing import Optional


def transposition(array: list[list]) -> list[list]:
    return [[array[j][i] for j in range(len(array))] for i in range(len(array[0]))]


def get_diagonal(array: list[list]) -> list[list]:  # TODO fix it - works only for 3x3 arrays
    diag1 = [array[0][0], array[len(array) // 2][len(array) // 2], array[len(array) - 1][len(array) - 1]]
    diag2 = [array[0][len(array) - 1], array[len(array) // 2][len(array) // 2], array[len(array) - 1][0]]
    return [diag1, diag2]


def get_diagonal_with_indexes(array: list[list]) -> list[list[tuple]]:
    # TODO
    pass


class Player(ABC):
    def __init__(self, player_symbol: int, enemy_symbol: int, empty_symbol: float):
        assert player_symbol in [0, 1] and enemy_symbol in [0, 1], "Symbol must be 1 or 0"
        assert player_symbol != enemy_symbol
        self.player_symbol = player_symbol
        self.enemy_symbol = enemy_symbol
        self.empty_symbol = empty_symbol

    @abstractmethod
    def getMove(self, game_array: list[list]) -> tuple:
        raise NotImplementedError


class HumanPlayer(Player):
    def __init__(self, player_symbol: int, enemy_symbol: int, empty_symbol: float):
        super().__init__(player_symbol, enemy_symbol, empty_symbol)

    def getMove(self, game_array: list[list]) -> tuple:
        print("enter x")
        x = input()
        print("enter y")
        y = input()
        return int(x), int(y)


class AiPlayer(Player):
    def __init__(self, player_symbol: int, enemy_symbol: int, empty_symbol: float):
        super().__init__(player_symbol, enemy_symbol, empty_symbol)

    def ___count_symbol(self, line: list, symbol: int) -> int:
        return line.count(symbol)

    def __block_enemy(self, game_array: list[list]) -> tuple:
        # check row
        for index, line in enumerate(game_array):
            if self.___count_symbol(line, self.enemy_symbol) == len(line) - 1:
                return index, line.index(self.empty_symbol)

        # check column
        for index, column in enumerate(transposition(game_array)):
            if self.___count_symbol(column, self.enemy_symbol) == len(column) - 1:
                return column.index(self.empty_symbol), index

        # check diagonal
        for index, diagonal in enumerate(get_diagonal_with_indexes(game_array)):
            if self.___count_symbol([cell[0] for cell in diagonal], self.enemy_symbol) == len(diagonal) - 1:
                index = [cell[0] for cell in diagonal].index(self.empty_symbol)
                return diagonal[index][1:3]

    def getMove(self, game_array: list[list]) -> tuple:
        pass


class Game:
    rules = {
        -inf: "_",
        1: "X",
        0: "O"
    }

    def __init__(self, player1: Player, player2: Player, size: int):
        self.player1 = player1
        self.player2 = player2
        self.array = [[-inf for _ in range(size)] for _ in range(size)]
        self.size = size

    def __check_row(self, array: list[list]):
        for row in array:
            if sum(row) == len(array[0]):
                return "Cross"
            if sum(row) == 0:
                return "Circle"
        return False

    def __check_who_win(self) -> Optional[str]:
        result = self.__check_row(self.array)
        if result:
            return result
        trans_array = transposition(self.array)
        result = self.__check_row(trans_array)
        if result:
            return result
        result = self.__check_row(get_diagonal(self.array))
        if result:
            return result
        else:
            return None

    def __make_move(self, player: Player):
        try:
            x, y = player.getMove(game_array=self.array)
            self.array[x][y] = player.player_symbol
        except (IndexError, ValueError):
            print("Try again")
            self.__make_move(player)

    def display(self):
        list_to_display = [[self.rules[field] for field in row] for row in self.array]
        for row in list_to_display:
            print(row)

    def play(self):
        self.display()

        for i in range(((self.size ** 2) // 2) + 1):
            print("Player1 move")
            self.__make_move(self.player1)
            self.display()
            result = self.__check_who_win()
            if result:
                print(result)
                break

            print("Player1 move")
            self.__make_move(self.player2)
            self.display()
            result = self.__check_who_win()
            if result:
                print(result)
                break
        else:
            return "Remis"


if __name__ == "__main__":
    player1 = HumanPlayer(1, 0, -inf)
    player2 = HumanPlayer(0, 1, -inf)
    game = Game(player1=player1, player2=player2, size=4)

    game.play()
