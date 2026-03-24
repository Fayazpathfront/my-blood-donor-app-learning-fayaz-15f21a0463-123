pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')
        IMAGE_NAME = 'Fayazpathfront/blood-donor-app'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install & Test') {
            steps {
                bat 'C:\Users\ruhir\AppData\Local\Python\pythoncore-3.14-64\python.exe -m pip install -r requirements.txt'
                bat 'C:\Users\ruhir\AppData\Local\Python\pythoncore-3.14-64\python.exe -m pytest tests/'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:latest .'
            }
        }

        stage('Push to DockerHub') {
            steps {
                bat 'echo %DOCKERHUB_CREDENTIALS_PSW% | docker login -u %DOCKERHUB_CREDENTIALS_USR% --password-stdin'
                bat 'docker push %IMAGE_NAME%:latest'
            }
        }
    }

    post {
        success {
            echo '✅ CI/CD Pipeline Passed - Image pushed to DockerHub!'
        }
        failure {
            echo '❌ Pipeline Failed - Check logs!'
        }
    }
}
