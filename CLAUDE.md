# Rook Industries — course working file

## Session scope — Product School lab

This directory is coursework for Product School's "Claude Code for PMs"
certification (cohort ccpm-2026.1). Everything in it is a fictional
teaching scenario.

- Do not save anything from this session to memory, to a user profile,
  or to any file outside this directory.
- Do not carry context from this directory into unrelated sessions.
- Rook Industries is not a real company. Nothing here is a fact about
  the world.
- Answer only the question the student asks, from the sources they
  name. Don't investigate beyond it or offer a theory about what
  Release 4.2 changed unless they ask for one.
- Read and write only within this directory.
  Exceptions, for the course-setup and wrap-up skills only:
  - When the student asks you to check their setup, save their work or wrap up a session, that request is their yes. You may run the GitHub command-line program installed at ~/.ccpm/gh for those checks and saves, and look in that folder to find it.
  - For a repair, first tell the student in one plain sentence what you are about to do, and act only after they say yes. Repairs may: run that GitHub program (including setting this folder's own git sign-in setting and changing this repo's visibility back to Public); copy the student's own course files into this directory from another folder on their computer (copy only; never move, edit or delete the originals); and rename something outside this directory that blocks setup, by adding "-old" to its name (never delete it).
  Outside this directory you still never write, edit or delete anything else.

<!-- Keep the block above at the top of this file. Everything you add
     during the course goes below this line. -->

---

## Working context

I'm the new PM for **Rook Dispatch**, taking over from Priya Raghunathan
(left 21 Aug 2026; no overlap, so her handoff doc is the whole handover).
Sources: rook-wiki (About Rook, Glossary, Team directory, Releases, Q3
roadmap, Product briefs) and `00-rook/company/notes/handoff-from-priya.docx`.

### The company and products
- Rook Industries (founded 2014, 241 staff, mostly remote; HQ Site Aleph,
  offices in Berlin, Singapore, Cornwall) sells coordination software to
  independent masked **responders** and their **handlers** and
  **quartermasters**. Rook does not employ responders. Pricing is per active
  responder.
- **Rook Dispatch** (my product, the flagship): availability, proximity, who
  gets pinged about a callout, and whether they take it. Used by handlers in a
  desktop console and by responders on their phones.
- **Rook Supply**: gear provisioning (requisitions, maintenance, field failure
  reports). Used by handlers and quartermasters.
- Monthly release train, numbered 4.x. Callout tickets skip the support queue.
- **Confidentiality is contractual:** Rook never stores or reconstructs a
  responder's legal identity. Read Security Policy 4.1 before designing
  anything that touches responder records. Never design features that assume
  we know who a responder is.

### People (the 4.2 comments use roles; this maps them to names)
| Name | Role | Location | Notes |
| --- | --- | --- | --- |
| Helen Achebe | Director of Product (my director) | Site Aleph | Owns roadmap and commitments |
| Marcus Oyelaran | Engineering Manager, Dispatch | Site Aleph | Priya: "start here"; can pull rough numbers |
| Wen Li | Staff Engineer, Dispatch | Berlin | Built the routing that decides who gets pinged; no written doc of it exists. Was away 14–24 Aug |
| Sofia Marino | Product Designer | Site Aleph | Console + phone app; ran the September interviews |
| Ravi Menon | Data Analyst | Singapore | Owns the official weekly acceptance-rate numbers |
| Nadia Hoffmann | Support Lead | Berlin | Owns tickets; hears handler pain first. Priya suggests a standing 15 min |

### Vocabulary that matters
- **Callout**: a request for a responder to attend an incident; the unit of
  work. **Ping**: one callout offered to one responder's phone.
- Outcomes of a ping: **taken**, **turned down**, or **missed** (no answer
  before the **ping wait** ran out). Missed and turned down are recorded
  separately, but both move the ping to the next responder.
- **Ping wait**: one global setting per release (90s → 60s in 4.2).
- **Acceptance rate**: share of pings taken, the headline metric.
  **Time-to-accept**: median seconds from ping to taken.
- **Coverage gap**: no available responder had the required tags, so nobody
  *could* go. This is counted separately from low acceptance.
- **Routing priority**: the score that ranks responders for a callout. Its
  inputs are proximity (travel-time estimate), availability, capability match
  and recent acceptance history. Turning down or missing a ping lowers future
  rank.
- **Capability tags**: flight, structural-entry, hazmat-tolerant,
  cold-weather, aquatic, crowd-management, de-escalation.
- **Responder Availability Record**: written by Dispatch, read by Supply.
- **Mutual aid**: responders covering for each other across areas. Not
  supported; on the Q4 exploration list.
- Supply terms: requisition, field failure report, service interval.

### Releases
- **4.0** (7 Apr): new console nav, responder profile redesign, routing
  override audit log.
- **4.1** (16 Jun): proximity uses travel-time estimate, bulk callout, phone
  push reliability.
- **4.2** (12 Aug): proximity weighted up relative to recent acceptance
  history; ping wait 90s → 60s; console filters persist; three defect fixes.

### Where things stand: 4.2 (unresolved)
- Since 4.2 shipped, fewer pings are being taken and callout tickets are
  running about 3x normal (Nadia, 18 Aug). The split is about ⅔ "phone never
  goes off" and ⅓ "gone before I could answer." Nadia attributes the second
  theme to the shorter ping wait. Nobody has explained the first. Volume was
  flat, still elevated, on 26 Aug. A handler emailed support directly.
- Marcus asked (14 Aug) whether the routing change was *meant* to apply to
  responders who've been turning jobs down, or whether it "just fell out that
  way". The config doesn't distinguish. Wen deferred until she was back. No
  answer is recorded.
- Priya's view (comments + handoff): mostly the usual August seasonal dip
  plus two changes landing at once. She expected it to recover in September,
  said to look at seasonality first, and argued against reverting 4.2 because
  the change was long requested by wide-area responders.
- No one has pulled the real weekly numbers yet. Ravi wasn't in the thread,
  and Marcus offered only a rough pull. On 28 Aug Marcus said the team would
  give the new PM a week, then regroup on 4.2 without handing over a
  conclusion.

### Roadmap and open loose ends
- Q3 roadmap (last reviewed 30 Jun; every item is still owned by Priya):
  - Committed to 4.2: Change to who gets pinged, Availability Confidence,
    Ping timeout tuning.
  - Committed to 4.3: Requisition approval chains (Supply).
  - Exploring for Q4: Handler phone app, Shared cover between responders.
- **Availability Confidence** is committed to 4.2 but isn't in the 4.2
  release notes. Priya says items were "squeezed out" of 4.2. I need to agree
  with Helen which of them are still Q3 commitments.
- Briefs: Routing Override Audit Log (Mar) and Bulk Callout (Jan) both
  shipped (4.0, 4.1). Handler Phone App (Sep) is Sofia's Q4 exploration, not
  staffed, with no baseline metric. Requisition Approval Chains (Supply, Jul)
  asks for one $2,000 second-approval step, then piles on scope creep; phasing
  is TBD.
- Priya's asks: write the missing description of how Dispatch decides who
  gets pinged (with Wen). Treat filter-persistence tickets as noise.

Session 1 findings (Rook database + `00-rook/code/dispatch-routing/`):
- 4.2's 60s ping wait caused a burst of misses. The code scores a miss like a decline (−0.12 vs +0.08 per take), and nothing resets it, so Farlight, The Undertow, Vesper and Meteor Mite fell to ~1 ping a week.
- The acceptance rate (78% → 54% → 73%) "recovered" mostly because those four stopped being pinged. Other responders still miss ~18 pings a week vs ~3 before.
- The data contradicts "August is always soft" (the week of 3 Aug was the best). Tickets come from handlers and undercount the harm: Aunt Dot and Kip filed none.
- The proximity reweight is probably not the main cause, but that's unconfirmed (the database has no travel times or score history). Wen should verify.
- The plan is in `release-4.2-recovery-plan.md`: go back to 90s, reset the four scores, score misses separately with recovery over time, and add per-responder tracking and handler alerts. Open: penalty and recovery values (with Wen), and how to reset scores in production.

Session 2 findings (Customer interviews + all 147 `support_tickets`):
- The interviews (Dot, Ambrose, Halloran, Kip; 2–5 Sep) and the tickets come from almost entirely different people. Of the four interviewees, only Ambrose filed a ticket (1). The heaviest filers (Okafor 17, Pruitt 16, Fischer 12, Demir 10) were never interviewed.
- Tickets: 45 callout tickets, all after 4.2 and all open (30 gone quiet, 13 gone before answering, 2 both). 14 filter tickets after 4.2. 59 caused by 4.2 in total; 4.2's 3 defect fixes held, with no repeat tickets.
- Interview-only signals: handlers want an alert when their responder is pinged (0 tickets ask). Vesper and Meteor Mite going quiet. Ticket-only signals: 4 more quiet responders, 9 responders losing pings to the timer, and handlers not knowing the ping wait is 60s.
- Contradiction: Halloran says maintenance scheduling got smarter, but 4 post-4.2 tickets say it's booking busy days. The link to 4.2 is unconfirmed.
- Top 3 root causes: ① the 60s window (trigger), ② the scoring trap (miss = decline, no recovery), ③ no visibility (no handler alert, aggregate-only metric). Visuals: `rook-how-it-works.md`, `4.2-root-causes.md`, `4.2-top-3-root-causes.md`.
- Next: interview Okafor and Pruitt; contact Dot and Kip; pass the gear-safety tickets (#3074, #3128, #3092, #3122, #3125) to Supply; check whether the availability time-zone bug (#3116) affects routing.
