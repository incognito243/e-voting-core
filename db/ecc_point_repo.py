# ecc_point_repo.py
from sqlalchemy.orm import Session
from entity.ecc_point import ECCPoint
from db.db import Base

class ECCPointModel(Base):
    __tablename__ = "ecc_points"

    id = Base.metadata.Column(Base.metadata.Integer, primary_key=True, autoincrement=True)
    x = Base.metadata.Column(Base.metadata.Integer, nullable=False)
    y = Base.metadata.Column(Base.metadata.Integer, nullable=False)
    is_origin = Base.metadata.Column(Base.metadata.Boolean, nullable=False)

    def to_entity(self) -> ECCPoint:
        return ECCPoint(self.x, self.y, self.is_origin)

    @staticmethod
    def from_entity(entity: ECCPoint) -> "ECCPointModel":
        return ECCPointModel(x=entity.x, y=entity.y, is_origin=entity.is_origin)

class ECCPointRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, point: ECCPoint):
        model = ECCPointModel.from_entity(point)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model.to_entity()