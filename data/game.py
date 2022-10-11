from sqlalchemy import Integer, Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Game(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True, autoincrement=True)
    current_player = Column(Integer, nullable=False, default=0)
    first_player = Column(Integer, ForeignKey('player.id'), nullable=False, default=1)
    second_player = Column(Integer, ForeignKey('player.id'), nullable=False, default=2)
    third_player = Column(Integer, ForeignKey('player.id'), nullable=False, default=3)
    fourth_player = Column(Integer, ForeignKey('player.id'), nullable=False, default=4)

    def __repr__(self):
        return f'<Game> {self.id} {self.current_player}'