from sqlalchemy import Integer, Column, Boolean, ForeignKey
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from .game import Game

class Player(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True, autoincrement=True)
    current_position = Column(Integer, default=0)
    skipping_move = Column(Boolean, default=False)
    number_move = Column(Integer)
    game_id = Column(Integer, ForeignKey(Game.id))


    def __repr__(self):
        return f'<Player> {self.id} Position: {self.current_position} Пропуск хода: {self.skipping_move}'