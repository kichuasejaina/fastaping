import json

from fastapi import FastAPI, APIRouter, Depends,HTTPException
from fastapi.responses import Response
import uvicorn
from routers import login_router, response_router
from app.app_setup import app_initiated
from middlewars.response_time import add_process_time_header
from utils.session_utils import get_user_from_request, is_authenticated
from models import Users
from typing import Union
from utils.session_utils import custom_http_exception_handler,NoLOggedIn
app = app_initiated

no_auth_routes = APIRouter(
    prefix='/anon',
    tags=['no_auth']
)

auth_routes = APIRouter(
    prefix='/authed',
    tags=['auth']
)


@no_auth_routes.get('/test')
def test_no_auth():
    """Sample NoAuth endpoint"""
    return {'msg': 'hello'}


@auth_routes.get('/test')
def test_auth(user: Union[Users, None] = Depends(get_user_from_request)):
    """Sample Auth endpoint"""
    return Response(json.dumps({'msg': f'hello {user.first_name if user is not None else ""}!!'}), status_code=200,
                        media_type='application/json')


app.include_router(auth_routes)
app.include_router(no_auth_routes)
app.include_router(login_router)
app.include_router(response_router)
app.middleware('http')(add_process_time_header)
# app.exception_handler(HTTPException)(custom_http_exception_handler)

if __name__ == '__main__':
    uvicorn.run(app='webapp:app', host='0.0.0.0', port=8081, reload=True)
