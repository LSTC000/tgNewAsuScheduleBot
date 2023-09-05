import datetime

from database.database_setup import BaseModel

from sqlalchemy import Column, BigInteger, BOOLEAN, VARCHAR, DateTime, sql, func


class UsersInfo(BaseModel):
    __tablename__ = 'users_info'

    # Telegram user id.
    user_id = Column(BigInteger, nullable=False, primary_key=True)
    # Last student name.
    student_name = Column(VARCHAR(128), nullable=True)
    # Last student schedule url.
    student_url = Column(VARCHAR(2048), nullable=True)
    # Last lecturer name.
    lecturer_name = Column(VARCHAR(128), nullable=True)
    # Last lecturer schedule url.
    lecturer_url = Column(VARCHAR(2048), nullable=True)
    # User alert.
    alert = Column(BOOLEAN, nullable=False)
    # Created user info.
    created_date = Column(DateTime(True), server_default=func.now())
    # Update user info.
    updated_date = Column(
        DateTime(True),
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        server_default=func.now()
    )

    query: sql.select
