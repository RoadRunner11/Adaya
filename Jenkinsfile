pipeline {
    agent { docker { image 'python:3.6.0' } }
    stages {
        stage("prepare environment"){
            sh """
                pip install -r requirements.txt
                """
        }
        stage('build') {
            steps {
                sh 'python --version'
            }
        }
    }
}