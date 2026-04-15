# SAMPLE-001 — Sample Project Structure

This is a **sample project directory** showing the expected layout for a new AHA case. It is not a real project — use it as a reference when setting up a new case.

## How to Use This Sample

When a real project starts:

1. Copy this directory: `cp -r projects/SAMPLE-001 projects/<REAL-CODE>`
2. Rename using the actual 4-letter project code (e.g. `ARIA`, `TGIN`, `MUSE`)
3. Fill in `CLAUDE.md` with real project info
4. Replace placeholder content in each file
5. Delete this `README.md` or replace it with a project-specific readme
6. Commit the new project folder on a feature branch

## Files in This Sample

| File | Purpose |
|---|---|
| `CLAUDE.md` | Project-specific Claude context (team, code, AHA elements, dates) |
| `01_Drawing-List.md` | Drawing list (derived from `templates/drawing-list/`) |
| `02_LOD-Matrix.md` | Element-vs-LOD matrix (derived from `templates/lod-matrix/`) |
| `03_Kickoff-Notes.md` | Kickoff meeting notes |
| `04_Instruction-Log.md` | Running log of task briefs sent to VN operator |
| `05_RFI-Log.md` | Running RFI log |

Actual task briefs go in `instructions/TB-<code>-<date>-<seq>.md`. RFIs go in `rfi/RFI-<code>-<date>-<seq>.md`.

## Expected Directory Layout (Post-Kickoff)

```
projects/<CODE>/
├── CLAUDE.md
├── 01_Drawing-List.md
├── 02_LOD-Matrix.md
├── 03_Kickoff-Notes.md
├── 04_Instruction-Log.md
├── 05_RFI-Log.md
├── instructions/
│   ├── TB-CODE-20250414-001.md
│   └── ...
├── rfi/
│   ├── RFI-CODE-20250414-001.md
│   └── ...
├── 01_Site/              ← site survey, soil report
├── 03_Geometry/          ← Rhino masters (for IRR cases)
├── 04_Drawings/          ← source files (DWG, RVT) — typically gitignored
├── 05_References/        ← reference materials
└── 06_Issue/             ← issued PDF sets
```

Large binary files (DWG, RVT, PDFs) live in Google Drive, not Git. Only text-based management files are tracked here.
