node('docker') {
    ansiColor('xterm') {
        stage('build') {
            sh 'docker build -t cosmotech-run .'
        }
        stage('run') {
            withCredentials([file(credentialsId: 'VELA_SPHINX_SECRET', variable: 'ENV_FILE')]) {
                sh 'cat $ENV_FILE'
                sh 'docker run --env-file $ENV_FILE cosmotech-run'
            }
        }
    }
}
