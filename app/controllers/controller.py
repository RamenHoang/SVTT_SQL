from ..models.models import *
from ..utils.export_report import *

import datetime


def insert_sinh_vien_controller(MSSV, HoTen: str, GioiTinh: int, SDT: str, Email: str, DiaChi: str, MaLop: str, Truong: str, Nganh: str, Khoa: int) -> bool:
    result = insert_sinh_vien(MSSV, HoTen, GioiTinh,
                              SDT, Email, DiaChi, MaLop, Truong, Nganh, Khoa)
    return result


def get_all_sinh_vien_controller():
    return get_all_sinh_vien()


def count_all_sinh_vien_controller():
    return count_all_sinh_vien()


def get_so_luong_sinh_vien_theo_truong_controller():
    return get_so_luong_sinh_vien_theo_truong()


def get_so_luong_sinh_vien_theo_nganh_controller():
    return get_so_luong_sinh_vien_theo_nganh()


def get_user_info_by_username_controller(username: str):
    return get_user_info_by_username(username)


def ti_le_sinh_vien_da_danh_gia_controller():
    return ti_le_sinh_vien_da_danh_gia()


def so_luong_sinh_vien_dat_ket_qua_controller():
    return so_luong_sinh_vien_dat_ket_qua()


def get_all_de_tai_thuc_tap_controller():
    return get_all_de_tai_thuc_tap()


def get_chi_tiet_de_tai_by_id_controller(id: str):
    return get_chi_tiet_de_tai_by_id(id)


def update_chi_tiet_de_tai_by_id_controller(id: str, ten: str, mota: str, isDeleted: int):
    return update_chi_tiet_de_tai_by_id(id, ten, mota, isDeleted)


def update_xoa_de_tai_by_id_controller(id: str):
    return update_xoa_de_tai_by_id(id)


def get_nhom_thuc_tap_by_user_id_controller(id: str):
    return get_nhom_thuc_tap_by_user_id(id)


def them_de_tai_thuc_tap_controller(ten: str, mota: str, isDeleted: int):
    return them_de_tai_thuc_tap(ten, mota, isDeleted)


def get_all_ky_thuc_tap_controller():
    return get_all_ky_thuc_tap()


def get_chi_tiet_ky_thuc_tap_by_id_controller(id: str):
    return get_chi_tiet_ky_thuc_tap_by_id(id)


def update_chi_tiet_ky_thuc_tap_by_id_controller(id: str, ngaybatdau: str, ngayketthuc: str, isDeleted: int, ghichu: str):
    return update_chi_tiet_ky_thuc_tap_by_id(id, ngaybatdau, ngayketthuc, isDeleted, ghichu)


def them_ky_thuc_tap_controller(ngaybatdau: str, ngayketthuc: str, isDeleted: int, ghichu: str):
    return them_ky_thuc_tap(ngaybatdau, ngayketthuc, isDeleted, ghichu)


def update_xoa_ky_thuc_tap_by_id_controller(id: str):
    return update_xoa_ky_thuc_tap_by_id(id)


def get_ds_nhom_thuc_tap_by_nguoi_huong_dan_controller(username: str):
    result = get_ds_nhom_thuc_tap_by_nguoi_huong_dan(username)
    return result


def get_ds_nhom_thuc_tap_controller():
    result = get_ds_nhom_thuc_tap()
    return result


def get_chi_tiet_nhom_thuc_tap_by_id_controller(id: str):
    result = get_chi_tiet_nhom_thuc_tap_by_id(id)
    return result


def get_all_nguoi_huong_dan_controller():
    return get_all_nguoi_huong_dan()


def get_chi_tiet_chinh_sua_nhom_controller():
    return get_chi_tiet_chinh_sua_nhom()


def update_chi_tiet_nhom_thuc_tap_by_id_controller(id: int, kytt: int, nguoihd: int, detai: int, soluong: int, tennhom: str, telegram: str, ghichu: str, isDeleted: int):
    return update_chi_tiet_nhom_thuc_tap_by_id(id, kytt, nguoihd, detai, soluong, tennhom, telegram, isDeleted, ghichu)


def update_xoa_nhom_thuc_tap_by_id_controller(id: str):
    return update_xoa_nhom_thuc_tap_by_id(id)


def them_nhom_thuc_tap_controller(nguoihd: str, kytt: str, detai: str, soluong: int, tennhom: str, telegram: str, isDeleted: int, ghichu: str):
    return them_nhom_thuc_tap(nguoihd, kytt, detai, soluong, tennhom, telegram, isDeleted, ghichu)


def get_chi_tiet_sinh_vien_by_id_controller(id: str):
    return get_chi_tiet_sinh_vien_by_id(id)


def get_trang_thai_sinh_vien_by_id_controller(id: str):
    return get_trang_thai_sinh_vien_by_id(id)


def get_chi_tiet_sinh_vien_chua_co_nhom_controller(id: str):
    return get_chi_tiet_sinh_vien_chua_co_nhom(id)


def get_chi_tiet_sinh_vien_da_co_nhom_controller(id: str):
    return get_chi_tiet_sinh_vien_da_co_nhom(id)


def get_chi_tiet_sinh_vien_da_danh_gia_controller(id: str):
    return get_chi_tiet_sinh_vien_da_danh_gia(id)


def verify_user_controller(username: str, password: str):
    return verify_user(username, password)


def verify_student_controller(email: str, password: str):
    return verify_student(email, password)


def get_ds_sinh_vien_by_username_controller(username: str, kythuctap: str, nhomhuongdan: str):
    return get_ds_sinh_vien_by_username(username, kythuctap, nhomhuongdan)

def get_dssv_by_kttid_nhomid_username_controller(kythuctap_id: int, nhomhuongdan_id: int, username: str):
    return get_dssv_by_kttid_nhomid_username(kythuctap_id, nhomhuongdan_id, username)

def get_ds_chi_tiet_cong_viec_by_idsinhvien_controller(sinhvien_id: int):
    return get_ds_chi_tiet_cong_viec_by_idsinhvien(sinhvien_id)

def update_xac_nhan_trang_thai_cong_viec_controller(idcongviec: int, username: str):
    return update_xac_nhan_trang_thai_cong_viec(idcongviec, username)

def get_chi_tiet_danh_gia_sv_by_id_controller(id: str):
    return get_chi_tiet_danh_gia_sv_by_id(id)


def update_danh_gia_sv_by_id_controller(sinhvienid: str, nhomid: int, ythuckyluat_number: float, ythuckyluat_text: str, tuanthuthoigian_number: float, tuanthuthoigian_text: str, kienthuc_number: float, kienthuc_text: str, kynangnghe_number: float, kynangnghe_text: str, khanangdoclap_number: float, khanangdoclap_text: str, khanangnhom_number: float, khanangnhom_text: str, khananggiaiquyetcongviec_number: float, khananggiaiquyetcongviec_text: str, danhgiachung_number: float):
    return update_danh_gia_sv_by_id(sinhvienid, nhomid, ythuckyluat_number, ythuckyluat_text, tuanthuthoigian_number, tuanthuthoigian_text, kienthuc_number, kienthuc_text, kynangnghe_number, kynangnghe_text, khanangdoclap_number, khanangdoclap_text, khanangnhom_number, khanangnhom_text, khananggiaiquyetcongviec_number, khananggiaiquyetcongviec_text, danhgiachung_number)


def update_danh_gia_sv_by_mssv_controller(mssv: str, ythuckyluat_number: float, ythuckyluat_text: str, tuanthuthoigian_number: float, tuanthuthoigian_text: str, kienthuc_number: float, kienthuc_text: str, kynangnghe_number: float, kynangnghe_text: str, khanangdoclap_number: float, khanangdoclap_text: str, khanangnhom_number: float, khanangnhom_text: str, khananggiaiquyetcongviec_number: float, khananggiaiquyetcongviec_text: str, danhgiachung_number: float):
    return update_danh_gia_sv_by_mssv(mssv, ythuckyluat_number, ythuckyluat_text, tuanthuthoigian_number, tuanthuthoigian_text, kienthuc_number, kienthuc_text, kynangnghe_number, kynangnghe_text, khanangdoclap_number, khanangdoclap_text, khanangnhom_number, khanangnhom_text, khananggiaiquyetcongviec_number, khananggiaiquyetcongviec_text, danhgiachung_number)


def get_id_nhom_by_sv_id_controller(id: str):
    return get_id_nhom_by_sv_id(id)


def xuat_phieu_danh_gia_controller(id: str):
    try:
        result = get_chi_tiet_sinh_vien_da_danh_gia(id)
        return result
    except Exception as e:
        return e


def get_ds_nhom_chua_co_cong_viec_controller(username: str):
    return get_ds_nhom_chua_co_cong_viec(username)


def get_ds_cong_viec_nhom_controller():
    return get_ds_cong_viec_nhom()


def get_ds_cong_viec_by_id_nhom_controller(id: int):
    return get_ds_cong_viec_by_id_nhom(id)


def get_dssv_by_nhom_id_controller(id: int):
    return get_dssv_by_nhom_id(id)


def them_cong_viec_nhom_controller(id: int, ngaybatdau: str, ngayketthuc: str, ten: str, mota: str):
    return them_cong_viec_nhom(id, ngaybatdau, ngayketthuc, ten, mota)


def get_goi_y_xa_phuong_controller(q: str):
    return get_goi_y_xa_phuong(q)


def get_danh_sach_nganh_controller():
    return get_danh_sach_nganh()


def get_danh_sach_truong_controller():
    return get_danh_sach_truong()


def insert_thong_tin_sinh_vien_controller(mssv: str, hoten: str, gioitinh: int, sdt: str, email: str, diachi: str, malop: str, truong: str, nganh: str, khoa: int):
    return insert_sinh_vien(mssv, hoten, gioitinh, sdt, email, diachi, malop, truong, nganh, khoa)


def update_nhom_thuc_tap_by_sv_id_controller(email: str, idnhom: int):
    return update_nhom_thuc_tap_by_sv_id(email, idnhom)


def get_dssv_da_danh_gia_by_nguoi_huong_dan_controller(username: str, kythuctap: int):
    return get_dssv_da_danh_gia_by_nguoi_huong_dan(username=username, kythuctap=kythuctap)


def update_xoa_sinh_vien_by_id_controller(id: int):
    return update_xoa_sinh_vien_by_id(id)


def update_sinh_vien_by_id_controller(id: int, mssv: str, hoten: str, gioitinh: int, sdt: str, email: str, diachi: str, malop: str, truong: int, nganh: int, khoa: int):
    return update_sinh_vien_by_id(id, mssv, hoten, gioitinh, sdt, email, diachi, malop, truong, nganh, khoa)


def get_danh_sach_nhom_theo_ky_id_controller(id: int):
    return get_danh_sach_nhom_theo_ky_id(id)


def get_ho_ten_sv_by_email_controller(email: str):
    return get_ho_ten_sv_by_email(email)


def kiem_tra_loai_tai_khoan_controller(username: str):
    return kiem_tra_loai_tai_khoan(username)


def xem_thong_tin_sv_controller(email: str):
    return xem_thong_tin_sv(email)


def them_chi_tiet_cong_viec_controller(id_congviec: int, id_sinhvien: int, trangthai: int, ghichu: str):
    return them_chi_tiet_cong_viec(id_congviec, id_sinhvien, trangthai, ghichu)


def get_chi_tiet_cong_viec_by_id_cong_viec_controller(id: int):
    return get_chi_tiet_cong_viec_by_id_cong_viec(id)


def get_chi_tiet_cong_viec_by_id_controller(id: int):
    return get_chi_tiet_cong_viec_by_id(id)


def xoa_cong_viec_by_id_controller(id: int):
    return xoa_cong_viec_by_id(id)


def get_dssv_by_id_cong_viec_controller(id: int):
    return get_dssv_by_id_cong_viec(id)


def xoa_chi_tiet_cong_viec_by_id_controller(id: int):
    return xoa_chi_tiet_cong_viec_by_id(id)


def update_chi_tiet_cong_viec_by_id_controller(id: int, svid: int, ghichu: str):
    return update_chi_tiet_cong_viec_by_id(id, svid, ghichu)


def insert_danh_gia_thuc_tap_controller(sv_id: int, nhd_id: int, dapan_1: int, dapan_2: int, dapan_3: int, dapan_4: int, gopy: str):
    return insert_danh_gia_thuc_tap(sv_id, nhd_id, dapan_1, dapan_2, dapan_3, dapan_4, gopy)


def get_ds_chi_tiet_danh_gia_controller():
    return get_ds_chi_tiet_danh_gia()


def get_ds_chi_tiet_danh_gia_by_id_controller(id: int):
    return get_ds_chi_tiet_danh_gia_by_id(id)


def get_chi_tiet_giao_viec_cho_sv_by_id_cong_viec_controller(id: int, sv_id: int):
    return get_chi_tiet_giao_viec_cho_sv_by_id_cong_viec(id, sv_id)
