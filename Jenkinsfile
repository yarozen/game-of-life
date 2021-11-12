pipeline {   
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building..'
                curl -fL https://getcli.jfrog.io | bash -s v2
                sleep 300
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}
