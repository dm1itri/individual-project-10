from sqlalchemy import Integer, Column, ForeignKey, Boolean
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from .question import Question


class Game(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True, autoincrement=True)
    current_player = Column(Integer, nullable=False, default=0)
    number_of_players = Column(Integer, nullable=False, default=2)
    max_number_of_questions = Column(Integer, nullable=False, default=10)
    number_of_questions_answered = Column(Integer, nullable=False, default=0)
    question_id = Column(Integer, default=None)
    is_over = Column(Boolean, default=False)
    # number_history = Column(Integer)  # текущий ход за всю игру

    def __repr__(self):
        return f'<Game> {self.id} Current_player: {self.current_player} Number_of_players: {self.number_of_players} Question_id {self.question_id}'