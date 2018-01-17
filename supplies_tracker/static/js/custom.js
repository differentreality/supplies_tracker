// var $ = jQuery();
// jQuery(document).ready(function($){

$(document).ready(function() {
  var oTable = $('.datatable').dataTable({
    responsive: true
  });
});

function clicked(e){
  if(!confirm('Are you sure?'))e.preventDefault();
}
