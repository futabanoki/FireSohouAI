# Development Rules

## ブランチ

- `main`: 公開可能な安定版
- `develop`: 統合前の開発版
- `feature/*`: 新機能
- `fix/*`: バグ修正
- `docs/*`: 文書
- `experiment/*`: 検証用

小規模な初期段階では、`main`と短期間の作業ブランチだけでも構いません。

## Issue

すべての大きな変更はIssueと関連付けます。

ラベル例:

- `field-feedback`
- `documentation`
- `camera`
- `mediapipe`
- `yolo`
- `evaluation`
- `dashboard`
- `privacy`
- `safety`
- `good first issue`

## Pull Request

- 1つのPRで1つの目的
- 変更理由を明記
- 動作確認方法を記載
- 個人情報を含まないことを確認
- 現場レビューが必要な場合は明示

## バージョン

- `0.x`: 実験・開発段階
- `1.0`: 現場運用と文書整備が完了した初回安定版
- 破壊的変更は明示する

## 訓練記録

訓練ごとに `docs/MeetingNotes/` またはIssueへ記録します。  
映像ファイル自体は、公開可否を確認してから扱います。
