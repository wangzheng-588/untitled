$(
    function () {
        let username = $("#username");
        let password = $("#pwd");
        let errorUsername = $("#user_error");
        let errorPwd = $("#pwd_error");
        let login = $("#login");


        function disableLogin() {
            login.attr('disable', true);
            login.addClass("disable");
        }

        function enableLogin() {
            login.removeClass("disable");
            login.removeAttr("disable");
        }


        function check() {
            if (username.val().length >= 6 && password.val().length > 0) {
                enableLogin();
            } else {
                disableLogin();
            }
        }


        disableLogin();


        username.blur(function () {

            if ($.trim(username.val()) === '') {
                errorUsername.text("用户名不能为空！");
                errorUsername.show();

            } else {
                errorUsername.hide();

            }

            if ($.trim(username.val()).length < 6) {
                errorUsername.text("用户名不能少于6位！");
                errorUsername.show();
            } else {
                errorUsername.hide();

                $.get("/user/check_user_exist", {"user_name": username.val()}, function (data) {
                    if (data.code == 200) {
                        let count = data.content.count;
                        if (count == 0) {
                            errorUsername.text("用户名不存在");
                            errorUsername.show();
                            disableLogin();
                        } else {
                            errorUsername.hide();
                            check();
                        }
                    }
                });


            }


        });

        password.blur(
            function () {
                if ($.trim(password.val()) === "") {
                    errorPwd.show();
                    errorPwd.text("密码不能为空");
                } else {
                    errorPwd.hide();
                }
            }
        );


        username.bind("input propertychange change", function () {

            if (username.val().length >= 6 && password.val().length > 0) {
                enableLogin();
            } else {
                disableLogin();
            }
        });

        password.bind("input propertychange change", function () {

            if (username.val().length >= 6 && password.val().length > 0) {
                console.log(password.val().length);
                enableLogin();
            } else {
                disableLogin();
            }
        });


        login.unbind('click').bind().bind('click',
            function () {
                let obj = $('#loginFormID').serialize();

                $.ajax(
                    {
                        type: "POST",
                        url: "/user/login_handler/",
                        data: obj,
                        dataType: "json",
                        async: false,
                        success: function (data) {

                            if (data.code == 200) {
                                window.location.href = "/user/user_center_info/";
                                alert(data.code);
                            } else {
                                alert("登录失败");
                            }
                        },
                    }
                );

            }
        );


    }
);