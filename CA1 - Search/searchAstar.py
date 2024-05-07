from collections import defaultdict
from math import inf
import copy
import time
from heapq import heapify, heappush, heappop

class Graph:
 
    def __init__(self):

        self.graph = defaultdict(list)
 
    def addEdge(self,u,v):
        self.graph[u].append(v)
 
    def BFS(self, s):
 
        visited = [False] * (max(self.graph) + 1)
 
        queue = []
 
        queue.append(s)
        visited[s] = True
 
        while queue:
 
            s = queue.pop(0)
            print (s, end = " ")
 
            for i in self.graph[s]:
                if visited[i] == False:
                    queue.append(i)
                    visited[i] = True

class State:
  def __init__(self,pos,path,cur_time,wait,hard_nodes,collected_recipes,done_morids, estimated_time):
    self.position=pos
    self.path=path
    self.current_time=cur_time
    self.wait=wait
    self.hard_nodes=hard_nodes
    self.collected_recipes=collected_recipes
    self.done_morids=done_morids
    self.est_time = estimated_time

  def __eq__(self, other):
    if(self.position==other.position and self.wait==other.wait and
       self.hard_nodes==other.hard_nodes and self.collected_recipes==other.collected_recipes
        and self.done_morids==other.done_morids and self.current_time==other.current_time and self.wait==other.wait):
        return True
    return False
  
  def __lt__(self, other):
    return self.est_time < other.est_time

  def add_recipe(self,recipe):
    self.collected_recipes.add(recipe)

  def add_morid(self,morid):
    self.done_morids.add(morid)

def cal_heuristic(state: State, morids, all_recipes):
    must_visit_nodes = set()
    for morid in morids:
      if morid not in state.done_morids:
        must_visit_nodes.add(morid)
    for recipe in all_recipes:
      if recipe not in state.collected_recipes:
        must_visit_nodes.add(recipe)
    
    return len(must_visit_nodes)

def Astar(graph: Graph, hard_nodes, morids_recipes, start_node, all_recipes, morids):
  initial_state = State(start_node, [start_node], 0, 0, {hard: 0 for hard in hard_nodes }, set(), set(),0)
  fringe = []
  heapify(fringe)
  explored = []
  heappush(fringe, initial_state)

  while(True):
    cur_state = heappop(fringe)
    explored.append(cur_state)


    #check goal
    if len(cur_state.done_morids) == len(morids):
      return [len(explored), cur_state.path, cur_state.current_time]

    #check if we have to wait
    if cur_state.wait > 0:
      cur_state.wait-=1
      cur_state.current_time+=1
      cur_state.est_time+=1
      heappush(fringe, cur_state)
      continue

    for neighbor in graph.graph[cur_state.position]:
      next_state = copy.deepcopy(cur_state)
      next_state.position = neighbor
      next_state.path.append(neighbor)
      next_state.current_time+=1
      next_state.wait = 0
      if neighbor in hard_nodes:
        next_state.wait = next_state.hard_nodes[neighbor]
        next_state.hard_nodes[neighbor]+=1

      # next_state.current_time+=next_state.wait
      # next_state.wait = 0

      if neighbor in all_recipes:
        next_state.add_recipe(neighbor)

      if neighbor in morids:
        if set(morids_recipes[neighbor]).issubset(next_state.collected_recipes):
          next_state.add_morid(neighbor) 
      next_state.est_time = cal_heuristic(next_state, morids, all_recipes) + next_state.current_time  
      if (next_state not in explored) and (next_state not in fringe):
        heappush(fringe, next_state)

g = Graph()
f = open("input3.txt")
n,m = map(int, f.readline().split())
for i in range(m):
  u,v = map(int, f.readline().split())
  g.addEdge(u, v)
  g.addEdge(v, u)
num_hard_nodes = int(f.readline())
hard_nodes = list(map(int, f.readline().split()))
s_num = int(f.readline())
morids = list()
morids_recipes = defaultdict(list)
all_recipes = set() 
for i in range(s_num):
  line = list(map(int,f.readline().split()))
  p = line[0]
  q = line[1]
  secret_recipes = line[2:]
  all_recipes.update(set(secret_recipes))
  morids.append(p)
  for k in range(q):
    morids_recipes[p].append(secret_recipes[k])
v = int(f.readline())
start_time = time.time()
print("Astar")
print(Astar(g, hard_nodes, morids_recipes, v, all_recipes, morids))
end_time = time.time()
print(end_time - start_time)
