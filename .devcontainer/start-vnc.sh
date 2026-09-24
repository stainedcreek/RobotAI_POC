#!/bin/bash
# 每次 Codespace 啟動時執行,建立虛擬螢幕 + 開 noVNC 服務
# 讓瀏覽器可以連進去看 Gazebo 的 3D 畫面

set -e
export DISPLAY=:1

mkdir -p ~/.vnc

# 如果已經在跑就不要重複啟動
if ! pgrep -f "Xtigervnc :1" > /dev/null; then
    # -SecurityTypes None: 這個 VNC 只透過 Codespaces 私有 port forward 存取,
    # 不會暴露在公開網路上,所以先不設密碼,求簡單能用
    tigervncserver :1 -localhost no -SecurityTypes None -geometry 1280x800 -depth 24
fi

if ! pgrep -f "fluxbox" > /dev/null; then
    fluxbox -display :1 &
fi

if ! pgrep -f "websockify" > /dev/null; then
    websockify -D --web=/usr/share/novnc/ 6080 localhost:5901
fi

echo "VNC ready. 在 Codespaces 的 PORTS 分頁把 6080 打開,網址後面加 /vnc.html"
