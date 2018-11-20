from ma import ma
from models.category import CategoryModel
from models.room import RoomModel
from schemas.room import RoomSchema


class CategorySchema(ma.ModelSchema):
    rooms = ma.Nested(RoomSchema, many=True)

    class Meta:
        model = CategoryModel
        dump_only = ("id",)
        include_fk = True
