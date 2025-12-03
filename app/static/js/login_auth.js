console.log("login_auth is loaded.");
errorMes = new Array()
errorMes[0] = "メールを入力してください";
errorMes[1] = "パスワードを入力してください";

$("#login_btn").on("click",function(){
    console.log("check");
    
    $(".error-text").empty();
    $(".error").remove();

    $("input[type='email'] , input[type='password']").each(function(index,e){
        console.log("each");
        if($(this).val()===""){
            $(this).after(`<div class="error">${errorMes[index]}</div>`);
            $(".error").css(`color`,`red`);
        };
    });
});
