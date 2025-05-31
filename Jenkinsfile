pipeline {
    agent {
        docker {
            image 'docker:20.10.24-dind'
            args '--privileged'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
            args '--storage-driver=overlay2'
            args '--group-add 0'  // Run as root
            label 'docker'  // Make sure you have a Jenkins agent with Docker installed
        }
    }

    environment {
        DOCKER_IMAGE = 'fastapi-cicd-demo'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        CONTAINER_NAME = "test-container-${env.BUILD_NUMBER}"
        TEST_RESULTS_DIR = "${WORKSPACE}/test-results"
        DOCKER_HOST = 'unix:///var/run/docker.sock'
    }

    stages {
        stage('Check Docker') {
            steps {
                sh '''
                    echo "Docker version:"
                    docker --version
                    echo "Docker info:"
                    docker info
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                }
            }
        }

        stage('Run Tests in Container') {
            steps {
                script {
                    sh "mkdir -p ${TEST_RESULTS_DIR}"
                    
                    // Start the application container
                    sh """
                    docker run -d \
                        --name ${CONTAINER_NAME} \
                        -p 8000:8000 \
                        ${DOCKER_IMAGE}:${DOCKER_TAG}
                    """
                    
                    // Wait for the application to start
                    sh """
                    for i in {1..10}; do
                        if curl -sSf http://localhost:8000/health; then
                            echo "Application is healthy!"
                            exit 0
                        fi
                        echo "Waiting for application to start... (attempt \$i/10)"
                        sleep 5
                    done
                    echo "Application failed to start"
                    exit 1
                    """
                    
                    // Run tests
                    sh """
                    docker exec ${CONTAINER_NAME} sh -c '\
                        mkdir -p /app/test-results && \
                        cd /app && \
                        python -m pytest app/tests/ -v \
                            --junitxml=/app/test-results/junit.xml \
                            --cov=app \
                            --cov-report=xml:/app/test-results/coverage.xml || \
                        (echo "Tests failed" && exit 1)'
                    """
                    
                    // Copy test results
                    sh "docker cp ${CONTAINER_NAME}:/app/test-results/ ${TEST_RESULTS_DIR}/"
                }
            }
            post {
                always {
                    junit "${TEST_RESULTS_DIR}/junit.xml"
                    publishCoverage adapters: [coberturaAdapter("${TEST_RESULTS_DIR}/coverage.xml")]
                }
            }
        }
    }

    post {
        always {
            script {
                // Cleanup containers
                sh "docker stop ${CONTAINER_NAME} || true"
                sh "docker rm -f ${CONTAINER_NAME} || true"
                cleanWs()
            }
        }
    }
}