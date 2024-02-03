from fastapi import APIRouter

from app.api.endpoints import charityproject_router, user_router

# from app.api.endpoints import (
#     meeting_room_router, reservation_router, user_router
# )

main_router = APIRouter()
main_router.include_router(
    charityproject_router, prefix='/charityprojects', tags=['Charity Projects']
)
# main_router.include_router(
#     reservation_router, prefix='/reservations', tags=['Reservations']
# )
main_router.include_router(user_router)