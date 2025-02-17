import json

from fastapi import APIRouter, Depends, Request
from fastapi.responses import Response
from pydantic import BaseModel
from models import Users, Password
from dbconfig.dbsetup import get_db
from sqlalchemy.orm import Session
from models import Session as SessionDB
import datetime


class LoginBody(BaseModel):
    username: str
    password: str


class SuccessResponse(BaseModel):
    status_code: int = 201
    msg: str


class ErrorResponse(BaseModel):
    status_code: int = 404
    msg: str


class SignUpBody(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


login_router = APIRouter()


@login_router.post('/login', responses={
    201: {'model': SuccessResponse},
    404: {'model': ErrorResponse},
}, status_code=201, tags=['login'])
def login(body: LoginBody, db: Session = Depends(get_db)):
    user_email = body.username
    user_pass = body.password
    user = db.query(Users).filter(Users.email == user_email).all()
    if len(user) == 0:
        resp = ErrorResponse(msg="Invalid User")
        return Response(resp.json(), status_code=404, media_type='application/json')

    user = user[0]
    # print(user)
    password = db.query(Password).filter(Password.user_id == user.id).first()

    if password.password != user_pass:
        resp = ErrorResponse(msg="Invalid Password")
        return Response(resp.json(), status_code=404, media_type='application/json')
    ses_db = SessionDB(user_id=user.id, created_at=datetime.datetime.now())
    db.add(ses_db)
    db.commit()

    resp = SuccessResponse(msg="Login Successful")
    response = Response(resp.json(), status_code=201, media_type='application/json')

    response.set_cookie('session_id', ses_db.session_id)
    return response


@login_router.post('/signup', tags=['signup', 'login'])
def signup(body: SignUpBody, db: Session = Depends(get_db)):
    user = Users(email=body.email, first_name=body.first_name, last_name=body.last_name)
    db.add(user)
    db.commit()

    pwd_data = Password(user_id=user.id, password=body.password)
    db.add(pwd_data)
    db.commit()

    return body

@login_router.post('/logout', tags=['logout', 'signout'])
def logout(req: Request, resp: Response, db: Session = Depends(get_db)):
    session_id = req.cookies.get('session_id',None)
    if session_id is not None:
        ses_obj = db.query(SessionDB).filter(SessionDB.session_id == session_id).first()
        db.delete(ses_obj)
        db.commit()

    resp = SuccessResponse(msg="Logout Successful")
    response = Response(resp.json(), status_code=201, media_type='application/json')
    response.delete_cookie('session_id')
    return response
