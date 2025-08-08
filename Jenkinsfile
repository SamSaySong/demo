// Script pipeline đã cài đặt chrome tại Agent Jenkins
// và sử dụng Robot Framework để chạy các bài kiểm tra tự động.

pipeline {
    agent any

    environment {
        PYTHON_CMD = 'python3.10'
        VENV_DIR = 'venv_robot_project_cicd'
    }

    stages {
        stage('Checkout Source Code') {
            steps {
                echo 'Starting to clone the Git repository...'
                git branch: 'main', url: 'https://github.com/SamSaySong/demo.git'
                echo 'Git repository cloned successfully!'
                sh 'ls -la'
            }
        }

        stage('Prepare Python Virtual Environment') {
            steps {
                echo "Creating dedicated virtual environment '${VENV_DIR}'..."
                script {
                    def actualPythonCmd = ''
                    if (sh(script: "command -v python3.10", returnStatus: true) == 0) {
                        actualPythonCmd = "python3.10"
                    } else if (sh(script: "command -v python3", returnStatus: true) == 0) {
                        def py3Version = sh(script: "python3 --version", returnStdout: true).trim()
                        if (py3Version.startsWith("Python 3.1")) {
                            actualPythonCmd = "python3"
                        } else {
                            error "Python 3 mặc định không phải 3.10+. Hãy cài python3.10 hoặc chỉnh sửa PYTHON_CMD."
                        }
                    } else {
                        error "Không tìm thấy python3.10 hoặc python3 trên Jenkins agent."
                    }
                    env.PYTHON_CMD = actualPythonCmd

                    def pythonVersionOutput = sh(script: "${env.PYTHON_CMD} --version", returnStdout: true).trim()
                    echo "Sử dụng Python: ${pythonVersionOutput}"

                    sh "rm -rf ${VENV_DIR}"
                    sh "${env.PYTHON_CMD} -m venv ${VENV_DIR}"
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies into the virtual environment...'
                sh """
                    # Kích hoạt môi trường ảo
                    . ${VENV_DIR}/bin/activate
                    
                    # Cài đặt pip mới nhất
                    pip install --upgrade pip
        
                    # Kiểm tra và cài đặt từ requirements.txt nếu tồn tại, nếu không thì cài đặt thủ công
                    if [ -f requirements.txt ]; then
                        echo "Installing dependencies from requirements.txt..."
                        pip install -r requirements.txt
                    else
                        echo "Warning: requirements.txt not found. Installing default dependencies."
                        pip install robotframework robotframework-seleniumlibrary
                    fi
        
                    # Kiểm tra xem robot đã được cài đặt thành công chưa
                    # Sử dụng '|| true' để ngăn Jenkins báo lỗi khi mã lỗi là 251
                    robot --version || true
        
                    # Hủy kích hoạt môi trường ảo
                    deactivate
                """
                echo 'Dependencies installed and verified.'
            }
        }

        stage('Ensure Stable ChromeDriver Version') {
            steps {
                script {
                    echo 'Fetching stable ChromeDriver version from Google Labs JSON...'

                    def jsonOutput = sh(
                        script: "curl -s https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json",
                        returnStdout: true
                    ).trim()

                    def downloadUrl = ''
                    def version = ''

                    new groovy.json.JsonSlurper().parseText(jsonOutput).with { parsed ->
                        version = parsed.channels.Stable.version
                        def info = parsed.channels.Stable.downloads.chromedriver.find { it.platform == 'linux64' }
                        downloadUrl = info?.url
                    }

                    if (!downloadUrl) {
                        error "Không tìm thấy ChromeDriver phù hợp cho Linux64 từ kênh Stable."
                    }

                    echo "Stable ChromeDriver version: ${version}"
                    echo "Download URL: ${downloadUrl}"

                    sh """
                        rm -rf chromedriver.zip chromedriver-linux64 bin || true
                        wget -q ${downloadUrl} -O chromedriver.zip
                        unzip -o chromedriver.zip
                        chmod +x chromedriver-linux64/chromedriver

                        mkdir -p bin
                        cp chromedriver-linux64/chromedriver bin/
                        export PATH=\$PATH:\$PWD/bin
                        chromedriver --version
                    """
                }
            }
        }

        stage('Run Robot Tests') {
                    steps {
                        echo 'Starting Robot Framework tests with demo.robot...'
                        sh """
                            # Kích hoạt môi trường ảo
                            . ${env.VENV_DIR}/bin/activate
                            
                            # Cài đặt biến môi trường DISPLAY cho trình duyệt headless
                            export DISPLAY=:99
        
                            # Chạy bài kiểm tra Robot Framework bằng đường dẫn tuyệt đối
                            ${env.WORKSPACE}/${env.VENV_DIR}/bin/robot -d results demo.robot
        
                            # Hủy kích hoạt môi trường ảo sau khi hoàn tất
                            deactivate
                        """
                        echo 'Robot Framework tests execution finished.'
                    }
                }
    }

    post {
        always {
            echo 'Pipeline finished.'
            script {
                if (fileExists("${env.VENV_DIR}")) {
                    echo "Cleaning up virtual environment: ${env.VENV_DIR}"
                    sh "rm -rf ${env.VENV_DIR}"
                }
            }
            sh "rm -rf chromedriver.zip chromedriver-linux64 bin || true"
            sh "find . -name '*.pyc' -delete || true"
            sh "find . -name '__pycache__' -type d -exec rm -rf {} + || true"
            echo "Cleanup complete."
        }
        success {
            echo 'Robot Framework tests completed successfully! 🎉'
        }
        failure {
            echo 'Robot Framework tests failed. Check logs for details. ❌'
        }
    }
}