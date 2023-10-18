<template>
    <div id="container">
        <div id="innerBox">
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
</template>

<script>
export default {
    name: 'index',
    data(){
        return{
            myImage: [
            // {
            //     Images: '22.03-LTS',
            //     Location: 'Remote',
            //     Status: 'Loading'
            // },{
            //     Images: '21.09',
            //     Location: 'Remote',
            //     Status: 'Ready'
            // },{
            //     Images: '22.03-LTS',
            //     Location: 'Local',
            //     Status: 'Downloading'
            // },{
            //     Images: '22.03-LTS',
            //     Location: 'Remote',
            //     Status: 'Downloadable'
            // },{
            //     Images: '21.09',
            //     Location: 'Remote',
            //     Status: 'Downloadable'
            // },{
            //     Images: '22.03-LTS',
            //     Location: 'Local',
            //     Status: 'Ready'
            // },
            ]
        }
    },
    methods:{
        getImageList(){
            // 获取虚拟机列表
            var that = this
            window.addEventListener('pywebviewready', function () {
                pywebview.api.getImageList().then(
                function(res){
                    console.log(res)
                    that.myImage = res
                    // res直接就是列表格式，字典的key就是说明文档上对应输出的小写
                }
            )
            })
        },
        reImageList(){
            // 获取虚拟机列表
            var that = this
            // window.addEventListener('pywebviewready', function () {
                pywebview.api.getImageList().then(
                function(res){
                    console.log(res)
                    that.myImage = res
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
                    console.log(res)
                    that.getImageList()
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
                        console.log(res)
                        // 然后 getImageList
                        that.getImageList()
                    }
                )
            // })
        },
        addImage(){
            var that = this
            pywebview.api.system_pyCreateFileDialog().then(
                function(res1){
                    console.log(res1)
                    window.pywebview.api.loadLocalImage(res1).then(
                        function(res2){
                            console.log(res2)
                            that.getImageList()
                        }
                    )
                }
            )
        },
        apiList(){
            // 获取虚拟机列表
            window.pywebview.api.getImageList().then(
                function(res){
                    console.log(res)
                    // res直接就是列表格式，字典的key就是说明文档上对应输出的小写
                }
            )
            
            // 下载镜像，输入镜像名。这个函数在开始下载时就会返回了，需要重新请求一次getImageList来获取下载状态
            var imageName
            window.pywebview.api.downloadImage(imageName).then(
                function(res){
                    console.log(res)
                    // 然后 getImageList
                }
            )

            // 加载本地镜像，需要路径和镜像名
            var path,name
            window.pywebview.api.loadLocalImage(path,name).then(
                function(res){
                    console.log(res)
                }
            )
            
            // 删除镜像，需要镜像名
            var name
            window.pywebview.api.deleteImage(name).then(
                function(res){
                    console.log(res)
                }
            )

            // 获取虚拟机列表
            window.pywebview.api.getInstanceList().then(
                function(res){
                    console.log(res)
                }
            )

            // 创建虚拟机，需要镜像名和虚拟机名
            var image,name
            window.pywebview.api.createInstance(image,name).then(
                function(res){
                    console.log(res)
                }
            )
            // 删除虚拟机，需要虚拟机名称。 
            var name
            window.pywebview.api.deleteInstance(name).then(
                function(res){
                    console.log(res)
                }
            )

        }
    },
    mounted(){
        console.log('moun')
        this.getImageList();
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
</style>
