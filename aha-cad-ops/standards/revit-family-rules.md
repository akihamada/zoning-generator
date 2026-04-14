# Revitファミリ作成ルール / Revit Family Rules

AHA プロジェクトで使用する Revit ファミリの作成・命名・管理規則。

## 基本方針

1. **適切なカテゴリを必ず使う**：Generic Model への逃げは原則禁止（例外は PM 承認）
2. **Shared Parameters は中央管理**：`AHA_SharedParameters.txt` のみを使用、案件内での独自追加禁止
3. **一品生産ディテールも再利用を前提**に設計：同一案件内で3回以上使う要素はファミリ化を検討

## ファミリ命名 / Family Naming

```
AHA_<Category>_<Descriptor>_<Variant>
```

例：
```
AHA_Door_Hinged_Single
AHA_Door_Pivot_Double
AHA_Window_Fixed_Rect
AHA_Furniture_Bench_Curved
AHA_Specialty_3DPrint_SoilWall
AHA_Specialty_Kinetic_Louver
AHA_Specialty_Art_LEDMatrix
```

- プレフィックス `AHA_` 固定（OOTB ファミリとの識別）
- Category：Revit カテゴリ英語名
- Descriptor：形状・機能の要約
- Variant：バリエーション識別子

## パラメータ規約 / Parameter Convention

### 命名
- 英語、`snake_case` で統一
- 単位は名前に含めない（`width_mm` ではなく `width`）
- 単位は Revit の Project Units に従う
- 略語は避ける（`wdth` ではなく `width`）

### Instance vs Type

| 種別 | 判断基準 |
|---|---|
| Instance | インスタンスごとに変わる（位置、配置オフセット等） |
| Type | 同一タイプで共通（標準寸法、材質、仕上げ） |

### 必須パラメータ

すべての AHA ファミリに以下を付与：

| パラメータ | 型 | 必須 | 備考 |
|---|---|---|---|
| `manufacturer` | Text | ○ | 既製品の場合 |
| `model` | Text | ○ | 既製品の型番 |
| `url` | Text |  | データシート等 |
| `description_jp` | Text | ○ | 日本語説明 |
| `description_en` | Text | ○ | 英語説明（越側向け） |
| `aha_category_tag` | Text | ○ | `3DP` / `IRR` / `KIN` / `SEN` / `ART` / `HIS` / `STD` |
| `source_project` | Text |  | 起源案件コード |
| `lod_level` | Integer | ○ | 200 / 300 / 350 / 400 |

## LOD（Level of Development）管理

| LOD | 幾何 | 情報 | 典型用途 |
|---|---|---|---|
| 200 | マッシング | 種別のみ | 基本設計 |
| 300 | スケマティック | 寸法確定 | 実施設計初期 |
| 350 | 接合部定義済 | 他工種インターフェース | 実施設計後半 |
| 400 | 製作対応 | 製作情報完備 | 施工図対応 |

各ファミリの `lod_level` パラメータに現行 LOD を記録。段階的に上げる。AHA特殊要素は通常より**1段階上**を目標とする。

## 異形形態の扱い / Irregular Geometry (Rhino ↔ Revit)

- **原型は Rhino で作成**し、履歴付きで管理
- Revit への取り込み手法：

  | 規模 | 手法 | 備考 |
  |---|---|---|
  | 小規模（単発部材） | SAT 経由 → In-Place Mass / Generic Model | 履歴追跡に注意 |
  | 中〜大規模 | `DirectShape` via Dynamo / Rhino.Inside.Revit | 推奨 |
  | 反復利用 | Adaptive Component 化 | コストかかるが保守性◎ |

- **Edit Family でのメッシュ編集は禁止**（性能劣化・破損の原因）
- タグ付けは **Shared Parameter を DirectShape に付与** して実施
- 原型 Rhino ファイルの保管場所：`projects/[案件コード]/03_Geometry/rhino_master/`
- ファイル名に日付・バージョンを含める（例：`ARIA_facade_v03_20250414.3dm`）

## 土系3Dプリント要素 / Soil 3D Print Elements

カテゴリ：**Structural Foundation** または **Generic Model**（構造非依存なら後者）

必須パラメータ：

| パラメータ | 型 | 例 |
|---|---|---|
| `material_mix` | Text | `AHA-Mix-03 (soil+MgO+fiber)` |
| `fiber_type` | Text | `Kenaf / PP / Bamboo` |
| `fiber_content_pct` | Number | `1.5` |
| `layer_height_mm` | Number | `8` |
| `print_orientation` | Text | `vertical / horizontal / tilted` |
| `curing_days` | Integer | `28` |
| `printer_model` | Text | — |
| `structural_role` | Text | `load-bearing / cladding / partition` |

**注意**：構造的位置づけは構造設計者の確認必須。ファミリ情報を根拠に施工判断しない。

## キネティック／センサー／アート要素

カテゴリ：**Specialty Equipment**

必須パラメータ：

| パラメータ | 型 | 備考 |
|---|---|---|
| `power_req_w` | Number | 消費電力 |
| `voltage` | Text | `AC100V / DC24V` 等 |
| `data_protocol` | Text | `DMX / Art-Net / OSC / MQTT` |
| `control_system` | Text | コントローラ型番 |
| `artist_ref` | Text | アーティスト名・連絡先 |
| `engineer_ref` | Text | 機構エンジニア連絡先 |
| `commissioning_note` | Text | 試運転・調整指示 |
| `maintenance_cycle` | Text | 保守周期 |

## ファミリ保管 / Family Storage

```
detail-library/
  families/
    ootb_replacements/    ← 既製品代替
    aha_standard/         ← AHA標準
    aha_specialty/        ← 3DP/IRR/KIN/SEN/ART/HIS
    project_specific/     ← 案件専用（再利用判定後に昇格）
```

**昇格フロー**：案件終了後、PM が再利用判定 → `aha_standard/` または `aha_specialty/` へ移動 → `detail-library/index.md` に登録。

## 禁止事項 / Prohibitions

- Generic Model への逃げ（例外は PM 承認必須）
- Shared Parameters の案件内独自追加
- Edit Family でのメッシュ編集（異形形態）
- 既製品ファミリの名称変更（出所追跡不能になる）
- 日本語パラメータ名（`description_jp` 等、日本語格納用フィールドのみ日本語可）

## 越側オペ向け注意 / Notes for VN Operators

- Always start from `AHA_RevitTemplate.rte`
- Never add custom Shared Parameters without PM approval — raise an RFI instead
- When importing Rhino geometry, use DirectShape via Rhino.Inside.Revit, **not** manual mesh edit
- Save family files as `AHA_<Category>_<Descriptor>_<Variant>.rfa`
- If a required parameter is missing in the template, stop and raise an RFI

## 関連ファイル

- `standards/file-naming.md`
- `standards/layer-naming.md`
- `checklists/L4-aha-specific.md`
