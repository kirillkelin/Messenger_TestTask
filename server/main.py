from contextlib import asynccontextmanager

from sqlalchemy import select, insert, text, func
from fastapi import FastAPI

from server.database import create_database, drop_database, async_session
from server.messages import Messages
from server.models import Message, MessageResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_database()
    yield
    await drop_database()


app = FastAPI(lifespan=lifespan)


@app.post("/messages")
async def get_messages(message: Message):
    async with async_session() as session:
        # await session.execute(text("LOCK TABLE messages IN EXCLUSIVE MODE"))
        await session.execute(text("LOCK TABLE messages IN SHARE ROW EXCLUSIVE MODE"))
        get_last_user_message = select(func.max(Messages.message_counter)).filter_by(username=message.username)
        current_row = await session.execute(get_last_user_message)
        current_user_counter = current_row.scalar()
        if current_user_counter is None:
            current_user_counter = 0
        add_new_message = insert(Messages).values(
            username=message.username, message=message.message,
            message_counter=current_user_counter + 1
        )
        await session.execute(add_new_message)
        get_last_ten_rows = select(Messages).order_by(Messages.id.desc()).limit(10)
        result = await session.execute(get_last_ten_rows)
        await session.commit()
    return [MessageResponse.model_validate(message) for message in result.scalars().all()]
