var Toast = Swal.mixin({
    toast: true,
    position: "top-end",
    showConfirmButton: false,
    timer: 3000,
});

$(document).ready(function() {
    $('#getOTPBtn').on('click', function() {
        let otpInput = $('#div_otp');
        let loginBtn = $('#div_button');
        let email = $('#emailInput');

        // Show input otp và button login
        otpInput.prop('hidden', false);
        loginBtn.prop('hidden', false);

        $.ajax({
            type: 'POST',
            url: '/gui_mail_otp?email='+email.val(),
            success: function() {
                Toast.fire({
                    icon: "success",
                    title: "Đã gửi mã OTP",
                });
            },
            error: function() {
                Toast.fire({
                    icon: "error",
                    title: "Đã xảy ra lỗi. Vui lòng liên hệ quản trị viên.",
                });
            }
        });
    });
});