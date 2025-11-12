FROM python:3.10.4-slim

WORKDIR /app

# === PHẦN THÊM VÀO ĐỂ GIẢI QUYẾT LỖI 127 ===
# Cài đặt các thư viện hệ thống cần thiết và Google Chrome (bản stable)
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    unzip \
    # Các thư viện phụ thuộc mà Chrome (headless) cần
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    --no-install-recommends \
    # Thêm kho lưu trữ (repository) của Google Chrome
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    # Cài đặt Google Chrome
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    # Dọn dẹp cache để giữ image nhẹ
    && rm -rf /var/lib/apt/lists/*

# Tự động tải CHÍNH XÁC phiên bản ChromeDriver phù hợp với Chrome đã cài
RUN \
    # 1. Lấy phiên bản Chrome (chỉ lấy số major, ví dụ: 127, 126)
    CHROME_MAJOR_VERSION=$(google-chrome --version | cut -d ' ' -f 3 | cut -d '.' -f 1) \
    && echo "Chrome major version: $CHROME_MAJOR_VERSION" \
    # 2. Lấy URL phiên bản ChromeDriver mới nhất cho phiên bản Chrome đó
    && DRIVER_VERSION_URL="https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_${CHROME_MAJOR_VERSION}" \
    && DRIVER_VERSION=$(wget -q -O - $DRIVER_VERSION_URL) \
    # (Dự phòng cho các phiên bản cũ hơn 115)
    || DRIVER_VERSION=$(wget -q -O - "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_MAJOR_VERSION}") \
    && echo "Using ChromeDriver version: $DRIVER_VERSION" \
    # 3. Tải và giải nén ChromeDriver
    && wget -q -O /tmp/chromedriver.zip "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${DRIVER_VERSION}/linux64/chromedriver-linux64.zip" \
    && unzip -q /tmp/chromedriver.zip -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip \
    # 4. Tạo một "lối tắt" (symlink) để Selenium có thể tìm thấy
    && ln -s /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver

# === KẾT THÚC PHẦN THÊM VÀO ===



COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
CMD ["robot", "-d", "/app/results", "demo.robot"]
# CMD ["robot", "demo.robot"]