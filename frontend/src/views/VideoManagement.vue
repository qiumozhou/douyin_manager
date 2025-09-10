<template>
  <div class="video-management">
    <el-container>
      <el-header class="header">
        <div class="header-content">
          <h1>视频管理</h1>
          <el-button type="primary" @click="showUploadDialog = true">
            上传视频
          </el-button>
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
          <el-card>
            <template #header>
              <div class="card-header">
                <span>视频列表</span>
                <el-input
                  v-model="searchQuery"
                  placeholder="搜索视频标题"
                  style="width: 200px"
                  clearable
                />
              </div>
            </template>
            
            <el-table :data="filteredVideos" style="width: 100%">
              <el-table-column prop="title" label="标题" />
              <el-table-column prop="description" label="描述" show-overflow-tooltip />
              <el-table-column prop="status" label="状态" width="100">
                <template #default="scope">
                  <el-tag :type="getStatusType(scope.row.status)">
                    {{ getStatusText(scope.row.status) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="publish_status" label="发布状态" width="100">
                <template #default="scope">
                  <el-tag :type="getPublishStatusType(scope.row.publish_status)">
                    {{ getPublishStatusText(scope.row.publish_status) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="created_at" label="创建时间" width="150" />
              <el-table-column label="操作" width="200">
                <template #default="scope">
                  <el-button size="small" @click="editVideo(scope.row)">
                    编辑
                  </el-button>
                  <el-button 
                    size="small" 
                    type="danger" 
                    @click="handleDeleteVideo(scope.row.id)"
                  >
                    删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-main>
      </el-container>
    </el-container>
    
    <!-- 上传视频对话框 -->
    <el-dialog v-model="showUploadDialog" title="上传视频" width="500px">
      <el-form :model="uploadForm" :rules="uploadRules" ref="uploadFormRef">
        <el-form-item label="视频文件" prop="file">
          <el-upload
            ref="uploadRef"
            :auto-upload="false"
            :on-change="handleFileChange"
            :limit="1"
            accept="video/*"
          >
            <el-button type="primary">选择视频文件</el-button>
          </el-upload>
        </el-form-item>
        <el-form-item label="标题" prop="title">
          <el-input v-model="uploadForm.title" placeholder="请输入视频标题" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input 
            v-model="uploadForm.description" 
            type="textarea" 
            placeholder="请输入视频描述"
            :rows="3"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showUploadDialog = false">取消</el-button>
        <el-button type="primary" @click="handleUpload" :loading="uploading">
          上传
        </el-button>
      </template>
    </el-dialog>
    
    <!-- 编辑视频对话框 -->
    <el-dialog v-model="showEditDialog" title="编辑视频" width="500px">
      <el-form :model="editForm" :rules="editRules" ref="editFormRef">
        <el-form-item label="标题" prop="title">
          <el-input v-model="editForm.title" placeholder="请输入视频标题" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input 
            v-model="editForm.description" 
            type="textarea" 
            placeholder="请输入视频描述"
            :rows="3"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" @click="handleEdit" :loading="editing">
          保存
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { listVideos, uploadVideo, updateVideo, deleteVideo } from '../api/videos'
import { DataBoard, VideoPlay, MagicStick, Share } from '@element-plus/icons-vue'

const route = useRoute()
const videos = ref([])
const searchQuery = ref('')
const showUploadDialog = ref(false)
const showEditDialog = ref(false)
const uploading = ref(false)
const editing = ref(false)

const uploadForm = reactive({
  file: null,
  title: '',
  description: ''
})

const editForm = reactive({
  id: null,
  title: '',
  description: ''
})

const uploadFormRef = ref()
const editFormRef = ref()
const uploadRef = ref()

const activeMenu = computed(() => route.path)

const filteredVideos = computed(() => {
  if (!searchQuery.value) return videos.value
  return videos.value.filter(video => 
    video.title.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const uploadRules = {
  title: [{ required: true, message: '请输入视频标题', trigger: 'blur' }],
  file: [{ required: true, message: '请选择视频文件', trigger: 'change' }]
}

const editRules = {
  title: [{ required: true, message: '请输入视频标题', trigger: 'blur' }]
}

const getStatusType = (status) => {
  const types = {
    'draft': 'info',
    'published': 'success',
    'failed': 'danger'
  }
  return types[status] || 'info'
}

const getStatusText = (status) => {
  const texts = {
    'draft': '草稿',
    'published': '已发布',
    'failed': '失败'
  }
  return texts[status] || status
}

const getPublishStatusType = (status) => {
  const types = {
    'pending': 'info',
    'processing': 'warning',
    'success': 'success',
    'failed': 'danger'
  }
  return types[status] || 'info'
}

const getPublishStatusText = (status) => {
  const texts = {
    'pending': '待发布',
    'processing': '发布中',
    'success': '已发布',
    'failed': '发布失败'
  }
  return texts[status] || status
}

const handleFileChange = (file) => {
  uploadForm.file = file.raw
}

const handleUpload = async () => {
  try {
    await uploadFormRef.value.validate()
    
    if (!uploadForm.file) {
      ElMessage.error('请选择视频文件')
      return
    }
    
    uploading.value = true
    const formData = new FormData()
    formData.append('file', uploadForm.file)
    formData.append('title', uploadForm.title)
    formData.append('description', uploadForm.description)
    
    await uploadVideo(formData)
    ElMessage.success('视频上传成功')
    showUploadDialog.value = false
    loadVideos()
    
    // 重置表单
    uploadForm.file = null
    uploadForm.title = ''
    uploadForm.description = ''
    uploadRef.value.clearFiles()
  } catch (error) {
    ElMessage.error('上传失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    uploading.value = false
  }
}

const editVideo = (video) => {
  editForm.id = video.id
  editForm.title = video.title
  editForm.description = video.description
  showEditDialog.value = true
}

const handleEdit = async () => {
  try {
    await editFormRef.value.validate()
    editing.value = true
    
    await updateVideo(editForm.id, {
      title: editForm.title,
      description: editForm.description
    })
    
    ElMessage.success('视频更新成功')
    showEditDialog.value = false
    loadVideos()
  } catch (error) {
    ElMessage.error('更新失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    editing.value = false
  }
}

const handleDeleteVideo = async (videoId) => {
  try {
    await ElMessageBox.confirm('确定要删除这个视频吗？', '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await deleteVideo(videoId)
    ElMessage.success('视频删除成功')
    loadVideos()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败: ' + (error.response?.data?.detail || error.message))
    }
  }
}

const loadVideos = async () => {
  try {
    const response = await listVideos()
    videos.value = response.data
  } catch (error) {
    console.error('加载视频列表失败:', error)
  }
}

onMounted(() => {
  loadVideos()
})
</script>

<style scoped>
.video-management {
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

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style> 