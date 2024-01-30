from ..config import create_connection
from ..send_otp import is_otp_valid
import datetime

conn = create_connection()
cursor = conn.cursor()

def insert_sinh_vien(MSSV: str, HoTen: str, GioiTinh: int, SDT: str, Email: str, DiaChi: str, MaLop: str, Truong: str, Nganh: str, Khoa: int) -> bool:
    try:
        i = cursor.execute("EXEC InsertSinhVien ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?", MSSV, HoTen, GioiTinh, SDT, Email, DiaChi, MaLop, Truong, Nganh, Khoa, 0).fetchone()
        result = i[0]
        conn.commit()
        return result
    except Exception as e:
        return False
    
def verify_user(username: str, password: str):
    try:
        cursor.execute("LoginUser ?, ?", username, password)
        result = cursor.fetchone()

        if not result or not result.IsValidUser:
            return False
        return True
    except Exception as e:
        return e

def verify_student(email: str, otp: int):
    try:
        result = is_otp_valid(email, otp)

        if not result:
            return False
        return True
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
        sinhvientoihan = cursor.execute("EXEC GetDSSVSapToiHanBaoCao").fetchone()[0]
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
        result = cursor.execute("EXEC UpdateChiTietDeTaiByID ?, ?, ?, ?", id, ten, mota, isDeleted)
        conn.commit()
        return True
    except Exception as e:
        return e
    
def update_xoa_de_tai_by_id(id: str):
    try:
        result = cursor.execute("EXEC UpdateXoaDeTaiByID ?", id)
        conn.commit()
        return True
    except Exception as e:
        return e
    
def get_nhom_thuc_tap_by_user_id(id: str):
    try:
        result = cursor.execute("EXEC GetNhomThucTapByUserID ?", id).fetchall()
        data = [{'ngay': i[0], 'id': i[1], 'ten': i[2], 'mota': i[3], 'tennhom': i[5]} for i in result]
        return data
    except Exception as e:
        return e

def them_de_tai_thuc_tap(ten: str, mota: str, isDeleted: int):
    try:
        result = cursor.execute("EXEC InsertDeTai ?, ?, ?", ten, mota, isDeleted)
        conn.commit()
        return True
    except Exception as e:
        return e
    
def get_all_ky_thuc_tap():
    try:
        result = cursor.execute("EXEC GetDSDeTaiTheoThoiHan").fetchall()
        data = [{'id': i[0], 'ngaybatdau': i[1], 'ngayketthuc': i[2], 'thoihan': i[3], 'ghichu': i[4]} for i in result]
        return data
    except Exception as e:
        return e
    
def get_chi_tiet_ky_thuc_tap_by_id(id: str):
    try:
        result = cursor.execute("EXEC GetChiTietKyThucTapByID ?", id).fetchone()
        return {'id': result[0], 'ngaybatdau': result[1], 'ngayketthuc': result[2], 'xoa': result[3], 'ghichu': result[4]}
    except Exception as e:
        return e
    
def update_chi_tiet_ky_thuc_tap_by_id(id: str, ngaybatdau: str, ngayketthuc: str, isDeleted: int, ghichu: str):
    try:
        result = cursor.execute("EXEC UpdateChiTietKyThucTapByID ?, ?, ?, ?, ?", id, ngaybatdau, ngayketthuc, isDeleted, ghichu)
        conn.commit()
        return True
    except Exception as e:
        return e
    
def them_ky_thuc_tap(ngaybatdau: str, ngayketthuc: str, isDeleted: int, ghichu: str):
    try:
        result = cursor.execute("EXEC InsertKyThucTap ?, ?, ?, ?", ngaybatdau, ngayketthuc, isDeleted, ghichu)
        conn.commit()
        return True
    except Exception as e:
        return e
    
def update_xoa_ky_thuc_tap_by_id(id: str):
    try:
        result = cursor.execute("EXEC UpdateXoaKyThucTapByID ?", id)
        conn.commit()
        return True
    except Exception as e:
        return e
    
def get_ds_nhom_thuc_tap():
    try:
        result = cursor.execute("EXEC GetDSNhomThucTap")
        data = [{'id': i[0], 'nguoihuongdan': i[2], 'ngaybatdau': i[3], 'tendetai': i[5], 'mota': i[6], 'xoa': i[1], 'soluong': i[10], 'ghichu': i[11], 'tennhom': i[12]} for i in result]
        return data
    except Exception as e:
        return e
    
def get_chi_tiet_nhom_thuc_tap_by_id(id: str):
    try:
        i = cursor.execute("EXEC GetChiTietNhomThucTapByID ?", id).fetchone()
        return {'id': i[0], 'nguoihuongdan_hoten': i[8], 'nguoihuongdan_id': i[1], 'nguoihuongdan_username': i[14], 'kythuctap_id': i[2], 'kythuctap_ngaybatdau': i[9], 'kythuctap_ngayketthuc': i[10], 'detai_id': i[3], 'detai_ten': i[11], 'detai_mota': i[12], 'nhomthuctap_dadangky': i[13], 'nhomthuctap_soluong': i[4], 'xoa': i[5], 'ghichu': i[6], 'nhomthuctap_tennhom': i[7]}
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
        ktt_obj = cursor.execute("SELECT ID, NgayBatDau FROM KyThucTap WHERE isDeleted != 2").fetchall()
        nhd_obj = cursor.execute("SELECT ID, HoTen FROM NguoiHuongDan").fetchall()
        detai_obj = cursor.execute("SELECT ID, Ten FROM DeTai WHERE isDeleted != 2").fetchall()

        ktt = [{'id': i[0], 'ngay': i[1]} for i in ktt_obj]
        nhd = [{'id': i[0], 'hoten': i[1]} for i in nhd_obj]
        detai = [{'id': i[0], 'ten': i[1]} for i in detai_obj]
        
        return {'kythuctap': ktt, 'nguoihuongdan': nhd, 'detai': detai}
    except Exception as e:
        return e
    
def update_chi_tiet_nhom_thuc_tap_by_id(id: int, kytt: int, nguoihd: int, detai: int, soluong: int, tennhom: str, isDeleted: int, ghichu: str):
    try:
        result = cursor.execute("EXEC UpdateChiTietNhomThucTapByID ?, ?, ?, ?, ?, ?, ?, ?", id, kytt, nguoihd, detai, soluong, isDeleted, ghichu, tennhom)
        conn.commit()
        return True
    except Exception as e:
        return e
    
def update_xoa_nhom_thuc_tap_by_id(id: str):
    try:
        result = cursor.execute("EXEC UpdateXoaNhomThucTapByID ?", id)
        conn.commit()
        return True
    except Exception as e:
        return e
    
def them_nhom_thuc_tap(nguoihd: str, kytt: str, detai: str, soluong: int, tennhom: str, isDeleted: int, ghichu: str):
    try:
        result = cursor.execute("EXEC InsertNhomThucTap ?, ?, ?, ?, ?, ?, ?", nguoihd, kytt, detai, soluong, isDeleted, ghichu, tennhom)
        conn.commit()
        return True
    except Exception as e:
        return e

def get_chi_tiet_sinh_vien_by_id(id: str):
    try:
        i = cursor.execute("EXEC GetThongTinChiTietSVByID ?", id).fetchone()
        return {'id': i[0], 'mssv': i[1], 'hoten': i[2], 'gioitinh': 'nam' if i[3]==1 else 'nữ', 'sdt': f'0{i[4]}', 'email': i[5], 'diachi': i[6], 'malop': i[7], 'khoa': i[8], 'nganh': i[9], 'truong': i[10], 'tendetai': i[12], 'ngaybatdau': i[13], 'nguoihuongdan': i[14]}
    except Exception as e:
        return e
    
def get_chi_tiet_sinh_vien_chua_co_nhom(id: str):
    try:
        i = cursor.execute("EXEC GetThongTinChiTietSVChuaCoNhomByID ?", id).fetchone()
        return {'id': i[0], 'mssv': i[1], 'hoten': i[2], 'gioitinh': i[3], 'sdt': f'{i[4]}', 'email': i[5], 'diachi': i[6], 'malop': i[7], 'khoa': i[8], 'nganh': i[9], 'id_nganh': i[10], 'truong': i[11], 'id_truong': i[12]}
    except Exception as e:
        return e
    
def get_chi_tiet_sinh_vien_da_co_nhom(id: str):
    try:
        i = cursor.execute("EXEC GetThongTinChiTietSVDaCoNhomByID ?", id).fetchone()
        return {'id': i[0], 'mssv': i[1], 'hoten': i[2], 'gioitinh': i[3], 'sdt': f'{i[4]}', 'email': i[5], 'diachi': i[6], 'malop': i[7], 'khoa': i[8], 'nganh': i[9], 'id_nganh': i[10], 'truong': i[11], 'id_truong': i[12], 'nguoihuongdan': i[13], 'ngaybatdau': i[14], 'tendetai': i[15], 'tennhom': i[16]}
    except Exception as e:
        return e
    
def get_chi_tiet_sinh_vien_da_danh_gia(id: str):
    try:
        i = cursor.execute("EXEC GetThongTinChiTietSVDaDanhGiaByID ?", id).fetchone()
        return {'id': i[0], 'mssv': i[1], 'hoten': i[2], 'gioitinh': i[3], 'sdt': f'{i[4]}', 'email': i[5], 'diachi': i[6], 'malop': i[7], 'khoa': i[8], 'nganh': i[9], 'id_nganh': i[10], 'truong': i[11], 'id_truong': i[12], 'nguoihuongdan': i[13], 'ngaybatdau': i[14], 'tendetai': i[15], 'ythuckyluat_number': i[19], 'ythuckyluat_text': i[20], 'tuanthuthoigian_number': i[21], 'tuanthuthoigian_text': i[22], 'kienthuc_number': i[23], 'kienthuc_text': i[24], 'kynangnghe_number': i[25], 'kynangnghe_text': i[26], 'khanangdoclap_number': i[27], 'khanangdoclap_text': i[28], 'khanangnhom_number': i[29], 'khanangnhom_text': i[30], 'khananggiaiquyetcongviec_number': i[31], 'khananggiaiquyetcongviec_text': i[32], 'danhgiachung_number': i[33], 'tennhom': i[34]}
    except Exception as e:
        return e
    
def get_ds_sinh_vien_by_username(username: str, kythuctap: str):
    try:
        result = cursor.execute("EXEC GetDSSVByNguoiHuongDanID ?, ?", username, kythuctap)
        return [{'id': i[0], 'mssv': i[1], 'hoten': i[2], 'gioitinh': 'Nam' if i[3]==1 else 'Nữ', 'nganh': i[4], 'truong': i[5], 'trangthai': i[6], 'detai': i[7], 'nhom': i[8], 'tennhom': i[9]} for i in result]
    except Exception as e:
        return e
    
def get_chi_tiet_danh_gia_sv_by_id(id: str):
    try:
        i = cursor.execute("EXEC GetChiTietDanhGiaSVByID ?", id).fetchone()
        return {'ythuckyluat_number': i[3], 'ythuckyluat_text': i[4], 'tuanthuthoigian_number': i[5], 'tuanthuthoigian_text': i[6], 'kienthuc_number': i[7], 'kienthuc_text': i[8], 'kynangnghe_number': i[9], 'kynangnghe_text': i[10], 'khanangdoclap_number': i[11], 'khanangdoclap_text': i[12], 'khanangnhom_number': i[13], 'khanangnhom_text': i[14], 'khananggiaiquyetcongviec_number': i[15], 'khananggiaiquyetcongviec_text': i[16], 'danhgiachung_number': i[17]}
    except Exception as e:
        return e
    
def update_danh_gia_sv_by_id(sinhvienid: str, nhomid: int, ythuckyluat_number: float, ythuckyluat_text: str, tuanthuthoigian_number: float, tuanthuthoigian_text: str, kienthuc_number: float, kienthuc_text: str, kynangnghe_number: float, kynangnghe_text: str, khanangdoclap_number: float, khanangdoclap_text: str, khanangnhom_number: float, khanangnhom_text: str, khananggiaiquyetcongviec_number: float, khananggiaiquyetcongviec_text: str, danhgiachung_number: float):
    try:
        result = cursor.execute("EXEC UpdateDanhGiaSVByID ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?", sinhvienid, nhomid, ythuckyluat_number, ythuckyluat_text, tuanthuthoigian_number, tuanthuthoigian_text, kienthuc_number, kienthuc_text, kynangnghe_number, kynangnghe_text, khanangdoclap_number, khanangdoclap_text, khanangnhom_number, khanangnhom_text, khananggiaiquyetcongviec_number, khananggiaiquyetcongviec_text, danhgiachung_number)
        cursor.commit()
        return True
    except Exception as e:
        return e
    
def update_danh_gia_sv_by_mssv(mssv: str, ythuckyluat_number: float, ythuckyluat_text: str, tuanthuthoigian_number: float, tuanthuthoigian_text: str, kienthuc_number: float, kienthuc_text: str, kynangnghe_number: float, kynangnghe_text: str, khanangdoclap_number: float, khanangdoclap_text: str, khanangnhom_number: float, khanangnhom_text: str, khananggiaiquyetcongviec_number: float, khananggiaiquyetcongviec_text: str, danhgiachung_number: float):
    try:
        result = cursor.execute("EXEC UpdateDanhGiaSVByMSSV ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?", mssv, ythuckyluat_number, ythuckyluat_text, tuanthuthoigian_number, tuanthuthoigian_text, kienthuc_number, kienthuc_text, kynangnghe_number, kynangnghe_text, khanangdoclap_number, khanangdoclap_text, khanangnhom_number, khanangnhom_text, khananggiaiquyetcongviec_number, khananggiaiquyetcongviec_text, danhgiachung_number)
        cursor.commit()
        return True
    except Exception as e:
        return e

def get_id_nhom_by_sv_id(id: str):
    try:
        i = cursor.execute("EXEC GetIDNhomBySVID ?", id).fetchone()
        return int(i[0])
    except Exception as e:
        return e
    
def get_ds_nhom_chua_co_cong_viec(username: str):
    """
        Get danh sách nhóm chưa có công việc bằng ID người hướng dẫn
    """
    try:
        result = cursor.execute("EXEC [GetDSNhomChuaCoCongViecByNguoiHDUsername] ?", username)
        data = [{'id': i[0], 'ngaybatdau': i[3], 'tendetai': i[5], 'idcongviec': i[7], 'tennhom': i[8]} for i in result]
        return data
    except Exception as e:
        return e
    

def get_ds_cong_viec_nhom():
    try:
        result = cursor.execute("EXEC GetDSCongViecNhom").fetchall()
        data = [{'id': i[0], 'ten_nhom': i[1], 'ngaybatdau': i[2], 'ngayketthuc': i[3], 'ten': i[4], 'mota': i[5]} for i in result]
        return data
    except Exception as e:
        return e
    
def get_ds_cong_viec_by_id_nhom(id: int):
    try:
        result = cursor.execute("EXEC GetCongViecByIDNhom ?", id).fetchall()
        data = [{'id': i[0], 'ngaybatdau': i[1], 'ngayketthuc': i[2], 'ten': i[3], 'mota': i[4]} for i in result]
        return data
    except Exception as e:
        return e

def get_chi_tiet_cong_viec_by_id_cong_viec(id: int):
    try:
        result = cursor.execute("EXEC GetChiTietCongViecByIDCongViec ?", id).fetchall()
        data = [{'id': i[0], 'id_congviec': i[1], 'id_sinhvien': i[2], 'trangthai': i[3], 'ghichu': i[4], 'tencongviec': i[5], 'nguoithuchien': i[6]} for i in result]
        return data
    except Exception as e:
        return e

def them_cong_viec_nhom(id: int, ngaybatdau: str, ngayketthuc: str, ten: str, mota: str):
    try:
        result = cursor.execute("EXEC InsertCongViec ?, ?, ?, ?, ?", id, ngaybatdau, ngayketthuc, ten, mota)
        cursor.commit()
        return True
    except Exception as e:
        return e
    
def them_chi_tiet_cong_viec(id_congviec: int, id_sinhvien: int, trangthai: int, ghichu: str):
    try:
        result = cursor.execute("EXEC InsertChiTietCongViec ?, ?, ?, ?", id_congviec, id_sinhvien, trangthai, ghichu)
        cursor.commit()
        return True
    except Exception as e:
        return e

def get_dssv_by_nhom_id(id: int):
    try:
        result = cursor.execute("EXEC GetDSSVByNhomID ?", id).fetchall()
        return [{'id': i[0], 'hoten': i[1]} for i in result]
    except Exception as e:
        return e
    
def get_goi_y_xa_phuong(q: str):
    try:
        result = cursor.execute("SELECT DiaChi FROM XaPhuong WHERE DiaChi LIKE '%' + ? + '%'", q).fetchall()
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
    
def update_nhom_thuc_tap_by_sv_id(idsinhvien: int, idnhom: int):
    try:
        # Kiểm tra xem đã đủ số lượng chưa
        registed = cursor.execute("EXEC GetSoLuongSVDaDangKyByNhomID ?", idnhom).fetchone()[0]
        quantity = cursor.execute("SELECT SoLuong FROM NHOMHUONGDAN WHERE ID = ?", idnhom).fetchone()[0]
        if(registed < quantity):
            result = cursor.execute("EXEC UpdateNhomThucTapBySinhVienID ?, ?", idsinhvien, idnhom)
            r = result.fetchone()[0]
            cursor.commit()
            return True
        else:
            return False
    except Exception as e:
        return e
    
def get_dssv_da_danh_gia_by_nguoi_huong_dan(username: str, kythuctap: int):
    try:
        result = cursor.execute("EXEC GetDSSVDanhGiaByNguoiHuongDanUsername ?, ?", username, kythuctap).fetchall()
        return [{'mssv': i[21], 'hoten': i[18], 'malop': i[19], 'nguoihuongdan': i[20], 'ythuckyluat_text': i[4], 'ythuckyluat_number': i[3], 'tuanthuthoigian_text': i[6], 'tuanthuthoigian_number': i[5], 'kienthuc_text': i[8], 'kienthuc_number': i[7], 'kynangnghe_text': i[10], 'kynangnghe_number': i[9], 'khanangdoclap_text': i[12], 'khanangdoclap_number': i[11], 'khanangnhom_text': i[14], 'khanangnhom_number': i[13], 'khananggiaiquyetcongviec_text': i[16], 'khananggiaiquyetcongviec_number': i[15], 'danhgiachung_number': i[17]} for i in result]
    except Exception as e:
        return e
    
def update_xoa_sinh_vien_by_id(id: int):
    try:
        result = cursor.execute("EXEC UpdateXoaSinhVienByID ?", id)
        r = result.fetchone()[0]
        cursor.commit()
        return r
    except Exception as e:
        return e

def update_sinh_vien_by_id(id: int, mssv: str, hoten: str, gioitinh: int, sdt: str, email: str, diachi: str, malop: str, truong: int, nganh: int, khoa: int):
    try:
        result = cursor.execute("EXEC UpdateSinhVienByID ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?", id, mssv, hoten, gioitinh, sdt, email, diachi, malop, truong, nganh, khoa)
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
        result = cursor.execute("EXEC GetHoTenSVByEmail ?", email)
        return result.fetchone()[0]
    except Exception as e:
        return e
    
def kiem_tra_loai_tai_khoan(username: str):
    try:
        if username:
            if '@' in username:
                result = cursor.execute("SELECT ID FROM SINHVIEN WHERE Email = ?", username)
                if result.fetchone()[0]:
                    return 2
            else:
                result = cursor.execute("SELECT ID FROM NGUOIHUONGDAN WHERE Username = ?", username)
                if result.fetchone()[0]:
                    return 1
        else:
            return 0
    except Exception as e:
        return e
    
def xem_thong_tin_sv(email: str):
    try:
        result = cursor.execute("EXEC GetChiTietSVByEmail ?", email)
        if result:
            i = result.fetchone()
            return {'mssv': i[1], 'hoten': i[2], 'gioitinh': i[3], 'sdt': i[4], 'email': i[5], 'diachi': i[6], 'malop': i[7], 'truong': i[14], 'nganh': i[15], 'khoa': i[10], 'nhomhuongdan': i[16], 'xacnhan': i[12]}
    except Exception as e:
        return e