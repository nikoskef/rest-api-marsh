import os
import os.path as op


from models.user import UserModel


def create_path():
    file_path = op.join(op.dirname(__file__), 'files')
    try:
        os.mkdir(file_path)
    except OSError:
        pass





