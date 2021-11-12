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
            image: python
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
          sh '''
          python -m venv venv
          source venv/bin/activate
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pyinstall
          pyinstaller game-of-life.py -F
          sleep 600
          '''
        }
      }
    }
  }
}
