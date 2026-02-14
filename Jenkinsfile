pipeline {
    agent any

    parameters {
        choice(name: 'TEST_SUITE', choices: ['all', 'api', 'ui', 'mobile'], description: 'Test suite to run')
        string(name: 'BROWSER', defaultValue: 'chrome', description: 'Browser for UI tests')
        string(name: 'BROWSER_VERSION', defaultValue: '131.0', description: 'Browser version')
        string(name: 'REMOTE_URL', defaultValue: 'https://selenoid.autotests.cloud/wd/hub', description: 'Selenoid hub URL')
        string(name: 'COMMENT', defaultValue: '', description: 'Comment for Allure notification')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Create .env') {
            steps {
                sh '''
                    cat > .env << 'ENVEOF'
API_TOKEN=***TMDB_API_TOKEN***
SELENOID_LOGIN=user1
SELENOID_PASSWORD=1234
BROWSERSTACK_USERNAME=***BSTACK_USERNAME***
BROWSERSTACK_ACCESS_KEY=***BSTACK_ACCESS_KEY***
BROWSERSTACK_APP_URL=***BSTACK_APP_URL***
ENVEOF
                '''
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
                            --alluredir=allure-results \
                            -v \
                            || true
                    """
                }
            }
        }
    }

    post {
        always {
            allure includeProperties: false, results: [[path: 'allure-results']]

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
