# Импортируем класс Depends.
from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charityproject import  charityproject_crud
from app.schemas.charityproject import (CharityProjectCreate, CharityProjectDB, CharityProjectUpdate)
# from app.schemas.charityproject import (
#     MeetingRoomCreate, MeetingRoomDB, MeetingRoomUpdate
# )

# Импортируем модель, чтобы указать её в аннотации.
from app.models.charityproject import CharityProject

from app.api.validators import check_name_duplicate, check_charityproject_exists

# from app.crud.donation import reservation_crud
# from app.schemas.reservation import ReservationDB

from app.core.user import current_superuser

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charityproject(
        charityproject: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    # Выносим проверку дубликата имени в отдельную корутину.
    # Если такое имя уже существует, то будет вызвана ошибка HTTPException
    # и обработка запроса остановится.
    await check_name_duplicate(charityproject.name, session)
    charityproject = await charityproject_crud.create(charityproject, session)
    return charityproject


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charityprojects(
        session: AsyncSession = Depends(get_async_session),
):
    all_charityproject = await charityproject_crud.get_multi(session)
    return all_charityproject


@router.patch(
    # ID обновляемого объекта будет передаваться path-параметром.
    '/{charityproject_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charityproject(
        charityproject_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    charityproject = await check_charityproject_exists(
        charityproject_id, session
    )

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    charityproject = await charityproject_crud.update(
        charityproject, obj_in, session
    )
    return charityproject
    

@router.delete(
    '/{charityproject_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_charityproject(
        charityproject_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    charityproject = await check_charityproject_exists(
        charityproject_id, session
    )
    charityproject = await charityproject_crud.remove(charityproject, session)
    return charityproject
