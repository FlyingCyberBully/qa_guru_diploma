pipeline {
    agent any

    parameters {
        choice(name: 'TEST_SUITE', choices: ['all', 'api', 'ui', 'mobile'], description: 'Test suite to run')
        string(name: 'BROWSER', defaultValue: 'chrome', description: 'Browser for UI tests')
        string(name: 'BROWSER_VERSION', defaultValue: '131.0', description: 'Browser version')
    }

    environment {
        ALLURE_RESULTS = 'allure-results'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    def marker = ''
                    if (params.TEST_SUITE != 'all') {
                        marker = "-m ${params.TEST_SUITE}"
                    }
                    sh """
                        python3 -m pytest tests/ ${marker} \
                            --alluredir=${ALLURE_RESULTS} \
                            || true
                    """
                }
            }
        }

        stage('Allure Report') {
            steps {
                allure includeProperties: false, results: [[path: "${ALLURE_RESULTS}"]]
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
