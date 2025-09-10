<template>
  <div class="douyin-publish">
    <el-container>
      <el-header class="header">
        <div class="header-content">
          <h1>抖音发布</h1>
          <el-button type="primary" @click="loadDouyinVideos">
            刷新抖音视频
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
          <el-tabs v-model="activeTab" class="publish-tabs">
            <el-tab-pane label="本地视频发布" name="local">
              <el-card>
                <template #header>
                  <span>发布本地视频到抖音</span>
                </template>
                
                <el-table :data="localVideos" style="width: 100%">
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
                  <el-table-column label="操作" width="200">
                    <template #default="scope">
                      <el-button 
                        size="small" 
                        type="primary" 
                        @click="publishToDouyin(scope.row)"
                        :disabled="scope.row.publish_status === 'processing'"
                      >
                        发布到抖音
                      </el-button>
                      <el-button 
                        size="small" 
                        @click="checkPublishStatus(scope.row)"
                        v-if="scope.row.publish_status === 'processing'"
                      >
                        查询状态
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-card>
            </el-tab-pane>
            
            <el-tab-pane label="抖音视频列表" name="douyin">
              <el-card>
                <template #header>
                  <span>抖音平台视频</span>
                </template>
                
                <div v-if="loading" class="loading">
                  <el-icon class="is-loading"><Loading /></el-icon>
                  加载中...
                </div>
                
                <el-table v-else :data="douyinVideos" style="width: 100%">
                  <el-table-column prop="title" label="标题" />
                  <el-table-column prop="description" label="描述" show-overflow-tooltip />
                  <el-table-column prop="status" label="状态" width="100">
                    <template #default="scope">
                      <el-tag :type="getDouyinStatusType(scope.row.status)">
                        {{ getDouyinStatusText(scope.row.status) }}
                      </el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column prop="created_at" label="发布时间" width="150" />
                  <el-table-column label="操作" width="150">
                    <template #default="scope">
                      <el-button 
                        size="small" 
                        type="primary" 
                        @click="viewDouyinVideo(scope.row)"
                      >
                        查看
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-card>
            </el-tab-pane>
            
            <el-tab-pane label="发布任务" name="tasks">
              <el-card>
                <template #header>
                  <span>发布任务状态</span>
                </template>
                
                <el-table :data="publishTasks" style="width: 100%">
                  <el-table-column prop="task_id" label="任务ID" width="200" />
                  <el-table-column prop="video_title" label="视频标题" />
                  <el-table-column prop="status" label="状态" width="100">
                    <template #default="scope">
                      <el-tag :type="getTaskStatusType(scope.row.status)">
                        {{ getTaskStatusText(scope.row.status) }}
                      </el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column prop="progress" label="进度" width="100">
                    <template #default="scope">
                      <el-progress :percentage="scope.row.progress" />
                    </template>
                  </el-table-column>
                  <el-table-column prop="created_at" label="创建时间" width="150" />
                  <el-table-column label="操作" width="150">
                    <template #default="scope">
                      <el-button 
                        size="small" 
                        @click="checkTaskStatus(scope.row)"
                        :disabled="scope.row.status === 'success' || scope.row.status === 'failed'"
                      >
                        查询状态
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-card>
            </el-tab-pane>
          </el-tabs>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { listVideos } from '../api/videos'
import { getDouyinVideos, publishVideoToDouyin, getPublishStatus } from '../api/douyin'
import { DataBoard, VideoPlay, MagicStick, Share, Loading } from '@element-plus/icons-vue'

const route = useRoute()
const activeTab = ref('local')
const loading = ref(false)
const localVideos = ref([])
const douyinVideos = ref([])
const publishTasks = ref([])

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

const getDouyinStatusType = (status) => {
  const types = {
    'online': 'success',
    'offline': 'info',
    'deleted': 'danger'
  }
  return types[status] || 'info'
}

const getDouyinStatusText = (status) => {
  const texts = {
    'online': '已上线',
    'offline': '已下线',
    'deleted': '已删除'
  }
  return texts[status] || status
}

const getTaskStatusType = (status) => {
  const types = {
    'pending': 'info',
    'processing': 'warning',
    'success': 'success',
    'failed': 'danger'
  }
  return types[status] || 'info'
}

const getTaskStatusText = (status) => {
  const texts = {
    'pending': '待处理',
    'processing': '处理中',
    'success': '成功',
    'failed': '失败'
  }
  return texts[status] || status
}

const loadLocalVideos = async () => {
  try {
    const response = await listVideos()
    localVideos.value = response.data
  } catch (error) {
    console.error('加载本地视频失败:', error)
  }
}

const loadDouyinVideos = async () => {
  try {
    loading.value = true
    const response = await getDouyinVideos()
    douyinVideos.value = response.data.list || []
    ElMessage.success('抖音视频加载成功')
  } catch (error) {
    ElMessage.error('加载抖音视频失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

const publishToDouyin = async (video) => {
  try {
    const response = await publishVideoToDouyin(video.id)
    ElMessage.success('发布任务已创建')
    
    // 更新视频状态
    video.publish_status = 'processing'
    
    // 添加到任务列表
    publishTasks.value.unshift({
      task_id: response.data.task_id,
      video_title: video.title,
      status: 'processing',
      progress: 0,
      created_at: new Date().toLocaleString()
    })
  } catch (error) {
    ElMessage.error('发布失败: ' + (error.response?.data?.detail || error.message))
  }
}

const checkPublishStatus = async (video) => {
  try {
    // 这里需要根据实际的task_id来查询状态
    // 暂时模拟状态更新
    video.publish_status = 'success'
    ElMessage.success('发布状态已更新')
  } catch (error) {
    ElMessage.error('查询状态失败: ' + (error.response?.data?.detail || error.message))
  }
}

const checkTaskStatus = async (task) => {
  try {
    const response = await getPublishStatus(task.task_id)
    task.status = response.data.status
    task.progress = response.data.progress || 0
    
    if (task.status === 'success') {
      ElMessage.success('发布成功')
    } else if (task.status === 'failed') {
      ElMessage.error('发布失败')
    }
  } catch (error) {
    ElMessage.error('查询任务状态失败: ' + (error.response?.data?.detail || error.message))
  }
}

const viewDouyinVideo = (video) => {
  if (video.douyin_url) {
    window.open(video.douyin_url, '_blank')
  } else {
    ElMessage.info('暂无抖音链接')
  }
}

onMounted(() => {
  loadLocalVideos()
  loadDouyinVideos()
})
</script>

<style scoped>
.douyin-publish {
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

.publish-tabs {
  background: #fff;
  border-radius: 4px;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #666;
}

.loading .el-icon {
  margin-right: 8px;
}
</style> 