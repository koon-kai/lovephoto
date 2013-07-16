jQuery(function(){
    //页面滚动
    jQuery(window).scroll(function() {
        //导航和回顶部的显隐
        var t = jQuery(window).scrollTop();
    
        if (t < 768){
             //alert(4);
            jQuery('#goTop').addClass('invisible');
        }
        if(t >= 768){
           // alert(2);
            jQuery('#goTop').removeClass('invisible');
        }
        
    })

    // 回顶端 
    jQuery('#goTop').click(function(){
        jQuery(document).stop().scrollTo(0, 400);
    })
})


Date.prototype.format = function(format)
{
    var o = {
        "M+" : this.getMonth()+1, //month
        "d+" : this.getDate(),    //day
        "h+" : this.getHours(),   //hour
        "m+" : this.getMinutes(), //minute
        "s+" : this.getSeconds(), //second
        "q+" : Math.floor((this.getMonth()+3)/3),  //quarter
        "S" : this.getMilliseconds() //millisecond
    }
    if(/(y+)/.test(format)) format=format.replace(RegExp.$1,
            (this.getFullYear()+"").substr(4 - RegExp.$1.length));
    for(var k in o)if(new RegExp("("+ k +")").test(format))
        format = format.replace(RegExp.$1,
                RegExp.$1.length==1 ? o[k] :
                ("00"+ o[k]).substr((""+ o[k]).length));
    return format;
}


function like(self){
   var href = self.href;
   
   $.ajax({
       url:href,
       type:'GET',
       cache: false,
       contentType: false,     //不可缺
       processData: false,     //不可缺
       dataType : "json",
       success:function(mes){
  		    var c, sel;
  		    if (mes.isOk === "true") {
    		    sel = $('#' + mes.message);
    		    sel.removeClass('icon-heart-empty').addClass('icon-heart');
    		    sel.parent().removeClass('like').addClass('liked');
    		    c = sel.parent().next('span');
    		    return $(c).html(parseInt($(c).html()) + 1);
  		    } else {
    		    return console.log(mes.message);
 	        }
       },
       error:function(e,mes){
  	        console.log(e, mes);
 		    if (mes.status === 401) {
   		 	    alert(mes.responseText);
    		    return window.location = '/login';
 	         }
       }
   });
}

function removePhoto(self){

    var id = self.name;
    if(confirm("确定要删除吗？")){
        return window.location  = '/del/photo/'+id;  
    }
}
