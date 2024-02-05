from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST.value,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return charity_project


def check_data_charity_project(
        project: CharityProjectUpdate) -> None:
    keys = ['description', 'full_amount', 'name']
    for key in keys:
        if key not in list(project.dict()) or project.dict()[key] == '':
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY.value,
                detail='Проверка данных не пройдена!')
    return


async def check_charity_project_for_deletion(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        charity_project_id, session
    )
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST.value,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return charity_project


async def check_charity_project_full_amount(
        charity_project_id: int,
        full_amount: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        charity_project_id, session
    )
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST.value,
            detail='Закрытый проект нельзя редактировать!'
        )
    if full_amount and charity_project.invested_amount > full_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST.value,
            detail='Нельзя установить требуемую сумму меньше уже вложенной.!'
        )
    return charity_project
