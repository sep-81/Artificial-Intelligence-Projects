from collections import defaultdict
from math import inf
import copy
import time

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
  def __init__(self,pos,path,cur_time,wait,hard_nodes,collected_recipes,done_morids):
    self.position=pos
    self.path=path
    self.current_time=cur_time
    self.wait=wait
    self.hard_nodes=hard_nodes
    self.collected_recipes=collected_recipes
    self.done_morids=done_morids

  def __eq__(self, other):
    if(self.position==other.position and self.wait==other.wait and
       self.hard_nodes==other.hard_nodes and self.collected_recipes==other.collected_recipes
        and self.done_morids==other.done_morids and self.current_time == other.current_time):
        return True
    return False
  
  def add_recipe(self,recipe):
    self.collected_recipes.add(recipe)

  def add_morid(self,morid):
    self.done_morids.add(morid)

def IDS(graph: Graph, hard_nodes, morids_recipes, start_node, all_recipes, morids, depth):
  if depth < 3:
    depth = 3
  for d in range(3,depth+1):  
    fringe = []
    explored = []
    initial_state = State(start_node, [start_node], 0, 0, {hard: 0 for hard in hard_nodes }, set(), set())
    # initial_state.current_time = 0
    fringe.append(initial_state)
    while True:
      if len(fringe) == 0:
        break
      cur_state = fringe.pop()
      explored.append(cur_state)
      if cur_state.path == [1, 3, 4, 5, 7, 10, 11, 9]: #  [1, 3, 4, 5, 7, 10, 11, 9, 8]:
        print("found",d)
      #check if we have to wait
      if cur_state.wait > 0:
        cur_state.wait-=1
        cur_state.current_time+=1
        fringe.append(cur_state)
        continue

      if cur_state.current_time > d:
        continue
      #check goal
      if len(cur_state.done_morids) == len(morids):
        return [d, len(explored), cur_state.path, cur_state.current_time]
      
      if cur_state.current_time == d:
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

        if neighbor in all_recipes:
          next_state.add_recipe(neighbor)

        if neighbor in morids:
          if set(morids_recipes[neighbor]).issubset(next_state.collected_recipes):
            next_state.add_morid(neighbor) 

        if (next_state not in explored) and (next_state not in fringe):
          fringe.append(next_state)
        # elif len(next_state.path) == 9:
        #   print(next_state.path)  
      

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
print("IDS")
depth = 50
print(IDS(g, hard_nodes, morids_recipes, v, all_recipes, morids, depth))
end_time = time.time()
print(end_time - start_time)
