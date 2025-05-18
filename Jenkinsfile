pipeline {
    agent any
    
    triggers {
        pollSCM('H/5 * * * *')
    }
    
    stages {
        stage('Update Repository') {
            steps {
                script {
                    echo "Working in current directory: ${pwd()}"
                    echo "Operating system: ${isUnix() ? 'Linux/Unix' : 'Windows'}"
                    
                    if (isUnix()) {
                        sh """
                            git fetch origin
                            git checkout main
                            git pull origin main
                        """
                    } else {
                        bat """
                            git fetch origin
                            git checkout main
                            git pull origin main
                        """
                    }
                    
                    echo "Successfully updated repository"
                }
            }
        }
    }
}