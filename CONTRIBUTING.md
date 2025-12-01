# 開発ガイドライン (Contributing Guide)

本プロジェクトでは、開発の透明性を確保し、Semantic Versioning による適切なバージョン管理を行うため、以下のルールに従って開発を進めます。

## 1. 基本方針 (Philosophy)

* **No Issue, No Code**: すべてのコード変更は Issue から始まります。
* **Semantic Versioning**: PRのタイトルと履歴に基づいて、自動的にバージョン（Major.Minor.Patch）が決定されます。
* **Squash & Merge**: `main` ブランチの履歴は「1機能/修正 = 1コミット」で綺麗に保ちます。そのため、**作業中のコミットメッセージは自由ですが、PRのタイトルは厳格に管理されます。**

---

## 2. 開発ワークフロー

### Step 1: Issue作成
タスクやバグを見つけたらIssueを作成します。用途に応じてテンプレートを選択してください。
* **Feature Request**: 新機能・タスク用（完了条件の記述必須）
* **Bug Report**: バグ報告用（再現手順の記述必須）

### Step 2: ブランチ作成
`main` ブランチから作業用ブランチを作成します。
**命名規則: `prefix/issue-number-description`**

* **prefix**: 後述のTypeに対応するもの（`feature/`, `fix/`, `docs/` など）
* **issue-number**: 対応するIssue番号
* **description**: ケバブケース（英小文字とハイフン）での簡潔な説明

**良い例:**
* ✅ `feature/123-login-page` (Issue #123 のログイン機能)
* ✅ `fix/45-auth-token-bug` (Issue #45 のバグ修正)
* ✅ `docs/update-readme` (Issueがない軽微な修正の場合、番号は省略可だが非推奨)

### Step 3: 実装 & Push
ローカルで開発を行います。最終的に Squash Merge されるため、作業中のコミットメッセージは自由です（`wip`, `fix` 等でも可）。

### Step 4: Pull Request (PR) 作成
GitHub上でPRを作成します。
* **タイトル**: **[命名規則](#3-命名規則とsemver-conventional-commits)** に完全に従ってください（CIでチェックされます）。
* **本文**: `Closes #123` や `Fixes #45` と記述し、Issueと紐付けます。変更内容やスクショ、テスト方法を記載します。
* **ラベル**: ブランチ名に基づき自動付与されます。
    * ⚠️ **破壊的変更の場合**: PR作成後、手動で `major` ラベルを付与してください。

### Step 5: レビュー & マージ
* CI (Lint PR, Tests) が通っていること。
* レビュアーの承認 (Approve) があること。
* **マージ担当**: 原則、PR作成者が行います。「Squash and Merge」を選択し、**コミットメッセージがPRタイトルと同じになっているか**最終確認してください。

### Step 6: マージ後の処理
* **Issue**: `Closes #xxx` の記述があれば自動で Close されます。
* **Branch**: GitHub設定により、マージ後に自動削除されます（または手動で削除してください）。

---

## 3. 命名規則とSemVer (Conventional Commits)

Pull Request のタイトルは、以下の **Conventional Commits** 形式である必要があります。

**フォーマット:**
```text
<type>(<scope>): <description>
```

* **type**: 変更の種類（必須・以下の表を参照）
* **scope**: 変更の影響範囲（任意）。括弧で囲む。
    * 例: `feat(api):`, `fix(ui):`, `chore(deps):`
* **description**: 変更内容の簡潔な説明（必須）。日本語可。

### Type 一覧とバージョンへの影響

| Type | 意味 | SemVerへの影響 | 対応するブランチ名 |
| :--- | :--- | :--- | :--- |
| **feat** | 新機能追加 | Minor (0.x.0) | `feature/xxx` |
| **fix** | バグ修正 | Patch (0.0.x) | `fix/xxx` |
| **perf** | パフォーマンス改善 | Patch | `fix/xxx` or `perf/xxx` |
| **revert** | 変更の取り消し | Patch | `fix/xxx` |
| **docs** | ドキュメント変更 | 影響なし | `docs/xxx` |
| **style** | コードフォーマットのみ | 影響なし | `style/xxx` |
| **refactor** | リファクタリング | 影響なし | `refactor/xxx` |
| **test** | テスト追加・修正 | 影響なし | `test/xxx` |
| **build** | ビルドシステム変更 | 影響なし | `chore/xxx` |
| **ci** | CI設定の変更 | 影響なし | `ci/xxx` |
| **chore** | その他雑多な変更 | 影響なし | `chore/xxx` |

### ⚠️ 破壊的変更 (Major Version Up)
後方互換性のない変更を含む場合は、以下の手順を行ってください。
1. Typeの後に `!` を付ける (例: `feat!: APIの認証方式を刷新`)
2. 本文フッターに `BREAKING CHANGE: 詳細` を記述する
3. **PRに手動で `major` ラベルを付与する** (Release Drafter用)

### ✅ 良いPRタイトルの例
* `feat(auth): ログインページを追加`
* `fix(api): ユーザー情報取得時のnullエラーを修正`
* `feat!: REST APIをGraphQLに移行` (破壊的変更)
* `docs: READMEのセットアップ手順を更新`
* `chore(deps): eslintを8.0.0に更新`

### ❌ 悪いPRタイトルの例
* `add login page` (Typeがない)
* `feat:ログイン機能` (コロンの後にスペースがない)
* `feat(auth) ログイン追加` (コロンがない)
* `update` (TypeもScopeもなく、内容が不明瞭)
* `feat(auth): Add login page and fix bug and refactor code` (複数の変更を1つのPRに混ぜている)

---

## 4. 自動化設定 (Setup for Maintainers)

本プロジェクトでは、以下のCI設定によりガイドラインの遵守を補助しています。

* **PRタイトルチェック**: [.github/workflows/check-pr-title.yml](.github/workflows/check-pr-title.yml)
* **自動ラベル付与**: [.github/workflows/labeler.yml](.github/workflows/labeler.yml)
* **ラベル設定定義**: [.github/labeler.yml](.github/labeler.yml)

---

## 5. リリースプロセス (Release Process)

本プロジェクトでは **[Release Drafter](https://github.com/release-drafter/release-drafter)** を使用してリリース作業を半自動化しています。

### 設定ファイル
* **Release Drafter設定**: [.github/release-drafter.yml](.github/release-drafter.yml)
* **Release Drafterワークフロー**: [.github/workflows/release-drafter.yml](.github/workflows/release-drafter.yml)

### ラベルとバージョンの対応

PRに付与されたラベルに基づいて、次回のバージョンが決定されます。

| ラベル | バージョンへの影響 | 備考 |
| :--- | :--- | :--- |
| `major` | 🚨 **Major** (x.0.0) | **手動付与**が必要です |
| `feature`, `feat` | 🚀 **Minor** (0.x.0) | `feature/*` ブランチから自動付与 |
| `fix`, `bug`, `perf` | 🐛 **Patch** (0.0.x) | `fix/*` ブランチ等から自動付与 |
| その他 (`docs`, `chore`等) | 影響なし | バージョン番号は上がりません |

### リリースの手順
1.  **ドラフトの自動生成**: PRが `main` にマージされるたびに、リリースノートの下書き（Draft）が自動更新されます。
2.  **リリースの実施**: メンテナーは任意のタイミングで GitHub の [Releases] ページを開き、Draft の内容を確認します。
3.  **Publish**: 内容に問題がなければ「Publish release」をクリックします。
    * この時点で Git Tag が作成されます。
    * 正式な Release Note として公開されます。
