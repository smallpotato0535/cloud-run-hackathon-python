from Player import *
import random

atk_range = 2
turnFirst="L"

dir_no = {
    "0": "N",
    "1": "E",
    "2": "S",
    "3": "W",
    "N": "0",
    "E": "1",
    "S": "2",
    "W": "3",
}

# return res {dict}
def shoot_now(me, states):
    for url, data in states.items():
        if url != me.url:
            if me.x == data['x']:
                if abs(me.y - data['y']) <= atk_range:
                    if facing_tar_not(me.dir, me.x, me.y, data['x'], data['y']):
                        return {"move":"T", "des":"shoot now"}
            elif me.y == data['y']:
                if abs(me.x - data['x']) <= atk_range:
                    if facing_tar_not(me.dir, me.x, me.y, data['x'], data['y']):
                        return {"move":"T", "des":"shoot now"}
    return {"move":False, "des":"dont shoot"}

def got_hit_and_run(me):
    if me.wasHit:
        return {"move":turnFirst, "des":"got_hit_and_run"}
    return {"move":'', "des":"not got hit"}

# return dict
def chase_an_enemy(dims, me, enemy):
    res = get_next_xy_to_chase_enemy(me, enemy)
    if len(res):
        res = get_action_to_location(dims, me.dir, me.x, me.y, enemy.x, enemy.y)
        return {"move":res["move"], "des":"chasing now"}
    return {"move":'', "des":"dont chase"}

# action to target location with closest distance
# return {dict}
def get_action_to_location(dims, cur_dir, cur_x, cur_y, tar_x, tar_y):
    x_diff = abs(cur_x - tar_x)
    y_diff = abs(cur_x - tar_y)
    res = {}
    res["xy_diff"] = x_diff + y_diff
    res["move"] = turn_or_walk(dims, cur_dir, cur_x, cur_y, tar_x, tar_y)
    return res

def turn_or_walk(dims, cur_dir, cur_x, cur_y, tar_x, tar_y):
    x_diff = cur_x - tar_x
    y_diff = cur_y - tar_y
    if abs(x_diff) > 0:
        if x_diff > 0 and cur_dir == "W":
            return "F"
        elif x_diff < 0 and cur_dir == "E":
            return "F"
        elif x_diff > 0 and cur_dir != "W":
            if (cur_dir == "N"):
                return "L"
            if (cur_dir == "S"):
                return "R"
            return turnFirst
        elif x_diff < 0 and cur_dir != "E":
            if (cur_dir == "N"):
                return "R"
            if (cur_dir == "S"):
                return "L"
            return turnFirst

    if abs(y_diff) > 0:
        if y_diff > 0 and cur_dir == "N":
            return "F"
        elif y_diff < 0 and cur_dir == "S":
            return "F"
        elif y_diff > 0 and cur_dir != "N":
            if (cur_dir == "W"):
                return "R"
            if (cur_dir == "E"):
                return "L"
            return turnFirst
        elif y_diff < 0 and cur_dir != "S":
            if (cur_dir == "W"):
                return "L"
            if (cur_dir == "E"):
                return "R"
            return turnFirst
    return dont_face_wall_or_fire(dims, cur_dir, cur_x, cur_y)

def dont_face_wall_or_fire(dims, cur_dir, cur_x, cur_y):
    turnFirst="L"
    # left
    if cur_x == 0:
        if cur_y == 0:
            if cur_dir == "N":
                return "R"
            elif cur_dir == "W":
                return "L"
        elif cur_y == dims[1]-1:
            if cur_dir == "W":
                return "R"
            elif cur_dir == "S":
                return "L"
        elif cur_dir == "W":
            return turnFirst
    # right
    elif cur_x == dims[0]-1:
        if cur_y == 0:
            if cur_dir == "N":
                return "L"
            elif cur_dir == "E":
                return "R"
        elif cur_y == dims[1]-1:
            if cur_dir == "E":
                return "L"
            elif cur_dir == "S":
                return "R"
        elif cur_dir == "E":
            return turnFirst
    # top
    elif cur_y == 0 and cur_dir == "N":
        return turnFirst
    # top
    elif cur_y == dims[1]-1 and cur_dir == "S":
        return turnFirst
    # fire
    return "T"

# return res {dict}
def check_corner(dims, me, states):
    empty_corner = check_empty_corner(dims, me, states)
    if len(empty_corner):
        move = {
            "min": 9999,
            "move": ''
        }
        for corner in empty_corner:
            if move["min"] > corner["xy_diff"]:
                move["min"] = corner["xy_diff"]
                move["move"] = corner["move"]
        # move to closest corner
        return {"move":move["move"], "des":"moving to corner/already at corner"}
    return {"move":False, "des":"dont move corner"}

# return empty corner {dict}
def check_empty_corner(dims, me, states):
    corner={
        "t1": [0, 0],
        "bl": [0, dims[1]-1],
        "tr": [dims[0]-1, 0],
        "br": [dims[0]-1, dims[1]-1],
    }
    empty_corner = []

    # check and return empty corner
    for key in corner:
        empty = True

        for url, data in states.items():
            # skipped me
            # empty = True, when we at corner
            if url != me.url:
                if data['x'] == corner[key][0] and data['y'] == corner[key][1]:
                    empty = False
                    break
        
        if empty:
            res = get_action_to_location(dims, me.dir, me.x, me.y, corner[key][0], corner[key][1])
            empty_corner.append({
                "xy": corner[key],
                "xy_diff": res["xy_diff"],
                "move": res["move"],
            })
    
    return empty_corner

# always move along x-axis first
# return xy {arr}
def get_next_xy_to_chase_enemy(me, enemy):
    x_diff = me.x - enemy.x
    y_diff = me.y - enemy.y
    res = enemy_at_wt_dir_in_cross(me.x, me.y, enemy.x, enemy.y)
    if res:
        return [me.x, me.y]
    #  at my top left/bot left
    elif x_diff > 0:
        return [me.x - x_diff, me.y]
    #  at my top right/bot right
    elif x_diff < 0:
        return [me.x + x_diff, me.y]

    #  at my top left/bot left
    elif y_diff > 0:
        return [me.x, me.y - y_diff]
    #  at my top right/bot right
    elif y_diff < 0:
        return [me.x, me.y + y_diff]
    return []

            

# return T/F
def facing_tar_not(cur_dir, cur_x, cur_y, tar_x, tar_y):
    enemy_dir = enemy_at_wt_dir_in_cross(cur_x, cur_y, tar_x, tar_y)
    if cur_dir == enemy_dir:
        return True
    return False

# x or y must at least 1 equal to each other, within the cross
# return dir
def enemy_at_wt_dir_in_cross(cur_x, cur_y, tar_x, tar_y):
    if cur_x == tar_x:
        if (cur_y > tar_y):
            return "N"
        else:
            return "S"
    elif cur_y == tar_y:
        if (cur_x > tar_x):
            return "W"
        else:
            return "E"

    elif cur_x == tar_x and cur_y == tar_y:
        return "overlap"
    return False

def move_randomly(dims, me):
    random_xy = [random.randrange(dims[0]), random.randrange(dims[1])]
    res = get_action_to_location(dims, me.dir, me.x, me.y, random_xy[0], random_xy[1])
    return {"move":res["move"], "des":"move randomly"}
def detect(enemy_arr,mytank):
    possible_hit = 0
    can_attack = False
    if len(enemy_arr)>0:
        for i in range (len(enemy_arr)):
            if mytank.x == enemy_arr[i].x:
                if mytank.y - enemy_arr[i].y <= atk_range and mytank.y - enemy_arr[i].y >= 0:
                    if enemy_arr[i].dir == "S":
                        possible_hit +=1
                    if mytank.dir == "N":
                        can_attack = True
                if mytank.y - enemy_arr[i].y >= -atk_range and mytank.y - enemy_arr[i].y <= 0:
                    if enemy_arr[i].dir == "N":
                        possible_hit +=1
                    if mytank.dir == "S":
                        can_attack = True
            if mytank.y == enemy_arr[i].y:
                if mytank.x - enemy_arr[i].x <= atk_range and mytank.x - enemy_arr[i].x >= 0:
                    if enemy_arr[i].dir == "E":
                        possible_hit +=1
                    if mytank.dir == "W":
                        can_attack = True
                if mytank.x - enemy_arr[i].x >= -atk_range and mytank.x - enemy_arr[i].x <= 0:
                    if enemy_arr[i].dir == "W":
                        possible_hit +=1
                    if mytank.dir == "E":
                        can_attack = True

    return {"possible_hit":possible_hit, "can_attack":can_attack}
def check_and_move(dims, x, y, direction):
    if direction == "N":
        if y - 1 <= 0:
            return "L"
    elif direction == "E":
        if x + 1 == dims[0]:
            return "L"
    elif direction == "S":
        if y + 1 == dims[1]:
            return "L"
    elif direction == "W":
        if x - 1 <= 0:
            return "L"     
    return "F"   
