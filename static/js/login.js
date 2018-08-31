/* financial system login v1.0.0*/
var login= new Vue({
	el:'#login',
	data:{
		form_id:'',
		form_pass:'',
		key_id:'',
		key_createdate:'',
	},
	methods:{
		login:function(){
			var login = this
			var mydata = new FormData();
			mydata.append('id',this.form_id);
			mydata.append('pass',this.form_pass);
			if(this.form_id!='' && this.form_pass!=''){
				login.$http.post('/login?type=4',mydata).then((successInfor)=>{
					if(successInfor.body.key==0){
            alert(successInfor.body.text)}
          if(successInfor.body.key==1){
						this.key_id=successInfor.body.id;
						this.key_createdate=successInfor.body.dldate;
            window.localStorage.id=this.key_id;
  					window.localStorage.createdate=this.key_createdate;
  					window.location.href="/admin?type=0";
					}
				},
				(errorInfor)=>{
					alert(successInfor.body.text);
				})
			}
		}
	}
})

/**
 * Particleground demo
 * @author Jonathan Nicol - @mrjnicol
 */

$(document).ready(function() {
  $('#particles').particleground({
    dotColor: '#5cbdaa',
    lineColor: '#5cbdaa'
  });
  $('.intro').css({
    'margin-top': -($('.intro').height() / 2)
  });
});
