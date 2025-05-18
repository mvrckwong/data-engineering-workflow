pipeline {
    agent any
    
    triggers {
        // Trigger every 5 minutes
        cron('H/5 * * * *')
    }
    
    stages {
        stage('Update Repository') {
            steps {
                script {
                    // Get repository base path from environment variable
                    def repoBasePath = env.GIT_REPO_PATH ?: '/mnt/Github'
                    // Append specific repository name
                    def repoName = 'data-engineering-workflow'
                    def fullRepoPath = "${repoBasePath}/${repoName}"
                    
                    echo "Repository path: ${fullRepoPath}"
                    
                    // First set the repository as safe to fix the dubious ownership error
                    if (isUnix()) {
                        sh """
                            # Fix the dubious ownership error
                            git config --global --add safe.directory ${fullRepoPath}
                            
                            # Now proceed with the git commands
                            cd ${fullRepoPath}
                            git fetch origin
                            git checkout main
                            git pull origin main
                        """
                    } else {
                        bat """
                            git config --global --add safe.directory ${fullRepoPath}
                            cd ${fullRepoPath}
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