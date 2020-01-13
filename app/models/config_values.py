from app.helpers.app_context import AppContext as AC
from app.models.db_mixin import DBMixin

db = AC().db


class ConfigValues(db.Model, DBMixin):
    __tablename__ = 'config_values'
    name = db.Column(db.String(50), unique=True, nullable=False)
    value =  db.Column(db.String(255), nullable=False)   
    
        
    def __init__(self, name, value):
        self.name = name
        self.value = value
    
    @classmethod
    def get_config_value(cls, name, page=None, per_page=None):
        filter_query = cls.name == name
        configvalue =  cls.get(filter_query,page,per_page)
        return configvalue[0].value