from sqlalchemy import Integer, Column, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from .game import Game


class Player(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True, autoincrement=True)
    current_position = Column(Integer, default=0)
    skipping_move = Column(Boolean, default=False)
    number_move = Column(Integer)
    is_occupied = Column(Boolean, default=False)
    number_of_points = Column(Integer, default=0)
    thinks_about_the_question = Column(Boolean, default=False)
    number_of_questions_received = Column(Integer, default=0)
    number_of_correct_answers = Column(Integer, default=0)
    game_id = Column(Integer, ForeignKey(Game.id))
    game = relationship('Game', backref='player')

    def __repr__(self):
        return f'<Player> {self.id} Game: {self.game_id} Position: {self.current_position} Skipping move: {self.skipping_move} Number move: {self.number_move} Is occupied: {self.is_occupied}'