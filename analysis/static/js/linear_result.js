
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
        model_params:[],//模型的参数列
        sin_pre_value:"",//预测单一值
        mul_pre_file:"",//多值预测文件
        mul_pre_result:"",//多值预测结果
        prediction_src:"",//模型预测图片
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
        sendselect(){
            myaxios = this.creataxios()
                let that = this
                data={}
                myaxios.post('/analysis/sendselect',data)
                .then(function(res){
                    //console.log(res)
                    if(res.status!=200){
                        that.makeToast('danger',"请选择x值和y值！")
                    }
                    else if(res.data.result=='404'){//文件过期
                        that.makeToast('danger',res.data.msg)
                        //that.deletefile(that.fileselectnum)
                    }
                    else{
                        that.showresult = true
                        that.model = res.data.model
                        params=[]
                        for(var i=0;i<res.data.model_params.length;i++){
                            if(res.data.model_params[i]!='const'){
                                params.push(res.data.model_params[i])
                            }
                        }
                        that.model_params = params
                        that.f1 = res.data.f1;
                        that.f2 = res.data.f2;
                        that.fileselectnum = res.data.fileindex
                        that.xselected = res.data.xselected
                        that.yselected = res.data.yselected
                        that.analytype = res.data.analytype
                        that.criterion = res.data.criterion
                        that.direction = res.data.direction
                        that.flavours = res.data.xlist
                        that.xselected_change = res.data.xselected_change=='None' ? that.xselected :res.data.xselected_change//设置方差齐性检验图形法的可选参数
                    }
                })
                .catch(function(err){
                    //console.log(err)
                    that.fileloading = false
                    that.makeToast('danger',"发生了错误: "+err)
                })
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
        getsin_pre_value(){//获取预测值
            params = []
            let i = 0;
            checkednull=1
            for(i;i<this.model_params.length;i++){
                ref = "param_"+i;
                value = this.$refs[ref][0].localValue
                if(value==""){
                    checkednull = 0;
                    break;
                }
                params.push(value)
            }//获取相对应的值
            if(checkednull==0){
                this.makeToast('danger',"请勿输入空值！")
            }
            else{
                //console.log(params)
                let that = this
                data={"fileindex":this.fileselectnum,"params":params,}
                myaxios = this.creataxios()
                myaxios.post('/analysis/getsin_pre_value',data)
                .then(function(res){
                     that.sin_pre_value = res.data.sin_pre_value
                })
            }
        },
        createPretable(){//生成参数表格
            var data = []
            var title = []
            for(var i=0;i<this.model_params.length;i++){
                if(this.model_params[i]!='const'){
                    title.push(this.model_params[i])
                }
            }
            data.push(title)
            var sheet = XLSX.utils.aoa_to_sheet(data);
            this.openDownloadDialog(this.sheet2blob(sheet), '参数模板.xlsx');
        },
        // 将一个sheet转成最终的excel文件的blob对象，然后利用URL.createObjectURL下载
        sheet2blob(sheet, sheetName) {
            sheetName = sheetName || 'sheet1';
            var workbook = {
                SheetNames: [sheetName],
                Sheets: {}
            };
            workbook.Sheets[sheetName] = sheet;
            // 生成excel的配置项
            var wopts = {
                bookType: 'xlsx', // 要生成的文件类型
                bookSST: false, // 是否生成Shared String Table，官方解释是，如果开启生成速度会下降，但在低版本IOS设备上有更好的兼容性
                type: 'binary'
            };
            var wbout = XLSX.write(workbook, wopts);
            var blob = new Blob([s2ab(wbout)], {type:"application/octet-stream"});
            // 字符串转ArrayBuffer
            function s2ab(s) {
                var buf = new ArrayBuffer(s.length);
                var view = new Uint8Array(buf);
                for (var i=0; i!=s.length; ++i) view[i] = s.charCodeAt(i) & 0xFF;
                return buf;
            }
            return blob;
        },
        openDownloadDialog(url, saveName)
            {
                if(typeof url == 'object' && url instanceof Blob)
                {
                    url = URL.createObjectURL(url); // 创建blob地址
                }
                var aLink = document.createElement('a');
                aLink.href = url;
                aLink.download = saveName || ''; // HTML5新增的属性，指定保存文件名，可以不要后缀，注意，file:///模式下不会生效
                var event;
                if(window.MouseEvent) event = new MouseEvent('click');
                else
                {
                    event = document.createEvent('MouseEvents');
                    event.initMouseEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
                }
                aLink.dispatchEvent(event);
            },
        submitpre_file(e){//上传多值预测文件
            var that=this
            let file = e.target.files[0];
            var formdata=new FormData();
            formdata.append('file',file,);
            formdata.append('fileindex',this.fileselectnum,);
            formdata.append("xselected",this.xselected);
            formdata.append("yselected",this.yselected);
            let config = {
                 headers:{'Content-Type':false},
                onUploadProgress: progressEvent => {
                    var complete = (progressEvent.loaded / progressEvent.total * 100 | 0) + '%'
                    this.progress = complete
                }
            };  //添加请求头
            myaxios = this.creataxios()
            myaxios.post('/analysis/uploadpre_file',formdata,config)
            .then(function(res){
                //console.log(res.data)
                if(res.data.result=='1'){
                    that.mul_pre_result = res.data.mul_pre_result
                }
                else if(res.data.result=='500'&&res.data.except=='keyerror'){
                    that.makeToast('danger',"请上传正确文件或下载参数模板，并重新填写上传")
                }
            })
            .catch(function(err){
                    that.makeToast('danger',err)
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
                if(this.$refs['my-modal']!=undefined){
                    this.$refs['my-modal'].hide();
                }
                this.progress=0;
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
        this.sendselect()
		}
})