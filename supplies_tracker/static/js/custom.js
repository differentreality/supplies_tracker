// var $ = jQuery();
// jQuery(document).ready(function($){

$(document).ready(function() {
  var oTable = $('.datatable').dataTable({
    responsive: true
  });

  $('#search-keyword').on('click', function() {
    $('#search-keyword').val('');
  });
});

function clicked(e){
  if(!confirm('Are you sure?'))e.preventDefault();
}
