import databases
import sqlalchemy

from config import config
metadata = sqlalchemy.MetaData()
user_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_name", sqlalchemy.String(50)),
    sqlalchemy.Column("mobile_no", sqlalchemy.String(11)),
    sqlalchemy.Column("email_id", sqlalchemy.String(50), unique=True),
    sqlalchemy.Column("password", sqlalchemy.String(50)),
    sqlalchemy.Column("is_active", sqlalchemy.Boolean, default=False),

)
engine = sqlalchemy.create_engine(
    config.DATABASE_URL,
)


metadata.create_all(engine)

# Use correct case for the force rollback variable
database = databases.Database(
    config.DATABASE_URL, force_rollback=config.DB_FORCE_ROLL_BACK
)

# Example async function to connect and interact with the database
async def example_db_operation():
    await database.connect()
    query = user_table.insert().values(
        user_name="John Doe", mobile_no="1234567890", email_id="john.doe@example.com", password="password", is_active=True
    )
    await database.execute(query)
    await database.disconnect()
import asyncio
asyncio.run(example_db_operation())