def label = "worker-${UUID.randomUUID().toString()}"


podTemplate(label: label, containers: [
  containerTemplate(name: 'python', image: 'python:alpine', command: 'cat', ttyEnabled: true)
]) {
  node(label) {
    stage('Build') {
      container('python') {
        sh "python build"
        sh "sleep 300"
      }
    }
  }
}
