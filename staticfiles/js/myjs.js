 $(document).ready(function(){
  

  $('.table').paging({limit:6});

  NProgress.start();
  NProgress.done();

  $(".datetimeinput").datepicker({changeMonth: true, dateFormat: 'yy-mm-dd'});
  
  // $(".datetimeinput").datepicker({changeYear: true,changeMonth: true, dateFormat: 'yy-mm-dd'});
 

});