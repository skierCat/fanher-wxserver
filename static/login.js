/* xfh v1.0.0*/
var login= new Vue({
	el:'#login',
	data:{
		form_id:'',
		form_pass:'',
		receive_data:'',
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
					this.receive_data=successInfor.body.text;
					if(successInfor.body.key!=0){
						this.key_id=successInfor.body.id;
						this.key_createdate=successInfor.body.dldate;
					}
					window.localStorage.id=this.key_id
					window.localStorage.createdate=this.key_createdate
					window.location.href="/finance?type=0";
				}, 
				(errorInfor)=>{
					alert(successInfor.body.text)
				})
			}
		}
	}
})