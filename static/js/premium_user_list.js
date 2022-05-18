document.getElementById("premium_input_reset").addEventListener("click", premium_userlist_func);

function premium_userlist_func() {
    document.getElementById("start_date").value = "";
    document.getElementById("end_date").value = "";
    location.reload();
}


document.getElementById("submit").addEventListener("click", premium_search_func);

function premium_search_func() {
    var result = document.getElementById("start_date").value;
    var result2 = document.getElementById("end_date").value;
    
}