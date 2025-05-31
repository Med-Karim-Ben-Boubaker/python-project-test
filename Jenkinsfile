pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.12.3'
        VENV_PATH = "${WORKSPACE}/venv"
    }

    stages {
        stage('Setup') {
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
                    ${VENV_PATH}/bin/pytest app/tests/ -v --cov=app --cov-report=xml:coverage.xml
                    """
                }
            }
            post {
                always {
                    junit '**/test-results/*.xml'
                    cobertura(coberturaReportFile: '**/coverage.xml')
                }
            }
        }

        stage('Build') {
            steps {
                echo 'Building the application...'
                // Add build steps here
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying to production...'
                // Add deployment steps here
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline completed.'
            cleanWs()
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}