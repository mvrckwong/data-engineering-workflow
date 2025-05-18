pipeline {
    agent any
    
    triggers {
        cron('0 * * * *')
    }
    
    stages {
        stage('Update Repository') {
            steps {
                script {
                    // Get the current directory where Jenkins has checked out your repo
                    def workspaceDir = pwd()
                    echo "Current workspace: ${workspaceDir}"
                    
                    if (isUnix()) {
                        // Linux commands - using the current directory
                        sh """
                            git fetch origin
                            git checkout main
                            git pull origin main
                        """
                    } else {
                        // Windows commands - using the current directory
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