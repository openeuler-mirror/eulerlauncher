<template>
    <div id="container">
        <div id="nav">
            <div class="navItem" @click="openImg">
                <img class="navImg" alt="" src="../assets/images/image.png">
                <div class="navText">Images</div>
            </div>
            <div class="navItem" @click="openVm">
                <img class="navImg" alt="" src="../assets/images/vm.png">
                <div class="navText">virtual machine</div>
            </div>
            <!-- <div class="navItem" @click="openSet">
                <img class="navImg" alt="" src="../assets/images/setting.png">
                <div class="navText">Settings</div>
            </div> -->
        </div>
        <div class="bottom">
            <!-- image盒子 -->
            <div class="boContainer" v-if="nowShowImg()">
                <div class="boInnerBox">
                    <el-button @click="addImage" type="primary" style="margin-bottom:20px;">Add Image From Local</el-button>
                    <el-button type="primary" style="margin-bottom:20px;" @click="reImageList">Refresh</el-button>
                    <div id="imageList">
                        <div class="title">Images</div>
                        <el-table :data="myImage" style="width: 100%;margin-bottom:20px">
                            <el-table-column prop="name" label="Images" width="180"></el-table-column>
                            <el-table-column prop="location" label="Location " width="180"></el-table-column>
                            <el-table-column prop="status" label="Status"></el-table-column>
                            <el-table-column prop="Option" label="Option">
                                <template #default="scope" style="display:flex">
                                    <el-button @click="delImage(scope.row.name)" v-if="scope.row.status == 'Ready'" type="danger" link size="small">删除</el-button>
                                    <el-button @click="downloadImage(scope.row.name)" v-if="scope.row.status == 'Downloadable'" type="primary" link size="small">下载</el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                    </div>
                </div>
            </div>
            <!-- VM盒子 -->
            <div class="boContainer" v-if="nowShowVm()">
                <div class="boInnerBox">
                    <el-button @click="openDia" type="primary" style="margin-bottom:20px;">Add New Virtual Machine</el-button>
                    <el-button @click="refresh" type="primary" style="margin-bottom:20px;">Refresh</el-button>
                    <div id="imageList">
                        <div class="title">My Virtual Machine</div>
                        <el-table :data="myIns" style="width: 100%;margin-bottom:20px">
                            <el-table-column prop="name" label="Name" width="90"></el-table-column>
                            <el-table-column prop="image" label="Image " width="180"></el-table-column>
                            <el-table-column prop="state" label="State" width="90"></el-table-column>
                            <el-table-column prop="ip" label="IP" width="180"></el-table-column>
                            <el-table-column prop="Option" label="Option">
                                <template #default="scope" style="display:flex">
                                    <el-button @click="delInstance(scope.row.name)" type="danger" link size="small">删除</el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                    </div>
                    <div class="dig" v-if="dialogFormVisible">
                        <div class="digInner">
                            <div class="diTitle">添加实例</div>
                            <el-form class="disForm">
                                <el-form-item label="实例名称" :label-width="formLabelWidth">
                                <el-input v-model="addInsName" autocomplete="off"></el-input>
                                </el-form-item>
                                <el-form-item label="选择镜像" :label-width="formLabelWidth">
                                <el-select v-model="addInsImage" placeholder="请选择镜像">
                                    <el-option v-for="(item,index) in imageList" :key="index" :label="item" :value="item"></el-option>
                                </el-select>
                                </el-form-item>
                            </el-form>
                            <div slot="footer" class="dialog-footer">
                                <el-button @click="dialogFormVisible = false" style="margin-right:20px;width:90px;height:40px">取 消</el-button>
                                <el-button type="primary" @click="confirmAdd" style="margin-right:20px;width:90px;height:40px">确 定</el-button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- <ImageView class="bottom" v-if="nowShowImg()"></ImageView> -->
        <!-- <VmView class="bottom" v-if="nowShowVm()"></VmView> -->
        <!-- <SettingView class="bottom" v-if="nowShowSet()"></SettingView> -->
    </div>
</template>
 
<script setup>
// import ImageView from './images.vue'
// import VmView from './vm.vue'
// import SettingView from './setting.vue'

</script>

<script>
export default {
    name: 'index',
    data(){
        return{
            nowImg:1,
            nowVm:0,
            // nowSet:0,
            myImage: [],
            dialogFormVisible: false,
            myIns: [],
            imageList:[],
            addInsName:'',
            addInsImage:'',
            formLabelWidth:'120px',
        }
    },
    methods:{
        nowShowImg(){
            // this.getImageList()
            // console.log(1)
            return this.nowImg
        },
        nowShowVm(){
            // this.refresh()
            return this.nowVm
        },
        // nowShowSet(){
        //     return this.nowSet
        // },
        openImg(){
            this.nowImg = 1;
            this.nowVm = 0;
            this.nowSet = 0;
        },
        openVm(){
            this.nowImg = 0;
            this.nowVm = 1;
            this.nowSet = 0;
        },
        // openSet(){
        //     this.nowImg = 0;
        //     this.nowVm = 0;
        //     this.nowSet = 1;
        // },
        // getImageList(){
        //     // 获取虚拟机列表
        //     var that = this
        //     window.addEventListener('pywebviewready', function () {
        //         pywebview.api.getImageList().then(
        //         function(res){
        //             // console.log(res)
        //             that.myImage = res
        //             // console.log(that.myImage)
        //             // res直接就是列表格式，字典的key就是说明文档上对应输出的小写
        //         }
        //     )
        //     })
        // },
        reImageList(){
            // 获取虚拟机列表
            var that = this
            // window.addEventListener('pywebviewready', function () {
                pywebview.api.getImageList().then(
                function(res){
                    // console.log(res)
                    that.myImage = res
                    // console.log(that.myImage)
                    // res直接就是列表格式，字典的key就是说明文档上对应输出的小写
                }
            )
            // })
        },
        delImage(name){
            var that = this
            // window.addEventListener('pywebviewready', function () {
                pywebview.api.deleteImage(name).then(
                function(res){
                    // console.log(res)
                    that.reImageList()
                }
            )
            // })
        },
        downloadImage(imageName){
            var that = this
            // window.addEventListener('pywebviewready', function () {
            //     console.log(imageName)
                pywebview.api.downloadImage(imageName).then(
                    function(res){
                        // console.log(res)
                        // 然后 getImageList
                        that.reImageList()
                    }
                )
            // })
        },
        addImage(){
            var that = this
            pywebview.api.system_pyCreateFileDialog().then(
                function(res1){
                    // console.log(res1)
                    window.pywebview.api.loadLocalImage(res1).then(
                        function(res2){
                            // console.log(res2)
                            that.reImageList()
                        }
                    )
                }
            )
        },
        // vm
        openDia(){
            this.dialogFormVisible = true
            var that = this
            this.imageList = []
            pywebview.api.getImageList().then(
                function(res){
                    for(var i=0;i<res.length;i++){
                        if (res[i].status == "Ready"){
                            that.imageList.push(res[i].name)
                            // console.log(that.imageList)
                        }
                    }
                }
            )
        },
        refresh(){
            var that = this
            // window.addEventListener('pywebviewready', function () {
                pywebview.api.getInstanceList().then(
                function(res){
                    // console.log(res)
                    that.myIns = res.slice(1)
                    console.log(that.myIns)
                }
            )
            // })
        },
        // getInstanceList(){
        //     var that = this
        //     window.addEventListener('pywebviewready', function () {
        //         pywebview.api.getInstanceList().then(
        //         function(res){
        //             that.myIns = res.slice(1);
        //             // console.log(that.myIns)
        //         }
        //     )
        //     })
        // },
        // getImageList(){
        //     // 获取虚拟机列表
        //     var that = this
        //     this.imageList = []
        //     window.addEventListener('pywebviewready', function () {
        //         pywebview.api.getImageList().then(
        //         function(res){
        //             // console.log(res)
        //             for(var i=0;i<res.length;i++){
        //                 if (res[i].status == "Ready"){
        //                     that.imageList.push(res[i].name)
        //                 }
        //             }
        //         }
        //     )
        //     })
        // },
        delInstance(name){
            var that = this
            // window.addEventListener('pywebviewready', function () {
                pywebview.api.deleteInstance(name).then(
                function(res){
                    // console.log(res)
                    that.refresh()
                }
            )
            // })
        },
        confirmAdd(){
            this.dialogFormVisible = false
            var image = this.addInsImage
            var name = this.addInsName
            // console.log(image)
            // console.log(name)
            // window.addEventListener('pywebviewready', function () {
                pywebview.api.createInstance(image,name).then(
                function(res){
                    // console.log(res)
                    that.refresh()
                }
            )
            // })
        }
    },
    mounted(){
        setTimeout(() =>{
            this.reImageList();
            this.refresh();
        }, 1000); // 延迟1秒执行
    }
}
</script> 

<style scoped src="../assets/css/index.css"></style>

<style scoped>
#container{
    height: 100vh;
    width: 100vw;
    display: flex;
    flex-direction: row;
}
#nav{
    height: 100%;
    width: 30%;
    background-color: rgb(239,239,242);
}
.bottom{
    height: 100%;
    width: 70%;
}
.navItem{
    height: 60px;
    width: 100%;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    flex-direction: row;
    cursor: pointer;
}
.navText{
    color: rgb(80,89,126);
    font-size: 20px;
    margin-left: 10px;
}
.navImg{
    height: 35px;
    margin-left: 20px;
}
.boContainer{
    height: 100%;
    width: 100%;
    display: flex;
    flex-direction: column;
    display: flex;
    justify-content: center;
    align-items: center;
}
.boInnerBox{
    height:90%;
    width:90%;
}
.title{
    font-size: 20px;
    margin-bottom: 20px;
}
.dig{
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    z-index: 2000;
    height: 100%;
    background-color: var(--el-overlay-color-lighter);
    display: flex;
    justify-content: center;
    align-items: center;
}
.digInner{
    height: 300px;
    width: 600px;
    background-color: #fff;
    display: flex;
    justify-content: flex-start;
    align-items: flex-start;
    flex-direction: column;
}
.diTitle{
    font-size: 30px;
    margin-top: 20px;
    margin-left: 20px;
}
.disForm{
    margin-top: 40px;
}
.dialog-footer{
    width: 100%;
    height: 50px;
    display: flex;
    justify-content: flex-end;
    align-items: center;
    flex-direction: row;
    margin-top: 30px;
}
</style>
