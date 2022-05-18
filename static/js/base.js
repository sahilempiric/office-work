// sessionStorage.setItem("pgination",'1');
// sessionStorage.setItem("entries",'10');


// var live_url = window.location.pathname;
// // console.log(live_url);

// if(live_url == '/allorder/' || live_url == '/activeorder/' || live_url == '/likeorder/' || live_url == '/followorder/' || live_url == '/completeorder/' || live_url == '/userlist/' || live_url == '/premiumuserlist/' || live_url == '/purchasecoin_other_method_list/' || live_url == '/purchasecoin_inapp_method_list/' || live_url == '/ip_block/' || live_url == '/coin_details/'){

    
//     $(document).on('change', '.custom-select-sm', function () {

//         var entries = $('.custom-select-sm').val();
//         sessionStorage.setItem("entries",entries);
//         console.log($('.custom-select-sm').val());
         
//     });
       
//     $(document).on('click', '.page-link ', function () {
       
//         var pgination = $(this).text();
//         sessionStorage.setItem("pgination",pgination);
//         console.log($(this).text());
     
         
//     });
//     var entries = sessionStorage.getItem("entries");
//     var pgination = sessionStorage.getItem("pgination");
//     console.log(entries);
//     console.log(pgination);

//     $.ajax({
//         url: live_url,
//         type: "get",
//         data: {
//             entries: entries,
//             pgination: pgination,
//         },
//         success: function(data){
//               if(data == 'ID is Required'){
//                 // alert("ID is Required")
//               }
//               else{
//                 // alert('Successfully!');
//                 sessionStorage.removeItem('entries');
//                 sessionStorage.removeItem('pgination');
  
//               }
//         }
//     });


    
// }