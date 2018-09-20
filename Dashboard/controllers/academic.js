$(document).ready(function () {
    
    window.onload = function(){

        
    };


    function ajaxCallsFunc(type, url, contentType, data, callback) {
        $.ajax({
          type: type,
          url: url,
          contentType: contentType,
          data: data,
          success: callback
        });
      }

    $lang_name = $("#lang_name")
    $lang_symbol = $("#lang_symbol")
    $dic_txt = $("#dic")
    $aff_txt = $("#aff")

    $("#okbtn").click(function(){

        console.log("i m here")
        $("#modal1").closeModal();

    });
    $("#drawgraph").click(function(){

        dummyData = JSON.stringify({

            "lang_name" : $("#lang_name").val(),
            "lang_symbol" : $("#lang_symbol").val(),
            "dic_data" : $("#dic").val(),
            "aff_data" : $("#aff").val()
        });
    
        ajaxCallsFunc('POST', "http://127.0.0.1:5000/SaveData", 'application/json', dummyData, function (branches) {
            
            
            console.log(typeof(branches));
            if(Object.size(branches) > 0){
                console.log("i m here");
                document.getElementById("header").innerHTML = "Error";
                document.getElementById("err_id").innerHTML = branches["Error"];
                $("#modal1").openModal();
            }
        });

    });
    
    Object.size = function(obj) {
        var size = 0, key;
        for (key in obj) {
            if (obj.hasOwnProperty(key)) size++;
        }
        return size;
    };
    
    $('select').material_select();
});