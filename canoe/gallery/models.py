from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped

from canoe.extensions import db


class Work(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(256))
    created: Mapped[str] = mapped_column(String(256))
    description: Mapped[str] = mapped_column(String(1000))
    image: Mapped[str] = mapped_column(String(256))
