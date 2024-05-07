import turtle
import math
import random
import time
from sys import argv
import copy

class Sim:
    # Set true for graphical interface
    GUI = False
    screen = None
    selection = []
    turn = ''
    dots = []
    red = []
    blue = []
    available_moves = []
    minimax_depth = 0
    prune = False
    number_of_nodes = 0

    def __init__(self, minimax_depth, prune, gui):
        self.GUI = gui
        self.prune = prune
        self.minimax_depth = minimax_depth
        self.number_of_nodes = 0
        if self.GUI:
            self.setup_screen()

    def setup_screen(self):
        self.screen = turtle.Screen()
        self.screen.setup(800, 800)
        self.screen.title("Game of SIM")
        self.screen.setworldcoordinates(-1.5, -1.5, 1.5, 1.5)
        self.screen.tracer(0, 0)
        turtle.hideturtle()

    def draw_dot(self, x, y, color):
        turtle.up()
        turtle.goto(x, y)
        turtle.color(color)
        turtle.dot(15)

    def gen_dots(self):
        r = []
        for angle in range(0, 360, 60):
            r.append((math.cos(math.radians(angle)), math.sin(math.radians(angle))))
        return r

    def initialize(self):
        self.selection = []
        self.available_moves = []
        for i in range(0, 6):
            for j in range(i, 6):
                if i != j:
                    self.available_moves.append((i, j))
        if random.randint(0, 2) == 1:
            self.turn = 'red'
        else:
            self.turn = 'blue'
        self.dots = self.gen_dots()
        self.red = []
        self.blue = []
        if self.GUI: turtle.clear()
        self.draw()

    def draw_line(self, p1, p2, color):
        turtle.up()
        turtle.pensize(3)
        turtle.goto(p1)
        turtle.down()
        turtle.color(color)
        turtle.goto(p2)

    def draw_board(self):
        for i in range(len(self.dots)):
            if i in self.selection:
                self.draw_dot(self.dots[i][0], self.dots[i][1], self.turn)
            else:
                self.draw_dot(self.dots[i][0], self.dots[i][1], 'dark gray')

    def draw(self):
        if not self.GUI: return 0
        self.draw_board()
        for i in range(len(self.red)):
            self.draw_line((math.cos(math.radians(self.red[i][0] * 60)), math.sin(math.radians(self.red[i][0] * 60))),
                           (math.cos(math.radians(self.red[i][1] * 60)), math.sin(math.radians(self.red[i][1] * 60))),
                           'red')
        for i in range(len(self.blue)):
            self.draw_line((math.cos(math.radians(self.blue[i][0] * 60)), math.sin(math.radians(self.blue[i][0] * 60))),
                           (math.cos(math.radians(self.blue[i][1] * 60)), math.sin(math.radians(self.blue[i][1] * 60))),
                           'blue')
        self.screen.update()
        time.sleep(1)
    
    def check_not_triangle(self, sort_edgs, i, j):
        for k in range(len(sort_edgs)):
            for u in range(k+1,len(sort_edgs)):
                if sort_edgs[k][0] == sort_edgs[u][0] or sort_edgs[k][1] == sort_edgs[u][1] or sort_edgs[k][1] == sort_edgs[u][0]:
                    three_dots = set([sort_edgs[k][0], sort_edgs[k][1], sort_edgs[u][0], sort_edgs[u][1]])
                    if i in three_dots and j in three_dots:
                        return 0
        return 1                  
    def _evaluate(self, red, blue, available_moves):
        #TODO
        score_red = 0
        score_blue = 0
        red.sort()
        blue.sort()
        for i in range(0, 5):
            for j in range(i+1, 6):
                if (i, j) in available_moves:
                    score_red += self.check_not_triangle(red, i, j)
                    score_blue += self.check_not_triangle(blue, i, j)
        if score_red == 0:
            return -100
        if score_blue == 0:
            return 100
        return score_red - score_blue    

    def minimax_pure(self, depth, player_turn, red, blue, available_moves, alpha_max = -math.inf, beta_min = math.inf):
        self.number_of_nodes += 1
        if depth == self.minimax_depth:
            return self._evaluate(red,blue,available_moves)

        # r = copy.deepcopy(red)
        # b = copy.deepcopy(blue)
        # av_mv = copy.deepcopy(available_moves)
        result_edg = 0

        if player_turn == "red": # max
          v = - math.inf
          red.sort()

          for i in range (len(available_moves)):
            edge = available_moves[i]
            if self.check_not_triangle(red, edge[0], edge[1]) == 0:
              if v < -100:
                v = -100
                alpha_max = max(alpha_max, v)
                result_edg = edge
                if beta_min <= alpha_max:
                  break
              continue

            av_mv = copy.deepcopy(available_moves)
            av_mv.pop(i)
            red.append(edge)
            res_v = self.minimax_pure(depth+1, "blue", red, blue, av_mv, alpha_max, beta_min)
            red.remove(edge)

            if res_v >= v:
              v = res_v
              result_edg = edge
              alpha_max = max(alpha_max, v)
              if beta_min <= alpha_max:
                break
            
            # available_moves.append(edge)

          if  depth == 0:
            return result_edg
          return v

        else: # min
          v = math.inf
          blue.sort()

          for i in range(len(available_moves)):
            edge = available_moves[i]
            if self.check_not_triangle(blue, edge[0], edge[1]) == 0:
              if v > 100:
                v = 100
                result_edg = edge
                beta_min = min(beta_min, v)
                if beta_min <= alpha_max:
                  break  
              continue
            
            blue.append(edge)
            av_mv = copy.deepcopy(available_moves)
            av_mv.pop(i)
            rest_v = self.minimax_pure(depth+1, "red", red, blue, av_mv, alpha_max, beta_min)
            blue.remove(edge)
            
            if rest_v < v:
              v = rest_v
              result_edg = edge
              beta_min = min(beta_min, v)
              if beta_min <= alpha_max:
                break

          if depth == 0:
            return result_edg
          return v

    def minimax(self, depth, player_turn, red, blue, available_moves):
        #TODO
        self.number_of_nodes += 1
        if depth == self.minimax_depth:
            return self._evaluate(red,blue,available_moves)

        # r = copy.deepcopy(red)
        # b = copy.deepcopy(blue)
        # av_mv = copy.deepcopy(available_moves)
        result_edg = 0

        if player_turn == "red": # max
          v = - math.inf
          red.sort()

          for i in range (len(available_moves)):
            edge = available_moves[i]
            if self.check_not_triangle(red, edge[0], edge[1]) == 0:
              if v < -100:
                v = -100
                result_edg = edge
              continue
            red.append(edge)
            av_mv = copy.deepcopy(available_moves)
            av_mv.pop(i)
            res_v = self.minimax(depth+1, "blue", red, blue, av_mv)
            if res_v >= v:
              v = res_v
              result_edg = edge
            
            red.remove(edge)
            # available_moves.append(edge)

          if  depth == 0:
            return result_edg
          return v

        else: # min
          v = math.inf
          blue.sort()

          for i in range(len(available_moves)):
            edge = available_moves[i]
            if self.check_not_triangle(blue, edge[0], edge[1]) == 0:
              if v > 100:
                v = 100
                result_edg = edge
              continue
            
            blue.append(edge)
            av_mv = copy.deepcopy(available_moves)
            av_mv.pop(i)
            rest_v = self.minimax(depth+1, "red", red, blue, av_mv)
            if rest_v < v:
              v = rest_v
              result_edg = edge
            blue.remove(edge)

          if depth == 0:
            return result_edg
          return v

    def enemy(self):
        return random.choice(self.available_moves)

    def swap_turn(self, turn):
        if turn == 'red':
            return 'blue'
        else:
            return 'red'
    def play(self):
        self.initialize()
        while True:
            if self.turn == 'red':
                if self.prune == True:
                    selection = self.minimax_pure(0, self.turn, self.red, self.blue, self.available_moves)
                else:
                  selection = self.minimax(0, self.turn, self.red, self.blue, self.available_moves) #??
                if selection[1] < selection[0]:
                    selection = (selection[1], selection[0])
            else:
                selection = self.enemy()
                if selection[1] < selection[0]:
                    selection = (selection[1], selection[0])
            if selection in self.red or selection in self.blue:
                raise Exception("Duplicate Move!!!")
            if self.turn == 'red':
                self.red.append(selection)
            else:
                self.blue.append(selection)

            self.available_moves.remove(selection)
            self.turn = self.swap_turn(self.turn)
            selection = []
            self.draw()
            r = self.gameover(self.red, self.blue)
            if r != 0:
                return r

    def gameover(self, r, b):
        if len(r) < 3 and len(b) < 3:
            return 0
        r.sort()
        for i in range(len(r) - 2):
            for j in range(i + 1, len(r) - 1):
                for k in range(j + 1, len(r)):
                    if r[i][0] == r[j][0] and r[i][1] == r[k][0] and r[j][1] == r[k][1]:
                        return 'blue'
        if len(b) < 3: return 0
        b.sort()
        for i in range(len(b) - 2):
            for j in range(i + 1, len(b) - 1):
                for k in range(j + 1, len(b)):
                    if b[i][0] == b[j][0] and b[i][1] == b[k][0] and b[j][1] == b[k][1]:
                        return 'red'
        return 0


if __name__=="__main__":

    game = Sim(minimax_depth=int(argv[1]), prune=True, gui=bool(int(argv[2])))
    start = time.time()
    results = {"red": 0, "blue": 0}
    num = 100
    number_of_nodes = 0
    for i in range(num):
        # print(i)
        results[game.play()] += 1
        number_of_nodes += game.number_of_nodes
        game.number_of_nodes = 0
    end = time.time()
    print(results)
    print("Time: ", (end - start)/num)
    print("Number of nodes: ", number_of_nodes/num)