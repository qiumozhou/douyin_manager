<template>
  <div class="ai-generation">
    <el-container>
      <el-header class="header">
        <div class="header-content">
          <h1>AI生成</h1>
        </div>
      </el-header>
      
      <el-container>
        <el-aside width="200px" class="sidebar">
          <el-menu 
            :default-active="activeMenu" 
            router
            class="sidebar-menu"
          >
            <el-menu-item index="/dashboard">
              <el-icon><DataBoard /></el-icon>
              <span>仪表板</span>
            </el-menu-item>
            <el-menu-item index="/videos">
              <el-icon><VideoPlay /></el-icon>
              <span>视频管理</span>
            </el-menu-item>
            <el-menu-item index="/ai">
              <el-icon><MagicStick /></el-icon>
              <span>AI生成</span>
            </el-menu-item>
            <el-menu-item index="/douyin">
              <el-icon><Share /></el-icon>
              <span>抖音发布</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        
        <el-main class="main-content">
          <el-tabs v-model="activeTab" class="ai-tabs">
            <el-tab-pane label="文本生成" name="text">
              <el-card>
                <template #header>
                  <span>AI文本生成</span>
                </template>
                <el-form :model="textForm" :rules="textRules" ref="textFormRef">
                  <el-form-item label="提示词" prop="prompt">
                    <el-input 
                      v-model="textForm.prompt" 
                      type="textarea" 
                      placeholder="请输入您想要生成的文本内容描述"
                      :rows="4"
                    />
                  </el-form-item>
                  <el-form-item>
                    <el-button 
                      type="primary" 
                      @click="generateText" 
                      :loading="generating"
                    >
                      生成文本
                    </el-button>
                  </el-form-item>
                </el-form>
                
                <div v-if="textResult" class="result-section">
                  <h4>生成结果：</h4>
                  <el-input 
                    v-model="textResult" 
                    type="textarea" 
                    :rows="6" 
                    readonly
                  />
                  <el-button @click="copyText" style="margin-top: 10px;">
                    复制文本
                  </el-button>
                </div>
              </el-card>
            </el-tab-pane>
            
            <el-tab-pane label="标题生成" name="title">
              <el-card>
                <template #header>
                  <span>AI标题生成</span>
                </template>
                <el-form :model="titleForm" :rules="titleRules" ref="titleFormRef">
                  <el-form-item label="视频内容" prop="content">
                    <el-input 
                      v-model="titleForm.content" 
                      type="textarea" 
                      placeholder="请描述您的视频内容"
                      :rows="4"
                    />
                  </el-form-item>
                  <el-form-item>
                    <el-button 
                      type="primary" 
                      @click="generateTitle" 
                      :loading="generating"
                    >
                      生成标题
                    </el-button>
                  </el-form-item>
                </el-form>
                
                <div v-if="titleResult" class="result-section">
                  <h4>生成结果：</h4>
                  <el-input 
                    v-model="titleResult" 
                    type="textarea" 
                    :rows="6" 
                    readonly
                  />
                  <el-button @click="copyText" style="margin-top: 10px;">
                    复制文本
                  </el-button>
                </div>
              </el-card>
            </el-tab-pane>
            
            <el-tab-pane label="描述生成" name="description">
              <el-card>
                <template #header>
                  <span>AI描述生成</span>
                </template>
                <el-form :model="descriptionForm" :rules="descriptionRules" ref="descriptionFormRef">
                  <el-form-item label="视频标题" prop="title">
                    <el-input 
                      v-model="descriptionForm.title" 
                      placeholder="请输入视频标题"
                    />
                  </el-form-item>
                  <el-form-item label="视频内容" prop="content">
                    <el-input 
                      v-model="descriptionForm.content" 
                      type="textarea" 
                      placeholder="请描述您的视频内容"
                      :rows="4"
                    />
                  </el-form-item>
                  <el-form-item>
                    <el-button 
                      type="primary" 
                      @click="generateDescription" 
                      :loading="generating"
                    >
                      生成描述
                    </el-button>
                  </el-form-item>
                </el-form>
                
                <div v-if="descriptionResult" class="result-section">
                  <h4>生成结果：</h4>
                  <el-input 
                    v-model="descriptionResult" 
                    type="textarea" 
                    :rows="6" 
                    readonly
                  />
                  <el-button @click="copyText" style="margin-top: 10px;">
                    复制文本
                  </el-button>
                </div>
              </el-card>
            </el-tab-pane>
            
            <el-tab-pane label="图片生成" name="image">
              <el-card>
                <template #header>
                  <span>AI图片生成</span>
                </template>
                <el-form :model="imageForm" :rules="imageRules" ref="imageFormRef">
                  <el-form-item label="图片描述" prop="prompt">
                    <el-input 
                      v-model="imageForm.prompt" 
                      type="textarea" 
                      placeholder="请描述您想要生成的图片内容"
                      :rows="4"
                    />
                  </el-form-item>
                  <el-form-item label="生成模型">
                    <el-select v-model="imageForm.model">
                      <el-option label="Stable Diffusion" value="stable-diffusion" />
                      <el-option label="DALL-E" value="dall-e" />
                    </el-select>
                  </el-form-item>
                  <el-form-item>
                    <el-button 
                      type="primary" 
                      @click="generateImage" 
                      :loading="generating"
                    >
                      生成图片
                    </el-button>
                  </el-form-item>
                </el-form>
                
                <div v-if="imageResult" class="result-section">
                  <h4>生成结果：</h4>
                  <div class="image-result">
                    <img :src="imageResult" alt="生成的图片" style="max-width: 100%; max-height: 400px;" />
                  </div>
                  <el-button @click="downloadImage" style="margin-top: 10px;">
                    下载图片
                  </el-button>
                </div>
              </el-card>
            </el-tab-pane>
          </el-tabs>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { generateText as apiGenerateText, generateTitle as apiGenerateTitle, generateDescription as apiGenerateDescription, generateImage as apiGenerateImage } from '../api/ai'
import { DataBoard, VideoPlay, MagicStick, Share } from '@element-plus/icons-vue'

const route = useRoute()
const activeTab = ref('text')
const generating = ref(false)
const textResult = ref('')
const titleResult = ref('')
const descriptionResult = ref('')
const imageResult = ref('')

const textForm = reactive({
  prompt: ''
})

const titleForm = reactive({
  content: ''
})

const descriptionForm = reactive({
  title: '',
  content: ''
})

const imageForm = reactive({
  prompt: '',
  model: 'stable-diffusion'
})

const textFormRef = ref()
const titleFormRef = ref()
const descriptionFormRef = ref()
const imageFormRef = ref()

const activeMenu = computed(() => route.path)

const textRules = {
  prompt: [{ required: true, message: '请输入提示词', trigger: 'blur' }]
}

const titleRules = {
  content: [{ required: true, message: '请输入视频内容', trigger: 'blur' }]
}

const descriptionRules = {
  title: [{ required: true, message: '请输入视频标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入视频内容', trigger: 'blur' }]
}

const imageRules = {
  prompt: [{ required: true, message: '请输入图片描述', trigger: 'blur' }]
}

const generateText = async () => {
  try {
    await textFormRef.value.validate()
    generating.value = true
    
    const response = await apiGenerateText(textForm.prompt)
    textResult.value = response.data.result
    ElMessage.success('文本生成成功')
  } catch (error) {
    ElMessage.error('生成失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    generating.value = false
  }
}

const generateTitle = async () => {
  try {
    await titleFormRef.value.validate()
    generating.value = true
    
    const response = await apiGenerateTitle(titleForm.content)
    titleResult.value = response.data.result
    ElMessage.success('标题生成成功')
  } catch (error) {
    ElMessage.error('生成失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    generating.value = false
  }
}

const generateDescription = async () => {
  try {
    await descriptionFormRef.value.validate()
    generating.value = true
    
    const response = await apiGenerateDescription(descriptionForm.title, descriptionForm.content)
    descriptionResult.value = response.data.result
    ElMessage.success('描述生成成功')
  } catch (error) {
    ElMessage.error('生成失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    generating.value = false
  }
}

const generateImage = async () => {
  try {
    await imageFormRef.value.validate()
    generating.value = true
    
    const response = await apiGenerateImage(imageForm.prompt, imageForm.model)
    imageResult.value = response.data.file_path
    ElMessage.success('图片生成成功')
  } catch (error) {
    ElMessage.error('生成失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    generating.value = false
  }
}

const copyText = () => {
  const textToCopy = textResult.value || titleResult.value || descriptionResult.value
  if (textToCopy) {
    navigator.clipboard.writeText(textToCopy)
    ElMessage.success('已复制到剪贴板')
  }
}

const downloadImage = () => {
  if (imageResult.value) {
    const link = document.createElement('a')
    link.href = imageResult.value
    link.download = 'generated-image.png'
    link.click()
  }
}
</script>

<style scoped>
.ai-generation {
  height: 100vh;
}

.header {
  background: #fff;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  align-items: center;
  padding: 0 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.header-content h1 {
  margin: 0;
  color: #333;
}

.sidebar {
  background: #fff;
  border-right: 1px solid #e6e6e6;
}

.sidebar-menu {
  border-right: none;
}

.main-content {
  padding: 20px;
  background: #f5f5f5;
}

.ai-tabs {
  background: #fff;
  border-radius: 4px;
}

.result-section {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #e6e6e6;
}

.result-section h4 {
  margin-bottom: 10px;
  color: #333;
}

.image-result {
  text-align: center;
  margin: 10px 0;
}
</style> 