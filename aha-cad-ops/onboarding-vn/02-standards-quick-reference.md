# 02 — Standards Quick Reference

Full standards are in `/aha-cad-ops/standards/` (Japanese). This is an English summary for quick reference.

## File Naming (ISO 19650-2)

```
<Project>-<Originator>-<Volume>-<Level>-<Type>-<Role>-<Number>[-<Status>-<Rev>]
```

Example: `ARIA-AHA-ZZ-01-DR-A-0201-S2-P03.dwg`

| Field | Meaning | Example |
|---|---|---|
| Project | Project code (≤4 chars) | `ARIA` |
| Originator | Organization | `AHA` |
| Volume | Block / zone, `ZZ` = whole | `ZZ` |
| Level | Floor, `ZZ` = whole, `00` = ground, `B1`–`Bn` = basement, `RF` = roof | `01` |
| Type | Info type | `DR` (drawing), `M3` (3D model), `SH` (schedule) |
| Role | Discipline | `A` arch, `S` struct, `M` mech, `E` elec, `P` plumb |
| Number | 4-digit sequence | `0201` |
| Status | ISO 19650 maturity | `S0`–`S4`, `A1` (authorized) |
| Rev | `P##` (design) or `C##` (construction) | `P03` |

**AHA-specific Role codes**: `3DP`, `IRR`, `KIN`, `SEN`, `ART`, `HIS`

### Number Blocks (architecture)

| Range | Use |
|---|---|
| 0000–0099 | Lists, legends, general notes |
| 0100–0199 | Site plan |
| 0200–0299 | Floor plans |
| 0300–0399 | Elevations |
| 0400–0499 | Sections |
| 0500–0599 | Wall sections |
| 0600–0699 | Details |
| 0700–0799 | Schedules (door / window / finish) |
| 0800–0899 | Furniture / fittings |
| 0900–0999 | AHA special elements |

## Layer Naming (ISO 13567)

```
<Discipline>-<Major>-<Minor>-<Status>
```

Examples:
```
A-WALL-EXTR-N    Architecture, Wall, Exterior, New
S-COLM----N      Structure, Column, (no minor), New
M-DUCT-SUPL-N    Mechanical, Duct, Supply, New
X-IRRG-FULL-N    Cross-discipline, Irregular geometry, Full height, New
```

- **Discipline** (1 char): `A` arch, `S` struct, `M` mech, `E` elec, `P` plumb, `L` landscape, `C` civil, `I` interior, `F` facade, `X` cross
- **Major** (4 chars): `WALL`, `DOOR`, `GLAZ`, `FLOR`, `CEIL`, `ROOF`, `STAR`, `RAIL`, `FURN`, `EQPM`, `FNSH`, `GRID`, `DIMS`, `TEXT`, `SYMB`, `HTCH`, `COLM`, `BEAM`, `SLAB`, `FNDN`, `DUCT`, `PIPE`, `LITE`, `POWR`, `DATA`
- **Minor** (4 chars, optional): `EXTR`, `INTR`, `FULL`, `PART`, `FRAM`, `LEAF`, `HEAD`, `SILL`, `SUPL`, `RETN`, `EXHS`
- **Status** (1 char): `N` new, `E` existing-to-remain, `D` demolish, `T` temporary, `R` relocate

**AHA extensions for Major**: `3DPR`, `IRRG`, `KINT`, `SENS`, `ARTD`, `HIST`

### Rules

- Uppercase only, hyphens only, no spaces, no Japanese characters
- Start from `AHA_LayerTemplate.dwt` (AutoCAD)
- Do NOT create new layers without approval → raise an RFI

## Drawing Notation

### Line Weights (mm, real size)

| Pen | Weight | Use |
|---|---|---|
| Extra-fine | 0.09 | hatch, background reference |
| Fine 1 | 0.13 | grids, dimension lines |
| Fine 2 | 0.18 | dimension text, symbols, standard notes |
| Medium 1 | 0.25 | hidden lines |
| Medium 2 | 0.35 | general outline (1:100 walls) |
| Thick 1 | 0.50 | section line (1:50) |
| Thick 2 | 0.70 | section line (1:100 and below) |
| Border | 1.00 | sheet border only |

See `standards/drawing-notation.md` Appendix A for scale-specific pen assignments.

### Text Heights

| Use | Height (mm) |
|---|---|
| Drawing title | 5.0–7.0 |
| Section / view title | 3.5 |
| Notes (standard) | 2.5 |
| Dimension values | 2.5 |
| Room names | 3.5 |
| Grid bubbles | 3.5 (inside Ø10 circle) |

### Dimensions

- **Unit: mm** (no unit symbol)
- **Precision: 1 mm**, do NOT round to 5
- Dimension text **above** the dimension line (Japanese convention)
- Arrows: 3 mm tick or open arrow
- Reference: grid OR finished surface — do NOT mix

### Hatching

| Material | Pattern | Notes |
|---|---|---|
| Concrete | `AR-CONC` | Dots + triangles |
| RC | `AR-CONC` + rebar lines | When showing structure |
| Steel | `ANSI31` | Diagonal lines |
| Timber (solid) | Grain pattern | Direction matters |
| Fiber insulation | `BATT` | Orientation matters |
| Foam insulation | Dedicated pattern | — |
| Soil (general) | Dots + `EARTH` | — |
| Soil (3DP) | `EARTH` + mix ID | e.g. `AHA-Mix-03` |

## Revit Family Rules

### Naming
```
AHA_<Category>_<Descriptor>_<Variant>
```
Examples: `AHA_Door_Hinged_Single`, `AHA_Specialty_3DPrint_SoilWall`

### Required Parameters (all families)

- `manufacturer`, `model`, `url`
- `description_jp`, `description_en`
- `aha_category_tag` (`STD` / `3DP` / `IRR` / `KIN` / `SEN` / `ART` / `HIS`)
- `source_project`
- `lod_level` (200 / 300 / 350 / 400)

### Rules

- Always start from `AHA_RevitTemplate.rte`
- Always use the correct category (no Generic Model escape)
- Parameter names: English, `snake_case`, no unit in name
- Shared parameters: use `AHA_SharedParameters.txt` only — do NOT add custom
- Rhino → Revit: use DirectShape via Rhino.Inside.Revit, NEVER Edit Family for meshes

## When in Doubt

Raise an **RFI** using `templates/rfi/rfi-form.md`. Improvisation creates rework; asking creates a record that helps the whole team.
