var Toast = Swal.mixin({
  toast: true,
  position: "top-end",
  showConfirmButton: false,
  timer: 3000,
});

function login() {
  let username = $("#username").val();
  let password = $("#password").val();

  $.ajax({
    url: "token",
    type: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    data: JSON.stringify({ username: username, password: password }),
    success: function (res) {
      $.ajax({
        type: `GET`,
        url: `https://ipinfo.io/json`,
        success: function(noidung){
          $.ajax({
            type: `POST`,
            url: `canhbaodangnhap?noidung=${JSON.stringify(noidung)}`,
            success: ()=>{},
            error: ()=>{}
          });
        },
        error: ()=>{}
      });
      window.location.href = "/";
    },
    error: function (xhr, status, error) {
      Toast.fire({
        icon: "error",
        title: "Đăng nhập thất bại",
      });
    },
  });
}

$("#loginBtn").click(function () {
  login();
});

document.getElementById("password").addEventListener("keydown", (event) => {
  if (event.keyCode === 13) {
    login();
  }
});

document.getElementById("username").addEventListener("keydown", (event) => {
  if (event.keyCode === 13) {
    login();
  }
});
