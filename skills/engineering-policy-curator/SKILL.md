---
name: engineering-policy-curator
description: 公開されたエンジニアリングPlaybook、コードレビュー指針、ADR資料から、対象プロジェクトに必要な知見だけを抽出し、出典と適用条件を持つAGENTS.md、docs/engineering、ADRテンプレートのドラフトを作成・更新する。新規プロジェクトの開発規約を整備する場合、既存規約を公開知見で改善する場合、仮想シニアエンジニア規約を作る場合、またはVibeplusがPlan作成前にプロジェクト規約の不足を検出した場合に使用する。
---

# Engineering Policy Curator

公開知見をそのまま大量投入せず、現在のプロジェクトで実行可能な規約へ編集する。すべての規約に適用条件、強度、根拠、出典を持たせ、人間の承認前に正式規約へしない。

## 基本原則

- 現在のコード、明示された要件、既存ADR、最寄りの`AGENTS.md`を公開資料より優先する。
- 公開されていることと再配布可能であることを区別し、ライセンスと帰属表示を保持する。
- 原文の大量コピーを避け、プロジェクト用の規則として要約する。直接引用は必要最小限にする。
- 一般論を`MUST`へ昇格させない。`MUST`は安全性、法令、データ保護、既存合意など明確な根拠がある場合に限定する。
- 生成した規約を既存ファイルへ黙って上書きしない。差分を提示し、人間の承認を得る。

## 1. プロジェクトを分類する

リポジトリの言語、フレームワーク、データストア、公開API、デプロイ方式、利用者、機密性、運用段階を調査する。`scripts/generate_policy.py --project-root <path>`を実行して不足している規約ファイルのドラフトを作る。既存ファイルは上書きされない。

次の領域から、プロジェクトに必要なものだけを選ぶ。

- 設計と変更管理
- テスト戦略
- コードレビューとPR
- セキュリティとデータ保護
- CI/CDとリリース
- 可観測性と信頼性
- アクセシビリティ
- ADRと技術的負債

## 2. 固定された公開知見を取得する

`references/source-catalog.json`を読み、選択した領域に対応するsourceとpathだけを使う。`scripts/sync_sources.py`を実行し、カタログに記録されたcommitをユーザーキャッシュへ取得する。ブランチ先端を直接規約生成へ使わない。

優先用途:

- Microsoft Engineering Playbook: 開発ライフサイクル全体の骨格
- Google Engineering Practices: レビュー、変更サイズ、変更説明
- Architecture Decision Record: 意思決定の記録方法

How They SREのような外部リンク集を将来追加する場合、リンク先本文を再配布せず索引として扱う。

## 3. 規約候補を抽出する

対象sourceの選択pathを検索し、現在のプロジェクトへ適用可能な内容だけを抽出する。各候補を`references/policy-schema.md`の形式へ正規化する。

候補ごとに確認する。

1. このプロジェクトで発生し得る具体的な失敗を防ぐか。
2. エージェントまたは人間が実行・検証できるか。
3. 適用範囲と例外を説明できるか。
4. 既存規約、コード、ADRと競合しないか。
5. 出典pathと固定commitを追跡できるか。

満たさない候補は規約へ入れず、必要なら`REFERENCE`として残す。

## 4. プロジェクト規約へ編集する

次の責務で分割する。

- `AGENTS.md`: 毎回守る短い操作規則と詳細文書へのリンク
- `docs/engineering/principles.md`: 判断原則と優先順位
- `docs/engineering/planning.md`: Plan、受け入れ条件、人間承認
- `docs/engineering/testing.md`: テスト層、最低条件、検証方法
- `docs/engineering/code-review.md`: レビュー観点、重大度、PRサイズ
- `docs/engineering/security.md`: 信頼境界、秘密情報、依存関係
- `docs/engineering/reliability.md`: SLO、可観測性、障害動作
- `docs/engineering/delivery.md`: CI/CD、migration、rollback
- `docs/engineering/decisions.md`: ADRを必要とする条件
- `docs/engineering/sources.md`: 出典、commit、ライセンス、採用規約
- `docs/engineering/adr/template.md`: ADRテンプレート

`AGENTS.md`へ説明文や一般論を詰め込まない。詳細は`docs/engineering`へ置き、タスクに関係する文書だけをエージェントが読む構造にする。

## 5. 競合を解決する

競合時は`references/conflict-resolution.md`に従う。人間の最新指示を最優先とし、プロジェクト固有の根拠が一般的な公開知見より上位になる。

既存規約を変更する場合は次を提示する。

- 追加、変更、削除する規約ID
- 変更理由と防ぐ失敗
- 既存挙動への影響
- 出典と固定commit
- 移行または例外処理

## 6. 人間レビューを受ける

正式反映前に規約ドラフトと差分を提示する。ユーザーは規約ごとに承認、修正、強度変更、却下を選べるようにする。技術的または法的な問題がある要求には根拠と代替案を示す。

承認された規約だけを正式ファイルへ反映する。人間の承認者、承認日、source revisionを`docs/engineering/sources.md`へ記録する。

## 7. 更新を管理する

`scripts/check_policy_drift.py`で上流branchと固定commitの差を検出する。差があっても規約を自動変更せず、source catalog更新、影響分析、規約差分、検証を含むPRを作る。

Vibeplus実行中に得たObsidian知識は規約候補にはできるが、自動昇格させない。再現性、複数回の有効性、現在のコードによる裏付けを確認し、人間が承認した場合だけプロジェクト規約へ反映する。
