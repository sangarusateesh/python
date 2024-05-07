$(function() {
    // $(document).ready(function () {
        $("#RegistrationForm").validate({
         rules: {
             user_name:{required:true},
             email: {required: true},
             phone:{required:true}
         },
         errorPlacement: function(){
             return false;
         },
         invalidHandler: function(event, validator) {($('.response').html('')); }
        });
     });


$(document).on("submit", ".v_form", function (e) { 
    console.log('satttt');return false;
    e.preventDefault();
    var formId=$(this).attr('id'),id=$('#'+formId+' input[name=id]').length > 0 ? $('#'+formId+' input[name=id]').val():'',proceed=false;
    var btn = $('#'+formId+' button[type=submit]');
    var btn_text = btn.text();
    if($('#'+formId).valid()){proceed=true;}
    $('#'+formId+' .response').html('');    
    if(proceed){ 
        btn.text('Please wait...');
        btn.prop('disabled', true);
        $.ajax({
            url:'controller',type:"post",dataType: 'json',data: new FormData($('#'+formId)[0]),
            success: function (response) { //console.log(typeof response, response);return false;
                var status,error,redirect,reload,msg,otp;
                if(response && isObject(response)){ 
                    status = response.hasOwnProperty("status") ? response.status : '';
                    error = response.hasOwnProperty("error") ? response.error : '';
                    redirect = response.hasOwnProperty("redirect") ? response.redirect : '';
                    reload = response.hasOwnProperty("reload") ? response.reload : '';
                    msg = response.hasOwnProperty("msg") ? response.msg : "Data Updated successfully.";
                }
                if(status === 'OK'){ 
                    if(redirect){
                        location.href= redirect;return false;
                    }else if(reload){ 
                        location.reload(true);return false;
                    }else{ 
                        $('#'+formId+' .response').html('<div class="alert alert-success"><i class="fa fa-check-circle"></i> '+ msg +'</div>');
                        if(['clients-form','slider-form','stats-form','settings-form','social-links-form','product-form','aboutus-form','time-form'].includes(formId)){ 
                            setTimeout(function() {location.reload(true);return false;},5000);
                        }else{
                            var resetForms = ['changePasswordForm','enquiry_form'];                        
                            if(((!id) || resetForms.includes(formId))){
                                $('#'+formId)[0].reset();
                                if($('.dropify').length > 0){$(".dropify").each(function() {resetDropify(this);});}
                                if($('.summernote').length > 0){$('.summernote').summernote('reset');}
                            }
                        }
                    }
                }else if(error){ $('#'+formId+' .response').html('<div class="alert alert-danger"><i class="fa fa-warning"></i> '+error+'</div>');}  
                btn.prop('disabled', false).text(btn_text);
            },
            error: function( xhr, textStatus, errorThrown ){ console.log(xhr.status);
                btn.prop('disabled', false).text(btn_text);
                xhr.status==401&&$("#myModal").modal('show');
            },
            cache: false,
            contentType: false,
            processData: false
        });
        $('html, body').animate({scrollTop: $('#'+formId+' .response').offset().top-100}, 1000);
    }     
});