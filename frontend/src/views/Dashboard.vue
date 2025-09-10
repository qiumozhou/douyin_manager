<template>
  <div class="dashboard">
    <el-container>
      <el-header class="header">
        <div class="header-content">
          <h1>抖音作品管理系统</h1>
          <div class="user-info">
            <span>欢迎，{{ authStore.user?.username }}</span>
            <el-button @click="handleLogout" type="text">退出</el-button>
          </div>
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
          <el-row :gutter="20">
            <el-col :span="6">
              <el-card class="stat-card">
                <div class="stat-content">
                  <div class="stat-number">{{ stats.totalVideos }}</div>
                  <div class="stat-label">总视频数</div>
                </div>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card class="stat-card">
                <div class="stat-content">
                  <div class="stat-number">{{ stats.publishedVideos }}</div>
                  <div class="stat-label">已发布</div>
                </div>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card class="stat-card">
                <div class="stat-content">
                  <div class="stat-number">{{ stats.draftVideos }}</div>
                  <div class="stat-label">草稿</div>
                </div>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card class="stat-card">
                <div class="stat-content">
                  <div class="stat-number">{{ stats.aiGenerations }}</div>
                  <div class="stat-label">AI生成</div>
                </div>
              </el-card>
            </el-col>
          </el-row>
          
          <el-row :gutter="20" style="margin-top: 20px;">
            <el-col :span="12">
              <el-card>
                <template #header>
                  <span>最近视频</span>
                </template>
                <el-table :data="recentVideos" style="width: 100%">
                  <el-table-column prop="title" label="标题" />
                  <el-table-column prop="status" label="状态" width="100">
                    <template #default="scope">
                      <el-tag :type="getStatusType(scope.row.status)">
                        {{ getStatusText(scope.row.status) }}
                      </el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column prop="created_at" label="创建时间" width="150" />
                </el-table>
              </el-card>
            </el-col>
            
            <el-col :span="12">
              <el-card>
                <template #header>
                  <span>快速操作</span>
                </template>
                <div class="quick-actions">
                  <el-button type="primary" @click="$router.push('/videos')">
                    上传视频
                  </el-button>
                  <el-button type="success" @click="$router.push('/ai')">
                    AI生成内容
                  </el-button>
                  <el-button type="warning" @click="$router.push('/douyin')">
                    发布到抖音
                  </el-button>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '../stores/auth'
import { listVideos } from '../api/videos'
import { DataBoard, VideoPlay, MagicStick, Share } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const stats = ref({
  totalVideos: 0,
  publishedVideos: 0,
  draftVideos: 0,
  aiGenerations: 0
})

const recentVideos = ref([])

const activeMenu = computed(() => route.path)

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

const handleLogout = () => {
  authStore.logout()
  ElMessage.success('已退出登录')
  router.push('/login')
}

const loadDashboardData = async () => {
  try {
    const response = await listVideos()
    const videos = response.data
    
    stats.value.totalVideos = videos.length
    stats.value.publishedVideos = videos.filter(v => v.status === 'published').length
    stats.value.draftVideos = videos.filter(v => v.status === 'draft').length
    
    recentVideos.value = videos.slice(0, 5)
  } catch (error) {
    console.error('加载仪表板数据失败:', error)
  }
}

onMounted(() => {
  loadDashboardData()
})
</script>

<style scoped>
.dashboard {
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

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
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

.stat-card {
  text-align: center;
}

.stat-content {
  padding: 20px;
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 10px;
}

.stat-label {
  color: #666;
  font-size: 14px;
}

.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.quick-actions .el-button {
  width: 100%;
}
</style> 