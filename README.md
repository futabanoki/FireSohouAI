# FireSohouAI

**AI-based Firefighting Drill Training & Analysis System**  
消防操法の教育・訓練・解析を支援するオープンソースプロジェクトです。

## 概要

FireSohouAI は、消防操法の現場知識とAI技術を組み合わせ、訓練の振り返り、姿勢解析、器具認識、時間計測、改善支援を行うための共通基盤を目指します。

本プロジェクトは、AIによる自動採点を最終判断とするものではありません。  
AIは客観的なデータを提供し、指導者・隊員による安全で公平な訓練を補助します。

## 主な対象

初期対象は、全国消防操法大会の**小型ポンプ操法**です。

## 開発予定機能

- Sora等を利用した教範映像・解析用映像の設計
- Raspberry Piによる訓練映像の撮影
- MediaPipeによる姿勢・関節角度解析
- YOLOによる器具・動作イベント認識
- 自動ラップ計測
- 理想動作と実演動作の比較
- 訓練結果ダッシュボード
- AIによる改善支援

## 基本方針

- Safety First：安全第一
- Human in the Loop：最終判断は人が行う
- Transparency：解析方法と評価基準を明示する
- Reproducibility：再現可能な手順とデータを残す
- Open Collaboration：消防関係者と開発者が協力できる環境を作る
- Privacy by Design：映像・個人情報を慎重に扱う

## ディレクトリ構成

```text
FireSohouAI/
├── .github/             # Issueテンプレート、CI設定
├── docs/                # 設計書、訓練記録、会議記録
├── sora/                # 映像生成プロンプト
├── raspberry_pi/        # 撮影・同期・保存プログラム
├── mediapipe/           # 姿勢解析
├── yolo/                # 器具・イベント認識
├── evaluation/          # 評価・比較・レポート
├── dashboard/           # 結果表示
├── datasets/            # 学習・検証用データ
└── sample_data/         # 公開可能なサンプル
```

## 開発状況

現在は、プロジェクト基盤と小型ポンプ操法の教範映像設計を進めています。

詳しくは [ROADMAP.md](ROADMAP.md) を参照してください。

## 参加方法

消防団員、消防学校・指導者、AI開発者、Raspberry Pi開発者、Web開発者、研究者、ドキュメント作成者など、さまざまな立場から参加できます。

参加前に [CONTRIBUTING.md](CONTRIBUTING.md) と [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) を確認してください。

## 注意事項

- 訓練映像を公開する場合は、撮影対象者と所属組織の同意を得てください。
- 顔、氏名、所属、位置情報、音声などの個人情報に配慮してください。
- 公式要領・審査基準の引用や転載は、権利関係と出典を確認してください。
- 本ソフトウェアの解析結果を、公式審査や人事評価の代替として使用しないでください。
- 実際の訓練では、所属組織の安全管理・指導方針を優先してください。

## ライセンス

Apache License 2.0

詳細は [LICENSE](LICENSE) を参照してください。
