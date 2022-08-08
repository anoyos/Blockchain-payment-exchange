from typing import Optional

from api_contrib.crud.base_mongo import CRUDBaseMongo
from bson.objectid import ObjectId
from pydantic import EmailStr

from app.core.security import get_password_hash
from app.core.security import verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserInDb


class CRUDUser(CRUDBaseMongo):
    async def get_by_email(self, email: EmailStr) -> Optional[UserInDb]:
        return await self.find_one({"email": email})

    async def create(self, obj_in: UserCreate) -> UserInDb:
        pwd_hash = get_password_hash(obj_in.password)
        db_obj = User(
            password_hash=pwd_hash,
            **obj_in.dict()
        )
        db_id = await self.insert_one(db_obj)
        return UserInDb(id=db_id, password_hash=pwd_hash, **obj_in.dict())

    async def authenticate(self, username: str, password: str) -> Optional[User]:
        user = await self.find_one({"username": username})
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    async def find_one(self, query: dict) -> Optional[UserInDb]:
        row = await self.collection.find_one(self.cast_id(query))
        if row:
            row['id'] = str(row.pop('_id'))
            return UserInDb(**row)
        else:
            return None

    async def count(self):
        return await self.collection.count_documents({})

    @staticmethod
    def is_active(user: User) -> bool:
        return user.is_active

    async def update(self, obj: UserInDb, values: dict):
        await self.collection.update_one({'_id': ObjectId(obj.id)},
                                         {'$set': values})
