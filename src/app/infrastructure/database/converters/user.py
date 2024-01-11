from dataclasses import fields

from src.app.application.user import dto
from src.app.infrastructure.database.models.user import User as UserModel


def convert_db_model_to_user_dto(user_model: UserModel) -> dto.User:
    return dto.User(
        id=user_model.id,
        nickname=user_model.nickname,
        fullname=user_model.fullname,
        email=user_model.email,
        photo_path=user_model.photo_path,
        reputation=user_model.reputation,
    )


def convert_user_dto_to_db_model(user_dto: dto.User) -> UserModel:
    return UserModel(
        id=user_dto.id,
        nickname=user_dto.nickname,
        fullname=user_dto.fullname,
        email=user_dto.email,
        photo_path=user_dto.photo_path,
        reputation=user_dto.reputation,
    )


def convert_user_create_dto_to_db_model(user_dto: dto.UserCreate) -> UserModel:
    return UserModel(
        nickname=user_dto.nickname,
        fullname=user_dto.fullname,
        email=user_dto.email,
        password=user_dto.password,
    )


def update_user_fields(
        existing_user: dto.User, user_update_dto: dto.UserUpdate,
) -> UserModel:
    result_model = UserModel()
    for field in fields(existing_user):
        existing_field_value = getattr(existing_user, field.name)

        if hasattr(user_update_dto, field.name):
            new_value = getattr(user_update_dto, field.name)
        else:
            new_value = None

        settable_value = new_value if new_value is not None else existing_field_value
        setattr(result_model, field.name, settable_value)
    return result_model
