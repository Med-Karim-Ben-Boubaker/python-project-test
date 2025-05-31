pipeline {
    agent any
    
    environment {
        IMAGE_NAME = 'fastapi-app'
        CONTAINER_NAME = 'test-app'
        PYTHON_VERSION = '3.12.3'
        VENV_PATH = "${WORKSPACE}/venv"
    }
    
    stages {
        stage('Startup') {
            steps {
                script {
                    sh "python -m venv ${VENV_PATH}"
                    sh "${VENV_PATH}/bin/pip install --upgrade pip"
                    sh "${VENV_PATH}/bin/pip install -r requirements.txt"
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    sh """
                    # Create test-results directory if it doesn't exist
                    mkdir -p test-results
                    # Run pytest with both JUnit XML and coverage reports
                    ${VENV_PATH}/bin/pytest app/tests/ -v \
                        --junitxml=test-results/junit.xml \
                        --cov=app \
                        --cov-report=xml:coverage.xml
                    """
                }
            }
            post {
                always {
                    junit 'test-results/*.xml'
                }
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