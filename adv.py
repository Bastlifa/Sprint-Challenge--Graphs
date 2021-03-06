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
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

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
        self.walked.add(player.current_room.id)
        self.add_room(player.current_room)
        self.prev_dir = None

    def add_room(self, room):
        self.rooms[room.id] = {
            'n': player.current_room.n_to.id if player.current_room.n_to else None,
            'e': player.current_room.e_to.id if player.current_room.e_to else None,
            's': player.current_room.s_to.id if player.current_room.s_to else None,
            'w': player.current_room.w_to.id if player.current_room.w_to else None,
        }
        for c in ['n', 'e', 's', 'w']:
            if self.rooms[room.id][c] is not None:
                next_room_id = self.rooms[room.id][c]
                if next_room_id not in self.rooms:
                    self.rooms[next_room_id] = {}
                self.rooms[next_room_id][reverse_dir(c)] = room.id

    def travel(self, direction):
        player.travel(direction)
        traversal_path.append(direction)
        self.add_room(player.current_room)
        self.walked.add(player.current_room.id)
    
    def get_random_dir(self, room):
        pass

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

        while s.size() > 0:
            r = s.pop()
            cur = r

            if r[1] not in self.walked:
                self.travel(r[0])
                r_next = player.current_room.id
                if len(self.get_unwalked_neighbors(r_next)) > 0:
                    for n in self.get_unwalked_neighbors(r_next):
                        s.push(n)
                elif len(self.walked) < len(self.rooms):

                    while len(self.get_unwalked_neighbors(player.current_room.id)) == 0 and\
                        len(self.walked) < len(self.rooms):
                        find_next = self.get_nearest_unwalked(player.current_room.id)
                        for j in find_next:
                            self.travel(j)
                    if len(self.get_unwalked_neighbors(player.current_room.id)) > 0:
                        s.push(self.get_unwalked_neighbors(player.current_room.id)[0])

    
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
            if r is not None:
                if r not in vis:
                    if r not in self.walked:
                        dir_path = []
                        for i in range(1, len(path)):
                            dir_path.append(self.get_dir(path[i-1], path[i]))
                        return dir_path
                    vis.add(r)
                    for next_d in self.rooms[r]:
                        if self.rooms[r][next_d] is not None:
                            new_path = [*path] + [self.rooms[r][next_d]]
                            q.enqueue(new_path)

# g = Graph()
# g.dft(player.current_room)

"""
Path determined by brute force. Ran the random_dir script for a few minutes, got a 954 path.
Quite inelegant, but I need a three, and it's late :)
Brian said brute force permitted. I had more clever ideas, but I'm sick as a dog, hard to work.
Also, maybe the ideas weren't so clever. I detail one in some comments at the top of random_dir.
"""

traversal_path = ['w', 'n', 'w', 'w', 's', 'n', 'w', 's', 's', 's', 'w', 'n', 'w', 'w', 'w', 'e', 'e', 'e',
's', 'w', 'w', 's', 'w', 'n', 's', 'e', 'n', 'e', 'e', 'e', 's', 'w', 's', 'w', 'e', 'n', 'w', 'e', 'e',
's', 's', 's', 's', 'w', 's', 's', 's', 'n', 'n', 'w', 's', 's', 'w', 'e', 'n', 'w', 'e', 'n', 'e', 'n',
'e', 's', 's', 's', 's', 'w', 'e', 'n', 'e', 'e', 's', 's', 's', 'w', 'e', 'n', 'e', 'w', 'n', 'n', 'w',
's', 'n', 'w', 'n', 'n', 'n', 'n', 'n', 'w', 's', 'w', 's', 'w', 's', 'n', 'e', 'n', 'w', 'w', 's', 'w',
'w', 'e', 'e', 's', 'w', 'w', 'w', 'w', 'e', 'e', 'e', 's', 'w', 'e', 's', 's', 's', 'n', 'w', 'w', 'e',
'e', 'n', 'w', 'e', 'n', 'n', 'e', 's', 's', 's', 's', 'e', 'w', 'n', 'e', 'w', 'n', 'n', 'n', 'n', 'n',
'w', 'e', 'e', 'e', 'e', 'n', 'w', 'w', 'n', 's', 'w', 'w', 'w', 's', 'w', 's', 'n', 'e', 'n', 'e', 'e',
'n', 'w', 'w', 'n', 'w', 'e', 's', 'e', 'n', 'n', 'w', 'n', 'w', 'e', 'e', 'n', 'w', 'n', 's', 'w', 'e',
'e', 'n', 's', 'e', 'e', 'e', 'n', 'w', 'w', 'e', 'e', 'e', 's', 'n', 'n', 'w', 'w', 'w', 'w', 'e', 'n',
'n', 's', 'w', 'w', 'w', 'e', 's', 'n', 'e', 'n', 'w', 'w', 'w', 'e', 'e', 'e', 'n', 's', 's', 'e', 's',
'e', 'e', 'e', 'n', 'w', 'w', 'e', 'n', 'w', 'e', 's', 'e', 's', 'e', 'n', 's', 'e', 'n', 's', 'e', 'n',
's', 'e', 'e', 'e', 's', 'e', 'n', 'e', 'n', 'e', 'n', 'e', 'n', 'n', 'e', 'n', 'n', 'e', 'n', 's', 'e',
'e', 'e', 'w', 'n', 's', 'w', 'n', 's', 'w', 'w', 's', 's', 'w', 'n', 's', 's', 's', 'w', 'n', 'n', 'n',
's', 's', 's', 's', 'w', 's', 'w', 'n', 'n', 'n', 'n', 's', 's', 'e', 'n', 'n', 's', 's', 'w', 's', 's',
's', 'e', 'e', 'n', 'e', 'e', 'e', 'e', 'e', 'e', 's', 'n', 'w', 'w', 'w', 'w', 'w', 'n', 'e', 'n', 'n',
'e', 'n', 'n', 'e', 'e', 'e', 's', 'n', 'w', 'w', 'w', 's', 's', 'e', 'n', 'e', 'w', 's', 'w', 'w', 's',
'e', 'e', 's', 'e', 'e', 'e', 's', 'n', 'w', 'w', 'w', 'n', 'e', 'n', 'e', 'w', 's', 'e', 'w', 'w', 'w',
's', 'n', 'w', 's', 'w', 's', 'w', 's', 'e', 's', 'n', 'e', 's', 'e', 'e', 'e', 'n', 's', 'e', 'w', 'w',
'w', 'w', 'n', 'e', 'e', 'w', 'w', 'w', 'w', 'w', 's', 'e', 's', 's', 'e', 'w', 'n', 'e', 'e', 's', 's',
's', 'e', 'n', 's', 'e', 'w', 'w', 's', 'e', 'e', 'w', 'w', 's', 'e', 'e', 'w', 'w', 'n', 'n', 'n', 'n',
'e', 'e', 'e', 'w', 's', 'n', 'w', 'w', 'n', 'e', 'e', 'e', 'w', 'w', 'w', 'w', 'w', 'n', 'w', 's', 's',
'n', 'n', 'n', 'w', 'w', 's', 's', 'e', 's', 'n', 'w', 's', 'w', 's', 's', 's', 's', 's', 's', 's', 's',
's', 's', 'n', 'n', 'n', 'n', 'n', 'w', 'w', 'w', 'n', 's', 'e', 's', 'w', 's', 'n', 'e', 'e', 's', 's',
's', 'n', 'n', 'n', 'w', 's', 'n', 'n', 'e', 'n', 'w', 'e', 'n', 'w', 'e', 'n', 'w', 'w', 's', 'n', 'e',
'e', 'n', 'w', 'e', 'n', 'w', 'e', 'e', 'e', 's', 's', 's', 's', 'e', 's', 's', 's', 's', 's', 'w', 's',
'n', 'e', 's', 's', 'n', 'n', 'n', 'n', 'e', 's', 'e', 's', 's', 'n', 'n', 'e', 's', 's', 'n', 'n', 'w',
'w', 's', 's', 'n', 'n', 'n', 'e', 'e', 'n', 'e', 'e', 's', 's', 's', 's', 'n', 'n', 'e', 'w', 'n', 'n',
'e', 'w', 'w', 's', 's', 'n', 'n', 'w', 's', 'w', 'w', 'w', 'n', 'w', 's', 's', 'n', 'n', 'e', 'n', 'n',
'w', 's', 'n', 'n', 'n', 'n', 'e', 'e', 's', 's', 's', 's', 's', 'e', 'w', 'n', 'n', 'n', 'e', 's', 'e',
'w', 's', 'e', 'e', 'e', 'e', 'w', 'w', 'w', 'w', 'n', 'n', 'w', 'n', 'e', 'n', 'e', 's', 's', 'n', 'n',
'w', 's', 'w', 'n', 'w', 's', 's', 'n', 'n', 'w', 'n', 'n', 'n', 'e', 'w', 'w', 'n', 's', 's', 'w', 'e',
'n', 'w', 'w', 's', 'w', 's', 's', 'n', 'n', 'e', 'n', 'e', 'e', 'e', 'n', 'n', 'w', 'n', 'w', 'e', 'n',
'w', 'n', 'n', 'n', 'w', 'w', 'n', 'w', 'e', 's', 'e', 'n', 's', 'e', 's', 's', 'w', 'n', 's', 'e', 's',
'w', 'w', 'n', 'n', 'w', 'n', 's', 'e', 's', 's', 'w', 'n', 's', 'w', 'n', 'n', 'n', 'n', 'n', 's', 's',
's', 's', 'w', 'n', 'w', 'w', 'w', 'w', 'w', 'e', 's', 'w', 'e', 'n', 'e', 'e', 'n', 'w', 'e', 'n', 'n',
's', 's', 's', 'e', 'n', 'n', 's', 's', 'e', 'n', 'n', 'n', 'w', 'e', 'n', 'n', 's', 's', 's', 's', 's',
's', 'w', 'w', 'e', 'e', 'e', 's', 'e', 'e', 'e', 'e', 'e', 'n', 's', 'e', 'n', 'n', 'w', 'n', 'n', 'w',
'n', 'e', 'w', 'w', 'e', 's', 'e', 's', 's', 'e', 'n', 'e', 'e', 'w', 'w', 'n', 'n', 'e', 'w', 'n', 'n',
'n', 'n', 'e', 'e', 'n', 'e', 'e', 'w', 'w', 's', 's', 's', 's', 'e', 's', 's', 'e', 'w', 'w', 'w', 'e',
'n', 's', 'e', 'n', 'e', 'e', 'w', 'n', 'e', 'n', 's', 'e', 'n', 's', 'e', 'w', 'w', 'w', 's', 'w', 'n',
'n', 'n', 'n', 's', 's', 'e', 'n', 'n', 's', 'e', 'n', 'e', 'e', 'w', 's', 'n', 'w', 'n', 's', 's', 'w',
's', 'w', 's', 'w', 'n', 'n', 'n', 'w', 'n', 'w', 'w', 'e', 'e', 's', 'w', 's', 's', 's', 'e', 'n', 'n',
's', 's', 'w', 'w', 'n', 'n', 's', 'w', 'n', 's', 'e', 's', 'w', 'w', 'w', 'w', 'n', 's', 'w', 'n', 's',
'e', 'e', 's', 'w', 'e', 'n', 'e', 'n', 'n', 'n', 'n', 's', 's', 's', 'w', 'n', 'n', 'w', 'e', 's', 's',
'e', 's', 'e', 'e', 'e', 's', 's', 's', 's', 's', 's', 's']

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

# print(traversal_path)

# print(g.rooms)
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
