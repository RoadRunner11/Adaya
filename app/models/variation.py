from app.helpers.app_context import AppContext as AC
from app.models.db_mixin import DBMixin

db = AC().db


class Variation(db.Model, DBMixin):
    __tablename__ = 'variation'
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name
