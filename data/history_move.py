from sqlalchemy import Integer, Column
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class HistoryMove(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'history_move'
    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(Integer, nullable=False)
    number_history = Column(Integer, nullable=False, default=0)  # текущий ход за всю игру
    number_move = Column(Integer, nullable=False, default=-1)  # номер ходящего (от 0 до 3)
    number_steps = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return f'<History of move> {self.number_history} in game {self.game_id} by {self.number_move} on {self.number_steps} steps.'