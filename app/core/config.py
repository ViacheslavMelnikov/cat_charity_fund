from pydantic import BaseSettings, EmailStr
from typing import Optional
import logging


class Settings(BaseSettings):
    app_title: str = 'Благотворительный фонд поддержки котиков'
    app_description: str = (
        'Фонд собирает пожертвования на различные целевые проекты:' +
        'на медицинское обслуживание нуждающихся хвостатых,' +
        'на обустройство кошачьей колонии в подвале, на корм' +
        'оставшимся без попечения кошкам — на любые цели,'
        'связанные с поддержкой кошачьей популяции.')
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    logging.basicConfig(level=logging.INFO)

    class Config:
        env_file = '.env'
        

settings = Settings()
