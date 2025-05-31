pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'fastapi-cicd-demo'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        CONTAINER_NAME = "test-container-${env.BUILD_NUMBER}"
        TEST_RESULTS_DIR = "${WORKSPACE}/test-results"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
            }
        }

        stage('Run Tests in Container') {
            steps {
                script {
                    // Create test results directory
                    sh "mkdir -p ${TEST_RESULTS_DIR}"

                    // Run the container and execute tests
                    def testContainer = docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").run(
                        "--name ${CONTAINER_NAME} \
                         -v ${TEST_RESULTS_DIR}:/app/test-results \
                         -e PYTHONPATH=/app \
                         -d"
                    )

                    try {
                        // Wait for the container to be ready
                        timeout(time: 30, unit: 'SECONDS') {
                            waitUntil {
                                try {
                                    sh "docker exec ${CONTAINER_NAME} curl -sSf http://localhost:8000/health > /dev/null"
                                    return true
                                } catch (err) {
                                    sleep 2
                                    return false
                                }
                            }
                        }

                        // Execute tests inside the container
                        sh """
                        docker exec ${CONTAINER_NAME} bash -c '\
                            mkdir -p /app/test-results && \
                            cd /app && \
                            python -m pytest app/tests/ -v \
                                --junitxml=test-results/junit.xml \
                                --cov=app \
                                --cov-report=xml:test-results/coverage.xml || \
                            (echo "Tests failed" && exit 1)'
                        """

                    } catch (err) {
                        // Print container logs if tests fail
                        sh "docker logs ${CONTAINER_NAME}"
                        error "Tests failed: ${err.getMessage()}"
                    } finally {
                        // Always stop and remove the test container
                        sh "docker stop ${CONTAINER_NAME} || true"
                        sh "docker rm -f ${CONTAINER_NAME} || true"
                    }
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
            // Clean up any stopped containers and unused images
            sh """
            docker ps -aq --filter "name=${CONTAINER_NAME}" | xargs -r docker rm -f || true
            docker system prune -f
            """
            cleanWs()
        }
    }
}