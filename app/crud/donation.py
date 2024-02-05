from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):
    async def get_all_donations(
            self,
            session: AsyncSession,
            fully_invested: Optional[bool] = None,
    ) -> list[Donation]:
        select_donation = select(Donation)
        select_donation = select_donation.where(Donation.fully_invested == fully_invested)
        donations = await session.execute(select_donation)
        return donations.scalars().all()

    async def get_by_user(
            self,
            session: AsyncSession,
            user: User
    ) -> list[Donation]:
        donations = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
