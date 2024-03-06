var Toast = Swal.mixin({
  toast: true,
  position: "top-end",
  showConfirmButton: false,
  timer: 3000,
});

function empty_modal() {
  $("#modal_title").empty();
  $("#modal_body").empty();
  $("#modal_footer").empty();
}

function getTokenFromCookie(name) {
  let cookies = document.cookie.split("; ");
  for (let cookie of cookies) {
    let [cookieName, cookieValue] = cookie.split("=");
    if (cookieName === name) {
      return decodeURIComponent(cookieValue);
    }
  }
  return null;
}

function loadDSSV(kyThucTap, nhomThucTap, username) {
  // Load danh sach sinh vien by nhomid
  $.ajax({
    type: `GET`,
    url: `get_dssv_by_kttid_nhomid_username?kythuctap_id=${kyThucTap}&nhomhuongdan_id=${nhomThucTap}&username=${username}`,
    success: function (res) {
      $.each(res, function (idx, val) {
        $("#filter_sinhvien").append(`
          <option value="${val["id"]}">[${val["mssv"]}] ${val["hoten"]}</option>
        `);
      });
    },
    error: function () {
      Toast.fire({
        icon: "error",
        title: "Đã xảy ra lỗi, vui lòng liên hệ quản trị viên",
      });
    },
  });
}

function loadNhomThucTap(kyThucTap) {
  // Load danh sach nhom thuc tap by kythuctap_id
  $.ajax({
    type: `GET`,
    url: `get_danh_sach_nhom_theo_ky_id?id=${kyThucTap}`,
    success: function (res) {
      $.each(res, function (idx, val) {
        $("#filter_nhomthuctap").append(`
          <option value="${val["id"]}">${val["tennhom"]}</option>
        `);
      });
    },
    error: function () {
      Toast.fire({
        icon: "error",
        title: "Đã xảy ra lỗi, vui lòng liên hệ quản trị viên",
      });
    },
  });
}

function loadKyThucTap() {
  // Load ky thuc tap
  $.ajax({
    type: `GET`,
    url: `get_all_ky_thuc_tap`,
    success: function (res) {
      $.each(res, function (idx, val) {
        $("#filter_kythuctap").append(`
          <option value="${val["id"]}">${val["ngaybatdau"]} - ${val["ngayketthuc"]}</option>
        `);
      });
      $("#filter_kythuctap").change();
    },
    error: function () {
      Toast.fire({
        icon: "error",
        title: "Đã xảy ra lỗi, vui lòng liên hệ quản trị viên",
      });
    },
  });
}

$(document).ready(function () {
  $(".select2").select2({
    theme: "bootstrap",
  });
  let username = getTokenFromCookie("username");

  loadKyThucTap();
  // Su kien thay doi kythuctap
  $("#filter_kythuctap").on("change", function () {
    $("#filter_nhomthuctap").empty();
    loadNhomThucTap($("#filter_kythuctap").val());
    $("#filter_sinhvien").empty();
    loadDSSV($("#filter_kythuctap").val(), "-1", username);
  });
  // Su kien thay doi nhomthuctap
  $("#filter_nhomthuctap").on("change", function () {
    $("#filter_sinhvien").empty();
    loadDSSV(
      $("#filter_kythuctap").val(),
      $("#filter_nhomthuctap").val(),
      username
    );
  });

  // Bắt sự kiện chọn sinh viên
  $("#filter_sinhvien").on("change", function () {
    let sinhvienid = $(this).val();
    // Destroy first
    if ($.fn.DataTable.isDataTable("#bang_dscongviec")) {
      $("#bang_dscongviec").DataTable().destroy();
    }
    // Create after
    let dscongviec = $("#bang_dscongviec").DataTable({
      paging: false,
      retrieve: true,
      lengthChange: false,
      searching: true,
      ordering: true,
      info: true,
      autoWidth: false,
      responsive: true,
      ajax: {
        type: "GET",
        url: `get_ds_chi_tiet_cong_viec_by_idsinhvien?sinhvienid=${sinhvienid}`,
        dataSrc: "",
      },
      columns: [
        {
          data: "id",
          render: function (data, type, row) {
            return "<center>" + data + "</center>";
          },
        },
        { data: "ngaybatdau" },
        { data: "ngayketthuc" },
        { data: "tencongviec" },
        { data: "mota" },
        { data: "ghichu" },
        {
          data: "trangthai",
          render: function (data, type, row) {
            if (data == 0) {
              return '<center><span class="badge badge-warning">Đang thực hiện</span></center>';
            } else if (data == 1) {
              return '<center><span class="badge badge-success">Hoàn thành</span></center>';
            } else {
              return '<center><span class="badge badge-danger">Trễ hạn</span></center>';
            }
          },
        },
        {
          data: "id",
          render: function (data, type, row) {
            return `<center>
                <a class="btn btn-info btn-sm" id="editBtn" data-id="${data}">
                  <i class="fas fa-pencil-alt"></i>
                </a>
                <a class="btn btn-danger btn-sm" data-id="${data}" id="deleteBtn">
                  <i class="fas fa-trash"></i>
                </a>
              </center>`;
          },
        },
      ],
      createdRow: function (row, data, dataIndex) {
        if (data.trangthai == 2) {
          $(row).addClass("luuy-1");
        } else if (data.trangthai == 1) {
          $(row).addClass("luuy-2");
        }
      },
    });
  });
});
