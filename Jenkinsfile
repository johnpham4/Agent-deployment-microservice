pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '5', daysToKeepStr: '5'))
        timestamps()
    }

    environment {
        DOCKER_REPOSITORY = 'minhjohn427/qa-chatbot'
        registryCredential = 'dockerhub'
        HELM_CHART_PATH = './helm'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Build & Push Docker Image') {
            steps {
                script {
                    echo "Building Docker image..."
                    def appImage = docker.build("${DOCKER_REPOSITORY}:${IMAGE_TAG}")

                    docker.withRegistry('', registryCredential) {
                        appImage.push()
                        appImage.push('latest')
                    }
                }
            }
        }

        stage('Lint Helm Chart') {
            steps {
                sh '''
                    if ! command -v helm &> /dev/null; then
                        curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
                        chmod 700 get_helm.sh
                        ./get_helm.sh
                    fi

                    helm lint ${HELM_CHART_PATH}
                    helm template qa-chatbot ${HELM_CHART_PATH} --values ${HELM_CHART_PATH}/values.yaml
                '''
            }
        }

        stage('Deploy to Development') {
            when {
                branch 'develop'
            }
            steps {
                sh '''
                    kubectl create namespace qa-chatbot-dev --dry-run=client -o yaml | kubectl apply -f -

                    helm upgrade --install qa-chatbot-dev ${HELM_CHART_PATH} \
                        --namespace qa-chatbot-dev \
                        --set app.image.repository=${DOCKER_REPOSITORY} \
                        --set app.image.tag=${IMAGE_TAG} \
                        --set ingress.hosts[0].host=qa-chatbot-dev.local \
                        --wait --timeout=300s
                '''
            }
        }

        stage('Deploy to Staging') {
            when {
                branch pattern: "release/.*", comparator: "REGEXP"
            }
            steps {
                sh '''
                    kubectl create namespace qa-chatbot-staging --dry-run=client -o yaml | kubectl apply -f -

                    helm upgrade --install qa-chatbot-staging ${HELM_CHART_PATH} \
                        --namespace qa-chatbot-staging \
                        --set app.image.repository=${DOCKER_REPOSITORY} \
                        --set app.image.tag=${IMAGE_TAG} \
                        --set ingress.hosts[0].host=qa-chatbot-staging.local \
                        --wait --timeout=300s
                '''
            }
        }

        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                input message: 'Deploy to Production?', ok: 'Deploy'

                sh '''
                    kubectl create namespace qa-chatbot-prod --dry-run=client -o yaml | kubectl apply -f -

                    helm upgrade --install qa-chatbot-prod ${HELM_CHART_PATH} \
                        --namespace qa-chatbot-prod \
                        --set app.image.repository=${DOCKER_REPOSITORY} \
                        --set app.image.tag=${IMAGE_TAG} \
                        --set ingress.hosts[0].host=qa-chatbot.local \
                        --set app.replicaCount=3 \
                        --wait --timeout=600s
                '''
            }
        }

        stage('Smoke Tests') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                    branch pattern: "release/.*", comparator: "REGEXP"
                }
            }
            steps {
                sh '''
                    echo "Running Smoke Tests..."
                    sleep 10

                    if [ "${BRANCH_NAME}" = "main" ]; then
                        NAMESPACE="qa-chatbot-prod"
                    elif [ "${BRANCH_NAME}" = "develop" ]; then
                        NAMESPACE="qa-chatbot-dev"
                    else
                        NAMESPACE="qa-chatbot-staging"
                    fi

                    kubectl get pods -n $NAMESPACE
                    kubectl wait --for=condition=ready pod -l app=qa-chatbot -n $NAMESPACE --timeout=300s
                    kubectl port-forward -n $NAMESPACE svc/qa-chatbot 8080:8001 &

                    PF_PID=$!
                    sleep 5

                    curl -f http://localhost:8080/health || exit 1
                    curl -f http://localhost:8080/metrics || exit 1

                    kill $PF_PID
                '''
            }
        }
    }

    post {
        always {
            echo "Cleaning up..."
            sh '''
                docker system prune -f || true
                rm -rf venv || true
            '''
            cleanWs()
        }

        success {
            echo 'Pipeline completed successfully!'
            sh '''
                curl -X POST -H 'Content-type: application/json' \
                --data '{"text":"QA Chatbot Build #${BUILD_NUMBER} (${BRANCH_NAME}) succeeded."}' \
                ${SLACK_WEBHOOK_URL} || true
            '''
        }

        failure {
            echo 'Pipeline failed!'
            sh '''
                curl -X POST -H 'Content-type: application/json' \
                --data '{"text":"QA Chatbot Build #${BUILD_NUMBER} (${BRANCH_NAME}) failed."}' \
                ${SLACK_WEBHOOK_URL} || true
            '''
        }
    }
}
