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
                bat 'docker build -t %IMAGE_NAME%:latest -t %IMAGE_NAME%:%BUILD_NUMBER% .'
            }
        }
        stage('Push to DockerHub') {
            steps {
                bat 'docker login -u %DOCKERHUB_CREDENTIALS_USR% -p %DOCKERHUB_CREDENTIALS_PSW%'
                bat 'docker push %IMAGE_NAME%:latest'
                bat 'docker push %IMAGE_NAME%:%BUILD_NUMBER%'
            }
        }
        stage('Deploy') {
            steps {
                bat 'docker rm -f blooddonor_web || true'
                bat 'docker rm -f blooddonor_nginx || true'
                bat 'docker-compose pull'
                bat 'docker-compose up -d'
            }
        }
        stage('Health Check') {
            steps {
                bat 'ping -n 6 127.0.0.1 > nul'
                bat 'curl -f http://localhost:80/health'
            }
        }
    }
    post {
        success {
            echo '✅ CI/CD Pipeline Passed - Blood Donor App is LIVE!'
            mail to: 'smdfayaz687@gmail.com',
                 subject: "✅ Build #${BUILD_NUMBER} Passed - Blood Donor App is LIVE!",
                 body: """
                 Hello Fayaz! 🩸

                 Your Blood Donor App pipeline has PASSED successfully!

                 Build Number : ${BUILD_NUMBER}
                 App URL      : http://localhost
                 Health Check : http://localhost/health
                 DockerHub    : fayazshaik15f21a0463/blood-donor-app:${BUILD_NUMBER}

                 All stages passed:
                 ✅ Checkout
                 ✅ Install & Test
                 ✅ Build Docker Image
                 ✅ Push to DockerHub
                 ✅ Deploy
                 ✅ Health Check

                 Regards,
                 Jenkins CI/CD 🚀
                 """
        }
        failure {
            echo '❌ Pipeline Failed - Check logs!'
            mail to: 'smdfayaz687@gmail.com',
                 subject: "❌ Build #${BUILD_NUMBER} Failed - Blood Donor App!",
                 body: """
                 Hello Fayaz! 🩸

                 Your Blood Donor App pipeline has FAILED!

                 Build Number : ${BUILD_NUMBER}
                 Jenkins URL  : http://localhost:8080

                 Please check Jenkins logs immediately!

                 Regards,
                 Jenkins CI/CD 🚀
                 """
        }
    }
}
