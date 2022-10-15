from sqlalchemy import Integer, Column, ForeignKey
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import relationship
from .db_session import SqlAlchemyBase


class Game(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True, autoincrement=True)
    current_player = Column(Integer, nullable=False, default=0)
    first_player = Column(Integer, ForeignKey('player.id'), nullable=False)
    second_player = Column(Integer, ForeignKey('player.id'), nullable=False)
    third_player = Column(Integer, ForeignKey('player.id'), nullable=False)
    fourth_player = Column(Integer, ForeignKey('player.id'), nullable=False, )
    player_id = relationship("Player", foreign_keys=[first_player, second_player, third_player, fourth_player], backref="player.id")

    def __repr__(self):
        return f'<Game> {self.id} {self.current_player}'