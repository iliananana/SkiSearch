import heapq
from cost import get_crashes, get_cost, get_heuristic

graph = {
    'Colorado State University': { 'neighbors': {'I-25mm_10'}},
    'I-25mm_10' : {'neighbors': {'I-25mm_20'}},
    'I-25mm_20' : {'neighbors': {'I-25mm_10', 'I-25mm_30'}},
    'I-25mm_30' : {'neighbors': {'I-25mm_20', 'I-25mm_40'}},
    'I-25mm_40' : {'neighbors': {'I-25mm_30', 'Eldora', 'I-25mm_50'}},
    'Eldora' : {'neighbors': {'I-25mm_40', 'I-25mm_50'}},
    'I-25mm_50' : {'neighbors': {'I-25mm_40', 'Eldora', 'I-25mm_60'}},
    'I-25mm_60' : {'neighbors': {'I-25mm_50', 'I-70mm_10'}},
    'I-70mm_10' : {'neighbors': {'I-25mm_60', 'I-70mm_20'}},
    'I-70mm_20' : {'neighbors': {'I-70mm_10', 'I-70mm_30'}},
    'I-70mm_30' : {'neighbors': {'I-70mm_20', 'Winter Park', 'I-70mm_40'}},
    #'Idaho Springs' : {'neighbors': {'I-70mm_30', 'I-70mm_40'}},
    'Winter Park' : {'neighbors': {'I-70mm_30', 'I-70mm_40'}},
    'I-70mm_40' : {'neighbors': {'I-70mm_30', 'Winter Park', 'I-70mm_50'}},
    #'Georgetown' : {'neighbors': {'I-70mm_40', 'I-70mm_50'}},
    'I-70mm_50' : {'neighbors': {'I-70mm_40', 'Loveland', 'Arapahoe Basin', 'I-70mm_60'}},
    'Loveland' : {'neighbors': {'I-70mm_50', 'I-70mm_60'}},
    'Arapahoe Basin': {'neighbors': {'I-70mm_50', 'I-70mm_60'}},
    'I-70mm_60' : {'neighbors': {'I-70mm_50', 'Loveland', 'Arapahoe Basin', 'Keystone', 'I-70mm_70'}},
    'Keystone' : {'neighbors': {'I-70mm_60', 'I-70mm_70'}},
    'I-70mm_70' : {'neighbors': {'I-70mm_60', 'Keystone', 'Breckenridge', 'Copper Mountain', 'I-70mm_80'}},
    'Breckenridge' : {'neighbors': {'I-70mm_70', 'I-70mm_80'}},
    'Copper Mountain' : {'neighbors': {'I-70mm_70', 'I-70mm_80'}},
    'I-70mm_80' : {'neighbors': {'I-70mm_70', 'Breckenridge', 'Copper Mountain', 'I-70mm_90'}},
    'I-70mm_90' : {'neighbors': {'I-70mm_80', 'Vail', 'I-70mm_100'}},
    'Vail' : {'neighbors': {'I-70mm_90', 'I-70mm_100'}},
    'I-70mm_100' : {'neighbors': {'I-70mm_90', 'Vail', 'Beaver Creek', 'I-70mm_110'}},
    'Beaver Creek' : {'neighbors': {'I-70mm_100', 'I-70mm_110'}},
    'I-70mm_110' : {'neighbors': {'I-70mm_100', 'Beaver Creek', 'I-70mm_120'}},
    'I-70mm_120' : {'neighbors': {'I-70mm_110'}},
}

resorts = ['Arapahoe Basin', # added
           'Aspen Snowmass',
           'Beaver Creek', # added
           'Breckenridge', # added
           'Cooper',
           'Copper Mountain', # added
           'Echo Mountain',
           'Eldora',  # added
           'Keystone', # added
           'Loveland', # added
           'Monarch',
           'Purgatory',
           'Silverton',
           'Steamboat',
           'Vail', # added
           'Winter Park'] # added

def get_input(best_neighbor, goal):
    while True:
        ans = input(f"Re-evaluating trip to {goal}, Accept new goal: {best_neighbor} (y/n)")
        if ans == 'y':
            goal = best_neighbor
            print('Accepted new goal resort: ', goal)
            break
        elif ans == 'n':
            print(f"Denied new goal: {best_neighbor}, Continuing to {goal}")
            break
    return goal

def crash_reroute(current, goal, total_cost):
    print(f'crash at {current} re-evaluating goal resort...')        # find the resort with the lowest estimated cost
    best_neighbor = None
    best_priority = float('inf')
    for neighbor in graph[current]['neighbors']:
        if neighbor in resorts:
            if neighbor != current:
                priority = total_cost[current] + heuristic(goal, current, neighbor)
                if priority < best_priority:
                    best_neighbor = neighbor
                    best_priority = priority
    if best_neighbor:
        goal = get_input(best_neighbor, goal)
    return goal

def heuristic(goal, current, neighbor):
    current_cost = get_cost(current)
    neighbor_cost = get_cost(neighbor)
    if neighbor_cost < current_cost:
        return (goal == neighbor) * (current_cost - neighbor_cost)
    return get_heuristic(goal, neighbor)

def a_star_search(start, goal):
    frontier = [(0, start)]
    visited = {}
    total_cost = {}
    visited[start] = None
    total_cost[start] = 0

    while frontier:
        current = heapq.heappop(frontier)[1]

        if current == goal:
            path = [goal]
            current = goal
            while current != start:
                current = visited[current]
                path.append(current)
            path.reverse()
            return path, total_cost, goal

        for neighbor in graph[current]['neighbors']:
            if neighbor != current:
                new_cost = total_cost[current] + get_cost(current)
                if neighbor not in total_cost or new_cost < total_cost[neighbor]:
                    total_cost[neighbor] = new_cost
                    priority = new_cost + heuristic(goal, current, neighbor)
                    heapq.heappush(frontier, (priority, neighbor))
                    visited[neighbor] = current

        if current in get_crashes():
            goal = crash_reroute(current, goal, total_cost)

    return visited, total_cost, goal

start = 'Colorado State University'

goal = 'Winter Park'
path, total_cost, new_goal = a_star_search(start, goal)
print('initial goal:', goal)
print('updated goal:', new_goal)
print('The optimal path to take is:', path)
print('The total cost is:', total_cost[new_goal])
print()


goal = 'Eldora'
path, total_cost, new_goal = a_star_search(start, goal)
print('initial goal:', goal)
print('updated goal:', new_goal)
print('The optimal path to take is:', path)
print('The total cost is:', total_cost[new_goal])
print()

goal = 'Copper Mountain'
path, total_cost, new_goal = a_star_search(start, goal)
print('initial goal:', goal)
print('updated goal:', new_goal)
print('The optimal path to take is:', path)
print('The total cost is:', total_cost[new_goal])
print()

goal = 'Beaver Creek'
path, total_cost, new_goal = a_star_search(start, goal)
print('initial goal:', goal)
print('updated goal:', new_goal)
print('The optimal path to take is:', path)
print('The total cost is:', total_cost[new_goal])
print()