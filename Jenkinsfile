pipeline {
    agent { docker { image 'python:3.6.0' } }
    stages {
        stage('prepare') {
            steps {
                echo 'Resolving the environments'
                pip3 install - r requirements.txt
            }
        }
        stage('build') {
            steps {
                sh 'python --version'
            }
        }
    }
}