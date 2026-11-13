
from random import randrange
from graphics import *
import time
from math import radians, cos, sin, sqrt
#problem 1 and 2
class Die:
    def roll(self):
        return randrange(6)

class Player:
    def __init__(self, name):
        self.name = name
        self.chips = 3

class TextInterface:
    def getNames(self):
        n = int(input("Number of players (3 or more): "))
        while n < 3:
            n = int(input("Enter at least 3 players: "))
        return [input("Player " + str(i + 1) + " name: ") for i in range(n)]

    def show(self, message):
        print(message)

    def close(self):
        pass

class GraphicalInterface:
    def __init__(self):
        self.win = GraphWin("LCR Game", 500, 400)
        self.win.setCoords(0, 0, 10, 10)
        self.message = Text(Point(5, 5), "")
        self.message.draw(self.win)
        self.hint = Text(Point(5, 2), "")
        self.hint.draw(self.win)

    def getInput(self, prompt):
        self.message.setText(prompt)
        self.hint.setText("Enter your answer and click anywhere")
        entry = Entry(Point(5, 4), 20)
        entry.draw(self.win)
        self.win.getMouse()
        answer = entry.getText()
        entry.undraw()
        self.message.setText("")
        self.hint.setText("")
        return answer

    def getNames(self):
        n = int(self.getInput("Number of players (3 or more):"))
        while n < 3:
            n = int(self.getInput("Enter at least 3 players:"))

        names = []
        for i in range(n):
            names.append(self.getInput("Enter player " + str(i + 1) + " name:"))
        return names

    def show(self, message):
        self.message.setText(message)
        time.sleep(0.5)

    def close(self):
        self.message.setText("Game over! Click to close.")
        self.hint.setText("")
        self.win.getMouse()
        self.win.close()

class LCRGame:
    def __init__(self, names, interface):
        self.players = [Player(name) for name in names]
        self.die = Die()
        self.pot = 0
        self.interface = interface

    def play(self):
        current = 0

        while sum(p.chips > 0 for p in self.players) > 1:
            player = self.players[current]

            if player.chips > 0:
                rolls = min(player.chips, 3)

                for i in range(rolls):
                    result = self.die.roll()

                    if result == 0:
                        player.chips -= 1
                        self.players[(current - 1) % len(self.players)].chips += 1
                        symbol = "L"
                    elif result == 1:
                        player.chips -= 1
                        self.pot += 1
                        symbol = "C"
                    elif result == 2:
                        player.chips -= 1
                        self.players[(current + 1) % len(self.players)].chips += 1
                        symbol = "R"
                    else:
                        symbol = "Dot"

                    self.interface.show(player.name + " rolled " + symbol)

            current = (current + 1) % len(self.players)

        for player in self.players:
            if player.chips > 0:
                player.chips += self.pot
                self.interface.show(
                    player.name + " wins with " + str(player.chips) + " chips!"
                )
                return

def main():
    choice = input("Choose interface: 1. Text  2. Graphical: ")

    if choice == "1":
        interface = TextInterface()
    elif choice == "2":
        interface = GraphicalInterface()
    else:
        print("Invalid choice.")
        return

    game = LCRGame(interface.getNames(), interface)
    game.play()
    interface.close()

main()

#problem 3 and 4
class Die:
    def __init__(self):
        self.value = 0

    def roll(self):
        self.value = randrange(1, 7)

    def getValue(self):
        return self.value

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

class TextInterface:
    def getNames(self):
        n = int(input("Number of players (2 or more): "))
        while n < 2:
            n = int(input("Enter at least 2 players: "))
        return [input("Player " + str(i + 1) + " name: ") for i in range(n)]

    def show(self, message):
        print(message)

    def close(self):
        pass

class GraphicalInterface:
    def __init__(self):
        self.win = GraphWin("Ship, Captain, and Crew", 500, 400)
        self.win.setCoords(0, 0, 10, 10)
        self.message = Text(Point(5, 5), "")
        self.message.draw(self.win)
        self.hint = Text(Point(5, 2), "")
        self.hint.draw(self.win)

    def getInput(self, prompt):
        self.message.setText(prompt)
        self.hint.setText("Enter your answer and click anywhere")
        entry = Entry(Point(5, 4), 20)
        entry.draw(self.win)
        self.win.getMouse()
        answer = entry.getText()
        entry.undraw()
        self.message.setText("")
        self.hint.setText("")
        return answer

    def getNames(self):
        n = int(self.getInput("Number of players (2 or more):"))
        while n < 2:
            n = int(self.getInput("Enter at least 2 players:"))

        names = []
        for i in range(n):
            names.append(self.getInput("Enter player " + str(i + 1) + " name:"))
        return names

    def show(self, message):
        self.message.setText(message)
        time.sleep(0.7)

    def close(self):
        self.message.setText("Game over! Click to close.")
        self.hint.setText("")
        self.win.getMouse()
        self.win.close()

class ShipGame:
    def __init__(self, names, interface):
        self.players = [Player(name) for name in names]
        self.interface = interface

    def takeTurn(self, player):
        remaining = [Die() for i in range(5)]
        ship = False
        captain = False
        crew = False
        score = 0

        for roll in range(3):
            for die in remaining:
                die.roll()

            values = [die.getValue() for die in remaining]

            if not ship and 6 in values:
                remaining.remove(next(d for d in remaining if d.getValue() == 6))
                ship = True

            if ship and not captain:
                if 5 in [d.getValue() for d in remaining]:
                    remaining.remove(next(d for d in remaining if d.getValue() == 5))
                    captain = True

            if captain and not crew:
                if 4 in [d.getValue() for d in remaining]:
                    remaining.remove(next(d for d in remaining if d.getValue() == 4))
                    crew = True

            self.interface.show(
                player.name + " roll " + str(roll + 1) + ": " + str(values)
            )

            if ship and captain and crew:
                score = sum(d.getValue() for d in remaining)
                self.interface.show("Cargo score: " + str(score))

        if ship and captain and crew:
            player.score = score
        else:
            player.score = 0

        self.interface.show(player.name + " final score: " + str(player.score))

    def play(self):
        activePlayers = self.players

        while len(activePlayers) > 1:
            self.interface.show("New Round")

            for player in activePlayers:
                self.takeTurn(player)

            highScore = max(p.score for p in activePlayers)
            winners = [p for p in activePlayers if p.score == highScore]

            if len(winners) == 1:
                self.interface.show(
                    winners[0].name + " wins with " +
                    str(winners[0].score) + " points!"
                )
                break

            self.interface.show("Tie! Tied players play again.")
            activePlayers = winners

def main():
    choice = input("Choose interface: 1. Text  2. Graphical: ")

    if choice == "1":
        interface = TextInterface()
    elif choice == "2":
        interface = GraphicalInterface()
    else:
        print("Invalid choice.")
        return

    game = ShipGame(interface.getNames(), interface)
    game.play()
    interface.close()

main()

#problem 5


class Projectile:
    def __init__(self, angle, velocity, height):
        self.xpos = 0
        self.ypos = height
        theta = radians(angle)
        self.xvel = velocity * cos(theta)
        self.yvel = velocity * sin(theta)
        self.moving = True

    def update(self, time):
        if not self.moving:
            return

        self.xpos += time * self.xvel
        yvel1 = self.yvel - 9.8 * time
        self.ypos += time * (self.yvel + yvel1) / 2.0
        self.yvel = yvel1

        if self.ypos <= 0.15:
            self.ypos = 0.15
            self.yvel = abs(self.yvel) * sqrt(0.60)

            if self.yvel ** 2 / 19.6 < 0.01:
                self.yvel = 0
                self.moving = False

    def getY(self):
        return self.ypos

    def getX(self):
        return self.xpos

    def isMoving(self):
        return self.moving

def main():
    win = GraphWin("Three Bouncing Balls", 600, 400)
    win.setCoords(0, 0, 15, 10)

    balls = [
        Projectile(90, 0, 9),
        Projectile(90, 0, 7),
        Projectile(90, 0, 5)
    ]

    circles = [
        Circle(Point(3, 9), 0.15),
        Circle(Point(7, 7), 0.15),
        Circle(Point(11, 5), 0.15)
    ]

    colors = ["red", "blue", "green"]

    for i in range(3):
        circles[i].setFill(colors[i])
        circles[i].draw(win)

    message = Text(Point(7.5, 9.7), "Three Bouncing Balls")
    message.draw(win)

    dt = 0.01

    while any(ball.isMoving() for ball in balls):
        if win.checkMouse() is not None:
            win.close()
            return

        for i in range(3):
            if balls[i].isMoving():
                balls[i].update(dt)
                circles[i].move(
                    0,
                    balls[i].getY() - circles[i].getCenter().getY()
                )

        time.sleep(dt)

    message.setText("Animation Complete - Click to Close")
    win.getMouse()
    win.close()

main()