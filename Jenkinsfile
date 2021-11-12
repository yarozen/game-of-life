def label = "worker-${UUID.randomUUID().toString()}"


podTemplate(label: label, containers: [
  containerTemplate(name: 'ubuntu', image: 'python:alpine', command: 'cat', ttyEnabled: true)
]) {
  node(label) {
    stage('Build') {
      container('ubuntu') {
        sh "echo 'ubuntu build'"
        sh "sleep 300"
      }
    }
  }
}
