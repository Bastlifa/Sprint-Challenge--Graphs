from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# util
def reverse_dir(direction):
        rev_dict = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}
        return rev_dict[direction]

# TODO: implement DLL for Stack and Queue
class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

# Graph
class Graph():
    def __init__(self):
        self.rooms = {}
        self.walked = set()
        self.add_room(player.current_room)

    def add_room(self, room):
        self.rooms[room.id] = {
            'n': player.current_room.n_to.id if player.current_room.n_to else None,
            'e': player.current_room.e_to.id if player.current_room.e_to else None,
            's': player.current_room.s_to.id if player.current_room.s_to else None,
            'w': player.current_room.w_to.id if player.current_room.w_to else None,
        }

    def travel(self, direction):
        player.travel(direction)
        traversal_path.append(direction)
        self.add_room(player.current_room)
    

    def get_unwalked_neighbors(self, room):
        unwalked = []
        for d in ['n', 'e', 's', 'w']:
            if self.rooms[room][d] is not None and \
            self.rooms[room][d] not in self.walked:
                unwalked.append([d, self.rooms[room][d]])
        random.shuffle(unwalked)
        return unwalked


    def dft(self, starting_room):
        s = Stack()

        s.push(self.get_unwalked_neighbors(starting_room.id)[0])
        cur = None
        # while len(self.walked) < len(self.rooms):
        k = 0
        while k < 15:
            while s.size() > 0:
                r = s.pop()
                cur = r
                if r[1] not in self.walked:
                    self.travel(r[0])
                    r_next = player.current_room.id
                    for n in self.get_unwalked_neighbors(r_next):
                        s.push(n)
            self.get_nearest_unwalked(cur[1])
            print(len(self.walked), len(self.rooms))
            k += 1
    
    def get_dir(self, room_1, room_2):
        if self.rooms[room_1]['n'] == room_2: return 'n'
        if self.rooms[room_1]['e'] == room_2: return 'e'
        if self.rooms[room_1]['s'] == room_2: return 's'
        if self.rooms[room_1]['w'] == room_2: return 'w'

    def get_nearest_unwalked(self, room):
        q = Queue()
        q.enqueue([room])
        vis = set()
        while q.size() > 0:
            path = q.dequeue()
            r = path[-1]
            # print('r', r)
            if r not in vis:
                if r not in self.walked:
                    dir_path = []
                    for i in range(1, len(path)):
                        dir_path.append(self.get_dir(path[i-1], path[i]))
                    return dir_path
                vis.add(r)
                for next_r in self.rooms[r]:
                    print('a', self.rooms[r])
                    new_path = [*path] + [self.rooms[r][next_r]]
                    q.enqueue(new_path)

    
g = Graph()
g.dft(player.current_room)

# find_path_to_closest_unexplored
    # def fptcu():
    #     pass

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

# player.travel('e')
# print('p', player.current_room.id)
# print('p', player.current_room.name)
# print('p.n_to', player.current_room.n_to.id if player.current_room.n_to else None)
# print('p.e_to', player.current_room.e_to.id if player.current_room.e_to else None)
# print('p.s_to', player.current_room.s_to.id if player.current_room.s_to else None)
# print('p.w_to', player.current_room.w_to.id if player.current_room.w_to else None)
print(traversal_path)
#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
