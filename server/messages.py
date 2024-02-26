from datetime import datetime

from sqlalchemy import text
from sqlalchemy.orm import mapped_column, Mapped

from server.database import Base


class Messages(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(index=True)
    message: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    message_counter: Mapped[int] = mapped_column()
