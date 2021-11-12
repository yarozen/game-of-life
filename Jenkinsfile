podTemplate(containers: [
    containerTemplate(
        name: 'python', 
        image: 'python:latest', 
        command: 'sleep', 
        args: '30d')
  ]) {

    node(POD_LABEL) {
        stage('Get a Python Project') {
            git url: 'https://github.com/yarozen/game-of-life.git', branch: 'main'
            container('python') {
                stage('Build a Python project') {
                    sh '''
                    sleep 600
                    '''
                }
            }
        }

    }
}
