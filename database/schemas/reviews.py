from database.database_setup import BaseModel

from sqlalchemy import Column, BigInteger, VARCHAR, DateTime, sql, func


class Reviews(BaseModel):
    __tablename__ = 'reviews'

    # Autoincrement id.
    id = Column(BigInteger, primary_key=True, autoincrement=True,
                server_default=sql.text('nextval(\'reviews_id_seq\')'))
    # Telegram user id.
    user_id = Column(BigInteger, nullable=False)
    # User review.
    review = Column(VARCHAR(2048), nullable=False)
    # Created review date.
    created_date = Column(DateTime(True), server_default=func.now())

    query: sql.select
