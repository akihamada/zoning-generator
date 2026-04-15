# 03 — Checklists Quick Reference

AHA uses four levels of checklists (L1–L4). Below is what **you (VN operator)** need to do at each.

## L1 — Basic-to-Detail Design Transition

**Owner**: Japan PM (not you).
**Your role**: Sign the completion form at kickoff to confirm you received:

- [ ] Project code (for file naming)
- [ ] LOD matrix for this project
- [ ] List of AHA-specific elements (3DP / IRR / KIN / SEN / ART / HIS)
- [ ] Slack channel access
- [ ] Drive folder access
- [ ] Reference drawings and specifications

Full checklist: `checklists/L1-basic-to-detail.md`

## L2 — 30 / 60 / 90 % Milestones

**Owner**: Japan PM + you.
**Your role**: complete the VN-side items before each gate review.

### 30 % — Framework Lock

Before the 30 % gate, ensure:

- [ ] Drawing list first draft created
- [ ] All sheets have title blocks and sheet numbers
- [ ] File names follow `standards/file-naming.md`
- [ ] All floor plans have grid lines and exterior walls confirmed
- [ ] Main openings placed
- [ ] At least 2 main sections drafted
- [ ] All elevations have outline and opening positions
- [ ] Level / height / max-height dimensions
- [ ] Common symbol / hatch / line-type legend sheet

### 60 % — Information Density

- [ ] All dimensions on plans and sections
- [ ] Chain dimensions close (total = sum of parts)
- [ ] Door, window, finish, equipment schedules — first drafts
- [ ] Detail reference markers placed on all sheets
- [ ] Wall section (1:20 or 1:30) first draft
- [ ] Main details drafted (openings, eaves, coping, foundations)

### 90 % — Issue-Ready

- [ ] All detail references resolved (no "SIM" or undefined)
- [ ] PDF output settings confirmed
- [ ] DWG / RVT cleaned (unused layers, worksets removed)
- [ ] File naming fully compliant

Full checklist: `checklists/L2-milestone-30-60-90.md`

## L3 — Pre-Issue Final Check

**Owner**: Japan PM.
**Your role**: Complete the VN self-check **3 days before** issue.

### Your Self-Check

- [ ] Line weights match `standards/drawing-notation.md`
- [ ] All dimensions in mm, no unit symbols
- [ ] Chain dimensions close
- [ ] No missing dimensions (openings, heights, level marks)
- [ ] No duplicate dimensions
- [ ] Title blocks filled (project, client, scale, drawer/checker/approver, date, rev, status)
- [ ] North arrow orientation correct
- [ ] Detail markers all resolved (no "SIM")
- [ ] Section markers match actual section drawings
- [ ] Schedules match drawings (door/window counts)
- [ ] Revision clouds placed where changed
- [ ] PDF paper size correct
- [ ] File names comply with `standards/file-naming.md`

### AutoCAD Cleanup

- [ ] `PURGE` executed
- [ ] `AUDIT` executed, zero errors
- [ ] XREFs resolved or bound

### Revit Cleanup

- [ ] Warnings < 100 (ideally < 50)
- [ ] Worksets cleaned
- [ ] `Purge Unused` executed
- [ ] Linked files paths confirmed

Full checklist: `checklists/L3-pre-issue.md`

## L4 — AHA-Specific Items

**Owner**: Design Lead.
**Your role**: when working on a project that includes AHA special elements, follow these rules.

### 3D Print Soil Elements (3DP)

- Material mix, fiber content, layer height, print orientation — all on drawings and spec
- Do NOT treat as load-bearing without structural engineer's written confirmation
- G-code-compatible geometry precision

### Irregular Geometry (IRR)

- Rhino master file path — confirm with PM before starting
- Do NOT edit the Rhino master
- Rhino → Revit: use DirectShape, never Edit Family mesh
- Mesh topology: no openings, duplicate faces, or flipped normals

### Kinetic (KIN) / Sensor (SEN) / Art (ART)

- Coordinate with MEP for power and data
- Parameters in Revit: power, voltage, protocol, control system, artist / engineer refs

### Historic Preservation (HIS)

- Draw from the existing survey, NOT from ideal dimensions
- Preservation / renovation / removal zones marked
- Dimensional tolerance noted

Full checklist: `checklists/L4-aha-specific.md`

## Summary

| Level | When | Who leads | You do |
|---|---|---|---|
| L1 | Project kickoff | PM | Confirm setup received |
| L2 | 30 % / 60 % / 90 % | PM + you | Meet VN-side items by gate |
| L3 | 3 days before issue | PM | Complete self-check |
| L4 | Throughout (if applicable) | Design Lead | Follow rules for special elements |
