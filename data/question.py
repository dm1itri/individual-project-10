from sqlalchemy import Integer, Column, Boolean, ForeignKey, String
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Question(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_question = Column(String(16), nullable=False)
    question = Column(String(256), nullable=False)
    answer_correct = Column(String(32), nullable=False)
    answer_2 = Column(String(32))
    answer_3 = Column(String(32))
    answer_4 = Column(String(32))

    def __repr__(self):
        return f'<QuestionID {self.id}> Question: {self.question} Type_question: {self.type_question}\nAnswer_correct: {self.answer_correct}\nAnswer_2: {self.answer_2}\nAnswer_3: {self.answer_3}\nAnswer_4: {self.answer_4}\n'