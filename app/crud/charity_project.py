from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name)
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def get_all_charity_project(
            self,
            session: AsyncSession,
            fully_invested: Optional[bool] = None,
    ) -> Optional[list[CharityProject]]:
        select_stmt = select(CharityProject)
        select_stmt = select_stmt.where(
            CharityProject.fully_invested == fully_invested
        )
        charity_project = await session.execute(select_stmt)
        return charity_project.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)
