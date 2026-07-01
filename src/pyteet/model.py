from pyteet import DATETIME_DB, database

import copy
from datetime import datetime, UTC

class Model:

    # MUST DEFINE
    TABLE = 'your_table'
    PRIMARY_KEY = 'id'
    CREATED_AT = 'created_at'
    UPDATED_AT = 'updated_at'
    CONNECTION = None # Use default database connection

    # Model data for DB mapping
    _data = {}
    # Model data that has been modified and unsaved
    _dirty = []

    def __init_subclass__(cls):
        super().__init_subclass__()
        if not hasattr(cls, 'TABLE'):
            raise TypeError(f'{cls.__name__} must define attribute TABLE')
        if not hasattr(cls, 'PRIMARY_KEY'):
            raise TypeError(f'{cls.__name__} must define attribute PRIMARY_KEY')
        if not hasattr(cls, 'CREATED_AT'):
            raise TypeError(f'{cls.__name__} must define attribute CREATED_AT')
        if not hasattr(cls, 'UPDATED_AT'):
            raise TypeError(f'{cls.__name__} must define attribute UPDATED_AT')
        if not hasattr(cls, 'CONNECTION'):
            raise TypeError(f'{cls.__name__} must define attribute CONNECTION')

    def __init__(self):
        self._data = {}
        self._dirty = []

    def __getattr__(self, name):
        # Method missing hook
        return self._data.get(name)

    def __setattr__(self, name, value):
        if hasattr(type(self), name):
            # Normal set
            super().__setattr__(name, value)
        else:
            # Map to Model data
            self._data[name] = value
            if not name in self._dirty:
                # Mark as dirty
                self._dirty.append(name)

    def copy(self):
        return copy.deepcopy(self._data)

    def creating(self):
        '''Called on save() for INSERT.'''
        pass

    def find(self, id: int) -> Model:
        sql = '''
            SELECT
                *
            FROM {}
            WHERE {} = %s
        '''.format(self.TABLE,
                   self.PRIMARY_KEY)
        data = database(self.CONNECTION).fetchone(sql, (id, ))
        if not data:
            return None
        inst = self.__class__()
        inst._data = data
        return inst

    def fetchall(self, sql, bind=None):
        rows = database(self.CONNECTION).fetchall(sql, bind)
        if not rows:
            return []
        for k, v in enumerate(rows):
            inst = self.__class__()
            inst._data = v
            rows[k] = inst
        return rows

    def fetchone(self, sql, bind=None):
        data = database(self.CONNECTION).fetchone(sql, bind)
        if not data:
            return None
        inst = self.__class__()
        inst._data = data
        return inst

    def for_api(self, data=None, recurse=False):
        if not data and not recurse:
            data = self.copy()
        if isinstance(data, dict):
            for k, v in data.items():
                data[k] = Model.for_api(self, v, True)
            return data
        if isinstance(data, list):
            for k, v in enumerate(data):
                data[k] = Model.for_api(self, v, True)
            return data
        if isinstance(data, datetime):
            return data.strftime(DATETIME_DB)
        if isinstance(data, Model):
            return data.for_api()
        return data

    def save(self):
        if not self._dirty:
            # Nothing to save
            return
        pk = getattr(self, self.PRIMARY_KEY)
        dt = datetime.now(UTC).strftime(DATETIME_DB)
        db = database(self.CONNECTION)
        is_insert = pk == None
        if is_insert:
            self.creating()
            if self.CREATED_AT:
                setattr(self, self.CREATED_AT, dt)
        self.saving()
        if self.UPDATED_AT:
            setattr(self, self.UPDATED_AT, dt)
        payload = {}
        for k in self._dirty:
            v = self._data.get(k)
            if isinstance(v, str):
                v = v.strip()
                self._data[k] = v
            payload[k] = v
        keys = list(payload.keys())
        values = tuple([payload[k] for k in keys])
        if is_insert:
            sql = '''
                INSERT INTO {} ({})
                VALUES ({})
            '''.format(self.TABLE,
                       ', '.join(keys),
                       ', '.join(['%s'] * len(values)))
            if db.driver == 'postgres':
                sql += '''
                    RETURNING {}
                '''.format(self.PRIMARY_KEY)
            pk = db.insert(sql, values)
            setattr(self, self.PRIMARY_KEY, pk)
            self._dirty = []
            return
        else:
            sql = '''
                UPDATE {}
                SET {}
                WHERE {} = %s
            '''.format(self.TABLE,
                       ', '.join(['{} = %s'.format(k) for k in keys]),
                       self.PRIMARY_KEY)
            values += (pk, )
            db.execute(sql, values)
            self._dirty = []
            return

    def saving(self):
        '''Called on save() for INSERT and UPDATE.'''
        pass

