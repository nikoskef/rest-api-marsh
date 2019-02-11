from ma import ma
from models.room import RoomModel
from models.category import CategoryModel



class RoomSchema(ma.ModelSchema):
    class Meta:
        model = RoomModel
        load_only = ("category", "company")
        dump_only = ("id", "created_at", "path")
        include_fk = True
