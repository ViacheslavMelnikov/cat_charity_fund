from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charityproject_crud
from app.models import CharityProject
from app.schemas.charityproject import CharityProjectUpdate
from http import HTTPStatus


async def check_name_duplicate(
        charityproject_name: str,
        session: AsyncSession,
) -> None:
    charityproject_id = await charityproject_crud.get_project_id_by_name(charityproject_name, session)
    if charityproject_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )

        
async def check_charityproject_exists(
        charityproject_id: int,
        session: AsyncSession,
) -> CharityProject:
    charityproject = await charityproject_crud.get(charityproject_id, session)
    if charityproject is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return charityproject


def check_data_charityproject(
        project: CharityProjectUpdate) -> None:
    keys = ['description', 'full_amount', 'name']
    if (
        not set(keys).issubset(list(project.dict())) or
        '' in project.dict().values()
    ):
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY.value,
            detail='Проверка данных не пройдена!')
    return


async def check_charityproject_for_deletion(
        charityproject_id: int,
        session: AsyncSession,
) -> CharityProject:
    charityproject = await charityproject_crud.get(
        charityproject_id, session
    )
    if charityproject.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST.value,
            detail=('Удаляет проект. Нельзя удалить проект, в который уже' +
                    'были инвестированы средства, его можно только закрыть.')
        )
    return charityproject


async def check_charityproject_full_amount(
        charityproject_id: int,
        full_amount: int,
        session: AsyncSession,
) -> CharityProject:
    charityproject = await charityproject_crud.get(
        charityproject_id, session
    )
    if charityproject.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST.value,
            detail='Закрытый проект нельзя редактировать!'
        )
    if full_amount and charityproject.invested_amount > full_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST.value,
            detail='Нельзя установить требуемую сумму меньше уже вложенной.!'
        )
    return charityproject