#!/usr/bin/python3
import models
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

classes = {"User": User, "State": State, "City": City, "Place": Place,
           "Amenity": Amenity, "Review": Review}


class DBStorage:
    """DBStorage engine"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage engine"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        new_dict = {}
        for clss in classes:
            if cls is None or cls in classes[clss] or cls in clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """Adds an object to current database session"""
        self.__session.add(obj)

    def save(self):
        """commits all changes to current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes from current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """creates all tables"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """Close the current session"""
        self.__session.remove()
