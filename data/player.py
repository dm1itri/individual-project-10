from sqlalchemy import Integer, Column, String, Boolean
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase


class Player(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True, autoincrement=True)
    #name = Column(String, nullable=False)
    #email = Column(String, nullable=False, unique=True)
    #hashed_password = Column(String, nullable=False)
    current_position = Column(Integer, default=0)
    skipping_move = Column(Boolean, default=False)

    def __repr__(self):
        return f'<Player> {self.id} {self.current_position}'