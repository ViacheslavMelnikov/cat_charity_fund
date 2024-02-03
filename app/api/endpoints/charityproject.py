from fastapi import APIRouter, Depends #+

from sqlalchemy.ext.asyncio import AsyncSession #*

from app.core.db import get_async_session
from app.crud.charityproject import  charityproject_crud
from app.schemas.charityproject import (CharityProjectCreate, CharityProjectDB, CharityProjectUpdate)

from app.models.charityproject import CharityProject

from app.api.validators import (
    check_name_duplicate,
    check_charityproject_exists,
    check_data_charityproject,
    check_charityproject_full_amount,
    check_charityproject_for_deletion) #+

# from app.crud.donation import reservation_crud
# from app.schemas.reservation import ReservationDB

from app.core.user import current_superuser

from app.services.investment import donation_to_the_project


router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charityproject(
        charityproject: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)):
    await check_name_duplicate(charityproject.name, session)
    charityproject = await charityproject_crud.create(charityproject, session)
    await donation_to_the_project(session)
    await session.refresh(charityproject)
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
    '/{charityproject_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charityproject(
        charityproject_id: int,
        object_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session)):
    
    check_data_charityproject(object_in)

    charityproject = await check_charityproject_exists(
        charityproject_id, session
    )

    if object_in.name is not None:
        await check_name_duplicate(object_in.name, session)

    charityproject = await check_charityproject_full_amount(
        charityproject_id, object_in.full_amount, session)

    charityproject = await charityproject_crud.update(
        charityproject, object_in, session
    )

    await donation_to_the_project(session)
    await session.refresh(charityproject)
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
