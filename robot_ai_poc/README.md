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

## Day 2:建置與執行
> 重要:如果你的 Codespace 已經是舊的(Day 1 建立的),先 rebuild container 讓新的 devcontainer.json 生效:
> `Ctrl+Shift+P` → `Codespaces: Rebuild Container`

Terminal 1 — 編譯:
```bash
cd /workspaces/RobotAI_POC
colcon build
source install/setup.bash
```

Terminal 1 — 跑 sensor:
```bash
ros2 run sensor_node sensor_node
```

Terminal 2(新分頁,記得先 `source install/setup.bash`)— 跑 decision:
```bash
source install/setup.bash
ros2 run decision_node decision_node
```

Terminal 3(新分頁,一樣先 source)— 跑 robot:
```bash
source install/setup.bash
ros2 run robot_node robot_node
```

### 驗收
robot_node 的 terminal 應該持續印出:
```
[ROBOT] MOVE_FORWARD
```
(因為 sensor_node 預設 distance=2.5, person=true)

開第 4 個 terminal,即時把距離改近:
```bash
source install/setup.bash
ros2 param set /sensor_node distance 0.8
```
robot_node 應該變成持續印出:
```
[ROBOT] STOP
```

改回：
```bash
ros2 param set /sensor_node distance 2.5
```
確認又變回 `MOVE_FORWARD`。也可以試試把 person_detected 設 false：
```bash
ros2 param set /sensor_node person_detected false
```
應該看到 `[ROBOT] SEARCH`。

三種狀態都能切換成功,Day 2 就完成了。

## 進度
- [x] Day 1: 環境建置 (Codespaces + ROS2 Jazzy)
- [x] Day 2: Sensor → Decision → Robot 基本串接
- [ ] Day 3: AI Perception node
- [ ] Day 4: Sensor Fusion (第二個感測器)
- [ ] Day 5: Fault Handling
- [ ] Day 6: Gazebo / Virtual Robot
- [ ] Day 7: 整理 Demo (架構圖 + 3 個情境 + 設計文件)
