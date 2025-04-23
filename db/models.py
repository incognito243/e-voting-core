from sqlalchemy import Column, Integer, String, JSON
from db import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False)
    public_key = Column(String, nullable=False)
    p = Column(String, nullable=False)
    q = Column(String, nullable=False)
    e = Column(String, nullable=False)
    d = Column(String, nullable=False)
    phi = Column(String, nullable=False)


class VotingServerModel(Base):
    __tablename__ = "voting_servers"

    id = Column(Integer, primary_key=True, index=True)
    server_name = Column(String, nullable=False)
    number_of_candidates = Column(Integer, nullable=False)
    maximum_number_of_voters = Column(Integer, nullable=False)
    public_key = Column(String, nullable=False)