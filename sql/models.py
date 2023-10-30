from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    foolders = relationship("Foolder", back_populates="owner")
    files = relationship("File", back_populates="owner")


class Foolder(Base):
    __tablename__ = "foolders"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="foolders")
    files = relationship("File", back_populates="foolder")


class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    location = Column(String, nullable=False, index=True)
    content_type = Column(String, nullable=False, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    foolder_id = Column(Integer, ForeignKey("foolders.id"), index=True)
    has_foolder = Column(Boolean, default=False)

    owner = relationship("User", back_populates="files")
    foolder = relationship("Foolder", back_populates="files")
