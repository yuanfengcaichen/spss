
const app = new Vue({
    el:"#app",
    data:{
        file:[],//上传文件
        progress:0,//上传进度
        result:0,//上传结果
        filelist:[],//已上传的文件列表
        fileselectnum:0,//已选择的文件序号

        analytype:"linear",//linear:线性回归，gradually:逐步回归
        criterion:"",//优化规则
        direction:"",//回归方向

        flavours:[],
        ylist:[],
        xselected: [],
        yselected: [],
        allSelected: false,
        indeterminate: false,

        showresult:false,//是否显示分析结果
        model:"",//模型
        f1:"",//计算f值
        f2:"",//理论f值
        prediction_src:"",//模型预测
        checkselect:'回归模型预测',
        nortype:'直方图',//正态性检验类型（直方图、qq图还是pp图、K-s检测）
        normality_src:'',//正态性检测图片地址
        pp_src:'',//pp图
        qq_src:'',//qq图
        ksdata:{},//K-S检测数据
        multicollinearity:[],//多重共线性检验数据
        lineselected:[],//线性相关性选择的列名
        linear_correlation_src:'',//线性相关性检验图片地址
        testmodel:'',//异常值检验模型数据
        testdw:'',//检测模型的dw
        vartype:'图形法',//方差齐性检测类型（图形法还是BP法）
        bpdata:[],//BP法数据
        xselected_change:[],//方差齐性检验可选参数
        oselected_1:'',//方差齐性检验参数1
        oselected_2:'',//方差齐性检验参数2
        variance_src:'',//方差齐性检验图片地址
        fileloading:false,//文件分析结果是否正在加载
        imgloading:false,//图片信息是否正在加载
    },
    methods:{
        creataxios(){
            let that = this
            let myaxios = axios.create({});
            myaxios.interceptors.request.use((config)=>{
                // 在发送请求之前做些什么
                if(config.url=="/analysis/uploadfile"||config.url=="/analysis/sendselect"){
                    this.fileloading = true
                }
                else{
                    this.imgloading = true
                }
                return config;
            }, function (error) {
                // 对请求错误做些什么

                console.log(error)
                return Promise.reject(error);
            });

            // 添加响应拦截器
            myaxios.interceptors.response.use((response)=> {
                // 对响应数据做点什么
                if(response.config.url=="/analysis/uploadfile"||response.config.url=="/analysis/sendselect"){
                    this.fileloading = false
                }
                else{
                    this.imgloading = false
                }
                //console.log(response)
                return response;
            }, function (error) {
                // 对响应错误做点什么
                that.fileloading = false
                that.imgloading = false
                //console.log(error)
                //that.makeToast('danger',"error")
                return Promise.reject(error);
            });
            return myaxios
        },
        showaddModal(){
            this.$refs['my-modal'].show()
        },
        submitfile(e){
            var that=this
            let file = e.target.files[0];
            var formdata=new FormData();
            formdata.append('file',file);
            let config = {
                headers:{'Content-Type':false},
                onUploadProgress: progressEvent => {
                    var complete = (progressEvent.loaded / progressEvent.total * 100 | 0) + '%'
                    this.progress = complete
                }
            };  //添加请求头
            myaxios = this.creataxios()
            myaxios.post('/analysis/uploadfile',formdata,config)
            .then(function(res){
                //console.log(res)
                if(res.data.result==1){
                    that.result = 1;
                    that.flavours = res.data.resultdata[0][1];
                    that.ylsit = res.data.resultdata[0][1];
                    for(let i=0;i<res.data.resultdata.length;i++){
                        that.filelist.push(res.data.resultdata[i]);
                    }
                    that.fileselectnum = res.data.resultdata[0][2];
                    that.xselected=[];
                    that.yselected = [];
                    that.lineselected=[];
                    that.oselected_1='';
                    that.oselected_1='';
                }
            })
        },
        toggleAll(checked) {
            this.xselected = checked ? this.flavours.slice() : []
          },
        sendselect(){
            this.cleardata();//初始化结果
            if(this.xselected.length==0){
                this.makeToast('danger',"请选择x值！")
            }
            else if(this.yselected.length == 0){
                this.makeToast('danger',"请选择y值！")
            }
            else if(this.analytype=="gradually"&&this.criterion==""){
                this.makeToast('danger',"请选择优化规则")
            }
            else if(this.analytype=="gradually"&&this.direction==""){
                this.makeToast('danger',"请选择回归方向")
            }
            else{
                myaxios = this.creataxios()
                let that = this
                data={"fileindex":this.fileselectnum,"xselected":this.xselected,"yselected":this.yselected,
                    "analytype":this.analytype,"criterion":this.criterion,"direction":this.direction}
                myaxios.post('/analysis/sendselect',data)
                .then(function(res){
                    //console.log(res)
                    if(res.status!=200){
                        that.makeToast('danger',"请选择x值和y值！")
                    }
                    else if(res.data.result=='404'){//文件过期
                        that.makeToast('danger',res.data.msg)
                        that.deletefile(that.fileselectnum)
                    }
                    else{
                        that.showresult = true
                        that.model = res.data.model
                        that.f1 = res.data.f1;
                        that.f2 = res.data.f2;
                        that.xselected_change = res.data.xselected_change=='None' ? that.xselected :res.data.xselected_change//设置方差齐性检验图形法的可选参数
                    }
                })
                .catch(function(err){
                    //console.log(err)
                    that.fileloading = false
                    that.makeToast('danger',"请勿选择时间或字符的列！")
                })
            }
        },
        deletefile(fid){//删除过期文件
            var i = 0;
            for(i;i<this.filelist.length;i++){
                if(this.filelist[i][2]==fid) {
                    break
                }
                else if(i==this.filelist.length-1){
                    i =-1
                    break
                }
            }
            if(i!=-1){
                this.filelist.splice(i,1)//删除过期文件
                this.fileselectnum=this.filelist[i][2];//修改已选择的文件序号
                this.flavours=this.filelist[i][1];
                this.ylist=this.filelist[i][1];
            }
        },
        cleardata(){
            this.model="";//模型
            this.f1="";//计算f值
            this.f2="";//理论f值
            this.prediction_src="";//模型预测
            this.checkselect='回归模型预测';
            this.nortype='直方图';//正态性检验类型（直方图、qq图还是pp图、K-s检测）
            this.normality_src='';//正态性检测图片地址
            this.pp_src='';//pp图
            this.qq_src='';//qq图
            this.ksdata={};//K-S检测数据
            this.multicollinearity=[];//多重共线性检验数据
            this.lineselected=[];//线性相关性选择的列名
            this.linear_correlation_src='';//线性相关性检验图片地址
            this.testmodel='';//异常值检验模型数据
            this.testdw='';//检测模型的dw
            this.vartype='图形法';//方差齐性检测类型（图形法还是BP法）
            this.bpdata=[];//BP法数据
            this.oselected_1='';//方差齐性检验参数1
            this.oselected_2='';//方差齐性检验参数2
            this.variance_src='';//方差齐性检验图片地址
        },
        changeselectfile(item){//修改选择的文件后
            this.fileselectnum=item[2];
            this.flavours=item[1];
            this.ylist=item[1];
            this.xselected=[];
            this.yselected=[];
        },
        getprediction(){
            let that = this
            data={"fileindex":this.fileselectnum,"xselected":this.xselected,"yselected":this.yselected}
            myaxios = this.creataxios()
            myaxios.post('/analysis/getprediction',data)
            .then(function(res){
                 that.prediction_src = res.data.prediction_src
            })
        },
        getnormality(){
            let that = this
            data={"fileindex":this.fileselectnum,"xselected":this.xselected,"yselected":this.yselected}
            myaxios = this.creataxios()
            myaxios.post('/analysis/getnormality',data)
            .then(function(res){
                 that.normality_src = res.data.normality_src
            })
        },
        getppqq(){
            let that = this
            data={"fileindex":this.fileselectnum,"xselected":this.xselected,"yselected":this.yselected}
            myaxios = this.creataxios()
            myaxios.post('/analysis/getppqq',data)
            .then(function(res){
                that.pp_src=res.data.pp_src
                that.qq_src=res.data.qq_src
            })
        },
        getks(){
            let that = this
            data={"fileindex":this.fileselectnum,"xselected":this.xselected,"yselected":this.yselected}
            myaxios = this.creataxios()
            myaxios.post('/analysis/getks',data)
            .then(function(res){
                that.ksdata = res.data.ks
                //console.log(res)
            })
        },
        getmulticol(){
            let that = this
            data={"fileindex":this.fileselectnum,"xselected":this.xselected,"yselected":this.yselected}
            myaxios = this.creataxios()
            myaxios.post('/analysis/getmulticol',data)
            .then(function(res){
                that.multicollinearity=res.data.multicollinearity
            })
        },
        getlinearcorrelate(){
            let that = this
            data={"fileindex":this.fileselectnum,"xselected":this.xselected,"yselected":this.yselected,"lineselected":this.lineselected}
            if(this.lineselected.length<2){
                this.makeToast('danger',"至少选择两列！")
            }
            else{
                this.$refs['lineselect-modal'].hide()
                myaxios = this.creataxios()
                myaxios.post('/analysis/getlinearcorrelate',data)
                .then(function(res){
                    that.linear_correlation_src=res.data.linear_correlation_src
                })
            }
        },
        getoutliertest(){
            let that = this
            data={"fileindex":this.fileselectnum,"xselected":this.xselected,"yselected":this.yselected}
            myaxios = this.creataxios()
            myaxios.post('/analysis/getoutliertest',data)
            .then(function(res){
                that.testmodel=res.data.testmodel
            })
        },
        getresidual(){
            let that = this
            data={"fileindex":this.fileselectnum,"xselected":this.xselected,"yselected":this.yselected}
            myaxios = this.creataxios()
            myaxios.post('/analysis/getresidual',data)
            .then(function(res){
                that.testdw=res.data.dw
            })
        },
        getbp(){
             let that = this
            data={"fileindex":this.fileselectnum,"xselected":this.xselected,"yselected":this.yselected,
                "oselected_1":this.oselected_1,"oselected_2":this.oselected_2}
            myaxios = this.creataxios()
            myaxios.post('/analysis/getbp',data)
            .then(function(res){
                that.bpdata = res.data.bp;
            })
        },
        getvariance(){
            let that = this
            data={"fileindex":this.fileselectnum,"xselected":this.xselected,"yselected":this.yselected,
                "oselected_1":this.oselected_1,"oselected_2":this.oselected_2}
            myaxios = this.creataxios()
            myaxios.post('/analysis/getvariance',data)
            .then(function(res){
                //console.log(res)
                that.variance_src=res.data.variance_src
            })
        },
        makeToast(variant = null,body) {
            this.$bvToast.toast(body, {
                title: '提示',
                variant: variant,
                solid: true
            })
        }
    },
    watch:{
        progress(curVal,oldVal){
            if(curVal=='100%'){
                this.makeToast('success',"上传成功！")
                this.$refs['my-modal'].hide();
                this.progress=0;
            }
        },
        xselected(newVal, oldVal) {
        // Handle changes in individual flavour checkboxes
            if(newVal.indexOf(this.yselected)!=-1){//如果选择的yselected在选择的xselected中就将选择的yselected设为空，否则的话会出现选择的x列和y列都有这个值
                this.yselected=""
            }
            this.ylist=[]
            for(let x of this.flavours){
                if(newVal.indexOf(x)==-1){
                    if(this.ylist.indexOf(x)==-1){//如果列表中的值不在x选择的列中也不在ylist中，就添加该值
                        this.ylist.push(x)
                    }
                }
                else{
                    if(this.ylist.indexOf(x)!=-1){//如果列表中的值在x选择的列中也在ylist中，就删除该值
                        this.ylist.splice(this.ylist.indexOf(x),1)
                    }
                }
            }
            if (newVal.length === 0) {
              this.indeterminate = false
              this.allSelected = false
            } else if (newVal.length === this.flavours.length) {
              this.indeterminate = false
              this.allSelected = true
            } else {
              this.indeterminate = true
              this.allSelected = false
            }
          },
        showresult(newVal, oldVal){
            if(newVal==true){
                this.getprediction();
            }
        },
        checkselect(newVal,oldVal){
            this.imgloading = false;
            if(newVal=='回归模型预测'){
                this.getprediction()
            }
            else if(newVal=='正态性检验'){
                this.nortype='直方图';
                this.getnormality()
            }
            else if(newVal=='多重共线性检验'){
                this.getmulticol()
            }
            else if(newVal=='线性相关性检验'){
                this.$refs['lineselect-modal'].show()
            }
            else if(newVal=='异常值检验'){
                this.getoutliertest()
            }
            else if(newVal=='残差独立性检验'){
                this.getresidual()
            }
            else if(newVal=='方差齐性检验'){
                this.vartype='BP法';
            }
        },
        nortype(newVal, oldVal){//正态性检测类型
            if(newVal=='直方图'){
                this.getnormality()
            }
            else if(newVal=='pp图与qq图'){
                this.getppqq()
            }else if(newVal=='Shapiro检验和K-S检验'){
                this.getks()
            }
        },
        vartype(newVal, oldVal){//方差齐性检测bp法
            if(newVal=='BP法'){
                this.getbp()
            }
        },
        oselected_1(newVal, oldVal){//方差齐性检测图形法
            if(newVal!=""&&this.oselected_2!=""){
                this.getvariance()
            }
        },
        oselected_2(newVal, oldVal){//方差齐性检测图形法
            if(newVal!=""&&this.oselected_1!=""){
                this.getvariance()
            }
        },
    },
    created() {
			let uri =window.location.href
			let x=uri.split('/')
			let type = x[x.length-1]
            if(type=="linear"){
                this.analytype="linear"
            }
            else if(type=="gradually"){
                this.analytype="gradually"
            }
		}
})