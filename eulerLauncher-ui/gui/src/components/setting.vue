<template>
    <div id="container" style="background-color: black;">
        1112
        <div id="xterm-container"></div>
    </div>
</template>

<script setup>
// import BtnUpdate from './BtnUpdate.vue'
</script>

<script>
import { Terminal } from 'xterm';
import 'xterm/css/xterm.css';
export default {
    name: 'index',
    data(){
        return{
            
        }
    },
    methods:{
        
    },
    mounted(){
        console.log(1)
        var term = new Terminal();
        term.open(document.getElementById('xterm-container'));
        // term.write('Hello from x1B[1;3;31mxterm.jsx1B[0m $ ')
    }
}
</script> 

<style scoped>
#container{
    height: 100vh;
    width: 100vw;
    display: flex;
    flex-direction: column;
}
</style>
