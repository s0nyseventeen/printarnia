pipeline{
	agent { label 'builtin' }
	stages{
		stage('Test'){
			steps{
				sh 'python3 -mpip install -r requirements.txt'
				sh 'python3 -munittest tests/test_* -v'
			}
		}
		stage('Build'){
			steps{
				sh 'docker build -t sheikhs .'
			}
		}
		stage('Deliver'){
			steps{
				withEnv ([
						"AWS_ACCESS_KEY_ID=${env.AWS_ACCESS_KEY_ID}",
						"AWS_SECRET_ACCESS_KEY=${env.AWS_SECRET_ACCESS_KEY}",
						"AWS_DEFAULT_REGION=${env.AWS_DEFAULT_REGION}"
					]) {
						sh 'docker login -u AWS -p $(aws ecr get-login-password --region us-east-2) 120691575341.dkr.ecr.us-east-2.amazonaws.com'
						sh 'docker tag sheikhs 120691575341.dkr.ecr.us-east-2.amazonaws.com/sheikhs:latest'
						sh 'docker push 120691575341.dkr.ecr.us-east-2.amazonaws.com/sheikhs:latest'
					}
			}
		}
	}
}
