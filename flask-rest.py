from flask import Flask, jsonify, render_template
from flask_restful import Api
from data import db_session
from data.game import Game
from data.player import Player
from api.routes import ApiGame, ApiPlayer, ApiPlayers

app = Flask(__name__)
db_session.global_init("db/games.sqlite")
api = Api(app)
api.add_resource(ApiGame, '/api/game/<int:game_id>')
api.add_resource(ApiPlayer, '/api/player/<int:player_id>')
api.add_resource(ApiPlayers, '/api/players/<int:game_id>')
'''
players = [Player() for i in range(4)]
game = Game()
game.first_player = players[0].id
game.second_player = players[1].id
game.third_player = players[2].id
game.fourth_player = players[3].id
with db_session.create_session() as session:
    session.add(game)
    session.add_all(players)
    session.commit()
'''


@app.get('/')
def index():

    return render_template('index.html')


@app.get('/currentPlayer')
def current_player():
    return jsonify({'currentPlayer': 0})


with db_session.create_session() as session:
    #for i in range(4):
    #    player = Player()
    #    player.current_position = 0
    #    player.skipping_move = False
    #    session.add(player)
    #session.commit()

    game = Game()
    game.current_player = 0
    players = [session.query(Player).get(i) for i in range(1, 5)]
    game.first_player = players[0].id
    game.second_player = players[1].id
    game.third_player = players[2].id
    game.fourth_player = players[3].id
    session.add(game)
    session.commit()
    '''
    game = session.query(Game).get(1)
    game.current_player = 0
    players = []
    for i in range(1, 5):
        player = session.query(Player).get(i)
        player.current_position = 0
        player.skipping_move = False
        players.append(player)
        session.commit()
        # game['first_player', 'second_player', 'third_player', 'fourth_player'][i - 1] = player
    game.first_player = players[0].id
    game.second_player = players[1].id
    game.third_player = players[2].id
    game.fourth_player = players[3].id
    session.commit()
    '''

if __name__ == '__main__':
    app.run('127.0.0.1', debug=True)