pipeline {
    agent any // Hoặc chỉ định một Jenkins agent cụ thể nếu bạn có nhiều node

    // Định nghĩa các biến môi trường cho pipeline
    environment {
        // Chúng ta sẽ cố gắng dùng 'python3.10' trước.
        // Đảm bảo Python 3.10 có trên máy chủ Jenkins và có thể được tìm thấy trong PATH.
        // Nếu không, bạn có thể cần cung cấp đường dẫn tuyệt đối, ví dụ: '/usr/bin/python3.10'
        PYTHON_CMD = 'python3.10' // Ưu tiên sử dụng Python 3.10
        VENV_DIR = 'venv_robot_project_cicd' // Tên thư mục cho môi trường ảo
    }

    stages {
        stage('Checkout Source Code') {
            steps {
                echo 'Starting to clone the Git repository...'
                git branch: 'main', url: 'https://github.com/SamSaySong/demo.git' 
                echo 'Git repository cloned successfully!'
                sh 'ls -la' // Liệt kê tất cả nội dung thư mục để xác nhận
            }
        }

        stage('Prepare Python Virtual Environment') {
            steps {
                echo "Creating dedicated virtual environment '${VENV_DIR}' for the project using ${PYTHON_CMD}..."
                script {
                    def actualPythonCmd = ''
                    // Tìm lệnh Python 3.10 hoặc Python 3 chung nếu 3.10 không có
                    if (sh(script: "command -v python3.10", returnStatus: true) == 0) {
                        actualPythonCmd = "python3.10"
                    } else if (sh(script: "command -v python3", returnStatus: true) == 0) {
                        // Kiểm tra xem python3 có phải là 3.10+ không
                        def py3Version = sh(script: "python3 --version", returnStdout: true).trim()
                        if (py3Version.startsWith("Python 3.1") || py3Version.startsWith("Python 3.12")) {
                            actualPythonCmd = "python3"
                        } else {
                            error "Lỗi: Phiên bản Python 3 mặc định không phải 3.10 trở lên. Vui lòng cài đặt python3.10 hoặc python3.10-venv trên máy chủ Jenkins."
                        }
                    } else {
                        error "Lỗi: Không tìm thấy lệnh Python (python3.10 hoặc python3). Vui lòng kiểm tra cài đặt Python trên máy chủ Jenkins."
                    }
                    env.PYTHON_CMD = actualPythonCmd // Cập nhật PYTHON_CMD với lệnh thực tế tìm được

                    // Kiểm tra phiên bản Python thực tế sẽ dùng
                    def pythonVersionOutput = sh(script: "${env.PYTHON_CMD} --version", returnStdout: true).trim()
                    echo "Sử dụng Python: ${pythonVersionOutput}"
                    
                    // Tạo môi trường ảo
                    // BƯỚC NÀY YÊU CẦU GÓI 'python3.10-venv' HOẶC 'python3-venv' TRÊN HỆ THỐNG JENKINS
                    sh "${env.PYTHON_CMD} -m venv ${env.VENV_DIR}"

                    // Cập nhật PATH để các lệnh 'pip' và 'robot' chạy từ môi trường ảo này
                    env.VIRTUAL_ENV_BIN = "${pwd()}/${env.VENV_DIR}/bin"
                    env.PATH = "${env.VIRTUAL_ENV_BIN}:${env.PATH}"
                    echo "Virtual environment created at: ${env.VIRTUAL_ENV_BIN}"
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies from requirements.txt into the virtual environment...'
                script {
                    // Cài đặt hoặc nâng cấp pip trong môi trường ảo
                    sh "pip install --upgrade pip"

                    // Kiểm tra sự tồn tại của requirements.txt
                    if (fileExists('requirements.txt')) {
                        sh "pip install -r requirements.txt"
                        echo "Dependencies from requirements.txt installed successfully."
                    } else {
                        echo "Warning: requirements.txt not found. Skipping dependency installation."
                    }

                    // Đảm bảo Robot Framework và SeleniumLibrary được cài đặt
                    // sh "pip install robotframework robotframework-seleniumlibrary"
                    // echo "Robot Framework and SeleniumLibrary installed successfully."
                }
            }
        }

        stage('Run Robot Tests') {
            steps {
                echo 'Starting Robot Framework tests with demo.robot...'
                // Chạy Robot Framework test bằng lệnh 'robot' từ môi trường ảo
                sh "robot -d results demo.robot"
                echo 'Robot Framework tests execution finished.'
            }
        }
    }

    // Các hành động sau khi pipeline hoàn tất
    post {
        always {
            echo 'Pipeline finished.'
            // Dọn dẹp môi trường ảo để đảm bảo workspace sạch sẽ cho lần chạy tiếp theo
            script {
                if (fileExists("${env.VENV_DIR}")) {
                    echo "Cleaning up virtual environment: ${env.VENV_DIR}"
                    sh "rm -rf ${env.VENV_DIR}" // Xóa thư mục venv và tất cả nội dung của nó
                    echo "Virtual environment ${env.VENV_DIR} removed."
                }
            }
            // Cleanup các file tạm khác nếu có
            sh "find . -name '*.pyc' -delete || true" 
            sh "find . -name '__pycache__' -type d -exec rm -rf {} + || true" 
            echo "Other temporary files cleaned up."
        }
        success {
            echo 'Robot Framework tests completed successfully! 🎉'
        }
        failure {
            echo 'Robot Framework tests failed. Check logs for details. ❌'
        }
    }
}