from datetime import timedelta

from fastapi import APIRouter
from starlette import status

from src.core.domain.users import errors, requests, dto
from src.core.domain.users.service import UserService
from src.settings import ACCESS_TOKEN_EXPIRE_DAYS

user_router = APIRouter()
service = UserService()


@user_router.post(
    path='/signin',
    status_code=status.HTTP_201_CREATED,
    tags=['Пользователь'],
    name='Авторизация пользователя',
)
async def signin(
        request: requests.AuthUser
) -> dto.Token:
    if request.username and request.password:
        user_in_db = await service.authenticate(dto.AuthUser(
            username=request.username,
            password=request.password
        ))
        if not user_in_db:
            raise errors.UsersHTTPError(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Не удалось войти в личный кабинет',
                headers={'WWW-Authenticate': 'Bearer'},
            )
        access_token_expires = timedelta(days=int(ACCESS_TOKEN_EXPIRE_DAYS))
        access_token = service.create_access_token(
            data={'sub': user_in_db.username}, expires_delta=access_token_expires
        )
        return dto.Token(access_token=access_token, token_type='bearer')
    else:
        raise errors.UsersHTTPError(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Обязательные поля должны быть заполнены: email, пароль'
        )


@user_router.post(
    path='/register',
    status_code=status.HTTP_200_OK,
    tags=['Пользователь'],
    name='Регистрация пользователя'
)
async def register_user(
        request: requests.RegisterUser,
):
    user = await service.register(request)
    if not user:
        raise errors.UsersHTTPError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Не удалось зарегистрироваться',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(days=int(ACCESS_TOKEN_EXPIRE_DAYS))
    access_token = service.create_access_token(
        data={'sub': user.username}, expires_delta=access_token_expires
    )
    return dto.Token(access_token=access_token, token_type='bearer')
