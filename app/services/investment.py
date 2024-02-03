from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud, donation_crud


async def project_completed(project: any, session: AsyncSession,) -> None:
    project.fully_invested = True
    project.close_date = datetime.now()
    return session


async def donation_to_the_project(
        session: AsyncSession,
) -> None:
    available_projects = await charity_project_crud.get_all_charity_project(
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
            await project_completed(project, session)

        for donat in available_donations:
            remainder_donation = (
                donat.full_amount -
                donat.invested_amount
            )
            if under_funding_project >= remainder_donation:
                project.invested_amount += remainder_donation
                donat.invested_amount += (
                    remainder_donation
                )
                await project_completed(donat, session)
                if project.invested_amount == project.full_amount:
                    await project_completed(project, session)
            else:
                project.invested_amount += under_funding_project
                await project_completed(project, session)
                donat.invested_amount += under_funding_project
            session.add(project)
            session.add(donat)
    await session.commit()
    return session
