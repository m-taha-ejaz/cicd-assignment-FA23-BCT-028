pipeline {
    agent any

    environment {
        IMAGE_NAME = 'assignment3-site'
        STAGING_PORT = '8092'
        PROD_PORT = '8093'
    }

    options {
        disableConcurrentBuilds()
        timestamps()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo 'Source code checkout completed'
            }
        }

        stage('Package') {
            steps {
                sh '''
                    docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .
                    docker image inspect ${IMAGE_NAME}:${BUILD_NUMBER}
                '''
            }
        }

        stage('Start Staging') {
            steps {
                sh '''
                    docker rm -f assignment3-ci-staging || true
                    docker run -d \
                      --name assignment3-ci-staging \
                      -p 127.0.0.1:${STAGING_PORT}:80 \
                      ${IMAGE_NAME}:${BUILD_NUMBER}

                    sleep 3
                    curl -fsS http://127.0.0.1:${STAGING_PORT}/ > /dev/null
                '''
            }
        }

        stage('Test') {
            agent {
                dockerfile {
                    dir 'tests'
                    args '--network host'
                    reuseNode true
                }
            }

            environment {
                HOME = '/tmp'
                BASE_URL = 'http://127.0.0.1:8092'
            }

            steps {
                sh '''
                    pytest tests/test_site.py -v \
                      --junitxml=test-results.xml
                '''
            }

            post {
                always {
                    junit 'test-results.xml'
                    archiveArtifacts(
                        artifacts: 'screenshot.png',
                        allowEmptyArchive: true
                    )
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Selenium tests passed. Deploying application.'

                sh '''
                    docker rm -f assignment3-prod || true

                    docker run -d \
                      --name assignment3-prod \
                      --restart unless-stopped \
                      -p ${PROD_PORT}:80 \
                      ${IMAGE_NAME}:${BUILD_NUMBER}

                    sleep 2
                    curl -fsS http://127.0.0.1:${PROD_PORT}/ > /dev/null
                '''
            }
        }
    }

    post {
        always {
            sh 'docker rm -f assignment3-ci-staging || true'
        }

        success {
            echo 'CI/CD pipeline completed successfully'
        }

        failure {
            echo 'Pipeline failed. Deployment quality gate enforced.'
        }
    }
}
