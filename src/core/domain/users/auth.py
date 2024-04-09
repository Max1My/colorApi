from fastapi import Depends
from starlette.requests import Request

from src.core.domain.users.service import oauth2_scheme, UserService
from . import dto


class Auth:
    def __init__(
            self
    ):
        super().__init__()

    async def __call__(
            self,
            request: Request,
            token: str = Depends(oauth2_scheme),
            service: UserService = Depends(),
    ) -> dto.UserView:
        user = await service.get_user(token)
        return user
