from typing import List, Optional
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, func
import datetime

positions = ['CEO','Manager','Team Lead','Senior Developer','Developer']

db = SQLAlchemy()

class Employee(db.Model):
    __tablename__ = "employee"
    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(nullable=False)
    position: Mapped[str] = mapped_column(nullable=False)                                       # из списка positions
    date: Mapped[datetime.datetime] = mapped_column(nullable=False)
    salary: Mapped[float] = mapped_column(nullable=False)
    manager_id: Mapped[Optional[int]] = mapped_column(ForeignKey("employee.id", ondelete="SET NULL"), nullable=True)

    manager: Mapped["Employee"] = relationship(
        "Employee",
        backref="subordinates",
        foreign_keys=[manager_id],
        remote_side=[id],
        lazy='joined',
        )