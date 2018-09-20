$(document).ready(function () {
  $selector = $("#select1")


  function ajaxCallsFunc(type, url, contentType, data, callback) {
    $.ajax({
      type: type,
      url: url,
      contentType: contentType,
      data: data,
      success: callback
    });
  }
  // $("#divReadOnlyFields :input").attr("disabled", true);

  window.onload = function(){

    ajaxCallsFunc('POST', "http://127.0.0.1:5000/langs", 'application/json', null, function (branches) {
      console.log(branches)
      for (var val in branches){
        $selector.append($("<option>"+branches[val]+"</option>"));        
        $selector.trigger('contentChanged');
      }
    });


  };
  

  $('select').on('contentChanged', function() {
    $(this).material_select();
  });


  

  $dict = $("#textarea1")
  $affix = $("#textarea2")
  $("#drawgraph").click(function () {

    var dummydata3 = JSON.stringify({
      "lang": $("#select1").val()
    });

    console.log(dummydata3);

    ajaxCallsFunc('POST', "http://127.0.0.1:5000/dummy", 'application/json', dummydata3, function (branches) {
        var dic_data = "";
        var affix_data = ";"

        dic_response = branches['dic'];
        affix_response = branches['affix']

        for (var keys in dic_response) {
          dic_data += dic_response[keys]
        }
        $dict.val(dic_data);
        $dict.trigger('autoresize'); 
        $dict.change();

        for (var keys in affix_response) {
          affix_data += affix_response[keys]
        }
        $affix.val(affix_data);
        $affix.trigger('autoresize'); 
        $affix.change();


      });
    }
  )
  

});