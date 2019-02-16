from ma import ma
from models.room import RoomModel
from models.category import CategoryModel


class RoomSchema(ma.ModelSchema):
    class Meta:
        model = RoomModel
        load_only = ("category_id", "company_id")
        dump_only = ("id", "created_at", "path", "company", "category")
        include_fk = True
