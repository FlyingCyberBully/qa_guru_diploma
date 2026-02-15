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
                withCredentials([
                    string(credentialsId: 'API_TOKEN', variable: 'API_TOKEN'),
                    string(credentialsId: 'SELENOID_LOGIN', variable: 'SELENOID_LOGIN'),
                    string(credentialsId: 'SELENOID_PASSWORD', variable: 'SELENOID_PASSWORD'),
                    string(credentialsId: 'BROWSERSTACK_USERNAME', variable: 'BSTACK_USER'),
                    string(credentialsId: 'BROWSERSTACK_ACCESS_KEY', variable: 'BSTACK_KEY'),
                    string(credentialsId: 'BROWSERSTACK_APP_URL', variable: 'BSTACK_APP'),
                    string(credentialsId: 'TG_BOT_TOKEN', variable: 'TG_TOKEN'),
                    string(credentialsId: 'TG_CHAT_ID', variable: 'TG_CHAT')
                ]) {
                    sh '''
                        cat > .env << ENVEOF
API_TOKEN=${API_TOKEN}
SELENOID_LOGIN=${SELENOID_LOGIN}
SELENOID_PASSWORD=${SELENOID_PASSWORD}
BROWSERSTACK_USERNAME=${BSTACK_USER}
BROWSERSTACK_ACCESS_KEY=${BSTACK_KEY}
BROWSERSTACK_APP_URL=${BSTACK_APP}
ENVEOF

                        cat > notifications/config.json << CFGEOF
{
  "base": {
    "project": "TMDB Diploma Project",
    "environment": "qa.guru",
    "comment": "API, UI & Mobile tests",
    "reportLink": "",
    "language": "ru",
    "allureFolder": "allure-report/",
    "enableChart": true
  },
  "telegram": {
    "token": "${TG_TOKEN}",
    "chat": "${TG_CHAT}",
    "replyTo": ""
  }
}
CFGEOF
                    '''
                }
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                    if ! command -v python3 > /dev/null 2>&1; then
                        apt-get update -qq > /dev/null 2>&1
                        apt-get install -y -qq python3 python3-pip python3-venv > /dev/null 2>&1
                    fi
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip > /dev/null 2>&1
                    pip install -r requirements.txt
                '''
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
                        . venv/bin/activate
                        REMOTE_URL=${params.REMOTE_URL} \
                        BROWSER_NAME=${params.BROWSER} \
                        BROWSER_VERSION=${params.BROWSER_VERSION} \
                        python -m pytest tests/ ${marker} \
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
                java "-DconfigFile=notifications/config.json" \
                     -jar ../allure-notifications-4.11.0.jar \
                     || true
            '''

            cleanWs()
        }
    }
}
