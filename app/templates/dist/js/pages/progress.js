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

function loadDSSV(kyThucTap, nhomThucTap){
  // Load danh sach sinh vien by nhomid
  $.ajax({
    type: `GET`,
    url: `get_ds_sinh_vien_by_username?kythuctap=${kyThucTap}&nhomthuctap=${nhomThucTap}`,
    success: function(res){
      $.each(res, function(idx, val){
        $('#filter_sinhvien').append(`
          <option value="${val['id']}">[${val['mssv']}] ${val['hoten']}</option>
        `);
      });
    },
    error: function(){
      Toast.fire({
        icon: "error",
        title: "Đã xảy ra lỗi, vui lòng liên hệ quản trị viên"
      });
    }
  });
}

function loadNhomThucTap(kyThucTap){
  // Load danh sach nhom thuc tap by kythuctap_id
  $.ajax({
    type: `GET`,
    url: `get_danh_sach_nhom_theo_ky_id?id=${kyThucTap}`,
    success: function(res){
      $.each(res, function(idx, val){
        $('#filter_nhomthuctap').append(`
          <option value="${val['id']}">${val['tennhom']}</option>
        `);
      });
      loadDSSV(kyThucTap, '-1');
    },
    error: function(){
      Toast.fire({
        icon: "error",
        title: "Đã xảy ra lỗi, vui lòng liên hệ quản trị viên"
      });
    }
  });
}

function loadKyThucTap(){
  // Load ky thuc tap
  $.ajax({
    type: `GET`,
    url: `get_all_ky_thuc_tap`,
    success: function(res){
      $.each(res, function(idx, val){
        $('#filter_kythuctap').append(`
          <option value="${val['id']}">${val['ngaybatdau']} - ${val['ngayketthuc']}</option>
        `);
      });
      $('#filter_kythuctap').change();
    },
    error: function(){
      Toast.fire({
        icon: "error",
        title: "Đã xảy ra lỗi, vui lòng liên hệ quản trị viên"
      });
    }
  }); 
}

$(document).ready(function () {
  $(".select2").select2({
    theme: "bootstrap",
  });

  loadKyThucTap();
  // Su kien thay doi kythuctap
  $("#filter_kythuctap").on("change", function () {
    $("#filter_nhomthuctap").empty();
    loadNhomThucTap($("#filter_kythuctap").val());
    $('#filter_sinhvien').empty();
    loadDSSV($("#filter_kythuctap").val(), '-1');
  });
  // Su kien thay doi nhomthuctap
  $("#filter_nhomthuctap").on("change", function () {
    $("#filter_sinhvien").empty();
    loadDSSV($("#filter_kythuctap").val(), $("#filter_nhomthuctap").val());
  });
});
