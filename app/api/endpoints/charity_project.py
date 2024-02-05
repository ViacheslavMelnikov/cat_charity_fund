from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_exists,
                                check_charity_project_for_deletion,
                                check_charity_project_full_amount,
                                check_data_charity_project,
                                check_name_duplicate)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investment import donation_to_the_project

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперпользователей. Создает благотворительный проект.
    """
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(
        charity_project, session
    )
    await donation_to_the_project(session)
    await session.refresh(new_project)
    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    """
    Получает список всех проектов.
    """
    return await charity_project_crud.get_multi(session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        project_id: int,
        object_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.
    Закрытый проект нельзя редактировать,
    также нельзя установить требуемую сумму меньше уже вложенной.
    """
    check_data_charity_project(object_in)

    charity_project = await check_charity_project_exists(
        project_id, session
    )

    if object_in.name is not None:
        await check_name_duplicate(object_in.name, session)

    charity_project = await check_charity_project_full_amount(
        project_id, object_in.full_amount, session
    )
    charity_project = await charity_project_crud.update(
        charity_project, object_in, session
    )
    await donation_to_the_project(session)
    await session.refresh(charity_project)
    return charity_project


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
        charity_project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров. Удаляет проект.
    Нельзя удалить проект, в который уже были инвестированы средства,
    его можно только закрыть.
    """
    charity_project = await check_charity_project_for_deletion(
        charity_project_id, session
    )
    return await charity_project_crud.remove(charity_project, session)
