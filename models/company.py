from typing import List

from db import db


class CompanyModel(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    website = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)

    rooms = db.relationship("RoomModel", lazy="dynamic")

    def __repr__(self):
        return self.name

    @classmethod
    def find_by_name(cls, name: str) -> "CompanyModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "CompanyModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["CompanyModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
