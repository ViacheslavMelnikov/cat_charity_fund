from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB
from app.services.investment import donation_to_the_project

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude={
        'user_id',
        'close_date',
        'invested_amount',
        'fully_invested'
    },
    response_model_exclude_none=True,
)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """
    Сделать пожертвование.
    """
    new_donation = await donation_crud.create(donation, session, user)
    await donation_to_the_project(session)
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude={
        'user_id',
        'close_date',
        'invested_amount',
        'fully_invested'
    }
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """
    Получить список моих пожертвований.
    """
    return await donation_crud.get_by_user(session=session, user=user)


@router.get(
    '/',
    response_model=list[DonationDB],
    dependencies=[Depends(current_superuser)],
    response_model_exclude={'close_date'}
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперюзеров.
    Получает список всех пожертвований.
    """
    return await donation_crud.get_multi(session)
