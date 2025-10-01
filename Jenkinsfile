node('docker') {
    ansiColor('xterm') {
        stage('build image') {
            sh 'docker build -t cosmotech-run .'
        }
        stage('deploy on premise') {
            withCredentials([file(credentialsId: 'VELA_SPHINX_SECRET', variable: 'ENV_FILE')]) {
                sh 'docker run --env-file $ENV_FILE cosmotech-run'
            }
        }
        stage('deploy on azure'){
            withCredentials([file(credentialsId: 'WARP_SPHINX_SECRET', variable: 'ENV_FILE')]) {
                sh 'docker run --env-file $ENV_FILE cosmotech-run'
            }
        }
    }
}
