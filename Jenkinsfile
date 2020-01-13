pipeline {
    agent { docker { 
        image 'python:3.8.0' 
        args '--user 0:0'
        } }
    stages {
        stage("prebuild"){
            steps{
                sh """
                echo "installing dependencies"
                pip install -r requirements.txt
                """
            }
            
        }
        stage('test') {
            steps {
                sh 'pytest --cov=app ./'
            }
        }
    }
}