<template>
    <div id="container">
        hello!!!!!!!!!!!!!!!!
    </div>
</template>

<script>
export default {
    name: 'index',
    data(){
        return{
            hardAnimation:'showUpdateBox'
        }
    },
    methods:{
    },
    mounted:function(){
    },
    destroyed:function(){
    }
}
</script> 

<style scoped src="../assets/css/index.css"></style>
<style scoped>
*{
    padding: 0;
    margin: 0;
}
#container{
    height: 100vh;
    width: 100vw;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
}
</style>
