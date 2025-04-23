from sqlalchemy.orm import Session
from models import UserModel, VotingServerModel

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_name: str, public_key: dict):
        user = UserModel(
            user_name=user_name,
            public_key=public_key
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_id(self, user_id: int):
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()

class VotingServerRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_voting_server(self, server_name: str, number_of_candidates: int, maximum_number_of_voters: int, public_key: dict):
        server = VotingServerModel(
            server_name=server_name,
            number_of_candidates=number_of_candidates,
            maximum_number_of_voters=maximum_number_of_voters,
            public_key=public_key
        )
        self.db.add(server)
        self.db.commit()
        self.db.refresh(server)
        return server

    def get_voting_server_by_id(self, server_id: int):
        return self.db.query(VotingServerModel).filter(VotingServerModel.id == server_id).first()