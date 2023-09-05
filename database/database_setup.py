from typing import List

from loader import db, logger

from data.config import PG_URL

import sqlalchemy as sa


class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)  # Inspect the class using SQLAlchemy.
        primary_key_columns: List[sa.Column] = table.primary_key.columns  # Get primary key columns.
        values = {
            column.name: getattr(self, self._column_name_map[column.name])  # Get attribute values.
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())  # Create a string representation.
        return f"<{model} {values_str}>"


async def startup_setup():
    await db.set_bind(PG_URL)  # Connect to the database using the URL.
    # await db.gino.drop_all()  # Drop all tables.
    await db.gino.create_all()  # Create all tables.


async def shutdown_setup():
    bind = db.pop_bind()  # Remove the database bind.
    if bind:
        logger.info("Close!")  # Log that the connection is being closed.
        await bind.close()  # Close the connection.
