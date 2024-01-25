var Toast = Swal.mixin({
    toast: true,
    position: "top-end",
    showConfirmButton: false,
    timer: 3000,
  });

$.ajax({
  type: 'GET',
  url: 'get_ds_nhom_thuc_tap_con_han',
  success: function(res){
    html = '';
    if(res.length>0){
      $.each(res, function(idx, val){
        html += '<option value="'+val.id+'">['+val.id+']\t'+val.tendetai+'</option>';
      });
    }else{
      html += '<option value="" selected>Hiện tại chưa có nhóm hoặc hết hạn chọn nhóm</option>'
    }

    $("#danhsachnhom").append(html);
  }
});

$("#danhsachnhom").on('change', function(){
  let nhom = $("#danhsachnhom").val();
  if (nhom != "") {
    $.ajax({
      type: 'GET',
      url: 'get_chi_tiet_nhom_thuc_tap_by_id?id='+ nhom,
      success: function(res){
        let soluongdangky = String(res.nhomthuctap_dadangky) + '/' + String(res.nhomthuctap_soluong);
        $("#nguoihuongdan").val(res.nguoihuongdan_hoten);
        $("#mota").val(res.detai_mota.replace(/<br\/>/g, "\r\n"));
        $("#soluongsv").val(soluongdangky);
      }
    });
  }else{
    $("#nguoihuongdan").val("");
    $("#mota").val("");
    $("#soluongsv").val("");
  }
});

if(document.cookie.indexOf('groupid')!==-1){
  $("#submitBtn").prop('disabled', true);
}else{
  $("#submitBtn").on('click', function(){
    let id_nhom = $("#danhsachnhom").val();
    if(document.cookie.indexOf('studentid') !== -1){
      let id_sinhvien = document.cookie.split('studentid=')[1].split(';')[0];
      $.ajax({
        type: 'POST',
        url: 'them_nhom_thuc_tap_sv?idsinhvien='+parseInt(id_sinhvien)+'&idnhom='+parseInt(id_nhom),
        success: function(res){
          if(res.status == 'OK'){
            Toast.fire({
              icon: "success",
              title: "Đã đăng ký",
            });
            $("#submitBtn").prop('disabled', true);
          }else{
            Toast.fire({
              icon: "error",
              title: "Nhóm đã đủ số lượng",
            });
          }
        },
        error: function(){
          Toast.fire({
            icon: "error",
            title: "Nhóm đã đủ số lượng.<br/>Vui lòng liên hệ người hướng dẫn.",
          });
        }
      });
    }
  })
}