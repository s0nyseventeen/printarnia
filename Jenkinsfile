pipeline{
        agent{ label 'builtin' }
        environment{
            AWS_ACCOUNT_ID='120691575341'
            AWS_DEFAULT_REGION='us-east-2'
            IMAGE_REPO_NAME='sheikhs'
            IMAGE_TAG='latest'
            REPO_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${IMAGE_REPO_NAME}"
        }
        stages{
                stage('Test'){
                        steps{
                                sh 'python3 -mpip install -r requirements.txt'
                                sh 'pytest tests -v'
                        }
                }
                stage('Build'){
                        steps{
                                sh "docker build -t ${IMAGE_REPO_NAME}:${IMAGE_TAG} ."
                        }
                }
                stage('Deliver'){
                        steps{
                            script{
                                sh "aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com"
                                sh "docker tag ${IMAGE_REPO_NAME}:${IMAGE_TAG} ${REPO_URI}:${IMAGE_TAG}"
                                sh "docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${IMAGE_REPO_NAME}:${IMAGE_TAG}"
                            }
                        }
                }
        }
}
