$(document).ready(function(){

	$(document).on('click','#del-bt',function(){
		var value=$(this).data('value');
		
		va = confirm("Do you want to delete this blog ?");

		if (va == true ){
			$.ajax({
			url: '/blog/blog_delete/'+value,
        	dataType: 'json',
        	type: 'get',
        	success: function (result) {
       			debugger;
       			location.reload();		
    			}
    		});
		}


	});		


})