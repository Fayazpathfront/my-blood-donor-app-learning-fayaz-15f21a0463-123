pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')
        IMAGE_NAME = 'fayazshaik15f21a0463/blood-donor-app'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Install & Test') {
            steps {
                bat 'C:\\Users\\ruhir\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe -m pip install -r requirements.txt'
                bat 'C:\\Users\\ruhir\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe -m pytest tests/'
            }
        }
        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:latest .'
            }
        }
        stage('Push to DockerHub') {
            steps {
                bat 'docker login -u %DOCKERHUB_CREDENTIALS_USR% -p %DOCKERHUB_CREDENTIALS_PSW%'
                bat 'docker push %IMAGE_NAME%:latest'
            }
        }
        stage('Deploy') {
    steps {
        bat 'docker rm -f blooddonor_db || true'
        bat 'docker-compose pull'
        bat 'docker-compose up -d'
    }
}
       stage('Health Check') {
    steps {
        bat 'ping -n 6 127.0.0.1 > nul'
        bat 'curl -f http://localhost:80/health'   // ← change 5000 to 80
    }
}
    }
    post {
        success {
            echo '✅ CI/CD Pipeline Passed - Blood Donor App is LIVE!'
        }
        failure {
            echo '❌ Pipeline Failed - Check logs!'
        }
    }
}
