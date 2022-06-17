
# Copyright 2020 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import logging
import random
from flask import Flask, request
from Player import *
from action import *

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = Flask(__name__)
moves = ['F', 'T', 'L', 'R']

@app.route("/", methods=['GET'])
def index():
    return "Let the battle begin!"

@app.route("/", methods=['POST'])
def move():
    # request.get_data()
    logger.info(request.json)
    # return moves[random.randrange(len(moves))]

    request.get_data()
    #logger.info(request.json)

    states = request.json['arena']['state']
    dims = request.json['arena']['dims']
    my_url = request.json['_links']['self']['href']
    my_state = states[my_url]
    player_info = request.json['arena']['state']
    myself = player_info[my_url]


    mytank = Player(my_url, my_state['x'], my_state['y'], my_state['direction'], my_state['wasHit'], my_state['score'])

    # logger.info(check_corner(dims, myself.direction, myself.x, myself.y, states))

    enemy_arr = []
    way_block = []
    block_me = False
    Zone = {"A":0,"B":0,"C":0,"D":0}
   
    for player_link, player in player_info.items():
        if player_link != my_url:
            if player['x'] == mytank.x or player['y'] == mytank.y:
                enemy = Player(player_link, player['x'],player['y'],player['direction'],player['wasHit'],player['score'])
                enemy_arr.append(enemy)
                if player['x'] == mytank.x:
                    if player['y'] - mytank.y == 1:
                        way_block.append("S")
                        if mytank.dir == "S":
                            block_me = True
                    elif mytank.y - player['y'] == 1:
                        way_block.append("N")
                        if mytank.dir == "N":
                            block_me = True
                elif player['y'] == mytank.y:
                    if player['x'] - mytank.x == 1:
                        way_block.append("E")
                        if mytank.dir == "E":
                            block_me = True
                    elif mytank.x - player['x'] == 1:
                        way_block.append("W")
                        if mytank.dir == "W":
                            block_me = True
                if mytank.x == 0:
                    way_block.append("W")
                elif mytank.x == dims[0]-1:
                    way_block.append("E")
                elif mytank.y == 0:
                    way_block.append("N")
                elif mytank.y == dims[1]-1:
                    way_block.append("S")
            if player['x'] <= dims[0]/2 -1 and player['y'] <= dims[1]/2 -1:
                Zone['A'] += 1
            elif player['x'] >= dims[0]/2 and player['y'] <= dims[1]/2 - 1:
                Zone['B'] += 1
            elif player['x'] <= dims[0]/2 -1 and player['y'] >= dims[1]/2:
                Zone['C'] += 1
            elif player['x'] >= dims[0]/2 and player['y'] >= dims[1]/2:
                Zone['D'] += 1

    res = detect(enemy_arr, mytank)
    if res['possible_hit'] > 1:
            if len(way_block) == 4:
                res = check_corner(dims, mytank, states)
                if res["move"]:
                    return res["move"]
                return "T"
            else:
                if block_me == True:
                    return "L"
            return check_and_move(dims,mytank.x,mytank.y,mytank.dir)

    if res['possible_hit'] <= 1 and res['can_attack'] == True:
        return "T"
    elif res['possible_hit'] == 1 and res['can_attack'] == False and block_me == False:
        return check_and_move(dims,mytank.x,mytank.y,mytank.dir)
    
    res = shoot_now(mytank, states)
    logger.info(res["des"])
    if res["move"]:
        return res["move"]

    res = got_hit_and_run(mytank)
    logger.info(res["des"])
    if res["move"]:
        return res["move"]
    
    res = check_corner(dims, mytank, states)
    logger.info(res["des"])
    if res["move"]:
        return res["move"]

    res = move_randomly(dims, mytank)
    logger.info(res["des"])
    if res["move"]:
        return res["move"]

    # should not reach here
    logger.info("Fire anyway, should not be here")
    return "T"
        
    return "Random Move"


if __name__ == "__main__":
  app.run(debug=False,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
  
