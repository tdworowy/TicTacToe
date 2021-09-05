from abc import ABC, abstractmethod
from builtins import NotImplementedError
from math import inf


class Player(ABC):
    def __init__(self, symbol):
        assert symbol in [0, 1], "Symbol must be 1 or 0"
        self.symbol = symbol

    @abstractmethod
    def getMove(self):
        raise NotImplementedError


class HumanPlayer(Player):
    def __init__(self, symbol):
        super().__init__(symbol)

    def getMove(self):
        print("enter x")
        x = input()
        print("enter y")
        y = input()
        return int(x), int(y)


class AiPlayer(Player):
    def __init__(self, symbol):
        super().__init__(symbol)

    def getMove(self):
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

    def __transposition(self, array: list[list]) -> list[list]:
        return [[array[j][i] for j in range(len(array))] for i in range(len(array[0]))]

    def __get_diagonal(self, array: list[list]) -> list[list]:
        diag1 = [array[0][0], array[len(array) // 2][len(array) // 2], array[len(array) - 1][len(array) - 1]]
        diag2 = [array[0][len(array) - 1], array[len(array) // 2][len(array) // 2], array[len(array) - 1][0]]
        return [diag1, diag2]

    def __check_row(self, array: list[list]):
        for row in array:
            if sum(row) == len(array[0]):
                return "Cross"
            if sum(row) == 0:
                return "Circle"
        return False

    def __check_who_win(self) -> str:
        result = self.__check_row(self.array)
        if result:
            return result
        trans_array = self.__transposition(self.array)
        result = self.__check_row(trans_array)
        if result:
            return result
        result = self.__check_row(self.__get_diagonal(self.array))
        if result:
            return result
        else:
            return None

    def __make_move(self, player: Player):
        try:
            x, y = player.getMove()
            self.array[x][y] = player.symbol
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
    player1 = HumanPlayer(1)
    player2 = HumanPlayer(0)
    game = Game(player1=player1, player2=player2, size=4)

    game.play()
