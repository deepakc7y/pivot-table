google.load("visualization", "1", {packages:["corechart", "charteditor"]});
var renderers = $.extend($.pivotUtilities.renderers,
  $.pivotUtilities.gchart_renderers);
function someFunction(data) {
  if(data!=""){
    document.getElementById("table").style.display = "inline";
  }
  $(function () {
  var input1 = $.csv.toArrays(data);
      $("#output").pivotUI(input1, { 
        renderers:renderers,
      });
  });
}
var x = document.getElementById("output").dataset.data;
someFunction(x);