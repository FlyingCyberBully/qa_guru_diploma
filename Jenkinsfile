pipeline {
    agent any

    parameters {
        choice(name: 'TEST_SUITE', choices: ['all', 'api', 'ui', 'mobile'], description: 'Test suite to run')
        string(name: 'BROWSER', defaultValue: 'chrome', description: 'Browser for UI tests')
        string(name: 'BROWSER_VERSION', defaultValue: '131.0', description: 'Browser version')
        string(name: 'REMOTE_URL', defaultValue: '', description: 'Selenoid hub URL (leave empty for local)')
        string(name: 'COMMENT', defaultValue: '', description: 'Comment for Allure notification')
    }

    environment {
        ALLURE_RESULTS = 'allure-results'

        // Credentials from Jenkins secret store
        API_TOKEN            = credentials('API_TOKEN')
        SELENOID_LOGIN       = credentials('SELENOID_LOGIN')
        SELENOID_PASSWORD    = credentials('SELENOID_PASSWORD')
        BROWSERSTACK_USERNAME   = credentials('BROWSERSTACK_USERNAME')
        BROWSERSTACK_ACCESS_KEY = credentials('BROWSERSTACK_ACCESS_KEY')
        BROWSERSTACK_APP_URL    = credentials('BROWSERSTACK_APP_URL')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
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
                        REMOTE_URL=${params.REMOTE_URL} \
                        BROWSER_NAME=${params.BROWSER} \
                        BROWSER_VERSION=${params.BROWSER_VERSION} \
                        python3 -m pytest tests/ ${marker} \
                            --alluredir=${ALLURE_RESULTS} \
                            -v \
                            || true
                    """
                }
            }
        }
    }

    post {
        always {
            allure includeProperties: false, results: [[path: "${ALLURE_RESULTS}"]]

            sh '''
                test -f ../allure-notifications-4.11.0.jar || \
                    curl -sL https://github.com/qa-guru/allure-notifications/releases/download/4.6.1/allure-notifications-4.11.0.jar \
                         -o ../allure-notifications-4.11.0.jar
            '''

            sh '''
                java "-DconfigFile=notifications/config.json" \
                     -jar ../allure-notifications-4.11.0.jar \
                     || true
            '''

            cleanWs()
        }
    }
}
