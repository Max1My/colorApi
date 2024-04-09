from loguru import logger
from sqlalchemy import select, delete
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import joinedload

from src.common.base import BaseRepository
from src.core.domain.colors import dto
from src.core.domain.colors.models import Color
from src.core.domain.palettes.models import Palette


class ColorRepository(BaseRepository):
    database_model = Color
    view_model = dto.ColorView

    def __init__(self):
        super().__init__()
        self.base_stmt = self.__base_stmt()

    def __base_stmt(self):
        stmt = (
            select(self.database_model)
            .options(
                joinedload(self.database_model.palette).joinedload(Palette.user)
            )
        )
        return stmt

    async def create(self, data: dto.ColorCreate):
        async with self.session() as session:
            async with session.begin():
                model = self._pydantic_to_model(data, self.database_model())
                session.add(model)
                await session.commit()
            await session.refresh(model)
            return model

    async def get_all(self, palette_id: int) -> list[dto.ColorView]:
        async with self.session() as session:
            async with session.begin():
                stmt = (
                    self.base_stmt
                    .where(self.database_model.palette_id == palette_id)
                )
                items = (await session.scalars(stmt)).unique().all()
                if items:
                    return [self._model_to_pydantic(item, self.view_model) for item in items]

    async def get_by_id(self, color_id: int) -> dto.ColorView:
        async with self.session() as session:
            async with session.begin():
                stmt = (
                    self.base_stmt
                    .where(self.database_model.id == color_id)
                )
                item = (await session.scalars(stmt)).unique().first()
                if item:
                    return self._model_to_pydantic(item, self.view_model)

    async def update(self, update_data: dto.ColorUpdate, color_model: dto.ColorView):
        async with self.session() as session:
            async with session.begin():
                model = self._pydantic_to_model(color_model, self.database_model())
                update_model = self._pydantic_to_model(update_data, model)
                updated_item = await session.merge(update_model)
            await session.commit()
            return updated_item

    async def delete(self, palette_id: int, color_ids: list[int]) -> bool:
        async with self.session() as session:
            async with session.begin():
                try:
                    stmt = (
                        delete(self.database_model)
                        .where(self.database_model.id.in_(color_ids))
                        .where(self.database_model.palette_id == palette_id)
                        .returning(self.database_model)
                    )
                    await session.scalars(stmt)
                    await session.commit()
                    logger.info('Цвет удален')
                    return True
                except DatabaseError as e:
                    await session.rollback()
                    logger.info(f'Ошибка при удалении цвета: {e}')
                    return False
