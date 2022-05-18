document.getElementById("select_lf").addEventListener("change", field_func);

function field_func() {
    var lf = document.getElementById("select_lf").value;
        if(lf == "0"){
            $(".like").show();
            $(".follow").hide();

        }
        else if(lf == "1"){
            $(".like").hide();
            $(".follow").show();
        }
}

document.getElementById("add_order").addEventListener("click", model_func);

function model_func(){
    $(".like").show();
    $(".follow").hide();

}



