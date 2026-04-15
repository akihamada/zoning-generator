# 04 — Daily Cycle (Evening Instruction → Next-Morning Review)

The Japan–Vietnam workflow runs on a **2-hour time difference** (Japan is 2 hours ahead of Vietnam).

## Standard Cycle

| Time (JST) | Time (ICT) | Who | Activity |
|---|---|---|---|
| 17:00–18:00 | 15:00–16:00 | Japan PM | Reviews today's work, prepares task briefs for tomorrow |
| 18:00 | 16:00 | Japan PM | Posts task briefs to Slack + saves to repo |
| 18:00–19:00 | 16:00–17:00 | VN operator | Reads briefs, asks clarifying questions if urgent |
| 19:00 (EOD) | 17:00 (EOD) | Japan PM | End of day |
| (Overnight JST) | 08:00–17:00 ICT | VN operator | Works on task briefs, raises RFIs |
| 09:00 | 07:00 | Japan PM | Starts day, reviews VN work from yesterday |
| 09:00–11:00 | 07:00–09:00 | Japan PM | Responds to RFIs, gives feedback |
| 11:00 | 09:00 | VN operator | Receives PM feedback, continues or revises |

## RFI Response Time by Priority

| Priority | Response time | When to use |
|---|---|---|
| **High** | Same day (Japan side) | Work is blocked; issue delay risk |
| **Medium** | By next-morning review | Affects next task; can work around for a few hours |
| **Low** | Weekly batch response | Informational; for future work |

## Communication Channels

| Channel | Use |
|---|---|
| **Slack — `#aha-<project>-daily`** | Daily standup, quick questions, task brief notifications |
| **Slack — `#aha-<project>-rfi`** | RFI summaries (full RFI in repo) |
| **Notion — project page** | Task tracker, meeting notes |
| **Google Drive** | Large file sharing (PDFs, images, scans) |
| **Git repository** | All standards, checklists, templates, task briefs, RFIs |

## Expected Behaviors

### From VN operator
- Read task briefs **before end of your day** so you can raise urgent RFIs during the overlap window
- Complete self-check on each task brief before returning
- Raise RFIs early, not at the end of the day
- Update Notion task tracker daily
- Save all work to Drive / repo at end of day (do not sit on local-only files)

### From Japan PM
- Post task briefs by 18:00 JST (16:00 ICT) — respect VN operator's evening
- Respond to High RFIs same day
- Give specific, actionable feedback (not "looks wrong, fix it")
- Update standards / checklists when a recurring issue is found

## Overlap Time Matters

The 1-hour overlap (17:00–18:00 JST / 15:00–16:00 ICT) is the **only real-time window**. Use it for:

- Voice calls for complex design questions
- Resolving High-priority RFIs
- Reviewing screen-shared work in progress
- Quick design-intent conversations

Do NOT reserve this time for general chat — it's precious.

## Friday / End of Week

- Japan PM posts a **weekly summary** Friday 17:00 JST covering:
  - What was completed
  - Open RFIs
  - Next week's priorities
  - Any standards / checklist updates

- VN operator posts a **personal weekly report** covering:
  - Hours on each task
  - Blockers
  - Questions for discussion
  - Learning / requests for training

## Escalation

If something goes wrong:

1. **Technical issue** (software crash, file corruption) → Slack PM immediately, do not wait
2. **Unclear instructions** → Raise RFI with High priority
3. **Time-zone emergency** (missed handoff) → Email + Slack PM
4. **Agency / contract issue** → Contact through agency, copy PM
