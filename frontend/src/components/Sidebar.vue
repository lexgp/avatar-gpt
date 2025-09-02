<template>
  <div class="sidebar">
    <h2 class="title">Система знаний</h2>
    <p class="description">
      Добро пожаловать! Здесь можно узнать основную информацию о системе.
    </p>
    <div class="buttons">
      <el-button type="primary" @click="askQuestion">Задать вопрос</el-button>
      <el-button type="success" @click="writeMessage">Написать сообщение</el-button>
    </div>
  </div>

  <el-dialog
    v-model="dialogVisible"
    title="Написать сообщение"
    width="400px"
  >
    <el-input
      type="textarea"
      v-model="messageText"
      placeholder="Введите сообщение"
      rows="4"
    ></el-input>
    <template #footer>
      <el-button @click="dialogVisible = false">Отмена</el-button>
      <el-button type="primary" @click="sendMessage">Отправить</el-button>
    </template>
  </el-dialog>

</template>

<script setup lang="ts">
import { ref } from 'vue'
const dialogVisible = ref(false)
const messageText = ref('')

const emit = defineEmits<{
  (e: 'send-message', text: string): void
}>()

function askQuestion() {
  console.log('Задать вопрос')
}

function writeMessage() {
  console.log('refjerifier')
  dialogVisible.value = true
}

function sendMessage() {
  emit('send-message', messageText.value)
  messageText.value = ''
  dialogVisible.value = false
}

</script>

<style scoped>
.sidebar {
  width: 400px;
  min-height: 100vh;
  /* background-color: #222; */
  color: #fff;
  padding: 20px;
  box-sizing: border-box;
  /* border-right: 1px solid #444; */
  display: flex;
  flex-direction: column;
  justify-content: center;
  position: absolute;
}

.title {
  margin: 0 0 10px;
  font-size: 24px;
}

.description {
  font-size: 14px;
  margin-bottom: 20px;
  line-height: 1.5;
}

.buttons {
  display: flex;
  /* flex-direction: column; */
  gap: 5px;
}
.buttons > * {
  width: 50%;
}
</style>
