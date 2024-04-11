from fastapi import FastAPI, Request, Depends, HTTPException, Cookie, UploadFile, File, Body
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import Response, JSONResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from hashlib import sha3_256
from typing import List

from .controllers.controller import *
from .send_otp import send_otp_email, is_otp_valid
from .send_telegram_message import sendMessageTelegram, admin_chat_id

import os
import jwt
import datetime
import pandas as pd
import zipfile
import shutil
import asyncio
import json

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
app.mount("/dist", StaticFiles(directory=os.path.join(os.getcwd(),
          "app", "templates", "dist")), name="dist")
app.mount("/plugins", StaticFiles(directory=os.path.join(os.getcwd(),
          "app", "templates", "plugins")), name="plugins")

templates = Jinja2Templates(
    directory=os.path.join(os.getcwd(), "app", "templates"))


class UserCredentials(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class DanhGiaSVByID(BaseModel):
    id: str
    ythuckyluat_number: float
    ythuckyluat_text: str
    tuanthuthoigian_number: float
    tuanthuthoigian_text: str
    kienthuc_number: float
    kienthuc_text: str
    kynangnghe_number: float
    kynangnghe_text: str
    khanangdoclap_number: float
    khanangdoclap_text: str
    khanangnhom_number: float
    khanangnhom_text: str
    khananggiaiquyetcongviec_number: float
    khananggiaiquyetcongviec_text: str
    danhgiachung_number: float


class ThongTinSV(BaseModel):
    mssv: str
    hoten: str
    gioitinh: int
    sdt: str
    email: str
    diachi: str
    malop: str
    truong: int
    nganh: int
    khoa: int


class ChiTietCongViec(BaseModel):
    id_congviec: int
    ghichu: str
    sinhvien: List[str]


SECRET_KEY = secret_key
ALGORITHM = algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = 60*3
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_user_route(credentials: UserCredentials):
    if '@' in credentials.username:
        id = verify_student_controller(email=credentials.username, password=sha3_256(
            bytes(credentials.password, 'utf-8')).hexdigest())
        if id:
            return {"isVerified": True, "permission": "student", "id": int(id)}
    else:
        id = verify_user_controller(username=credentials.username, password=sha3_256(
            bytes(credentials.password, 'utf-8')).hexdigest())
        if id:
            return {"isVerified": True, "permission": get_phan_quyen_controller(credentials.username), "id": int(id)}


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    return username

# Middleware để bắt lỗi 404 và xử lý


@app.middleware("http")
async def catch_404(request, call_next):
    response = await call_next(request)
    if response.status_code == 404:
        return templates.TemplateResponse('404.html', context={'request': request})
    return response


@app.post("/token", response_model=Token)
async def login_for_access_token(credentials: UserCredentials):
    result = verify_user_route(credentials)
    if result['isVerified']:
        access_token_expires = datetime.timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": credentials.username, "permission": result['permission'], "id": result['id']}, expires_delta=access_token_expires)
        response = JSONResponse(
            {"access_token": access_token, "token_type": "bearer"})
        response.set_cookie("token", access_token, httponly=False)
        response.set_cookie("username", credentials.username, httponly=False)
        return response
    raise HTTPException(
        status_code=400, detail="Incorrect username or password")


def create_access_token(data: dict, expires_delta: datetime.timedelta):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.get("/logout")
async def logout(token: str = Cookie(None)):
    response = RedirectResponse('/login')
    response.delete_cookie("token")
    response.delete_cookie("email")
    response.delete_cookie("username")
    return response


@app.get('/')
async def home(request: Request, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                tong_sinh_vien: int = count_all_sinh_vien_controller()
                ti_le_da_danh_gia: float = ti_le_sinh_vien_da_danh_gia_controller()
                so_luong_ket_qua: int = so_luong_sinh_vien_dat_ket_qua_controller()
                return templates.TemplateResponse('index.html', context={'request': request, 'dashboard_tongsinhvien': tong_sinh_vien, 'dashboard_tiledadanhgia': ti_le_da_danh_gia, 'dashboard_soluongdat': so_luong_ket_qua['dat'], 'dashboard_soluongkhongdat': so_luong_ket_qua['khong_co_nhom']})
            else:
                return RedirectResponse('/sinhvien')
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/login')
async def login(request: Request, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                return RedirectResponse(url='/')
            else:
                return RedirectResponse('/sinhvien')
        except jwt.PyJWTError:
            return templates.TemplateResponse('login.html', context={'request': request})
    else:
        return templates.TemplateResponse('login.html', context={'request': request})


@app.get('/dangky')
async def nhap_thong_tin_sinh_vien(request: Request):
    return templates.TemplateResponse('student.html', context={'request': request})


@app.get('/hosonguoihuongdan')
async def hosonguoihuongdan(request: Request, id: str):
    result = get_user_info_by_username(id)
    profile = {'hoten': result[0], 'sdt': result[1], 'email': result[2], 'chucdanh': result[3],
               'phong': result[4], 'zalo': result[5], 'facebook': result[6], 'github': result[7], 'avatar': result[8]}
    return templates.TemplateResponse('profile.html', context={'request': request, 'profile': profile})


@app.get('/danhgiasinhvien')
async def danhgiasinhvien(request: Request, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                return templates.TemplateResponse('student_review.html', context={'request': request})

        except jwt.PyJWTError:
            return templates.TemplateResponse('login.html', context={'request': request})
    return RedirectResponse('/login')


@app.get('/giaoviec')
async def giaoviec(request: Request, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                response = templates.TemplateResponse(
                    'assign.html', context={'request': request})
                response.set_cookie("username", username, httponly=False)
                return response
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/danhsachdetai')
async def danhsachdetai(request: Request, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                return templates.TemplateResponse('projects.html', context={'request': request})

        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/danhsachkythuctap')
async def danhsachkythuctap(request: Request, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                return templates.TemplateResponse('internships.html', context={'request': request})

        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/danhsachnhomthuctap')
async def danhsachnhomthuctap(request: Request, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                return templates.TemplateResponse('groups.html', context={'request': request})

        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/get_ds_de_tai_profile')
async def get_ds_de_tai_profile(id: str):
    return JSONResponse(status_code=200, content=get_nhom_thuc_tap_by_user_id_controller(id))


@app.get('/get_so_luong_sinh_vien_theo_truong')
async def get_so_luong_sinh_vien_theo_truong_route(token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                return get_so_luong_sinh_vien_theo_truong_controller()
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/get_so_luong_sinh_vien_theo_nganh')
async def get_so_luong_sinh_vien_theo_nganh_route(token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                return get_so_luong_sinh_vien_theo_nganh_controller()
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/get_all_sinh_vien')
async def get_all_sinh_vien_route(token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                result = get_all_sinh_vien_controller()
                ds: list = [{'id': i[0], 'mssv': i[1], 'hoten': i[2], 'gioitinh': i[3],
                             'nganh': i[4], 'truong': i[5], 'trangthai': i[6], 'luuy': i[7]} for i in result]
                return JSONResponse(status_code=200, content=ds)
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/get_user_info_by_username')
async def get_user_info_by_username_route(id: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                result = get_user_info_by_username_controller(username)
                if result:
                    return JSONResponse(status_code=200, content={'hoten': result[0], 'sdt': result[1], 'email': result[2], 'chucdanh': result[3], 'phong': result[4], 'zalo': result[5], 'facebook': result[6], 'github': result[7], 'avatar': result[8]})
                else:
                    return JSONResponse(status_code=400, content={'status': 'User not found'})
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')


@app.get('/get_all_de_tai')
async def get_all_de_tai(token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                return JSONResponse(status_code=200, content=get_all_de_tai_thuc_tap_controller())
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/get_chi_tiet_de_tai_by_id')
async def get_chi_tiet_de_tai_by_id_route(id: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                return JSONResponse(status_code=200, content=get_chi_tiet_de_tai_by_id_controller(id))
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.post('/update_chi_tiet_de_tai_by_id')
async def update_chi_tiet_de_tai_by_id_route(id: str, ten: str, mota: str, isDeleted: int, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                result = update_chi_tiet_de_tai_by_id_controller(
                    id, ten, mota, isDeleted)
                return JSONResponse(status_code=200, content={'status': 'OK'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.post('/update_xoa_de_tai_by_id')
async def update_xoa_de_tai_by_id_route(id: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                result = update_xoa_de_tai_by_id_controller(id)
                if result:
                    return JSONResponse(status_code=200, content={'status': 'OK'})
                else:
                    return JSONResponse(status_code=200, content={'status': 'NOT OK'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.post('/them_de_tai_thuc_tap')
async def them_de_tai_thuc_tap_route(ten: str, mota: str, isDeleted: int, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                result = them_de_tai_thuc_tap_controller(ten, mota, isDeleted)
                return JSONResponse(status_code=200, content={'status': 'OK'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/get_all_ky_thuc_tap')
async def get_all_ky_thuc_tap_route(token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                return JSONResponse(status_code=200, content=get_all_ky_thuc_tap_controller())
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/get_ky_thuc_tap_by_username')
async def get_ky_thuc_tap_by_username_route(token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                return JSONResponse(status_code=200, content=get_ky_thuc_tap_by_username_controller(payload.get("sub")))
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/get_chi_tiet_ky_thuc_tap_by_id')
async def get_chi_tiet_ky_thuc_tap_by_id_route(id: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                return JSONResponse(status_code=200, content=get_chi_tiet_ky_thuc_tap_by_id_controller(id))
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.post('/update_chi_tiet_ky_thuc_tap_by_id')
async def update_chi_tiet_ky_thuc_tap_by_id_route(id: str, ngaybatdau: str, ngayketthuc: str, isDeleted: int, ghichu: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                result = update_chi_tiet_ky_thuc_tap_by_id_controller(
                    id, ngaybatdau, ngayketthuc, isDeleted, ghichu)
                return JSONResponse(status_code=200, content={'status': 'OK'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.post('/them_ky_thuc_tap')
async def them_ky_thuc_tap_route(ngaybatdau: str, ngayketthuc: str, isDeleted: int, ghichu: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                result = them_ky_thuc_tap_controller(
                    ngaybatdau, ngayketthuc, isDeleted, ghichu)
                return JSONResponse(status_code=200, content={'status': 'OK'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.post('/update_xoa_ky_thuc_tap_by_id')
async def update_xoa_ky_thuc_tap_by_id_route(id: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                result = update_xoa_ky_thuc_tap_by_id_controller(id)
                if result:
                    return JSONResponse(status_code=200, content={'status': 'OK'})
                else:
                    return JSONResponse(status_code=200, content={'status': 'NOT OK'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/get_ds_nhom_thuc_tap')
async def get_ds_nhom_thuc_tap_route():
    result = get_ds_nhom_thuc_tap_controller()
    return JSONResponse(status_code=200, content=result)


@app.get('/get_ds_nhom_thuc_tap_by_username')
async def get_ds_nhom_thuc_tap_by_username_route(username: str):
    result = get_ds_nhom_thuc_tap_by_nguoi_huong_dan_controller(username)
    return JSONResponse(status_code=200, content=result)


@app.get('/get_ds_nhom_thuc_tap_con_han')
async def get_ds_nhom_thuc_tap_con_han_route():
    result = get_ds_nhom_thuc_tap_controller()
    current_date = datetime.datetime.now().date()
    data: list = []
    for i in result:
        ngay_bat_dau = datetime.datetime.strptime(
            i['ngaybatdau'], '%d/%m/%Y').date()
        if ngay_bat_dau >= current_date:
            data.append(i)
    return JSONResponse(status_code=200, content=data)


@app.get('/get_ds_nhom_chua_co_cong_viec')
async def get_ds_nhom_chua_co_cong_viec_route(token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                return get_ds_nhom_chua_co_cong_viec_controller(username)
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/get_ds_cong_viec_nhom')
async def get_ds_cong_viec_nhom_route(token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                return get_ds_cong_viec_nhom_controller()
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.post('/them_cong_viec_nhom')
async def them_cong_viec_nhom_route(id: int, ngaybatdau: str, ngayketthuc: str, ten: str, mota: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                result = them_cong_viec_nhom_controller(
                    id, ngaybatdau, ngayketthuc, ten, mota)
                if result:
                    return JSONResponse(status_code=200, content={'status': 'OK'})
                else:
                    return JSONResponse(status_code=200, content={'status': 'NOT OK'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/get_dssv_by_nhom_id')
async def get_dssv_by_nhom_id_route(id: int, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                return get_dssv_by_nhom_id_controller(id)
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/get_ds_cong_viec_by_id_nhom')
async def get_ds_cong_viec_by_id_nhom_route(id: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                return get_ds_cong_viec_by_id_nhom_controller(id)
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/get_chi_tiet_nhom_thuc_tap_by_id')
async def get_chi_tiet_nhom_thuc_tap_by_id_route(id: str):
    return JSONResponse(status_code=200, content=get_chi_tiet_nhom_thuc_tap_by_id_controller(id))


@app.get('/get_all_nguoi_huong_dan')
async def get_all_nguoi_huong_dan_route():
    return JSONResponse(status_code=200, content=get_all_nguoi_huong_dan_controller())


@app.get('/get_chi_tiet_chinh_sua_nhom')
async def get_chi_tiet_chinh_sua_nhom_route(token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                return get_chi_tiet_chinh_sua_nhom_controller()
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.post('/update_chi_tiet_nhom_thuc_tap_by_id')
async def update_chi_tiet_nhom_thuc_tap_by_id_route(id: int, kytt: int, nguoihd: int, detai: int, soluong: int, tennhom: str, telegram: str, isDeleted: int, ghichu: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                result = update_chi_tiet_nhom_thuc_tap_by_id_controller(
                    id, kytt, nguoihd, detai, soluong, tennhom, telegram, ghichu, isDeleted)
                return JSONResponse(status_code=200, content={'status': 'OK'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.post('/update_xoa_nhom_thuc_tap_by_id')
async def update_xoa_nhom_thuc_tap_by_id_route(id: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                result = update_xoa_nhom_thuc_tap_by_id_controller(id)
                if result:
                    return JSONResponse(status_code=200, content={'status': 'OK'})
                else:
                    return JSONResponse(status_code=200, content={'status': 'NOT OK'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.post('/them_nhom_thuc_tap')
async def them_nhom_thuc_tap_route(nguoihd: str, kytt: str, detai: str, soluong: int, tennhom: str, telegram: str, isDeleted: int, ghichu: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                result = them_nhom_thuc_tap_controller(
                    nguoihd, kytt, detai, soluong, tennhom, telegram, isDeleted, ghichu)
                return JSONResponse(status_code=200, content={'status': 'OK'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/get_chi_tiet_sinh_vien_by_id')
async def get_chi_tiet_sinh_vien_by_id_route(id: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                condition = get_trang_thai_sinh_vien_by_id_controller(id)
                result: dict = {}
                if condition['trangthai'] == 0:
                    result = get_chi_tiet_sinh_vien_chua_co_nhom_controller(id)
                elif condition['trangthai'] == 1:
                    result = get_chi_tiet_sinh_vien_da_co_nhom_controller(id)
                else:
                    result = get_chi_tiet_sinh_vien_da_danh_gia_controller(id)
                result['trangthai'] = condition['trangthai']
                return JSONResponse(status_code=200, content=result)
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/get_ds_sinh_vien_by_username')
async def get_ds_sinh_vien_by_username_route(kythuctap: str, nhomthuctap: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                return JSONResponse(status_code=200, content=get_ds_sinh_vien_by_username_controller(username, kythuctap, nhomthuctap))
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/get_dssv_by_kttid_nhomid_username')
async def get_dssv_by_kttid_nhomid_username_route(kythuctap_id: int, nhomhuongdan_id: int, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                return JSONResponse(status_code=200, content=get_dssv_by_kttid_nhomid_username_controller(kythuctap_id, nhomhuongdan_id, username))
        except jwt.PyJWKError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/get_ds_chi_tiet_cong_viec_by_idsinhvien')
async def get_ds_chi_tiet_cong_viec_by_idsinhvien_route(sinhvienid: int, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                return JSONResponse(status_code=200, content=get_ds_chi_tiet_cong_viec_by_idsinhvien_controller(sinhvienid))
        except jwt.PyJWKError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.post('/update_xac_nhan_trang_thai_cong_viec')
async def update_xac_nhan_trang_thai_cong_viec_route(idcongviec: int, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                result = update_xac_nhan_trang_thai_cong_viec_controller(
                    idcongviec, username)
                if result:
                    return JSONResponse(status_code=200, content={'status': 'OK'})
                else:
                    return JSONResponse(status_code=200, content={'status': 'NOT OK'})
            elif permission == "student":
                result = update_sv_xac_nhan_hoan_thanh_cong_viec_controller(
                    idcongviec, username)
                if result:
                    return JSONResponse(status_code=200, content={'status': 'OK'})
                else:
                    return JSONResponse(status_code=200, content={'status': 'NOT OK'})
        except jwt.PyJWKError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/get_chi_tiet_danh_gia_sv_by_id')
async def get_chi_tiet_danh_gia_sv_by_id_route(id: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                return get_chi_tiet_danh_gia_sv_by_id_controller(id=id)
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.post('/update_danh_gia_sv_by_id')
async def update_danh_gia_sv_by_id_route(sinhvienid: str, nhomid: int, ythuckyluat_number: float, ythuckyluat_text: str, tuanthuthoigian_number: float, tuanthuthoigian_text: str, kienthuc_number: float, kienthuc_text: str, kynangnghe_number: float, kynangnghe_text: str, khanangdoclap_number: float, khanangdoclap_text: str, khanangnhom_number: float, khanangnhom_text: str, khananggiaiquyetcongviec_number: float, khananggiaiquyetcongviec_text: str, danhgiachung_number: float, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                result = update_danh_gia_sv_by_id_controller(sinhvienid, nhomid, ythuckyluat_number, ythuckyluat_text, tuanthuthoigian_number, tuanthuthoigian_text, kienthuc_number, kienthuc_text, kynangnghe_number,
                                                             kynangnghe_text, khanangdoclap_number, khanangdoclap_text, khanangnhom_number, khanangnhom_text, khananggiaiquyetcongviec_number, khananggiaiquyetcongviec_text, danhgiachung_number)
                if result:
                    return JSONResponse(status_code=200, content={'status': 'OK'})
                else:
                    return JSONResponse(status_code=200, content={'status': 'EXPIRED'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/get_id_nhom_by_sv_id')
async def get_id_nhom_by_sv_id_route(id: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                result = get_id_nhom_by_sv_id_controller(id)
                return JSONResponse(status_code=200, content={'id': result})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/xuat_danh_gia')
async def xuat_danh_gia(id: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                i = xuat_phieu_danh_gia_controller(id)
                headers = {
                    # Mở tệp PDF trong trình duyệt
                    "Content-Disposition": f"inline; filename={i['mssv']}.pdf",
                    "Content-Type": "application/pdf",  # Loại nội dung của tệp PDF
                }
                if i is not TypeError and i is not None:
                    if i['kyhieu_truong'] == "VLUTE":
                        data: dict = {
                            "student_fullname": i['hoten'],
                            "student_class": i['malop'],
                            "mentor_fullname": i['nguoihuongdan'],
                            "r1_text": i['ythuckyluat_text'],
                            "r2_text": i['tuanthuthoigian_text'],
                            "r3_text": i['kienthuc_text'],
                            "r4_text": i['kynangnghe_text'],
                            "r5_text": i['khanangdoclap_text'],
                            "r6_text": i['khanangnhom_text'],
                            "r7_text": i['khananggiaiquyetcongviec_text'],
                            "r1_number": str(i['ythuckyluat_number']),
                            "r2_number": str(i['tuanthuthoigian_number']),
                            "r3_number": str(i['kienthuc_number']),
                            "r4_number": str(i['kynangnghe_number']),
                            "r5_number": str(i['khanangdoclap_number']),
                            "r6_number": str(i['khanangnhom_number']),
                            "r7_number": str(i['khananggiaiquyetcongviec_number']),
                            "r8_number": str(i['danhgiachung_number'])
                        }
                        r = vlute_xuat_danh_gia(
                            'pdf/phieudanhgia_vlute.pdf', f"{i['mssv']}.pdf", data, username)
                        if r:
                            with open(r, 'rb') as f:
                                docx_content = f.read()

                            os.remove(os.path.join(
                                f'DOCX/{username}', f"{i['mssv']}.pdf"))
                            return Response(content=docx_content, headers=headers)
                        else:
                            return JSONResponse(status_code=400, content={'status': 'ERR'})
                    else:
                        return JSONResponse(status_code=200, content={'status': 'Phiếu chỉ dành cho sinh viên SPKT Vĩnh Long (VLUTE)'})
                else:
                    return JSONResponse(status_code=404, content={'status': 'Sinh viên chưa có đánh giá'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/ctu_xuat_phieu_tiep_nhan')
async def ctu_xuat_phieu_tiep_nhan_route(id: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                i = ctu_xuat_phieu_tiep_nhan_controller(id)
                if i is not TypeError:
                    if i['kyhieu_truong'] == "CTU":
                        data: dict = {
                            "ngaybatdau": i['ngaybatdau'],
                            "ngayketthuc": i['ngayketthuc'],
                            "nhd_hoten": i['nguoihuongdan'],
                            "nhd_sdt": i['sdt_nguoihuongdan'],
                            "nhd_email": i['email_nguoihuongdan'],
                            "sv_hoten": i['hoten'],
                            "sv_mssv": i['mssv'],
                            "sv_malop": i['malop'],
                            "sv_nganh": i['nganh']
                        }
                        headers = {
                            # Mở tệp PDF trong trình duyệt
                            "Content-Disposition": f"inline; filename={i['mssv']}.pdf",
                            "Content-Type": "application/pdf",  # Loại nội dung của tệp PDF
                        }
                        r = ctu_xuat_phieu_tiep_nhan(
                            'pdf/phieutiepnhan_ctu.pdf', f"phieutiepnhan_{i['mssv']}.pdf", data, username)
                        if r:
                            with open(r, 'rb') as f:
                                docx_content = f.read()

                            os.remove(os.path.join(
                                f'DOCX/{username}', f"phieutiepnhan_{i['mssv']}.pdf"))
                            return Response(content=docx_content, headers=headers)
                    else:
                        return JSONResponse(status_code=200, content={'status': 'Phiếu chỉ dành cho SV ĐH Cần Thơ (CTU)'})
                else:
                    return JSONResponse(status_code=400, content={'status': 'ERR'})
            else:
                return JSONResponse(status_code=404, content={'status': 'Lỗi khi xuất phiếu'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/ctu_xuat_phieu_giao_viec')
async def ctu_xuat_phieu_giao_viec_route(id: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                i = ctu_xuat_phieu_giao_viec_controller(id, username)
                # return JSONResponse(status_code=200, content=i)
                if i is not TypeError:
                    if i['kyhieu_truong'] == "CTU":
                        data: dict = {
                            "sv_hoten": i['sv_hoten'],
                            "sv_mssv": i['sv_mssv'],
                            "ngaybatdau": i['ktt_ngaybatdau'],
                            "ngayketthuc": i['ktt_ngayketthuc'],
                            "nhd_hoten": i['nguoihuongdan_hoten'],
                            "tuan1_batdau": i['congviec'][0]['ngaybatdau'],
                            "tuan1_ketthuc": i['congviec'][0]['ngayketthuc'],
                            "tuan1_congviec": i['congviec'][0]['tencongviec'],
                            "tuan2_batdau": i['congviec'][1]['ngaybatdau'],
                            "tuan2_ketthuc": i['congviec'][1]['ngayketthuc'],
                            "tuan2_congviec": i['congviec'][1]['tencongviec'],
                            "tuan3_batdau": i['congviec'][2]['ngaybatdau'],
                            "tuan3_ketthuc": i['congviec'][2]['ngayketthuc'],
                            "tuan3_congviec": i['congviec'][2]['tencongviec'],
                            "tuan4_batdau": i['congviec'][3]['ngaybatdau'],
                            "tuan4_ketthuc": i['congviec'][3]['ngayketthuc'],
                            "tuan4_congviec": i['congviec'][3]['tencongviec'],
                            "tuan5_batdau": i['congviec'][4]['ngaybatdau'],
                            "tuan5_ketthuc": i['congviec'][4]['ngayketthuc'],
                            "tuan5_congviec": i['congviec'][4]['tencongviec'],
                            "tuan6_batdau": i['congviec'][5]['ngaybatdau'],
                            "tuan6_ketthuc": i['congviec'][5]['ngayketthuc'],
                            "tuan6_congviec": i['congviec'][5]['tencongviec'],
                            "tuan7_batdau": i['congviec'][6]['ngaybatdau'],
                            "tuan7_ketthuc": i['congviec'][6]['ngayketthuc'],
                            "tuan7_congviec": i['congviec'][6]['tencongviec'],
                            "tuan8_batdau": i['congviec'][7]['ngaybatdau'],
                            "tuan8_ketthuc": i['congviec'][7]['ngayketthuc'],
                            "tuan8_congviec": i['congviec'][7]['tencongviec']
                        }
                        headers = {
                            # Mở tệp PDF trong trình duyệt
                            "Content-Disposition": f"inline; filename={i['sv_mssv']}.pdf",
                            "Content-Type": "application/pdf",  # Loại nội dung của tệp PDF
                        }
                        r = ctu_xuat_phieu_giao_viec(
                            'pdf/phieugiaoviec_ctu.pdf', f"phieugiaoviec_{i['sv_mssv']}.pdf", data, username)
                        if r:
                            with open(r, 'rb') as f:
                                docx_content = f.read()

                            os.remove(os.path.join(
                                f'DOCX/{username}', f"phieugiaoviec_{i['sv_mssv']}.pdf"))
                            return Response(content=docx_content, headers=headers)
                    else:
                        return JSONResponse(status_code=200, content={'status': 'Phiếu chỉ dành cho SV ĐH Cần Thơ (CTU)'})
                else:
                    return JSONResponse(status_code=400, content={'status': 'Sinh viên chưa có công việc'})
            else:
                return JSONResponse(status_code=404, content={'status': 'Lỗi khi xuất phiếu'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/ctu_xuat_phieu_theo_doi')
async def ctu_xuat_phieu_theo_doi_route(id: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                i = ctu_xuat_phieu_theo_doi_controller(id, username)
                # return JSONResponse(status_code=200, content=i)
                if i is not TypeError:
                    if i['kyhieu_truong'] == "CTU":
                        data: dict = {
                            "sv_hoten": i['sv_hoten'],
                            "sv_mssv": i['sv_mssv'],
                            "ngaybatdau": i['ktt_ngaybatdau'],
                            "ngayketthuc": i['ktt_ngayketthuc'],
                            "nhd_hoten": i['nguoihuongdan_hoten'],
                            "tuan1_batdau": i['congviec'][0]['ngaybatdau'],
                            "tuan1_ketthuc": i['congviec'][0]['ngayketthuc'],
                            "tuan1_congviec": i['congviec'][0]['tencongviec'],
                            "tuan2_batdau": i['congviec'][1]['ngaybatdau'],
                            "tuan2_ketthuc": i['congviec'][1]['ngayketthuc'],
                            "tuan2_congviec": i['congviec'][1]['tencongviec'],
                            "tuan3_batdau": i['congviec'][2]['ngaybatdau'],
                            "tuan3_ketthuc": i['congviec'][2]['ngayketthuc'],
                            "tuan3_congviec": i['congviec'][2]['tencongviec'],
                            "tuan4_batdau": i['congviec'][3]['ngaybatdau'],
                            "tuan4_ketthuc": i['congviec'][3]['ngayketthuc'],
                            "tuan4_congviec": i['congviec'][3]['tencongviec'],
                            "tuan5_batdau": i['congviec'][4]['ngaybatdau'],
                            "tuan5_ketthuc": i['congviec'][4]['ngayketthuc'],
                            "tuan5_congviec": i['congviec'][4]['tencongviec'],
                            "tuan6_batdau": i['congviec'][5]['ngaybatdau'],
                            "tuan6_ketthuc": i['congviec'][5]['ngayketthuc'],
                            "tuan6_congviec": i['congviec'][5]['tencongviec'],
                            "tuan7_batdau": i['congviec'][6]['ngaybatdau'],
                            "tuan7_ketthuc": i['congviec'][6]['ngayketthuc'],
                            "tuan7_congviec": i['congviec'][6]['tencongviec'],
                            "tuan8_batdau": i['congviec'][7]['ngaybatdau'],
                            "tuan8_ketthuc": i['congviec'][7]['ngayketthuc'],
                            "tuan8_congviec": i['congviec'][7]['tencongviec']
                        }
                        headers = {
                            # Mở tệp PDF trong trình duyệt
                            "Content-Disposition": f"inline; filename={i['sv_mssv']}.pdf",
                            "Content-Type": "application/pdf",  # Loại nội dung của tệp PDF
                        }
                        r = ctu_xuat_phieu_theo_doi(
                            'pdf/phieutheodoi_ctu.pdf', f"phieutheodoi_{i['sv_mssv']}.pdf", data, username)
                        if r:
                            with open(r, 'rb') as f:
                                docx_content = f.read()

                            os.remove(os.path.join(
                                f'DOCX/{username}', f"phieutheodoi_{i['sv_mssv']}.pdf"))
                            return Response(content=docx_content, headers=headers)
                    else:
                        return JSONResponse(status_code=200, content={'status': 'Phiếu chỉ dành cho SV ĐH Cần Thơ (CTU)'})
                else:
                    return JSONResponse(status_code=400, content={'status': 'Sinh viên chưa có công việc'})
            else:
                return JSONResponse(status_code=404, content={'status': 'Lỗi khi xuất phiếu'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/goi_y_dia_chi')
async def goi_y_dia_chi(q: str):
    return JSONResponse(status_code=200, content=get_goi_y_xa_phuong_controller(q))


@app.get('/get_ds_dia_chi')
async def get_ds_dia_chi_route():
    return JSONResponse(status_code=200, content=get_ds_dia_chi_controller())


@app.get('/get_danh_sach_nganh')
async def get_danh_sach_nganh_route():
    return JSONResponse(status_code=200, content=get_danh_sach_nganh_controller())


@app.get('/get_danh_sach_truong')
async def get_danh_sach_truong_route():
    return JSONResponse(status_code=200, content=get_danh_sach_truong_controller())


@app.post('/thong_tin_sinh_vien')
async def thong_tin_sinh_vien_route(sv: ThongTinSV):
    result = insert_sinh_vien_controller(
        sv.mssv, sv.hoten, sv.gioitinh, sv.sdt, sv.email, sv.diachi, sv.malop, sv.truong, sv.nganh, sv.khoa, sha3_256(bytes(default_password, 'utf-8')).hexdigest())
    if result:
        sent = send_otp_email(sv.email, sv.hoten)
        if sent:
            insert_taikhoan = insert_taikhoan_sinhvien_controller(
                result, sha3_256(bytes(default_password, 'utf-8')).hexdigest(), 1)
            response = JSONResponse(status_code=200, content={'status': 'OK'})
            response.set_cookie('studentid', result,
                                max_age=5356800)  # Hạn 2 tháng
            asyncio.create_task(sendMessageTelegram(
                message=f"<code>Sinh viên đăng ký thông tin</code>\n\n<b>Họ tên: </b>{sv.hoten}\n<b>MSSV:</b> {sv.mssv}\n<b>SĐT:</b> {sv.sdt}\n<b>Email:</b> {sv.email}", chat_id=admin_chat_id, format='html'))
            return response
    else:
        return JSONResponse(status_code=400, content={'status': 'BADDDD REQUEST'})


@app.post('/update_xoa_sinh_vien_by_id')
async def update_xoa_sinh_vien_by_id(id: int, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                result = update_xoa_sinh_vien_by_id_controller(id)
                if result:
                    return JSONResponse(status_code=200, content={'status': 'OK'})
                else:
                    return JSONResponse(status_code=200, content={'status': 'BADDDD REQUEST'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    else:
        return RedirectResponse('/login')


@app.get('/get_chi_tiet_sinh_vien_moi_nhap_thong_tin')
async def get_chi_tiet_sinh_vien_moi_nhap_thong_tin(id: str):
    return JSONResponse(status_code=200, content=get_chi_tiet_sinh_vien_chua_co_nhom_controller(id))


@app.post('/them_nhom_thuc_tap_sv')
async def them_nhom_thuc_tap_sv_route(email: str, idnhom: int):
    result = update_nhom_thuc_tap_by_sv_id_controller(email, idnhom)
    if result:
        response = JSONResponse(status_code=200, content={'status': 'OK'})
        response.set_cookie('groupid', result, max_age=5356800)
        return response
    else:
        return JSONResponse(status_code=400, content={'status': 'BADDDD REQUEST'})


@app.post('/import_danh_gia_sv')
async def import_danh_gia_sv(file: UploadFile = File(...), token: str = Cookie(None)):
    uploaded_folder = os.path.join(os.getcwd(), 'uploaded', 'xlsx')
    os.makedirs(uploaded_folder, exist_ok=True)

    file_path = os.path.join(uploaded_folder, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Xử lý file vừa upload
    df = pd.read_excel(file_path)
    try:
        for i in df.itertuples(index=False):
            result = update_danh_gia_sv_by_mssv_controller(
                i[0], i[4], i[3], i[6], i[5], i[8], i[7], i[10], i[9], i[12], i[11], i[14], i[13], i[16], i[15], i[17])
        os.remove(file_path)
        return JSONResponse(status_code=200, content={'status': 'OK'})
    except Exception as e:
        return JSONResponse(status_code=400, content={'status': 'BADDDD REQUEST'})


@app.get('/xuat_ds_sinh_vien_da_danh_gia')
async def xuat_ds_sinh_vien_da_danh_gia(kythuctap: int, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                tencty: str = 'Trung tâm CNTT - VNPT Vĩnh Long'
                result = get_dssv_da_danh_gia_by_nguoi_huong_dan(
                    username=username, kythuctap=kythuctap)
                output_path = os.path.join('DOCX', username)
                zip_output = os.path.join('DOCX', f'{username}.zip')
                # Lặp qua danh sách sinh viên có đánh giá, tạo các file docx
                for i in result:
                    r = export(username=username, mssv=i['mssv'], sv_hoten=i['hoten'], sv_lop=i['malop'], tt_donvi=tencty, tt_nguoihuongdan=i['nguoihuongdan'], dg_ythuckyluat_number=i['ythuckyluat_number'], dg_ythuckyluat_text=i['ythuckyluat_text'], dg_tuanthuthoigian_number=i['tuanthuthoigian_number'], dg_tuanthuthoigian_text=i['tuanthuthoigian_text'], dg_kienthuc_number=i['kienthuc_number'], dg_kienthuc_text=i['kienthuc_text'], dg_kynangnghe_number=i[
                               'kynangnghe_number'], dg_kynangnghe_text=i['kynangnghe_text'], dg_khanangdoclap_number=i['khanangdoclap_number'], dg_khanangdoclap_text=i['khanangdoclap_text'], dg_khanangnhom_number=i['khanangnhom_number'], dg_khanangnhom_text=i['khanangnhom_text'], dg_khananggiaiquyetcongviec_number=i['khananggiaiquyetcongviec_number'], dg_khananggiaiquyetcongviec_text=i['khananggiaiquyetcongviec_text'], dg_danhgiachung_number=i['danhgiachung_number'])

                # Tạo file nén các file docx
                with zipfile.ZipFile(zip_output, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
                    for root, _, files in os.walk(output_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, output_path)
                            zipf.write(file_path, arcname)

                try:
                    # Xoá thư mục chứa các file docx vừa nén
                    shutil.rmtree(
                        output_path, ignore_errors=False, onerror=None)
                    # Download file nén
                    return FileResponse(zip_output, headers={"Content-Disposition": f"attachment; filename=dssv_{username}.zip"})
                except Exception as e:
                    return JSONResponse(status_code=400, content={'status': 'BADDDD REQUEST'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.post('/update_sinh_vien_by_id')
async def update_sinh_vien_by_id_route(id: int, mssv: str, hoten: str, gioitinh: int, sdt: str, email: str, diachi: str, malop: str, truong: int, nganh: int, khoa: int, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                result = update_sinh_vien_by_id_controller(
                    id, mssv, hoten, gioitinh, sdt, email, diachi, malop, truong, nganh, khoa)
                if result:
                    return JSONResponse(status_code=200, content={'status': 'OK'})
                else:
                    return JSONResponse(status_code=400, content={'status': 'BADDDD REQUEST'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    else:
        return RedirectResponse('/login')


@app.get('/get_danh_sach_nhom_theo_ky_id')
async def get_danh_sach_nhom_theo_ky_id_route(id: int, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                result = get_danh_sach_nhom_theo_ky_id(id, payload.get("sub"))
                if result:
                    return JSONResponse(status_code=200, content=result)
                else:
                    return JSONResponse(status_code=400, content={'status': 'BADDDD REQUEST'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    else:
        return RedirectResponse('/login')


@app.post('/xac_thuc_otp')
async def xac_thuc_otp(email: str, otp: str):
    result = is_otp_valid(email=email, entered_otp=otp)
    if result:
        return JSONResponse(status_code=200, content={'status': 'OK'})
    else:
        return JSONResponse(status_code=500, content={'status': 'OTP Expired'})


@app.post('/gui_mail_otp')
async def gui_mail_otp(email: str):
    try:
        hoten = get_ho_ten_sv_by_email_controller(email)
        ngayHetHan = check_sv_con_han_thuc_tap(email)
        if (True):
            send_otp_email(email, hoten)
            return JSONResponse(status_code=200, content={'status': 'OK'})
        else:
            return JSONResponse(status_code=200, content={'status': 'Expired'})
    except Exception as e:
        return JSONResponse(status_code=500, content={'status': 'Email system has problem'})


@app.get('/sinhvien')
async def sv_index(request: Request, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                response = templates.TemplateResponse(
                    'sv_index.html', context={'request': request})
                response.set_cookie("email", username, httponly=False)
                return response
            else:
                return RedirectResponse('/login')
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    else:
        return RedirectResponse('/login')


@app.get('/danhgiakythuctap')
async def sv_danhgiakythuctap(request: Request, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return templates.TemplateResponse('sv_review.html', context={'request': request})
            else:
                return RedirectResponse('/login')
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    else:
        return RedirectResponse('/login')


@app.get('/xem_thong_tin_sv')
async def xem_thong_tin_sv_route(username: str):
    return JSONResponse(status_code=200, content=xem_thong_tin_sv_controller(email=username))


@app.post('/them_chi_tiet_cong_viec')
async def them_chi_tiet_cong_viec_route(data: ChiTietCongViec = Body(...), token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                inserted_result: dict = {}
                for i in data.sinhvien:
                    result = them_chi_tiet_cong_viec_controller(
                        id_congviec=data.id_congviec, id_sinhvien=int(i), trangthai=0, ghichu=data.ghichu)
                    if result == 1:
                        congviec = get_chi_tiet_giao_viec_cho_sv_by_id_cong_viec_controller(
                            data.id_congviec, int(i))
                        congviec_ghichu = data.ghichu.replace('<br>', '\n')
                        congviec_mota = str(
                            congviec['motacongviec']).replace('<br>', '\n')
                        asyncio.create_task(sendMessageTelegram(
                            message=f"<code>Thông báo giao việc</code>\n\n<b>Người thực hiện:</b> <code>[{congviec['mssv']}] {congviec['nguoinhanviec']}</code>\n<b>Công việc:</b> {congviec['tencongviec']}\n<b>Thời gian:</b> {congviec['ngaybatdau']} đến {congviec['ngayketthuc']}\n<b>Nội dung công việc:</b>\n<pre language='c++'>{congviec_mota}</pre>\n<b>Ghi chú:</b>\n<pre language='c++'>{congviec_ghichu}</pre>", chat_id=str(congviec['telegram_id']), format='html'))
                        inserted_result[congviec['mssv']] = 1
                    elif result == 2:
                        inserted_result[congviec['mssv']] = 2
                    else:
                        inserted_result[congviec['mssv']] = 3

                return JSONResponse(status_code=200, content={'status': 'INSERTED', 'result': inserted_result})
            else:
                return JSONResponse(status_code=400, content={'status': 'BADDDD REQUEST', 'result': {}})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    else:
        return RedirectResponse('/login')


@app.get('/get_chi_tiet_cong_viec_by_id_cong_viec')
async def get_chi_tiet_cong_viec_by_id_cong_viec_route(id: int):
    return JSONResponse(status_code=200, content=get_chi_tiet_cong_viec_by_id_cong_viec_controller(id))


@app.get('/get_chi_tiet_cong_viec_by_id')
async def get_chi_tiet_cong_viec_by_id_route(id: int):
    return JSONResponse(status_code=200, content=get_chi_tiet_cong_viec_by_id_controller(id))


@app.post('/xoa_cong_viec_by_id')
async def xoa_cong_viec_by_id_route(id: int, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                result = xoa_cong_viec_by_id_controller(id)
                if result:
                    return JSONResponse(status_code=200, content={'status': 'OK'})
                else:
                    return JSONResponse(status_code=400, content={'status': 'BADDDD REQUEST'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    else:
        return RedirectResponse('/login')


@app.post('/xoa_chi_tiet_cong_viec_by_id')
async def xoa_chi_tiet_cong_viec_by_id_route(id: int, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                result = xoa_chi_tiet_cong_viec_by_id_controller(id)
                if result:
                    return JSONResponse(status_code=200, content={'status': 'OK'})
                else:
                    return JSONResponse(status_code=400, content={'status': 'BADDDD REQUEST'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    else:
        return RedirectResponse('/login')


@app.post('/update_chi_tiet_cong_viec_by_id')
async def update_chi_tiet_cong_viec_by_id_route(id: int, svid: int, ghichu: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                result = update_chi_tiet_cong_viec_by_id_controller(
                    id, svid, ghichu)
                if result:
                    return JSONResponse(status_code=200, content={'status': 'OK'})
                else:
                    return JSONResponse(status_code=400, content={'status': 'BADDDD REQUEST'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    else:
        return RedirectResponse('/login')


@app.get('/get_dssv_by_id_cong_viec')
async def get_dssv_by_id_cong_viec_route(id: int):
    result = get_dssv_by_id_cong_viec_controller(id)
    if result:
        return JSONResponse(status_code=200, content=result)
    else:
        return JSONResponse(status_code=200, content={'status': 'BADDDD REQUEST'})


@app.post('/danh_gia_thuc_tap')
async def danh_gia_thuc_tap_route(email: str, id_nhd: int, dapan_1: int, dapan_2: int, dapan_3: int, dapan_4: int, gopy: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            sv_id = xem_thong_tin_sv(email)
            result = insert_danh_gia_thuc_tap_controller(
                sv_id['id'], id_nhd, dapan_1, dapan_2, dapan_3, dapan_4, gopy)
            if result:
                return JSONResponse(status_code=200, content={'status': 'OK'})
            else:
                return JSONResponse(status_code=400, content={'status': 'BADDDD REQUEST'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    else:
        return RedirectResponse('/login')


@app.get('/get_ds_chi_tiet_danh_gia')
async def get_ds_chi_tiet_danh_gia_route(token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                result = get_ds_chi_tiet_danh_gia_controller()
                if result:
                    return JSONResponse(status_code=200, content=result)
                else:
                    return JSONResponse(status_code=200, content=[])
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    else:
        return RedirectResponse('/login')


@app.get('/get_ds_chi_tiet_danh_gia_by_id')
async def get_ds_chi_tiet_danh_gia_by_id_route(id: int, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                result = get_ds_chi_tiet_danh_gia_by_id_controller(id)
                if result:
                    return JSONResponse(status_code=200, content=result)
                else:
                    return JSONResponse(status_code=400, content={'status': 'BADDDD REQUEST'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    else:
        return RedirectResponse('/login')


@app.post('/danh_gia_nhieu_sv')
async def danh_gia_nhieu_sv_route(dssv: str, ythuckyluat_number: float, ythuckyluat_text: str, tuanthuthoigian_number: float, tuanthuthoigian_text: str, kienthuc_number: float, kienthuc_text: str, kynangnghe_number: float, kynangnghe_text: str, khanangdoclap_number: float, khanangdoclap_text: str, khanangnhom_number: float, khanangnhom_text: str, khananggiaiquyetcongviec_number: float, khananggiaiquyetcongviec_text: str, danhgiachung_number: float, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                if isinstance(eval(dssv), int):
                    nhomid = get_id_nhom_by_sv_id_controller(str(dssv))
                    result = update_danh_gia_sv_by_id_controller(str(dssv), nhomid, ythuckyluat_number, ythuckyluat_text, tuanthuthoigian_number, tuanthuthoigian_text, kienthuc_number, kienthuc_text, kynangnghe_number,
                                                                 kynangnghe_text, khanangdoclap_number, khanangdoclap_text, khanangnhom_number, khanangnhom_text, khananggiaiquyetcongviec_number, khananggiaiquyetcongviec_text, danhgiachung_number)
                else:
                    for sinhvienid in eval(dssv):
                        nhomid = get_id_nhom_by_sv_id_controller(
                            str(sinhvienid))
                        result = update_danh_gia_sv_by_id_controller(str(sinhvienid), nhomid, ythuckyluat_number, ythuckyluat_text, tuanthuthoigian_number, tuanthuthoigian_text, kienthuc_number, kienthuc_text, kynangnghe_number,
                                                                     kynangnghe_text, khanangdoclap_number, khanangdoclap_text, khanangnhom_number, khanangnhom_text, khananggiaiquyetcongviec_number, khananggiaiquyetcongviec_text, danhgiachung_number)
                return JSONResponse(status_code=200, content={'status': 'OK'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/theodoitiendo')
async def theodoitiendo(request: Request, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                return templates.TemplateResponse('progress.html', context={'request': request})

        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/congviecsinhvien')
async def congviecsinhvien(request: Request, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "student":
                return templates.TemplateResponse('sv_tasks.html', context={'request': request})

        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/get_ds_congviec_by_sinhvien_email')
async def get_ds_congviec_by_sinhvien_email(token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            permission = payload.get("permission")
            if permission == "student":
                return get_ds_congviec_by_sinhvien_email_controller(username)
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/get_chi_tiet_cong_viec_by_id_cong_viec_email_sv')
async def get_chi_tiet_cong_viec_by_id_cong_viec_email_sv_route(id: int, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            permission = payload.get("permission")
            if permission == "student":
                result = get_chi_tiet_cong_viec_by_id_cong_viec_email_sv_controller(
                    id, username)
                return JSONResponse(status_code=200, content=result)
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/quanlytaikhoan')
async def quan_ly_tai_khoan(request: Request, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin":
                return templates.TemplateResponse('accounts.html', context={'request': request})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/get_ds_tai_khoan')
async def get_ds_tai_khoan(token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin":
                return get_ds_tai_khoan_controller()
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.post('/update_password')
async def update_password_route(old_password: str, new_password: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            username = payload.get("sub")
            if permission == "admin" or permission == "user":
                result = update_password_controller(username, sha3_256(bytes(
                    old_password, 'utf-8')).hexdigest(), sha3_256(bytes(new_password, 'utf-8')).hexdigest())
                if result == 1:
                    return JSONResponse(status_code=200, content={'status': 'OK'})
                else:
                    return JSONResponse(status_code=200, content={'status': 'NOT_MODIFY'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.post('/reset_password')
async def reset_password_route(id: int, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin":
                result = update_reset_mat_khau_nguoi_huong_dan_by_id_controller(
                    id, sha3_256(bytes(default_password, 'utf-8')).hexdigest())
                if result == 1:
                    return JSONResponse(status_code=200, content={'status': 'OK'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.post('/update_xoa_nguoi_huong_dan_by_id')
async def update_xoa_nguoi_huong_dan_by_id_route(id: int, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin":
                result = update_xoa_nguoi_huong_dan_by_id_controller(id)
                if result == 1:
                    return JSONResponse(status_code=200, content={'status': 'OK'})
                else:
                    return JSONResponse(status_code=200, content={'status': 'EXISTS'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.post('/update_ban_nguoi_huong_dan_by_id')
async def update_ban_nguoi_huong_dan_by_id_route(id: int, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin":
                result = update_ban_nguoi_huong_dan_by_id_controller(id)
                if result == 1:
                    return JSONResponse(status_code=200, content={'status': 'OK'})
                else:
                    return JSONResponse(status_code=200, content={'status': 'IS_ADMIN'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.post('/update_active_nguoi_huong_dan_by_id')
async def update_active_nguoi_huong_dan_by_id_route(id: int, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin":
                result = update_active_nguoi_huong_dan_by_id_controller(id)
                if result == 1:
                    return JSONResponse(status_code=200, content={'status': 'OK'})
                else:
                    return JSONResponse(status_code=200, content={'status': 'NOT_BANNED'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.post('/update_phan_quyen_nguoi_huong_dan_by_id')
async def update_phan_quyen_nguoi_huong_dan_by_id_route(id: int, role: int, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin":
                if (role <= 1):
                    result = update_phan_quyen_nguoi_huong_dan_by_id_controller(
                        id, role)
                    if result == 1:
                        return JSONResponse(status_code=200, content={'status': 'OK'})
                    else:
                        return JSONResponse(status_code=200, content={'status': 'NOT_UPDATE'})
                else:
                    return JSONResponse(status_code=200, content={'status': 'INCORRECT_ROLE'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/get_thong_tin_nguoi_huong_dan_by_id')
async def get_thong_tin_nguoi_huong_dan_by_id_route(id: int, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin":
                result = get_thong_tin_nguoi_huong_dan_by_id_controller(id)
                return JSONResponse(status_code=200, content=result)
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.post('/update_chi_tiet_tai_khoan_by_id')
async def update_chi_tiet_tai_khoan_by_id(id: int, hoten: str, sdt: str, email: str, chucdanh: str, phong: str, zalo: str, facebook: str, github: str, avatar: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin":
                result = update_chi_tiet_tai_khoan_by_id_controller(
                    id, hoten, sdt, email, chucdanh, phong, zalo, facebook, github, avatar)
                if result == 1:
                    return JSONResponse(status_code=200, content={'status': 'OK'})
                else:
                    return JSONResponse(status_code=200, content={'status': 'NOT_UPDATE'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.post('/them_nguoi_huong_dan')
async def them_nguoi_huong_dan(hoten: str, sdt: str, email: str, chucdanh: str, phong: str, username: str, zalo: str, facebook: str, github: str, avatar: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin":
                result = them_nguoi_huong_dan_controller(hoten, sdt, email, chucdanh, phong, username, sha3_256(
                    bytes(default_password, 'utf-8')).hexdigest(), zalo, facebook, github, avatar)
                if isinstance(result, int):
                    return JSONResponse(status_code=200, content={'status': 'OK'})
                else:
                    return JSONResponse(status_code=200, content={'status': 'NOT_CREATE'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/checkIsAdmin')
async def check_is_admin(token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin":
                return JSONResponse(status_code=200, content={'status': 'OK'})
            else:
                return JSONResponse(status_code=200, content={'status': 'NOT_OK'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/doimatkhau')
async def doi_mat_Khau(request: Request, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "admin" or permission == "user":
                return templates.TemplateResponse('change_password.html', context={'request': request})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.get('/doimatkhau_sv')
async def doi_mat_Khau(request: Request, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            if permission == "student":
                return templates.TemplateResponse('sv_change_password.html', context={'request': request})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.post('/update_password_sv')
async def update_password_sv_route(old_password: str, new_password: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            username = payload.get("sub")
            if permission == "student":
                result = update_password_sv_controller(username, sha3_256(bytes(
                    old_password, 'utf-8')).hexdigest(), sha3_256(bytes(new_password, 'utf-8')).hexdigest())
                if result == 1:
                    return JSONResponse(status_code=200, content={'status': 'OK'})
                else:
                    return JSONResponse(status_code=200, content={'status': 'NOT_MODIFY'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.post('/update_thong_tin_sv')
async def update_thong_tin_sv_route(mssv: str, hoten: str, gioitinh: int, sdt: str, diachi: str, malop: str, khoa: int, nganh: int, truong: int, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            sv_id = payload.get("id")
            email = payload.get("sub")
            if permission == "student":
                result = update_thong_tin_sv_controller(
                    sv_id, mssv, hoten, gioitinh, sdt, email, diachi, malop, khoa, nganh, truong)
                if result == 1:
                    return JSONResponse(status_code=200, content={'status': 'OK'})
                else:
                    return JSONResponse(status_code=200, content={'status': 'NOT_MODIFY'})
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')


@app.post('/canhbaodangnhap')
async def canhbaodangnhap_route(noidung: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permission = payload.get("permission")
            username = payload.get("sub")
            if permission == "admin":
                asyncio.create_task(sendMessageTelegram(message=f"<code>Cảnh báo đăng nhập</code>\n\n<b>Tài khoản:</b> <code>{username}</code>\n<b>Thông tin thiết bị đăng nhập:</b>\n<pre language='json'>"+json.loads(
                    json.dumps(noidung, indent=2)).replace('","', '",\n"')+"</pre>", chat_id=admin_chat_id, format='HTML'))
        except jwt.PyJWTError:
            return RedirectResponse('/login')
    return RedirectResponse('/login')
