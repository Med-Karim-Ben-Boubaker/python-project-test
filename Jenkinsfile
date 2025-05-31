pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.9'
        VENV_PATH = "${env.WORKSPACE}/venv"
    }
    
    stages {
        stage('Setup') {
            steps {
                script {
                    // Create and activate virtual environment
                    sh 'python -m venv ${VENV_PATH}'
                    sh '${VENV_PATH}/bin/pip install --upgrade pip'
                    
                    // Install dependencies
                    sh '${VENV_PATH}/bin/pip install -r requirements.txt'
                }
            }
        }
        
        stage('Lint') {
            steps {
                script {
                    // Run flake8 for linting
                    sh '''
                    ${VENV_PATH}/bin/pip install flake8
                    ${VENV_PATH}/bin/flake8 app --count --select=E9,F63,F7,F82 --show-source --statistics
                    ${VENV_PATH}/bin/flake8 app --count --max-complexity=10 --max-line-length=127 --statistics
                    '''
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    // Run tests with coverage
                    sh '${VENV_PATH}/bin/pytest --cov=app --cov-report=xml'
                }
            }
            post {
                always {
                    // Publish test results
                    junit '**/test-results/*.xml'
                    // Publish coverage report
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: false,
                        keepAll: true,
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report',
                        reportTitles: 'Coverage Report'
                    ])
                }
            }
        }
        
        stage('Build') {
            steps {
                echo 'Building the application...'
                // Add build steps here if needed
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                echo 'Deploying to production...'
                // Add deployment steps here
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline completed.'
            // Clean up workspace
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
