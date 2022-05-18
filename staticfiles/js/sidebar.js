// $(document).on('click', '.sidebar_selection', function () {
    
//     $(".sidebar_selection").removeClass("active");
//     $(this).addClass("active");
// });

var pathname = window.location.pathname;
// var all_arr = pathname.split("/")
$(".sidebar_selection").removeClass("active");

if (pathname == "/unknown/home/"){
    $('.Dashboard').addClass("active");
    
}
else if(pathname == "/unknown/appcoindetail/" || pathname == "/unknown/offer/" || pathname == "/unknown/maintenence/" || pathname == "/unknown/ads/" || pathname == "/unknown/other/"){
    $('.App_Data').addClass("active");
}
else if(pathname == "/unknown/dailynotification/" || pathname == "/unknown/sendnotification/"){
    $('.Notification').addClass("active");
}
else if(pathname == "/unknown/coin_details/"){
    $('.Coin_Details').addClass("active");
}
else if(pathname == "/unknown/ip_block/"){
    $('.IP_Block').addClass("active");
}
else if(pathname == "/unknown/manage_profile/"){
    $('.Manage_Profile').addClass("active");
}
else if(pathname == "/unknown/activeorder/" || pathname == "/unknown/allorder/" || pathname == "/unknown/likeorder/" || pathname == "/unknown/followorder/" || pathname == "/unknown/completeorder/" ){
    $('.Order_List').addClass("active");
}
else if(pathname == "/unknown/userlist/"){
    $('.User_List').addClass("active");
}
else if(pathname == "/unknown/premiumuserlist/"){
    $('.Premium_User').addClass("active");
}
else if(pathname == "/unknown/purchasecoin_other_method_list/" || pathname == "/unknown/purchasecoin_inapp_method_list/"){
    $('.Purchase_Coin_List').addClass("active");
}