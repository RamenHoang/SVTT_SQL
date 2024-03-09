from ..config import create_connection
from ..send_otp import is_otp_valid
import datetime
import bleach

conn = create_connection()
cursor = conn.cursor()


def protect_xss(input: str):
    return bleach.clean(input, tags=['br'], attributes={})


def insert_sinh_vien(MSSV: str, HoTen: str, GioiTinh: int, SDT: str, Email: str, DiaChi: str, MaLop: str, Truong: str, Nganh: str, Khoa: int, Password: str) -> bool:
    try:
        result = cursor.execute("EXEC InsertSinhVien ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?", protect_xss(MSSV), protect_xss(
            HoTen), GioiTinh, protect_xss(SDT), protect_xss(Email), protect_xss(DiaChi), protect_xss(MaLop), Truong, Nganh, Khoa, 0)
        conn.commit()
        return result.fetchone()[0]
    except Exception as e:
        return e


def insert_taikhoan_sinhvien(sinhvien_id: int, password: str, is_verified: int):
    try:
        i = cursor.execute("EXEC InsertTaiKhoanSV ?, ?, ?",
                           sinhvien_id, protect_xss(password), is_verified)
        conn.commit()
        return True
    except Exception as e:
        return e


def verify_user(username: str, password: str):
    try:
        result = cursor.execute("LoginUser ?, ?", protect_xss(
            username), protect_xss(password)).fetchone()[0]
        if result == 1:
            return True
        else:
            return False
    except Exception as e:
        return e


def verify_student(email: str, password: str):
    try:
        result = cursor.execute("LoginStudent ?, ?", protect_xss(
            email), protect_xss(password)).fetchone()[0]
        if result == 1:
            return True
        else:
            return False
    except Exception as e:
        return e


def get_all_sinh_vien():
    try:
        result = cursor.execute("EXEC GetDSSVDashboard").fetchall()
        return result
    except Exception as e:
        return e


def count_all_sinh_vien():
    try:
        result = cursor.execute("SELECT COUNT(*) FROM SINHVIEN")
        return result.fetchone()[0]
    except Exception as e:
        return e


def ti_le_sinh_vien_da_danh_gia():
    try:
        sinhvientoihan = cursor.execute(
            "EXEC GetDSSVSapToiHanBaoCao").fetchone()[0]
        return sinhvientoihan
    except Exception as e:
        return e


def so_luong_sinh_vien_dat_ket_qua():
    try:
        result = cursor.execute("EXEC GetSoLuongSinhVienDatKetQua").fetchone()
        return {'dat': result[0], 'khong_dat': result[1]}
    except Exception as e:
        return e


def get_so_luong_sinh_vien_theo_truong():
    try:
        result = cursor.execute("EXEC GetSoLuongSinhVienTheoTruong")
        return [{'truong': i.Ten, 'soluong': i.SLSV} for i in result.fetchall()]
    except Exception as e:
        return e


def get_so_luong_sinh_vien_theo_nganh():
    try:
        result = cursor.execute("EXEC GetSoLuongSinhVienTheoNganh")
        return [{'nganh': i.NGANH, 'soluong': i.SL} for i in result.fetchall()]
    except Exception as e:
        return e


def get_trang_thai_sinh_vien_by_id(id: str):
    try:
        i = cursor.execute("EXEC GetTrangThaiSinhVienByID ?", id).fetchone()
        return {'id': i[0], 'trangthai': i[6]}
    except Exception as e:
        return e


def get_user_info_by_username(username: str):
    try:
        result = cursor.execute("EXEC GetUserInfo ?", username)
        return result.fetchone()
    except Exception as e:
        return e


def get_all_de_tai_thuc_tap():
    try:
        result = cursor.execute("SELECT * FROM DeTai WHERE isDeleted != 2")
        return [{'id': i[0], 'ten': i[1], 'mota': i[2], 'xoa': i[3]} for i in result.fetchall()]
    except Exception as e:
        return e


def get_chi_tiet_de_tai_by_id(id: str):
    try:
        result = cursor.execute("EXEC GetChiTietDeTaiByID ?", id).fetchone()
        return {'id': result[0], 'ten': result[1], 'mota': result[2], 'xoa': result[3]}
    except Exception as e:
        return e


def update_chi_tiet_de_tai_by_id(id: str, ten: str, mota: str, isDeleted: int):
    try:
        result = cursor.execute("EXEC UpdateChiTietDeTaiByID ?, ?, ?, ?", protect_xss(
            id), protect_xss(ten), protect_xss(mota), (isDeleted))
        conn.commit()
        return True
    except Exception as e:
        return e


def update_xoa_de_tai_by_id(id: str):
    try:
        result = cursor.execute(
            "EXEC UpdateXoaDeTaiByID ?", protect_xss(id)).fetchone()[0]
        conn.commit()
        if result == 1:
            return True
        else:
            return False
    except Exception as e:
        return e


def get_nhom_thuc_tap_by_user_id(id: str):
    try:
        result = cursor.execute("EXEC GetNhomThucTapByUserID ?", id).fetchall()
        data = [{'ngay': i[0], 'id': i[1], 'ten': i[2],
                 'mota': i[3], 'tennhom': i[5]} for i in result]
        return data
    except Exception as e:
        return e


def them_de_tai_thuc_tap(ten: str, mota: str, isDeleted: int):
    try:
        result = cursor.execute("EXEC InsertDeTai ?, ?, ?", protect_xss(
            ten), protect_xss(mota), isDeleted)
        conn.commit()
        return True
    except Exception as e:
        return e


def get_all_ky_thuc_tap():
    try:
        result = cursor.execute("EXEC GetDSDeTaiTheoThoiHan").fetchall()
        data = [{'id': i[0], 'ngaybatdau': i[1], 'ngayketthuc': i[2],
                 'thoihan': i[3], 'ghichu': i[4]} for i in result]
        return data
    except Exception as e:
        return e


def get_chi_tiet_ky_thuc_tap_by_id(id: str):
    try:
        result = cursor.execute(
            "EXEC GetChiTietKyThucTapByID ?", id).fetchone()
        return {'id': result[0], 'ngaybatdau': result[1], 'ngayketthuc': result[2], 'xoa': result[3], 'ghichu': result[4]}
    except Exception as e:
        return e


def update_chi_tiet_ky_thuc_tap_by_id(id: str, ngaybatdau: str, ngayketthuc: str, isDeleted: int, ghichu: str):
    try:
        result = cursor.execute("EXEC UpdateChiTietKyThucTapByID ?, ?, ?, ?, ?", protect_xss(
            id), protect_xss(ngaybatdau), protect_xss(ngayketthuc), (isDeleted), protect_xss(ghichu))
        conn.commit()
        return True
    except Exception as e:
        return e


def them_ky_thuc_tap(ngaybatdau: str, ngayketthuc: str, isDeleted: int, ghichu: str):
    try:
        result = cursor.execute("EXEC InsertKyThucTap ?, ?, ?, ?", protect_xss(
            ngaybatdau), protect_xss(ngayketthuc), isDeleted, protect_xss(ghichu))
        conn.commit()
        return True
    except Exception as e:
        return e


def update_xoa_ky_thuc_tap_by_id(id: str):
    try:
        result = cursor.execute(
            "EXEC UpdateXoaKyThucTapByID ?", protect_xss(id)).fetchone()[0]
        conn.commit()
        if result == 1:
            return True
        else:
            return False
    except Exception as e:
        return e


def get_ds_nhom_thuc_tap_by_nguoi_huong_dan(username: str):
    try:
        result = cursor.execute(
            "EXEC GetDSNhomThucTapByNguoiHuongDanUsername ?", username)
        data = [{'id': i[0], 'nguoihuongdan': i[2], 'ngaybatdau': i[3], 'tendetai': i[5], 'mota': i[6],
                 'xoa': i[1], 'soluong': i[10], 'ghichu': i[11], 'tennhom': i[12]} for i in result]
        return data
    except Exception as e:
        return e


def get_ds_nhom_thuc_tap():
    try:
        result = cursor.execute("EXEC GetDSNhomThucTap")
        data = [{'id': i[0], 'nguoihuongdan': i[2], 'ngaybatdau': i[3], 'tendetai': i[5], 'mota': i[6],
                 'xoa': i[1], 'soluong': i[10], 'ghichu': i[11], 'tennhom': i[12], 'telegram_id': i[13]} for i in result]
        return data
    except Exception as e:
        return e


def get_chi_tiet_nhom_thuc_tap_by_id(id: str):
    try:
        i = cursor.execute("EXEC GetChiTietNhomThucTapByID ?", id).fetchone()
        return {'id': i[0], 'nguoihuongdan_hoten': i[9], 'nguoihuongdan_id': i[1], 'nguoihuongdan_username': i[15], 'kythuctap_id': i[2], 'kythuctap_ngaybatdau': i[9], 'kythuctap_ngayketthuc': i[10], 'detai_id': i[3], 'detai_ten': i[11], 'detai_mota': i[13], 'nhomthuctap_dadangky': i[14], 'nhomthuctap_soluong': i[4], 'xoa': i[5], 'ghichu': i[6], 'nhomthuctap_tennhom': i[7], 'nhomthuctap_telegram': i[8]}
    except Exception as e:
        return e


def get_all_nguoi_huong_dan():
    try:
        result = cursor.execute("EXEC GetAllNguoiHuongDan").fetchall()
        return [{'id': i[0], 'hoten': i[1]} for i in result]
    except Exception as e:
        return e


def get_chi_tiet_chinh_sua_nhom():
    try:
        ktt_obj = cursor.execute(
            "SELECT ID, NgayBatDau FROM KyThucTap WHERE isDeleted != 2").fetchall()
        nhd_obj = cursor.execute(
            "SELECT ID, HoTen FROM NguoiHuongDan").fetchall()
        detai_obj = cursor.execute(
            "SELECT ID, Ten FROM DeTai WHERE isDeleted != 2").fetchall()

        ktt = [{'id': i[0], 'ngay': i[1]} for i in ktt_obj]
        nhd = [{'id': i[0], 'hoten': i[1]} for i in nhd_obj]
        detai = [{'id': i[0], 'ten': i[1]} for i in detai_obj]

        return {'kythuctap': ktt, 'nguoihuongdan': nhd, 'detai': detai}
    except Exception as e:
        return e


def update_chi_tiet_nhom_thuc_tap_by_id(id: int, kytt: int, nguoihd: int, detai: int, soluong: int, tennhom: str, telegram: str, isDeleted: int, ghichu: str):
    try:
        result = cursor.execute("EXEC UpdateChiTietNhomThucTapByID ?, ?, ?, ?, ?, ?, ?, ?, ?", id, kytt, nguoihd,
                                detai, soluong, isDeleted, protect_xss(ghichu), protect_xss(tennhom), protect_xss(telegram))
        conn.commit()
        return True
    except Exception as e:
        return e


def update_xoa_nhom_thuc_tap_by_id(id: str):
    try:
        result = cursor.execute(
            "EXEC UpdateXoaNhomThucTapByID ?", protect_xss(id)).fetchone()[0]
        conn.commit()
        return True if result == 1 else False
    except Exception as e:
        return e


def them_nhom_thuc_tap(nguoihd: str, kytt: str, detai: str, soluong: int, tennhom: str, telegram: str, isDeleted: int, ghichu: str):
    try:
        result = cursor.execute("EXEC InsertNhomThucTap ?, ?, ?, ?, ?, ?, ?, ?", protect_xss(nguoihd), protect_xss(
            kytt), protect_xss(detai), soluong, isDeleted, protect_xss(ghichu), protect_xss(tennhom), protect_xss(telegram))
        conn.commit()
        return True
    except Exception as e:
        return e


def get_chi_tiet_sinh_vien_by_id(id: str):
    try:
        i = cursor.execute("EXEC GetThongTinChiTietSVByID ?", id).fetchone()
        return {'id': i[0], 'mssv': i[1], 'hoten': i[2], 'gioitinh': 'nam' if i[3] == 1 else 'nữ', 'sdt': f'0{i[4]}', 'email': i[5], 'diachi': i[6], 'malop': i[7], 'khoa': i[8], 'nganh': i[9], 'truong': i[10], 'tendetai': i[12], 'ngaybatdau': i[13], 'nguoihuongdan': i[14]}
    except Exception as e:
        return e


def get_chi_tiet_sinh_vien_chua_co_nhom(id: str):
    try:
        i = cursor.execute(
            "EXEC GetThongTinChiTietSVChuaCoNhomByID ?", id).fetchone()
        return {'id': i[0], 'mssv': i[1], 'hoten': i[2], 'gioitinh': i[3], 'sdt': f'{i[4]}', 'email': i[5], 'diachi': i[6], 'malop': i[7], 'khoa': i[8], 'nganh': i[9], 'id_nganh': i[10], 'truong': i[11], 'id_truong': i[12]}
    except Exception as e:
        return e


def get_chi_tiet_sinh_vien_da_co_nhom(id: str):
    try:
        i = cursor.execute(
            "EXEC GetThongTinChiTietSVDaCoNhomByID ?", id).fetchone()
        return {'id': i[0], 'mssv': i[1], 'hoten': i[2], 'gioitinh': i[3], 'sdt': f'{i[4]}', 'email': i[5], 'diachi': i[6], 'malop': i[7], 'khoa': i[8], 'nganh': i[9], 'id_nganh': i[10], 'truong': i[11], 'id_truong': i[12], 'nguoihuongdan': i[13], 'ngaybatdau': i[14], 'tendetai': i[15], 'tennhom': i[16]}
    except Exception as e:
        return e


def get_chi_tiet_sinh_vien_da_danh_gia(id: str):
    try:
        i = cursor.execute(
            "EXEC GetThongTinChiTietSVDaDanhGiaByID ?", id).fetchone()
        return {'id': i[0], 'mssv': i[1], 'hoten': i[2], 'gioitinh': i[3], 'sdt': f'{i[4]}', 'email': i[5], 'diachi': i[6], 'malop': i[7], 'khoa': i[8], 'nganh': i[9], 'id_nganh': i[10], 'truong': i[11], 'id_truong': i[12], 'nguoihuongdan': i[13], 'ngaybatdau': i[14], 'tendetai': i[15], 'ythuckyluat_number': i[19], 'ythuckyluat_text': i[20], 'tuanthuthoigian_number': i[21], 'tuanthuthoigian_text': i[22], 'kienthuc_number': i[23], 'kienthuc_text': i[24], 'kynangnghe_number': i[25], 'kynangnghe_text': i[26], 'khanangdoclap_number': i[27], 'khanangdoclap_text': i[28], 'khanangnhom_number': i[29], 'khanangnhom_text': i[30], 'khananggiaiquyetcongviec_number': i[31], 'khananggiaiquyetcongviec_text': i[32], 'danhgiachung_number': i[33], 'tennhom': i[34]}
    except Exception as e:
        return e


def get_ds_sinh_vien_by_username(username: str, kythuctap: str, nhomhuongdan: str):
    try:
        result = cursor.execute(
            "EXEC GetDSSVByNguoiHuongDanID ?, ?, ?", protect_xss(username), protect_xss(kythuctap), protect_xss(nhomhuongdan))
        handanhgia = 0
        # ngayketthuc = get_han_thuc_tap_by_nhom_id(int(nhomhuongdan))['ngayketthuc']
        # print(ngayketthuc)
        # if (datetime.datetime.now() - datetime.timedelta(days=3)) <= datetime.datetime.strptime(ngayketthuc, "%Y-%m-%d"):
        #     handanhgia = 1
        # else:
        #     handanhgia = 0

        return [{'id': i[0], 'mssv': i[1], 'hoten': i[2], 'gioitinh': 'Nam' if i[3] == 1 else 'Nữ', 'nganh': i[4], 'truong': i[5], 'trangthai': i[6], 'detai': i[7], 'nhom': i[8], 'tennhom': i[9], 'handanhgia': handanhgia} for i in result]
    except Exception as e:
        return e


def get_dssv_by_kttid_nhomid_username(kythuctap_id: int, nhomhuongdan_id: int, username: str):
    try:
        result = cursor.execute("EXEC GetDSSVByKTTID_NhomID_NHDUsername ?, ?, ?",
                                kythuctap_id, nhomhuongdan_id, protect_xss(username))
        return [{'id': i[0], 'mssv': i[1], 'hoten': i[2]} for i in result.fetchall()]
    except Exception as e:
        return e


def get_ds_chi_tiet_cong_viec_by_idsinhvien(sinhvien_id: int):
    try:
        result = cursor.execute(
            "EXEC GetDSChiTietCongViecByIDSinhVien ?", sinhvien_id)
        return [{'id': i[0], 'ngaybatdau': i[1], 'ngayketthuc': i[2], 'tencongviec': i[3], 'mota': i[4], 'ghichu': i[5], 'trangthai': i[6], 'xacnhan': i[7]} for i in result.fetchall()]
    except Exception as e:
        return e


def update_xac_nhan_trang_thai_cong_viec(idcongviec: int, username: str):
    try:
        result = cursor.execute("EXEC UpdateXacNhanTrangThaiCongViec ?, ?",
                                idcongviec, protect_xss(username)).fetchone()[0]
        cursor.commit()
        if result == 1:
            return True
        else:
            return False
    except Exception as e:
        return e


def update_sv_xac_nhan_hoan_thanh_cong_viec(idcongviec: int, email: str):
    try:
        result = cursor.execute("EXEC UpdateSVXacHoanThanhThaiCongViec ?, ?",
                                idcongviec, protect_xss(email)).fetchone()[0]
        cursor.commit()
        if result == 1:
            return True
        else:
            return False
    except Exception as e:
        return e


def get_chi_tiet_danh_gia_sv_by_id(id: str):
    try:
        i = cursor.execute("EXEC GetChiTietDanhGiaSVByID ?", id).fetchone()
        return {'ythuckyluat_number': i[3], 'ythuckyluat_text': i[4], 'tuanthuthoigian_number': i[5], 'tuanthuthoigian_text': i[6], 'kienthuc_number': i[7], 'kienthuc_text': i[8], 'kynangnghe_number': i[9], 'kynangnghe_text': i[10], 'khanangdoclap_number': i[11], 'khanangdoclap_text': i[12], 'khanangnhom_number': i[13], 'khanangnhom_text': i[14], 'khananggiaiquyetcongviec_number': i[15], 'khananggiaiquyetcongviec_text': i[16], 'danhgiachung_number': i[17]}
    except Exception as e:
        return e


def get_han_thuc_tap_by_nhom_id(id: int):
    try:
        i = cursor.execute("EXEC GetHanThucTapByIDNhom ?", id).fetchone()
        return {'id': i[0], 'ngaybatdau': i[1], 'ngayketthuc': i[2]}
    except Exception as e:
        return e


def update_danh_gia_sv_by_id(sinhvienid: str, nhomid: int, ythuckyluat_number: float, ythuckyluat_text: str, tuanthuthoigian_number: float, tuanthuthoigian_text: str, kienthuc_number: float, kienthuc_text: str, kynangnghe_number: float, kynangnghe_text: str, khanangdoclap_number: float, khanangdoclap_text: str, khanangnhom_number: float, khanangnhom_text: str, khananggiaiquyetcongviec_number: float, khananggiaiquyetcongviec_text: str, danhgiachung_number: float):
    try:
        thongtinnhom = get_han_thuc_tap_by_nhom_id(nhomid)
        # datetime.timedelta(days=3) số ngày được phép đánh giá/sửa đánh giá sau khi kết thúc kỳ thực tập
        if (datetime.datetime.now() - datetime.timedelta(days=3)).date() <= thongtinnhom['ngayketthuc']:
            result = cursor.execute("EXEC UpdateDanhGiaSVByID ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?", protect_xss(sinhvienid), nhomid, ythuckyluat_number, protect_xss(ythuckyluat_text), tuanthuthoigian_number, protect_xss(tuanthuthoigian_text), kienthuc_number, protect_xss(
                kienthuc_text), kynangnghe_number, protect_xss(kynangnghe_text), khanangdoclap_number, protect_xss(khanangdoclap_text), khanangnhom_number, protect_xss(khanangnhom_text), khananggiaiquyetcongviec_number, protect_xss(khananggiaiquyetcongviec_text), danhgiachung_number)
            cursor.commit()
            return True
        else:
            return False
    except Exception as e:
        return e


def update_danh_gia_sv_by_mssv(mssv: str, ythuckyluat_number: float, ythuckyluat_text: str, tuanthuthoigian_number: float, tuanthuthoigian_text: str, kienthuc_number: float, kienthuc_text: str, kynangnghe_number: float, kynangnghe_text: str, khanangdoclap_number: float, khanangdoclap_text: str, khanangnhom_number: float, khanangnhom_text: str, khananggiaiquyetcongviec_number: float, khananggiaiquyetcongviec_text: str, danhgiachung_number: float):
    try:
        result = cursor.execute("EXEC UpdateDanhGiaSVByMSSV ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?", protect_xss(mssv), ythuckyluat_number, protect_xss(ythuckyluat_text), tuanthuthoigian_number, protect_xss(tuanthuthoigian_text), kienthuc_number, protect_xss(
            kienthuc_text), kynangnghe_number, protect_xss(kynangnghe_text), khanangdoclap_number, protect_xss(khanangdoclap_text), khanangnhom_number, protect_xss(khanangnhom_text), khananggiaiquyetcongviec_number, protect_xss(khananggiaiquyetcongviec_text), danhgiachung_number)
        cursor.commit()
        return True
    except Exception as e:
        return e


def get_id_nhom_by_sv_id(id: str):
    try:
        i = cursor.execute("EXEC GetIDNhomBySVID ?",
                           protect_xss(id)).fetchone()
        return int(i[0])
    except Exception as e:
        return e


def get_ds_nhom_chua_co_cong_viec(username: str):
    """
        Get danh sách nhóm chưa có công việc bằng ID người hướng dẫn
    """
    try:
        result = cursor.execute(
            "EXEC [GetDSNhomChuaCoCongViecByNguoiHDUsername] ?", protect_xss(username))
        data = [{'id': i[0], 'ngaybatdau': i[3], 'tendetai': i[5],
                 'idcongviec': i[7], 'tennhom': i[8]} for i in result]
        return data
    except Exception as e:
        return e


def get_ds_cong_viec_nhom():
    try:
        result = cursor.execute("EXEC GetDSCongViecNhom").fetchall()
        data = [{'id': i[0], 'ten_nhom': i[1], 'ngaybatdau': i[2],
                 'ngayketthuc': i[3], 'ten': i[4], 'mota': i[5]} for i in result]
        return data
    except Exception as e:
        return e


def get_ds_cong_viec_by_id_nhom(id: int):
    try:
        result = cursor.execute("EXEC GetCongViecByIDNhom ?", id).fetchall()
        data = [{'id': i[0], 'ngaybatdau': i[1], 'ngayketthuc': i[2],
                 'ten': i[3], 'mota': i[4]} for i in result]
        return data
    except Exception as e:
        return e


def get_chi_tiet_cong_viec_by_id_cong_viec(id: int):
    try:
        result = cursor.execute(
            "EXEC GetChiTietCongViecByIDCongViec ?", id).fetchall()
        data = [{'id': i[0], 'id_congviec': i[1], 'id_sinhvien': i[2], 'trangthai': i[3],
                 'ghichu': i[4], 'tencongviec': i[5], 'nguoithuchien': i[6]} for i in result]
        return data
    except Exception as e:
        return e


def get_chi_tiet_cong_viec_by_id(id: int):
    try:
        result = cursor.execute("EXEC GetChiTietCongViecByID ?", id).fetchall()
        data = [{'id': i[0], 'id_congviec': i[1], 'id_sinhvien': i[2],
                 'trangthai': i[3], 'ghichu': i[4]} for i in result]
        return data
    except Exception as e:
        return e


def update_chi_tiet_cong_viec_by_id(id: int, svid: int, ghichu: str):
    try:
        result = cursor.execute(
            "EXEC UpdateChiTietCongViecByID ?, ?, ?", id, svid, protect_xss(ghichu))
        cursor.commit()
        if result.fetchone()[0] == 1:
            return True
        else:
            return False
    except Exception as e:
        return e


def xoa_chi_tiet_cong_viec_by_id(id: int):
    try:
        result = cursor.execute("EXEC UpdateXoaChiTietCongViecByID ?", id)
        cursor.commit()
        if result.fetchone()[0] == 1:
            return True
        else:
            return False
    except Exception as e:
        return e


def xoa_cong_viec_by_id(id: int):
    try:
        result = cursor.execute(
            "EXEC UpdateXoaCongViecByID ?", id).fetchone()[0]
        cursor.commit()
        if result == 1:
            return True
        else:
            return False
    except Exception as e:
        return e


def them_cong_viec_nhom(id: int, ngaybatdau: str, ngayketthuc: str, ten: str, mota: str):
    try:
        result = cursor.execute("EXEC InsertCongViec ?, ?, ?, ?, ?", id, protect_xss(
            ngaybatdau), protect_xss(ngayketthuc), protect_xss(ten), protect_xss(mota)).fetchone()
        cursor.commit()
        if result[0] == 1:
            return True
        else:
            return False
    except Exception as e:
        return e


def them_chi_tiet_cong_viec(id_congviec: int, id_sinhvien: int, trangthai: int, ghichu: str):
    try:
        # Gọi stored procedure và truyền tham số
        result = cursor.execute("EXEC InsertChiTietCongViec ?, ?, ?, ?", id_congviec,
                                id_sinhvien, trangthai, protect_xss(ghichu)).fetchone()[0]
        # Lấy giá trị của biến đầu ra
        cursor.commit()
        return result
    except Exception as e:
        return e


def get_dssv_by_id_cong_viec(id: int):
    try:
        result = cursor.execute("EXEC GetDSSVByIDCongViec ?", id).fetchall()
        return [{'id': i[0], 'hoten': i[1]} for i in result]
    except Exception as e:
        return e


def get_dssv_by_nhom_id(id: int):
    try:
        result = cursor.execute("EXEC GetDSSVByNhomID ?", id).fetchall()
        return [{'id': i[0], 'hoten': i[1], 'danhgia': i[2]} for i in result]
    except Exception as e:
        return e


def get_goi_y_xa_phuong(q: str):
    try:
        result = cursor.execute(
            "SELECT DiaChi FROM XaPhuong WHERE DiaChi LIKE '%' + ? + '%'", q).fetchall()
        return [i[0] for i in result]
    except Exception as e:
        return e


def get_danh_sach_nganh():
    try:
        result = cursor.execute("SELECT ID, Ten FROM Nganh").fetchall()
        return [{'id': i[0], 'ten': i[1]} for i in result]
    except Exception as e:
        return e


def get_danh_sach_truong():
    try:
        result = cursor.execute("SELECT ID, Ten FROM Truong").fetchall()
        return [{'id': i[0], 'ten': i[1]} for i in result]
    except Exception as e:
        return e


def update_nhom_thuc_tap_by_sv_id(email: str, idnhom: int):
    try:
        # Kiểm tra xem đã đủ số lượng chưa
        registed = cursor.execute(
            "EXEC GetSoLuongSVDaDangKyByNhomID ?", idnhom).fetchone()[0]
        quantity = cursor.execute(
            "SELECT SoLuong FROM NHOMHUONGDAN WHERE ID = ?", idnhom).fetchone()[0]
        if (registed < quantity):
            result = cursor.execute(
                "EXEC UpdateNhomThucTapBySinhVienEmail ?, ?", protect_xss(email), idnhom)
            r = result.fetchone()[0]
            cursor.commit()
            if r:
                return r
            else:
                return False
        else:
            return False
    except Exception as e:
        return e


def get_dssv_da_danh_gia_by_nguoi_huong_dan(username: str, kythuctap: int):
    try:
        result = cursor.execute("EXEC GetDSSVDanhGiaByNguoiHuongDanUsername ?, ?", protect_xss(
            username), kythuctap).fetchall()
        return [{'mssv': i[21], 'hoten': i[18], 'malop': i[19], 'nguoihuongdan': i[20], 'ythuckyluat_text': i[4], 'ythuckyluat_number': i[3], 'tuanthuthoigian_text': i[6], 'tuanthuthoigian_number': i[5], 'kienthuc_text': i[8], 'kienthuc_number': i[7], 'kynangnghe_text': i[10], 'kynangnghe_number': i[9], 'khanangdoclap_text': i[12], 'khanangdoclap_number': i[11], 'khanangnhom_text': i[14], 'khanangnhom_number': i[13], 'khananggiaiquyetcongviec_text': i[16], 'khananggiaiquyetcongviec_number': i[15], 'danhgiachung_number': i[17]} for i in result]
    except Exception as e:
        return e


def update_xoa_sinh_vien_by_id(id: int):
    try:
        result = cursor.execute(
            "EXEC UpdateXoaSinhVienByID ?", id).fetchone()[0]
        cursor.commit()
        return result
    except Exception as e:
        return e


def update_sinh_vien_by_id(id: int, mssv: str, hoten: str, gioitinh: int, sdt: str, email: str, diachi: str, malop: str, truong: int, nganh: int, khoa: int):
    try:
        result = cursor.execute("EXEC UpdateSinhVienByID ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?", id, protect_xss(mssv), protect_xss(
            hoten), gioitinh, protect_xss(sdt), protect_xss(email), protect_xss(diachi), protect_xss(malop), truong, nganh, khoa)
        r = cursor.fetchone()[0]
        cursor.commit()
        return r
    except Exception as e:
        return e


def get_danh_sach_nhom_theo_ky_id(id: int):
    try:
        result = cursor.execute("EXEC GetDSNhomTheoKyID ?", id)
        return [{'id': i[0], 'tennhom': i[1], 'tendetai': i[2]} for i in result.fetchall()]
    except Exception as e:
        return e


def get_ho_ten_sv_by_email(email: str):
    try:
        result = cursor.execute("EXEC GetHoTenSVByEmail ?", protect_xss(email))
        return result.fetchone()[0]
    except Exception as e:
        return e


def kiem_tra_loai_tai_khoan(username: str):
    username = protect_xss(username)
    try:
        if username:
            if '@' in username:
                result = cursor.execute(
                    "SELECT ID FROM SINHVIEN WHERE Email = ?", username)
                if result.fetchone()[0]:
                    return 2
            else:
                result = cursor.execute(
                    "SELECT ID FROM NGUOIHUONGDAN WHERE Username = ?", username)
                if result.fetchone()[0]:
                    return 1
        else:
            return 0
    except Exception as e:
        return e


def xem_thong_tin_sv(email: str):
    email = protect_xss(email)
    try:
        result = cursor.execute("EXEC GetChiTietSVByEmail ?", email)
        if result:
            i = result.fetchone()
            return {'id': i[0], 'mssv': i[1], 'hoten': i[2], 'gioitinh': i[3], 'sdt': i[4], 'email': i[5], 'diachi': i[6], 'malop': i[7], 'truong': i[14], 'nganh': i[15], 'khoa': i[10], 'nhomhuongdan': i[16], 'xacnhan': i[12]}
    except Exception as e:
        return e


def insert_danh_gia_thuc_tap(sv_id: int, nhd_id: int, dapan_1: int, dapan_2: int, dapan_3: int, dapan_4: int, gopy: str):
    try:
        check = cursor.execute(
            "SELECT COUNT(ID) FROM CHITIET_DANHGIA WHERE ID_SinhVien = ?", sv_id).fetchone()[0]
        if check == 0:
            result = cursor.execute("EXEC InsertChiTietDanhGia ?, ?, ?, ?, ?, ?, ?",
                                    sv_id, nhd_id, dapan_1, dapan_2, dapan_3, dapan_4, protect_xss(gopy))
            cursor.commit()
            if result.fetchone()[0]:
                return True
        else:
            return False
    except Exception as e:
        return e


def get_ds_chi_tiet_danh_gia():
    try:
        result = cursor.execute("EXEC GetDSChiTietDanhGia").fetchall()
        if result:
            return [{'id': i[0], 'id_sinhvien': i[1], 'mssv': i[8], 'hoten_sinhvien': i[9], 'tennhom': i[10], 'ngaybatdau': i[12], 'nguoihuongdan_ten': i[13], 'nguoihuongdan_id': i[14], 'tendetai': i[15]} for i in result]
        else:
            return []
    except Exception as e:
        return e


def get_ds_chi_tiet_danh_gia_by_id(id: int):
    try:
        i = cursor.execute("EXEC GetDSChiTietDanhGiaByID ?", id).fetchone()
        return {'id': i[0], 'dapan_1': i[3], 'dapan_2': i[4], 'dapan_3': i[5], 'dapan_4': i[6], 'gopy': i[7], 'mssv': i[8], 'hoten': i[9], 'tennhom': i[10], 'kythuctap': i[12], 'nguoihuongdan': i[13], 'detai': i[15]}
    except Exception as e:
        return e


def check_sv_con_han_thuc_tap(email: str):
    try:
        i = cursor.execute("EXEC CheckSVConHanThucTapByEmail ?",
                           protect_xss(email)).fetchone()
        return i
    except Exception as e:
        return False


def get_chi_tiet_giao_viec_cho_sv_by_id_cong_viec(id: int, sv_id: int):
    try:
        result = cursor.execute(
            "EXEC GetChiTietGiaoViecChoSVByIDCongViec ?, ?", id, sv_id).fetchone()
        return {'nguoinhanviec': result[0], 'mssv': result[1], 'nguoigiaoviec': result[2], 'tencongviec': result[3], 'ngaybatdau': result[4], 'ngayketthuc': result[5], 'ghichu': result[6], 'motacongviec': result[7], 'telegram_id': result[8]}
    except Exception as e:
        return e


def get_ds_congviec_by_sinhvien_email(email: str):
    try:
        idNhom = cursor.execute(
            "EXEC GetChiTietSVByEmail ?", protect_xss(email)).fetchone()[11]
        return get_ds_cong_viec_by_id_nhom(idNhom)
    except Exception as e:
        return e


def get_chi_tiet_cong_viec_by_id_cong_viec_email_sv(id: int, email: str):
    try:
        result = cursor.execute(
            "EXEC GetChiTietCongViecByIDCongViecEmailSV ?, ?", id, protect_xss(email)).fetchone()
        data = [{'id': result[0], 'id_congviec': result[1], 'id_sinhvien': result[2],
                 'ghichu': result[3], 'tencongviec': result[4], 'nguoithuchien': result[5], 'trangthai': result[6], 'xacnhan': result[7]}]
        return data
    except Exception as e:
        return e


def update_password(username: str, password: str):
    try:
        result = cursor.execute("EXEC UpdatePassword ?, ?", protect_xss(username), protect_xss(password))
        cursor.commit()
        return result.fetchone()[0]
    except Exception as e:
        return e


def get_phan_quyen(username: str):
    try:
        result = cursor.execute("EXEC GetPhanQuyenByUsername ?", protect_xss(username))
        # Role: {0: "user", 1: "administrator"}
        return "admin" if result.fetchone()[0] == 1 else "user"
    except Exception as e:
        return e
    

def get_ds_tai_khoan():
    try:
        result = cursor.execute("EXEC GetDSTaiKhoanNguoiHuongDan").fetchall()
        return [{'id': i[0], 'hoten': i[1], 'username': i[2], 'email': i[3], 'role': i[4], 'trangthai': i[5]} for i in result]
    except Exception as e:
        return e


def update_xoa_nguoi_huong_dan_by_id(id: int):
    try:
        result = cursor.execute("EXEC UpdateXoaNguoiHuongDanByID ?", id).fetchone()
        cursor.commit()
        return result[0]
    except Exception as e:
        return e


def update_ban_nguoi_huong_dan_by_id(id: int):
    try:
        result = cursor.execute("EXEC UpdateBanNguoiHuongDanByID ?", id).fetchone()
        cursor.commit()
        return result[0]
    except Exception as e:
        return e


def update_active_nguoi_huong_dan_by_id(id: int):
    try:
        result = cursor.execute("EXEC UpdateActiveNguoiHuongDanByID ?", id).fetchone()
        cursor.commit()
        return result[0]
    except Exception as e:
        return e


def update_reset_mat_khau_nguoi_huong_dan_by_id(id: int, password: str):
    try:
        result = cursor.execute("EXEC UpdateResetMatKhauNguoiHuongDanByID ?, ?", id, protect_xss(password)).fetchone()
        cursor.commit()
        return result[0]
    except Exception as e:
        return e


def update_phan_quyen_nguoi_huong_dan_by_id(id: int, role: int):
    try:
        result = cursor.execute("EXEC UpdateQuyenNguoiHuongDanByID ?, ?", id, role).fetchone()
        cursor.commit()
        return result[0]
    except Exception as e:
        return e


def get_thong_tin_nguoi_huong_dan_by_id(id: int):
    try:
        result = cursor.execute("EXEC GetChiTietTaiKhoanByID ?", id).fetchone()
        return {'id': result[0], 'hoten': result[1], 'sdt': result[2], 'email': result[3], 'chucdanh': result[4], 'phong': result[5], 'zalo': result[6], 'facebook': result[7], 'github': result[8], 'avatar': result[9]}
    except Exception as e:
        return e


def update_chi_tiet_tai_khoan_by_id(id: int, hoten: str, sdt: str, email: str, chucdanh: str, phong: str, zalo: str, facebook: str, github: str, avatar: str):
    try:
        result = cursor.execute("EXEC UpdateChiTietTaiKhoanByID ?, ?, ?, ?, ?, ?, ?, ?, ?, ?", id, protect_xss(hoten), protect_xss(sdt), protect_xss(email), protect_xss(chucdanh), protect_xss(phong), protect_xss(zalo), protect_xss(facebook), protect_xss(github), protect_xss(avatar)).fetchone()
        cursor.commit()
        print(result)
        return result[0]
    except Exception as e:
        return e