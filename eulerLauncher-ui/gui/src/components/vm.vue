<template>
    <div id="container">
        <div id="innerBox">
            <el-button @click="openDia" type="primary" style="margin-bottom:20px;">Add New Virtual Machine</el-button>
            <el-button @click="refresh" type="primary" style="margin-bottom:20px;">Refresh</el-button>
            <div id="imageList">
                <div class="title">My Virtual Machine</div>
                <el-table :key="update" :data="myVm" style="width: 100%;margin-bottom:20px">
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
</template>

<script>
export default {
    name: 'index',
    data(){
        return{
            update: false,
            dialogFormVisible: false,
            myVm: [
                // {image: "22.03-LTS",
                // ip: "172.28.19.251",
                // name: "test",
                // state: "Running",}
            // {
            //     name:'test1',
            //     image: '2203-load',
            //     state: 'Running',
            //     iP: '172.22.57.220'
            // },{
            //     name:'test2',
            //     image: '2203-load',
            //     state: 'Running',
            //     iP: 'N/A'
            // },
            ],
            imageList:[],
            addInsName:'',
            addInsImage:'',
            formLabelWidth:'120px',
        }
    },
    methods:{
        openDia(){
            this.dialogFormVisible = true
            var that = this
            this.imageList = []
            pywebview.api.getImageList().then(
                function(res){
                    for(var i=0;i<res.length;i++){
                        if (res[i].status == "Ready"){
                            that.imageList.push(res[i].name)
                            that.update=!that.update
                            console.log(that.imageList)
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
                    that.myVM = res.slice(1)
                    that.update=!that.update
                    console.log(that.myVM)
                }
            )
            // })
        },
        getInstanceList(){
            var that = this
            window.addEventListener('pywebviewready', function () {
                pywebview.api.getInstanceList().then(
                function(res){
                    that.myVM = res.slice(1);
                    that.update=!that.update
                    console.log(that.myVM)
                }
            )
            })
        },
        getImageList(){
            // 获取虚拟机列表
            var that = this
            window.addEventListener('pywebviewready', function () {
                pywebview.api.getImageList().then(
                function(res){
                    console.log(res)
                    for(var i=0;i<res.length;i++){
                        if (res[i].status == "Ready"){
                            that.imageList.push(res[i].name)
                        }
                    }
                }
            )
            })
        },
        delInstance(name){
            var that = this
            window.addEventListener('pywebviewready', function () {
                pywebview.api.deleteInstance(name).then(
                function(res){
                    console.log(res)
                    that.getInstanceList()
                }
            )
            })
        },
        confirmAdd(){
            this.dialogFormVisible = false
            var image = this.addInsImage
            var name = this.addInsName
            console.log(image)
            console.log(name)
            // window.addEventListener('pywebviewready', function () {
                pywebview.api.createInstance(image,name).then(
                function(res){
                    console.log(res)
                }
            )
            // })
        }
    },
    mounted(){
        this.getInstanceList();
    }
}
</script> 

<script setup>
// import BtnUpdate from './BtnUpdate.vue'

</script>

<style scoped>
#container{
    height: 100%;
    width: 100%;
    display: flex;
    flex-direction: column;
    display: flex;
    justify-content: center;
    align-items: center;
}
#innerBox{
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
