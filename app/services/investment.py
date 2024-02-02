from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud


async def direction_fully(direction: any, session: AsyncSession,) -> None:
    direction.fully_invested = True
    direction.close_date = datetime.now()
    return session


async def placement_of_donations_by_projects(
        session: AsyncSession,
) -> None:
    open_projects = await charity_project_crud.get_all_charity_project(
        session=session,
        fully_invested=False
    )
    open_donations = await donation_crud.get_all_donations(
        session=session,
        fully_invested=False
    )
    for project in open_projects:
        uncovered_part_project = (
            project.full_amount - project.invested_amount
        )
        if uncovered_part_project == 0:
            await direction_fully(project, session)
        for ind in range(len(open_donations)):
            unallocated_part_donation = (
                open_donations[ind].full_amount -
                open_donations[ind].invested_amount
            )
            if uncovered_part_project >= unallocated_part_donation:
                project.invested_amount += unallocated_part_donation
                open_donations[ind].invested_amount += (
                    unallocated_part_donation
                )
                await direction_fully(open_donations[ind], session)
                if project.invested_amount == project.full_amount:
                    await direction_fully(project, session)
            else:
                project.invested_amount += uncovered_part_project
                await direction_fully(project, session)
                open_donations[ind].invested_amount += uncovered_part_project
            session.add(project)
            session.add(open_donations[ind])
    await session.commit()
    return session
