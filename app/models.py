from sqlalchemy import Column, Integer, String, Float, Boolean

from app.database import Base


class Posts(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="True", nullable=False)
    rating = Column(Float, nullable=False)
