from typing import Any, List

from beanie import init_beanie, PydanticObjectId
from models.plant import Plants
from models.controller import Controllers
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = None

    async def initialize_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(database=client.get_default_database(),
                          document_models=[Controllers, Plants])

    class Config:
        env_file = ".env"


class Database:
    def __init__(self, model):
        self.model = model

    async def save(self, document) -> None:
        await document.create()
        return

    async def get(self, id: PydanticObjectId) -> Any:
        doc = await self.model.get(id)
        if doc:
            return doc
        return False

    async def get_all(self) -> List[Any]:
        docs = await self.model.find_all().to_list()
        return docs

    async def update(self, id: PydanticObjectId, body: BaseModel) -> Any:
        doc_id = id
        des_body = body.dict()
        print('1', des_body)

        des_body = {k: v for k, v in des_body.items() if v is not None}
        print('2', des_body)
        update_query = {"$set": {
            field: value for field, value in des_body.items()
        }}
        print('3', des_body)
        doc = await self.get(doc_id)
        print('4', doc)
        if not doc:
            return False
        await doc.update(update_query)
        return doc

    async def delete(self, id: PydanticObjectId) -> bool:
        doc = await self.get(id)
        if not doc:
            return False
        await doc.delete()
        return True

    async def all_plant_for_controller(self, id: PydanticObjectId) -> List[Any]:
        docs = await self.model.find(self.model.controller == id).to_list()
        return docs

