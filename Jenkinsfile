pipeline{
	agent{
		node{
			label 'docker-sheikhs'
		}
	}
	stages{
		stage('Test'){
			steps{
				sh 'pip install -r requirements.txt'
				sh 'python3 -munittest tests/test_* -v'
			}
		}
		stage('Build'){
			steps{
				echo 'Build'
			}
		}
		stage('Deliver'){
			steps{
				echo 'Deliver'
			}
		}
	}
}
