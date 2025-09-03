<template>
  <div class="sidebar">
    <h2 class="title">Справочная система</h2>
    <p class="description">
      Голосовой доступ к документообороту и RAG-системе.
    </p>
    <div class="buttons">
      <!-- <el-button type="primary" @click="askQuestion">Задать вопрос</el-button> -->
      <el-button
        :type="isRecording ? 'danger' : 'primary'"
        :loading="isProcessing"
        @click="startRecording"
      >
        {{ isRecording ? '🎤 Стоп' : '🎤 Задать вопрос' }}
      </el-button>

      <span class="text-loading" v-if="isRecording">Идёт запись...</span>
      <el-button v-else
        type="success"
        :loading="isProcessing"
        @click="writeMessage"
      >
        Написать сообщение
      </el-button>
    </div>
  </div>

  <el-dialog
    v-model="dialogVisible"
    title="Написать сообщение"
    width="400px"
  >
    <el-input
      @key.c.enter
      type="textarea"
      v-model="messageText"
      placeholder="Введите сообщение"
      rows="4"
      id="messageInput"
      tabindex="0"
    ></el-input>
    <template #footer>
      <el-button @click="dialogVisible = false">Отмена</el-button>
      <el-button type="primary" @click="sendMessage">Отправить</el-button>
    </template>
  </el-dialog>

</template>

<script setup lang="ts">
import { ref, nextTick, watch } from 'vue'

const isRecording = ref(false)
const audioChunks: BlobPart[] = []
let mediaRecorder: MediaRecorder | null = null

const dialogVisible = ref(false)
const messageText = ref('')

const emit = defineEmits<{
  (e: 'send-message', text: string): void
  (e: 'send-audio', blob: Blob): void
}>()

defineProps({
  isProcessing: {
    type: Boolean,
    default: false
  }
})

// function askQuestion() {
//   console.log('Задать вопрос')
// }

function writeMessage() {
  console.log('refjerifier')
  dialogVisible.value = true
}

function sendMessage() {
  emit('send-message', messageText.value)
  messageText.value = ''
  dialogVisible.value = false
}

watch(dialogVisible, (val) => {
  if (val) {
    setTimeout(() => {
      nextTick(() => {
        const messageInput = document.querySelector('#messageInput') as HTMLInputElement
        messageInput.focus()
      })
    }, 500);
  }
})

async function startRecording() {

  if (isRecording.value) {
    await stopAndSendRecording()
    return
  }

  const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
  mediaRecorder = new MediaRecorder(stream)
  audioChunks.length = 0

  mediaRecorder.ondataavailable = (event) => {
    audioChunks.push(event.data)
  }

  mediaRecorder.start()
  isRecording.value = true
}

async function stopAndSendRecording() {
  if (!mediaRecorder || !isRecording.value) return

  mediaRecorder.onstop = async () => {
    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' })
    emit('send-audio', audioBlob)
  }

  mediaRecorder.stop()
  isRecording.value = false
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

.text-loading {
  padding: 8px 15px;
  font-size: 14px;
}
</style>
