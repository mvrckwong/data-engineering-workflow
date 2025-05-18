pipeline {
    agent any
    
    triggers {
        // Poll the SCM every 5 minutes for changes
        pollSCM('H/5 * * * *')
    }
    
    stages {
        stage('Update Repository') {
            steps {
                script {
                    def workspaceDir = pwd()
                    echo "Current workspace: ${workspaceDir}"
                    
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