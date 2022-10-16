from sqlalchemy import Integer, Column
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Game(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True, autoincrement=True)
    current_player = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return f'<Game> {self.id} {self.current_player}'