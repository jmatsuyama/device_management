# デバイス管理システム 設計書

## 1. システム概要

### 1.1 目的
- デバイス（PC）の管理と配布を効率化するシステム
- ロッカーを使用した安全な受け渡しの実現
- 組織間（JEIS/JR）での機器受け渡しの管理

### 1.2 システム構成
- フレームワーク: Flask (Python)
- データベース: SQLite (タイムゾーン対応)
- フロントエンド: HTML/JavaScript/Bootstrap
- 認証: セッションベース認証
- 設定:
  - SQLite: PARSE_DECLTYPES | PARSE_COLNAMES（日時型のタイムゾーン対応）
  - DateTime: timezone=True（UTC保存）

## 2. データベース設計

### 2.1 テーブル構造

#### Locker (ロッカー)
| カラム名 | 型 | NULL | 説明 |
|---------|-----|------|------|
| id | Integer | NO | 主キー |
| name | String(50) | NO | ロッカー名 |
| is_locked | Boolean | NO | ロック状態 |
| last_updated | DateTime | NO | 最終更新日時 |
| password | String(4) | YES | 一時パスワード |
| password_expiry | DateTime | YES | パスワード有効期限 |
| device_id | Integer (FK) | YES | 格納デバイスID |

#### Device (デバイス)
| カラム名 | 型 | NULL | 説明 |
|---------|-----|------|------|
| id | Integer | NO | 主キー |
| location | String(100) | NO | 設置場所 |
| pc_id | String(100) | NO | PC識別子 |
| status | String(50) | NO | ステータス |
| release_date | DateTime | YES | 解除期限 |
| is_replacement | Boolean | NO | 故障機交換フラグ |

#### User (ユーザー)
| カラム名 | 型 | NULL | 説明 |
|---------|-----|------|------|
| id | Integer | NO | 主キー |
| name | String(100) | NO | ユーザー名 |
| user_id | String(50) | NO | ログインID |
| password | String(100) | NO | パスワード |
| organization | String(10) | NO | 所属組織(JEIS/JR) |

### 2.2 リレーション
```
Locker --[0..1]--< Device (device_id による参照)
```

## 3. 機能設計

### 3.1 認証機能
- ログイン/ログアウト
- セッション管理
- 組織別アクセス制御（JEIS/JR）

### 3.2 デバイス管理機能
- デバイス一覧表示
- デバイス追加
- デバイス編集
- デバイス削除
- CSVエクスポート
- CSVインポート

### 3.3 ロッカー管理機能
- ロッカー一覧表示
- ロッカー状態管理
- パスワード発行
- パスワード認証
- デバイス受け渡し管理

### 3.4 ユーザー管理機能
- ユーザー一覧表示
- ユーザー追加
- ユーザー削除
- 組織別権限管理

## 4. 画面設計

### 4.1 共通レイアウト
- ナビゲーションバー
  - ホーム
  - デバイス一覧
  - ロッカー一覧
  - ユーザー管理
  - ログアウト

### 4.2 画面一覧
1. ログイン画面 (`login.html`)
2. ホーム画面 (`home.html`)
3. 受付画面 (`reception.html`)
4. パスワード入力画面 (`password_input.html`)
5. デバイス一覧画面 (`devices_new.html`)
6. デバイス追加画面 (`add.html`)
7. デバイス編集画面 (`edit.html`)
8. ロッカー一覧画面 (`lockers_new.html`)
9. ユーザー一覧画面 (`users_new.html`)
10. ユーザー追加画面 (`add_user.html`)
11. マスター管理画面 (`master_new.html`)

## 5. API設計

### 5.1 認証関連
```
POST   /login                    # ログイン
GET    /logout                   # ログアウト
```

### 5.2 デバイス管理
```
GET    /devices                  # デバイス一覧
GET    /add                      # デバイス追加フォーム
POST   /add                      # デバイス追加処理
GET    /edit/<id>               # デバイス編集フォーム
POST   /edit/<id>               # デバイス更新処理
GET    /delete/<id>             # デバイス削除
GET    /master                  # マスター管理画面
GET    /export_devices          # CSVエクスポート
POST   /import_devices_csv      # CSVインポート
```

### 5.3 ロッカー管理
```
GET    /lockers                 # ロッカー一覧
GET    /toggle_locker/<id>      # ロッカー状態切替
GET    /get_available_lockers   # 利用可能ロッカー取得
POST   /issue_password          # パスワード発行
POST   /verify_password_reception # パスワード検証
```

### 5.4 ユーザー管理
```
GET    /users                   # ユーザー一覧
GET    /add_user               # ユーザー追加フォーム
POST   /add_user               # ユーザー追加処理
GET    /delete_user/<id>       # ユーザー削除
```

## 6. セキュリティ設計

### 6.1 認証・認可
- セッションベースの認証
- 組織別アクセス制御
- ログイン必須ルート保護

### 6.2 データ保護
- パスワードのセキュア管理
- SQLインジェクション対策
- CSRF対策

### 6.3 運用セキュリティ
- 一時パスワードの有効期限管理
- ロッカーの自動施錠
- アクセスログの記録

## 7. 非機能要件

### 7.1 パフォーマンス
- データベースインデックス最適化
- キャッシュ戦略
- 応答時間の最適化

### 7.2 可用性
- エラーハンドリング
- データバックアップ
- システム監視

### 7.3 保守性
- モジュール化された設計
- コードの可読性
- エラーログ管理