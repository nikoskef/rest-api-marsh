from typing import Dict, List
from datetime import datetime

from models.company import CompanyModel

from db import db


class RoomModel(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(1200))
    difficulty = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    duration = db.Column(db.String(30), nullable=False)
    is_active = db.Column(db.Boolean)

    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    category = db.relationship("CategoryModel")

    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    company = db.relationship("CompanyModel")

    path = db.Column(db.Unicode(100))

    def __repr__(self):
        return self.name

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
