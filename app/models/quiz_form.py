from app.helpers.app_context import AppContext as AC
from app.models.db_mixin import DBMixin
from flask_sqlalchemy import SQLAlchemy

db = AC().db

class QuizForm(db.Model, DBMixin):
    __tablename__ = 'quiz_form'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=1)
    birthday = db.Column(db.DateTime, nullable=False)
    occupation = db.Column(db.String(255))
    size = db.Column(db.String(255))
    fav_brands = db.Column(db.String(255))
    instagram_handle = db.Column(db.String(255))
    interest = db.Column(db.String(255))
    style = db.Column(db.String(255))
    user = db.relationship('User')

    output_column = ['id', 'birthday', 'occupation',
                     'user.email', 'size', 'fav_brands', 'instagram_handle', 'interest', 
                     'style', ]

    # def update_from_dict(self, obj_dict, not_updatable_columns=[]):
    #     """
    #     update_from_dict updates self by using dict

    #     Args:
    #         obj_dict (dict):
    #         not_updatable_columns (list, optional): columns that won't be updated

    #     Returns:
    #         [type]: [description]
    #     """
    #     not_updatable_columns = not_updatable_columns if len(
    #         not_updatable_columns) > 0 else self.not_updatable_columns
    #     flag = False
    #     if obj_dict:
    #         for key in obj_dict:
    #             if hasattr(self, key):
    #                 if key in not_updatable_columns:
    #                     continue
    #                 else:
    #                     setattr(self, key, obj_dict[key])
    #                 flag = True       
    #     return flag
