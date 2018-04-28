from sqlalchemy import exc

import database

class BaseModel:
    PER_PAGE = 100

    def save(self):
        database.db.session.add(self)
        self._flush()

    def delete(self):
        database.db.session.delete(self)
        self._flush()

    def _flush(self):
        try:
            database.db.session.flush()
        except exc.DatabaseError:
            database.db.session.rollback()
            raise

    def attr_map(self, attr_map):
        for prop in attr_map:
            if hasattr(self, prop):
                setattr(self, prop, attr_map.get(prop))
