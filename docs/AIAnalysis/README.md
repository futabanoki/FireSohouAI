# AI Analysis

## MediaPipe

初期解析対象:

- 左右肩
- 左右肘
- 左右手首
- 左右腰
- 左右膝
- 左右足首

初期算出項目:

- 肘角度
- 膝角度
- 腰角度
- 体幹前傾
- 歩幅
- 移動軌跡
- 動作開始時刻

## YOLO

初期認識候補:

- person
- portable_pump
- hose
- nozzle
- suction_hose
- strainer
- water_tank
- target

イベント候補:

- equipment_pickup
- coupling_start
- coupling_complete
- suction_hose_insert
- water_discharge_start
- target_fall

## 評価の原則

- 信頼度を保存する
- 誤検出を手動修正できるようにする
- 自動結果と公式評価を区別する
- 推定不能を無理に数値化しない
- カメラ条件の違いを比較時に考慮する
