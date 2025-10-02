node('docker') {
    ansiColor('xterm') {
        cleanWs()
        stage('checkout') {
            git url: 'https://github.com/Cosmo-Tech/run.git',
                branch: 'main',
                credentialsId: '99baa078-02ed-46df-bc7d-2ca01fb32d1d'
        }
        stage('build image') {
            sh 'docker build -t cosmotech-run .'
        }
        stage('deploy') {
            parallel(
                'deploy on premise': {
                    withCredentials([file(credentialsId: 'VELA_SPHINX_SECRET', variable: 'ENV_FILE')]) {
                        sh 'docker run --env-file $ENV_FILE cosmotech-run'
                    }
                },
                'deploy on azure': {
                    withCredentials([file(credentialsId: 'WARP_SPHINX_SECRET', variable: 'ENV_FILE')]) {
                        sh 'docker run --env-file $ENV_FILE cosmotech-run'
                    }
                }
            )
        }
    }
}
