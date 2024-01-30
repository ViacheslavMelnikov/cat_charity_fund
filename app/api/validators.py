# app/api/validators.py
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charityproject_crud
# from app.crud.donation import reservation_crud
from app.models import CharityProject, Donation, User

# from app.crud.donation import reservation_crud


async def check_name_duplicate(
        charityproject_name: str,
        session: AsyncSession,
) -> None:
    charityproject_id = await charityproject_crud.get_project_id_by_name(charityproject_name, session)
    if charityproject_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Проект с таким именем уже существует!',
        )

        
async def check_charityproject_exists(
        charityproject_id: int,
        session: AsyncSession,
) -> CharityProject:
    charityproject = await charityproject_crud.get(charityproject_id, session)
    if charityproject is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return charityproject


# async def check_reservation_intersections(**kwargs) -> None:
#     reservations = await reservation_crud.get_reservations_at_the_same_time(
#         **kwargs
#     )
#     if reservations:
#         raise HTTPException(
#             status_code=422,
#             detail=str(reservations)
#         ) 
    

# async def check_reservation_before_edit(
#         reservation_id: int,
#         session: AsyncSession,
#         # Новый параметр корутины.
#         user: User,
# ) -> Reservation:
#     reservation = await reservation_crud.get(
#         obj_id=reservation_id, session=session
#     )
#     if not reservation:
#         raise HTTPException(status_code=404, detail='Бронь не найдена!')
#     # Новая проверка и вызов исключения.
#     if reservation.user_id != user.id and not user.is_superuser:
#         raise HTTPException(
#             status_code=403,
#             detail='Невозможно редактировать или удалить чужую бронь!'
#         )
#     return reservation  