pipeline {
  agent any

  parameters {
    choice(name: 'ACTION', choices: ['deploy', 'rollback'], description: 'deploy 发布新版本；rollback 回退到旧版本')
    string(name: 'TARGET_RELEASE', defaultValue: '', description: '回滚目标版本目录名；留空则回退 previous 或上一个版本')
    string(name: 'FRONTEND_SERVER_NAME', defaultValue: '_', description: 'Nginx server_name')
    string(name: 'FRONTEND_LISTEN_PORT', defaultValue: '80', description: 'Nginx 监听端口')
    string(name: 'BACKEND_UPSTREAM', defaultValue: 'http://127.0.0.1:25889', description: '后端 upstream')
    string(name: 'KEEP_RELEASES', defaultValue: '5', description: '保留最近几个版本')
  }

  environment {
    API_BASE_URL = ''
    ENABLE_BACKEND_PROXY = '1'
    FRONTEND_DEFAULT_SERVER = '1'
  }

  stages {
    stage('Validate') {
      when { expression { params.ACTION == 'deploy' } }
      steps {
        sh 'if command -v node >/dev/null 2>&1; then node --check app.js; fi'
      }
    }
    stage('Deploy') {
      when { expression { params.ACTION == 'deploy' } }
      steps {
        sh '''sudo env SOURCE_DIR="$WORKSPACE" RELEASE_ID="${BUILD_NUMBER}-${GIT_COMMIT}" FRONTEND_SERVER_NAME="${FRONTEND_SERVER_NAME}" FRONTEND_LISTEN_PORT="${FRONTEND_LISTEN_PORT}" BACKEND_UPSTREAM="${BACKEND_UPSTREAM}" KEEP_RELEASES="${KEEP_RELEASES}" API_BASE_URL="${API_BASE_URL}" ENABLE_BACKEND_PROXY="${ENABLE_BACKEND_PROXY}" FRONTEND_DEFAULT_SERVER="${FRONTEND_DEFAULT_SERVER}" bash deploy/jenkins-deploy.sh'''
      }
    }
    stage('Rollback') {
      when { expression { params.ACTION == 'rollback' } }
      steps {
        sh '''sudo env TARGET_RELEASE="${TARGET_RELEASE}" FRONTEND_LISTEN_PORT="${FRONTEND_LISTEN_PORT}" bash deploy/rollback.sh'''
      }
    }
  }
}
