# ディテールライブラリ Index

AHA 案件横断で再利用可能なディテール集の総目録。各ディテールは `items/<category>/<detail-id>/` 配下に格納し、本 index で検索可能にする。

**現在の登録数**：0 / 目標 100

## 部位カテゴリ / Categories

| カテゴリ | ディレクトリ | 説明 |
|---|---|---|
| 外壁標準 | `items/exterior-wall/` | 外壁一般部の納まり |
| 開口部 | `items/openings/` | 窓・ドア・建具廻り |
| 屋根・軒先 | `items/roof/` | 屋根、軒先、笠木、パラペット |
| 基礎 | `items/foundation/` | 基礎立上り、土間、アンカー |
| 防水 | `items/waterproofing/` | 陸屋根、バルコニー、外構防水 |
| 内部造作 | `items/interior/` | 幅木、廻縁、造作家具廻り |
| 階段・手摺 | `items/stair/` | 階段、手摺、ガラス手摺 |
| ガラス・サッシ | `items/glazing/` | カーテンウォール、サッシ廻り |
| AHA特殊要素 | `items/aha-specialty/` | 3DP／IRR／KIN／SEN／ART／HIS |

## 登録フォーマット / Entry Format

各ディテールは以下のファイルをセットで格納：

```
items/<category>/<detail-id>/
├── meta.json          # メタデータ（下記スキーマ）
├── detail.dwg         # AutoCAD 原図
├── detail.rvt         # Revit（該当時）
├── detail.pdf         # PDF プレビュー
├── notes.md           # 設計意図・注意点・使用条件
└── references/        # 参考資料
```

### meta.json スキーマ

```json
{
  "id": "EXT-WALL-001",
  "title_jp": "木造外壁標準部（外断熱・杉板張り）",
  "title_en": "Timber Exterior Wall w/ External Insulation",
  "category": "exterior-wall",
  "source_project": "ARIA-2023",
  "created": "2025-04-14",
  "last_updated": "2025-04-14",
  "reuse_count": 0,
  "structural_system": "timber",
  "lod_level": 400,
  "applicable_regions": ["JP"],
  "aha_tags": [],
  "dependencies": ["GLAZ-001"],
  "status": "draft"
}
```

## ID 命名規則 / ID Convention

```
<CAT>-<SUB>-<NNN>
```

例：
- `EXT-WALL-001` 外壁標準部
- `OPN-WIN-012` 窓廻り
- `ROF-EAV-003` 軒先
- `3DP-JNT-001` 3Dプリント部材接合
- `IRR-PNL-002` 異形パネル
- `HIS-WAL-001` 歴史建築壁保存

## 検索用タグ / Search Tags

| カテゴリ | タグ例 |
|---|---|
| 構造 | `timber`, `rc`, `steel`, `mixed` |
| 断熱方式 | `ext-insulation`, `int-insulation`, `cavity` |
| 仕上 | `cedar-board`, `plaster`, `concrete-exposed`, `metal-panel` |
| 性能 | `passive-house`, `zeh`, `high-humidity` |
| AHA特性 | `hyper-naturalism`, `computing-wildness`, `3dp`, `irr`, `kin`, `sen`, `art`, `his` |

## 運用ルール / Operation Rules

1. 案件終了後、PM がディテール再利用判定を実施
2. 再利用候補は本 index に追加（`meta.json` 作成）
3. 他案件での使用時に `reuse_count` を更新
4. 年1回、登録全件のレビューを実施（陳腐化・規約変更対応）

## 登録済みディテール / Registered Details

| ID | タイトル | カテゴリ | 起源案件 | LOD | 再利用数 |
|---|---|---|---|---|---|
| — | （未登録） | — | — | — | — |

## 関連ファイル

- `standards/revit-family-rules.md`
- `checklists/L4-aha-specific.md`
