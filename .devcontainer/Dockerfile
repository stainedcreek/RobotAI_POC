FROM ros:jazzy-ros-base

ENV DEBIAN_FRONTEND=noninteractive
# Codespaces 容器沒有 GPU,強制用軟體算圖(llvmpipe),畫面會比較慢但穩定能跑
ENV LIBGL_ALWAYS_SOFTWARE=1
ENV DISPLAY=:1

# 基礎工具 + ROS2 demo + colcon
RUN apt-get update && apt-get install -y \
    curl wget lsb-release gnupg \
    python3-pip python3-colcon-common-extensions \
    ros-jazzy-demo-nodes-cpp ros-jazzy-demo-nodes-py \
    && rm -rf /var/lib/apt/lists/*

# 虛擬螢幕 + VNC + noVNC(瀏覽器看畫面用)
RUN apt-get update && apt-get install -y \
    tigervnc-standalone-server tigervnc-common \
    fluxbox \
    novnc websockify \
    mesa-utils libgl1-mesa-dri libglx-mesa0 \
    && rm -rf /var/lib/apt/lists/*

# 安裝 Gazebo Harmonic(官方 apt 來源)
# 參考: https://gazebosim.org/docs/harmonic/install_ubuntu
RUN curl https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" \
       | tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null \
    && apt-get update \
    && apt-get install -y gz-harmonic ros-jazzy-ros-gz ros-jazzy-ros-gz-sim-demos \
    && rm -rf /var/lib/apt/lists/*

COPY start-vnc.sh /usr/local/bin/start-vnc.sh
RUN chmod +x /usr/local/bin/start-vnc.sh
