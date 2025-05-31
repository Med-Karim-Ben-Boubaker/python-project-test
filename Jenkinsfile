pipeline {
    agent any
    
    environment {
        IMAGE_NAME = 'fastapi-app'
        CONTAINER_NAME = 'test-app'
    }
    
    stages {
        stage('Unit Tests') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    python -m pytest tests/ -v
                '''
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME} ."
            }
        }
        
        stage('Run & Test Container') {
            steps {
                // Start container
                sh "docker run -d --name ${CONTAINER_NAME} -p 8080:8000 ${IMAGE_NAME}"
                
                // Wait and test
                sh '''
                    sleep 10
                    curl -f http://localhost:8080/health || exit 1
                    echo "✅ Application is running!"
                '''
            }
        }
    }
    
    post {
        always {
            sh '''
                docker stop test-app || true
                docker rm test-app || true
            '''
        }
    }
}