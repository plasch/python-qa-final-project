pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'chmod +x setup.sh'
                sh './setup.sh'
            }
        }
        stage('Test') {
            steps {
                sh './venv/bin/pytest'
            }
        }
    }

    post {

        always {

            script {
                allure([
                        includeProperties: false,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: 'allure-results']]
                ])
            }

            cleanWs()
        }
    }
}