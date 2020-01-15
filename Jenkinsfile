pipeline {
    agent { docker { 
        image 'python:3.8.0' 
        args '--user 0:0'
        } }
    stages {
        stage("prebuild"){
            steps{
                sh """
                git clean -fdx
                echo "installing dependencies"
                pip install -r requirements.txt
                """
            }
            
        }
        stage('test') {
            steps {
                sh 'pytest --cov-report xml:cobertura-coverage.xml --cov=app ./'
            }
        }
        stage('Record Coverage') {
            when { branch 'master' }
            steps {
                script {
                    currentBuild.result = 'SUCCESS'
                 }
                step([$class: 'MasterCoverageAction', scmVars: [GIT_URL: env.GIT_URL]])
            }
        }
        stage('PR Coverage to Github') {
            when { allOf {not { branch 'master' }; expression { return env.CHANGE_ID != null }} }
            steps {
                script {
                    currentBuild.result = 'SUCCESS'
                 }
                step([$class: 'CompareCoverageAction', publishResultAs: 'statusCheck', scmVars: [GIT_URL: env.GIT_URL]])
            }
        }
    }
}