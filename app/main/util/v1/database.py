from app.main import db 
from sqlalchemy import func

def save_db(object, name = None):

    if name == None:
        name = object.__tablename__

    try:
        db.session.add(object)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception( f'Database {str(name)} : {str(e)}')


def get_count(object):
    count_object = object.statement.with_only_columns([func.count()]).order_by(None)
    count = object.session.execute(count_object).scalar()
    return count

        