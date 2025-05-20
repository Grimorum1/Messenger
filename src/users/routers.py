from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession



from db.db_setup import db_helper as db_base
from . import service, schemas

router = APIRouter(prefix="/users", tags=["Users"])



@router.post("/")
async def add_user(
        user: schemas.UserCreate,
        session: AsyncSession = Depends(db_base.scoped_session_dependency),):
    return service.create_users(user=user, session=session)



@router.get("/", response_model=list[schemas.UserBase])
async def get_users(
    session: AsyncSession = Depends(db_base.scoped_session_dependency),
):
    return await service.get_users(session=session)



@router.get("/{user_id}/", response_model=schemas.UserBase)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(db_base.scoped_session_dependency),
):
    user = await get_user(session=session, user_id=user_id)
    if user:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {user_id} not found!",
    )

