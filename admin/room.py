from flask import url_for
from jinja2 import Markup
import os
import os.path as op
from sqlalchemy.event import listens_for
from flask_admin import form

from admin.modelview import MyModelView
from models.room import RoomModel

file_path = 'static/images/'


@listens_for(RoomModel, 'after_delete')
def del_image(mapper, connection, target):
    if target.path:
        # Delete image
        try:
            os.remove(op.join(file_path, target.path))
        except OSError:
            pass

        # Delete thumbnail
        try:
            os.remove(op.join(file_path,
                              form.thumbgen_filename(target.path)))
        except OSError:
            pass


class RoomView(MyModelView):
    column_editable_list = ['category', 'company']

    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=form.thumbgen_filename('images/' + model.path)))

    column_formatters = {
        'path': _list_thumbnail
    }

    form_extra_fields = {
        'path': form.ImageUploadField('Image',
                                      base_path=file_path,
                                      relative_path='test',
                                      thumbnail_size=(100, 100, True))
    }