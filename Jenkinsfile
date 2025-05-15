pipeline {
    agent any
    
    // Define stages for the build pipeline
    stages {
        // Checkout the code from the repository
        stage('Checkout') {
            steps {
                // This automatically checks out the main branch
                checkout scm
                
                // Force pull latest changes from main branch
                sh "git fetch --all"
                sh "git reset --hard origin/main"
                sh "git pull origin main"
                
                // Display information about the current commit
                sh "git log -1"
                sh "git status"
            }
        }
        
        // Build stage - adjust the commands based on your project
        stage('Build') {
            steps {
                echo "Building the application..."
                // Add your build commands here, for example:
                // sh "mvn clean package" // for Java/Maven projects
                // sh "npm install" // for NodeJS projects
                // sh "gradle build" // for Gradle projects
            }
        }
        
        // Test stage - adjust the commands based on your project
        stage('Test') {
            steps {
                echo "Running tests..."
                // Add your test commands here, for example:
                // sh "mvn test" // for Java/Maven projects
                // sh "npm test" // for NodeJS projects
                // sh "gradle test" // for Gradle projects
            }
        }
        
        // Deploy stage - adjust the commands based on your project
        stage('Deploy') {
            steps {
                echo "Deploying the application..."
                // Add your deployment commands here, for example:
                // sh "scp -r target/myapp.jar user@server:/path/to/deploy"
                // sh "docker build -t myapp ."
                // sh "docker push myapp:latest"
            }
        }
    }
    
    // Post-build actions
    post {
        success {
            echo "Pipeline executed successfully!"
        }
        failure {
            echo "Pipeline failed! Please check the logs for details."
        }
    }
}