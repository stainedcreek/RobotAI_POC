# AI-Robot Task Integration PoC

ROS 2 + Virtual Sensor + AI Perception + Task Decision + Virtual Robot

## 專案故事
虛擬機器人收到「偵測人員並保持安全距離」的任務 → 感測 → AI → 決策 → MOVE/STOP → 異常處理。

## 環境
- ROS 2 Jazzy (ros-base)
- 透過 GitHub Codespaces 開發,不需在本機安裝任何東西

## 開發環境啟動方式
1. 打開這個 repo 的 GitHub 頁面
2. 點 `Code` → `Codespaces` → `Create codespace on main`
3. 等待 Container build 完成(第一次約 2-5 分鐘)
4. 打開 Terminal,確認環境:
   ```bash
   ros2 --version
   ```

## Day 1 驗收
Terminal 1:
```bash
ros2 run demo_nodes_cpp talker
```

Terminal 2(開新分頁):
```bash
ros2 run demo_nodes_py listener
```

應該看到:
```
Publishing: 'Hello World'
I heard: [Hello World]
```

看到這個就代表 ROS2 環境正常,可以往下做 Day 2。

## 專案結構
```
robot_ai_poc/
├── src/
│   ├── sensor_node/      # 產生虛擬感測資料 (person_detected, distance)
│   ├── ai_node/          # AI perception,輸出 object + confidence
│   ├── decision_node/    # 根據感測+AI結果決定 MOVE / STOP / HOLD
│   └── robot_node/       # 接收指令,模擬機器人動作
├── config/                # 參數設定 (YAML)
├── launch/                # ROS2 launch files
├── docs/                  # 架構圖、設計決策說明
└── tests/                 # 測試腳本
```

## 進度
- [x] Day 1: 環境建置 (Codespaces + ROS2 Jazzy)
- [ ] Day 2: Sensor → Decision → Robot 基本串接
- [ ] Day 3: AI Perception node
- [ ] Day 4: Sensor Fusion (第二個感測器)
- [ ] Day 5: Fault Handling
- [ ] Day 6: Gazebo / Virtual Robot
- [ ] Day 7: 整理 Demo (架構圖 + 3 個情境 + 設計文件)
