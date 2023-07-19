import os
from typing import Optional, List, Union

from bson import ObjectId
from fastapi import FastAPI, status, Query, HTTPException, Header, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from .db import db, PyObjectId


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    username: str = Field(
        ...,
        regex='^(?![0-9._])(?!.*[._]$)(?!.*\d_)(?!.*_\d)[a-z0-9_]+$',
        description='Allow only alphabetic eng character & number endswith.'
    )
    firstname: Optional[str] = None
    lastname: Optional[str] = None

    class Config:
        json_encoders = {ObjectId: str}
        validate_assignment = True
        schema_extra = {
            'example': {
                'username': 'dev',
                'firstname': 'watcharapon',
                'lastname': 'weeraborirak'
            }
        }


class ResponseUser(BaseModel):
    id: Union[str, None] = Field(None, alias='_id')
    username: str
    firstname: Optional[str] = None
    lastname: Optional[str] = None


class UpdatedUser(BaseModel):
    username: str = Field(
        ...,
        regex='^(?![0-9._])(?!.*[._]$)(?!.*\d_)(?!.*_\d)[a-z0-9_]+$',
        description='Allow only alphabetic eng character & number endswith.'
    )
    firstname: Optional[str] = None
    lastname: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            'example': {
                'username': 'dev',
                'firstname': 'watcharapon',
                'lastname': 'weeraborirak'
            }
        }


class FindUsers(BaseModel):
    counts: int
    skip: int
    limit: int
    users: List[Union[ResponseUser, None]] = []


app = FastAPI()
collection = 'users'


async def x_token_auth(user_agent: str = Header(...)):
    if user_agent != os.environ['USER_AGENT']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Header is not valid.')
    return user_agent


async def check_duplicate(payload: User, user_agent=Depends(x_token_auth)):
    if await db.find_one(collection=collection, query={'username': payload.username}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username already exist.')
    return payload


async def evaluate_duplicate_account_update(payload: ResponseUser, user_agent=Depends(x_token_auth)):
    if user := await db.find_one(collection=collection, query={'username': payload.username}):
        if user['_id'] == payload.id:
            return payload
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username already exist.')
    return payload


@app.get('/user/find', status_code=status.HTTP_200_OK, response_model=FindUsers)
async def find_users(
        user_agent=Depends(x_token_auth),
        skip: Union[int, None] = Query(default=0,
                                       title='Skip or start items in collection', ge=0),
        limit: Union[int, None] = Query(default=10,
                                        title='Limit or end items in collection', ge=1),
):
    total_count = db.get_collection_countable(collection=collection)
    users = await db.find(collection=collection, query={})
    stored_model = users.skip(skip).limit(limit)
    stored_model = list(stored_model)
    result = {
        'counts': total_count,
        'skip': skip,
        'limit': limit,
        'users': stored_model
    }
    if not stored_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found item.')
    return result


@app.get('/user/find/{id}', status_code=status.HTTP_200_OK, response_model=User)
async def find_one_user(
        id: str,
        user_agent=Depends(x_token_auth)
):
    user = await db.find_one(collection=collection, query={'_id': id})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found item.')
    return user


@app.post('/user/create', response_model=User, status_code=status.HTTP_201_CREATED)
async def user_create(
        user: User = Depends(check_duplicate),
):
    store_model = jsonable_encoder(user)
    await db.insert_one(collection=collection, data=store_model)
    return store_model


@app.put('/user/update/{id}',
         response_model=UpdatedUser,
         status_code=status.HTTP_200_OK)
async def update_user(id: str,
                      user: UpdatedUser,
                      user_agent=Depends(x_token_auth)):
    item_model = jsonable_encoder(user)
    query = {'_id': id}
    values = {'$set': item_model}
    if (await db.update_one(
            collection=collection,
            query=query,
            values=values)) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Not found {id} or update already exits.')
    return item_model


@app.delete('/user/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def purge_intermediate_level(
        id: str,
        user_agent=Depends(x_token_auth)
):
    if (await db.delete_one(collection=collection, query={'_id': id})) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"course is not found {id}."
        )
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={'status': 'success'})
