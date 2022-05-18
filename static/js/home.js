document.getElementById("user_list_box").addEventListener("click", userlist_func);
document.getElementById("active_user_box").addEventListener("click", userlist_func);

function userlist_func() {
    window.location = "/unknown/userlist/";
}


document.getElementById("like_order_box").addEventListener("click", likeorder_func);

function likeorder_func() {
    window.location = "/unknown/likeorder/";
}


document.getElementById("follow_order_box").addEventListener("click", followorder_func);

function followorder_func() {
    window.location = "/unknown/followorder/";
}


document.getElementById("premium_user_box").addEventListener("click", premiumuserlist_func);

function premiumuserlist_func() {
    window.location = "/unknown/premiumuserlist/";
}


