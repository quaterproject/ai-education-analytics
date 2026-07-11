from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

def format_async_pg_url(url: str) -> str:
    if not url.startswith("postgresql"):
        return url
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
    
    parsed = urlparse(url)
    qsl = parse_qsl(parsed.query)
    
    new_qsl = []
    for k, v in qsl:
        if k == "sslmode":
            new_qsl.append(("ssl", "require"))
        elif k == "channel_binding":
            continue
        else:
            new_qsl.append((k, v))
            
    new_query = urlencode(new_qsl)
    parsed = parsed._replace(query=new_query)
    return urlunparse(parsed)

# Setup Async Engine
db_url = format_async_pg_url(settings.DATABASE_URL)

connect_args = {}
if db_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_async_engine(
    db_url,
    connect_args=connect_args,
    echo=settings.APP_ENV == "development" and settings.DEBUG
)

# Async Session Factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

# Declarative Base
class Base(DeclarativeBase):
    pass

# Dependency Injection for DB Sessions
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
