# pylint: disable=E0611,E0401
from typing import List

from fastapi import FastAPI, status, APIRouter
from pydantic import BaseModel
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DoesNotExist

# from models import User, UserSchema, InUserSchema

from tortoise_orm.models import User, UserSchema, InUserSchema

app = FastAPI(title="Tortoise ORM FastAPI example")


class Status(BaseModel):
    message: str


users_router = APIRouter()


@users_router.post("", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user: InUserSchema):
    user_obj = await User.create(**user.dict(exclude_unset=True))
    return await UserSchema.from_tortoise_orm(user_obj)


@users_router.get("", response_model=List[UserSchema])
async def get_users():
    return await UserSchema.from_queryset(User.all())


@users_router.get("/{user_id}", response_model=UserSchema)
async def get_user(user_id: int):
    return await UserSchema.from_queryset_single(User.get(id=user_id))


@users_router.put(
    "/{user_id}", response_model=UserSchema, status_code=status.HTTP_202_ACCEPTED
)
async def update_user(user_id: int, user: InUserSchema):
    await User.filter(id=user_id).update(**user.dict(exclude_unset=True))
    return await UserSchema.from_queryset_single(User.get(id=user_id))


@users_router.delete(
    "/{user_id}", response_model=Status, status_code=status.HTTP_202_ACCEPTED
)
async def delete_user(user_id: int):
    deleted_count = await User.filter(id=user_id).delete()
    if not deleted_count:
        raise DoesNotExist(f'User with id: "{user_id}" does not exist')
    return Status(message=f"Deleted user {user_id}")


app.include_router(users_router, prefix="/users", tags=["Users"])


register_tortoise(
    app,
    db_url="sqlite://:memory:",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
