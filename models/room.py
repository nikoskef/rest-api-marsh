from typing import Dict, List

from db import db


class RoomModel(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(40), nullable=False)
    location = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(1200))
    rateofescape = db.Column(db.String(20))
    image = db.Column(db.String(80))
    duration = db.Column(db.String(30), nullable=False)
    playedon = db.Column(db.String(80))

    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    category = db.relationship("CategoryModel")

    @classmethod
    def find_by_id(cls, _id: int) -> "RoomModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name_company(cls, name: str, company: str) -> "RoomModel":
        return cls.query.filter_by(name=name, company=company).first()

    @classmethod
    def get_all_rooms(cls) -> Dict[str, List['RoomModel']]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
