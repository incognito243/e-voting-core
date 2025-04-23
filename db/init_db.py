from db import Base, engine
from models import UserModel, VotingServerModel

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()