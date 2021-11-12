def label = "worker-${UUID.randomUUID().toString()}"


podTemplate(label: label, containers: [
  containerTemplate(name: 'python', image: 'python:alpine', command: 'cat', ttyEnabled: true)
]) {
  node(label) {
    stage('Build') {
      container('python') {
        sh "echo 'python build'"
        sh "sleep 300"
      }
    }
  }
}
