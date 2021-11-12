pipeline {
  agent {
    kubernetes {
      yaml '''
        apiVersion: v1
        kind: Pod
        metadata:
        spec:
          containers:
          - name: python
            image: python:alpine
            command:
            - cat
            tty: true
        '''
    }
  }
  stages {
    stage('Run python') {
      steps {
        container('python') {
          sh 'python --version'
        }
      }
    }
  }
}
