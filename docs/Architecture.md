# System Architecture

## 全体構成

```text
教範・理想動作
      |
      v
映像設計 / Soraプロンプト
      |
      v
理想モデル動画 ------------------+
                                 |
訓練現場                         |
      |                          |
      v                          v
Raspberry Pi / Camera ---> 映像取り込み
                                 |
                    +------------+------------+
                    |                         |
                    v                         v
              MediaPipe                    YOLO
              姿勢推定                器具・イベント検出
                    |                         |
                    +------------+------------+
                                 |
                                 v
                         時間・姿勢・動線比較
                                 |
                                 v
                         レポート / Dashboard
                                 |
                                 v
                           次回訓練へ反映
```

## コンポーネント

### sora

教材用・解析用の映像プロンプト、シーン設計、生成条件を管理します。

### raspberry_pi

撮影、時刻記録、カメラ設定、保存、同期を担当します。

### mediapipe

人体キーポイント、関節角度、体幹角度、歩幅、移動軌跡などを算出します。

### yolo

ホース、筒先、吸管、ポンプ、防火水槽、標的などの器具と、把持・結合・投入などのイベント検出を担当します。

### evaluation

理想動画と実演動画の時間・姿勢・動線を比較し、差分を出力します。

### dashboard

訓練結果、動画、グラフ、改善履歴を表示します。

## データフロー

1. 撮影条件と訓練情報を記録
2. 元動画を保存
3. 解析用コピーを作成
4. MediaPipe・YOLOを実行
5. フレーム単位の結果を保存
6. イベント時刻を抽出
7. 理想モデルと比較
8. レポートを生成
9. 訓練記録と関連Issueへ反映

## 初期データ形式

```text
session_id
recorded_at
team_id
role
camera_id
fps
resolution
video_path
event_name
event_time_sec
joint_name
angle_deg
object_class
confidence
notes
```

## 設計上の原則

- 元動画を直接変更しない
- 解析処理を再実行可能にする
- カメラ条件をメタデータとして保存する
- 手動修正と自動推定を区別する
- 評価値と公式減点を混同しない
