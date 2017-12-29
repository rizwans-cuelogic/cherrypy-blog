$(document).ready(function(){

if(document.getElementById("preview") == null)
{
	$('#attachments').show(); 
}

if ($('#preview').css('display') !== 'none'){
	$('#attachments').removeAttr("required"); 
}

$(document).on('click','#button1',function(){
		var value=$(this).attr('value');
		deleteAttachment(value)
});


deleteAttachment=function(value){
		
		va =confirm("Do You Want To Delete?")
		if (va == true){	
			$.ajax({
			url: '../deleteimage',
        	data:{'value':value},
        	dataType: 'json',
        	type: 'post',
        	success: function (result) {
       
				$('#attachments').show();
				$('#preview').remove();
				$('#attachments').attr("required","True");	
    		}
    		});
		}	
	}

})