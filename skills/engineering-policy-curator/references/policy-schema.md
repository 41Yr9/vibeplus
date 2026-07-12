# Policy schema

各規約を次の要素で管理する。

```yaml
id: review.small-change
level: MUST | SHOULD | CONSIDER | REFERENCE
applies_when:
  - pull-request
rule: 実行可能な一文の規則
rationale: 防ぐ失敗または得られる効果
verification: 規則を確認する方法
exceptions: 例外条件と承認方法
sources:
  - source: google-engineering-practices
    path: review/developer/small-cls.md
    commit: 40文字のcommit SHA
project_evidence:
  - ADR、コード、障害記録、Obsidianノート
approved_by: human identifier
approved_at: YYYY-MM-DD
```

規約IDは`<domain>.<short-name>`とする。規約本文では`MUST`などの意味を変えない。

- `MUST`: 違反すると安全性、正確性、合意済み契約を損なう。
- `SHOULD`: 原則として守り、例外には根拠を要求する。
- `CONSIDER`: Planまたはレビューで検討結果を残す。
- `REFERENCE`: 判断材料であり、遵守を要求しない。
