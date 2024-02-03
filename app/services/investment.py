from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charityproject_crud, donation_crud

async def direction_fully(direction: any, session: AsyncSession,) -> None:
    direction.fully_invested = True
    direction.close_date = datetime.now()
    return session


async def placement_of_donations_by_projects(
        session: AsyncSession,
) -> None:
    available_projects = await charityproject_crud.get_all_charity_project(
        session=session,
        fully_invested=False
    )
    available_donations = await donation_crud.get_all_donations(
        session=session,
        fully_invested=False
    )
    for project in available_projects:
        under_funding_project = (
            project.full_amount - project.invested_amount
        )
        if under_funding_project == 0:
            await direction_fully(project, session)
        for ind in range(len(available_donations)):
            remainder_donation = (
                available_donations[ind].full_amount -
                available_donations[ind].invested_amount
            )
            if under_funding_project >= remainder_donation:
                project.invested_amount += remainder_donation
                available_donations[ind].invested_amount += (
                    remainder_donation
                )
                await direction_fully(available_donations[ind], session)
                if project.invested_amount == project.full_amount:
                    await direction_fully(project, session)
            else:
                project.invested_amount += under_funding_project
                await direction_fully(project, session)
                available_donations[ind].invested_amount += under_funding_project
            session.add(project)
            session.add(available_donations[ind])
    await session.commit()
    return session
