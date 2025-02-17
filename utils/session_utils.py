import datetime

from fastapi import Request, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from models import Users, Password, Session as SessionDB
from dbconfig.dbsetup import get_db
from app.app_setup import app_initiated as app
import base64


def is_session_expired(session_id, db: Session, expiry_in_seconds=120):
    ses_obj = db.query(SessionDB).filter(SessionDB.session_id == session_id).first()
    created_at = ses_obj.created_at
    expiry = created_at + datetime.timedelta(seconds=expiry_in_seconds)
    current_time = datetime.datetime.now()
    # print(expiry, current_time)
    if current_time > expiry:
        return True

    return False


def cleanup_session(session_id, db: Session, resp: Response):
    ses_obj = db.query(SessionDB).filter(SessionDB.session_id == session_id).first()
    db.delete(ses_obj)
    db.commit()
    resp.delete_cookie('session_id')


def get_user_from_session_id(session_id, db: Session):
    ses_obj = db.query(SessionDB).filter(SessionDB.session_id == session_id).first()
    user_obj = db.query(Users).filter(Users.id == ses_obj.user_id).first()
    return user_obj


class NoLOggedIn(HTTPException):
    def __init__(self, status_code=404, detail="Please Login", cookie_clean=[]):
        super().__init__(status_code=status_code, detail=detail)
        self.cookie_Clean = cookie_clean


@app.exception_handler(NoLOggedIn)
async def custom_http_exception_handler(request, exc: NoLOggedIn):
    resp =  JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "No Login User",
            "message": exc.detail,
            "code": "InvalidLogin"
        },
    )
    for i in exc.cookie_Clean:
        resp.delete_cookie(i)
    return resp



def get_user_from_request(req: Request, resp: Response, db: Session = Depends(get_db)):
    session_id = req.cookies.get('session_id', None)
    if session_id is not None:
        if is_session_expired(session_id, db) is True:
            cleanup_session(session_id, db, resp)
            raise NoLOggedIn(status_code=404, detail="Session Expired.",cookie_clean=['session_id'])
        return get_user_from_session_id(session_id, db)
    
    if 'authorization' in req.headers.keys():
        type_of_auth = req.headers.get('authorization').split(' ')[0]
        value = req.headers.get('authorization').split(' ')[1]
        if type_of_auth.lower() == 'basic':
            userid_pass_split = base64.decodebytes(value.encode()).decode().split(":")
            user_id = userid_pass_split[0]
            passwd = ":".join(userid_pass_split[1:])
            # print(user_id, passwd)
            user_obj = db.query(Users).filter(Users.email == user_id).first()
            if user_obj is None:
                raise NoLOggedIn(status_code=404, detail="Invalid Token.")
            
            password_obj = db.query(Password).filter(Password.user_id == user_obj.id).first()
            if password_obj is None:
                raise NoLOggedIn(status_code=404, detail="Invalid Token.")
            password = password_obj.password
            if password == passwd:
                return user_obj
            raise NoLOggedIn(status_code=404, detail="Invalid Token.")
            
    raise NoLOggedIn(status_code=404, detail="Please Login")


def is_authenticated(req: Request):
    session_id = req.cookies.get('session_id', None)
    if session_id is not None:
        return True
    return False
