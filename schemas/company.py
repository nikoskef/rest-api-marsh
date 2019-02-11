from ma import ma
from models.company import CompanyModel
from models.room import RoomModel
from schemas.room import RoomSchema


class CompanySchema(ma.ModelSchema):
    rooms = ma.Nested(RoomSchema, many=True)

    class Meta:
        model = CompanyModel
        dump_only = ("id",)
        include_fk = True