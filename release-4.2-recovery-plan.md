# Release 4.2: recovery plan

**Product:** Rook Dispatch · **Author:** PM, Dispatch · **Status:** Draft for
review with Marcus Oyelaran (Engineering Manager), Wen Li (Staff Engineer) and
Helen Achebe (Director of Product)

**Sources:** the rook-wiki pages (Releases/4.2 and its comments, Glossary,
Rook Dispatch, Rook Supply, Q3 roadmap, Team directory, Sept 2026
interviews); the Rook database (`pings`, `callouts`, `support_tickets`,
`responders`, covering 29 Jun – 7 Sep 2026); the code in
`00-rook/code/dispatch-routing/`; and Priya's handoff doc. Anything marked
*inferred* is my reading of these sources, not a recorded fact.

---

## 1. Problem

4.2 shipped on 12 Aug 2026 with two routing changes (`config.py`):

| Setting | Before 4.2 | 4.2 |
| --- | --- | --- |
| `OFFER_TIMEOUT_SECONDS` (ping wait) | 90 | 60 |
| `WEIGHT_PROXIMITY` | 0.45 | 0.60 |
| `WEIGHT_RECENT_ACCEPTANCE` | 0.40 | 0.25 |

Since then:

- **Four reliable responders have almost disappeared from Dispatch.**

  | Responder | Handler | Pings, 29 Jun–11 Aug (~6 wks) | Pings, 12 Aug–6 Sep (~4 wks) | Taken since 4.2 |
  | --- | --- | --- | --- | --- |
  | Farlight | Linda Pruitt | 75 | 11 | 2 |
  | The Undertow | Desmond Okafor | 75 | 14 | 3 |
  | Vesper | Aunt Dot | 86 | 17 | 5 |
  | Meteor Mite | Kip | 70 | 14 | 3 |

  By late August each was getting about 1 ping a week, and almost all of
  those were missed.
- **Everyone else is missing more pings.** Excluding those four, weekly
  missed pings went from about 2–6 before the release to 21 in release week
  and 18 in the week of 31 Aug.
- **Support load is up.** Tickets went from 5–8 a week to 20, 27, 32 and 25
  in the four weeks after release.
- **The headline metric hides all of this.** The acceptance rate was 75–78%
  before, fell to 54% in release week, and was back to 73% by 31 Aug. It
  recovered mainly because the four responders stopped being pinged, so
  their misses dropped out of the average (17 misses in release week → 3).

## 2. Root cause

1. **The 60s ping wait caused a burst of misses.** In release week, the four
   responders missed 4–5 pings each; in the week before, they missed 0–1. In
   her interview, Aunt Dot describes Vesper reaching the phone just after the
   ping has gone ("he loses it more than he wins it").
2. **A miss is scored as a "no."** `offer.py` and `history.py` apply the same
   `DECLINE_PENALTY` (0.12) to *missed* and *turned down*. The Glossary and
   the database treat them as separate outcomes; the code does not.
3. **Losing is faster than earning back.** −0.12 per miss or decline versus
   +0.08 per take (`config.py`).
4. **A low score means fewer chances to recover.** Pings go down the ranked
   list one at a time and stop at the first "yes" (`offer.py`). A responder
   who falls below a nearby peer is pinged only when that peer says no.
   Example: Meteor Mite and The Gale both cover Eastgate. After 4.2, Meteor
   Mite went from 70 to 14 pings, and The Gale from 82 to 69 over a shorter
   period.
5. **Nothing resets the score.** `history.py` has no recovery over time. Its
   2019 TODO ("should this ease back toward NEUTRAL_SCORE…?") was never
   decided.

*Inferred:* the change to who gets pinged (proximity weighted up) is not the
main driver. It *lowered* the acceptance weight, which should soften this
effect, and the Eastgate pair shows the effect within a single area. The
database has no travel times or score history, so I can't fully rule out a
contribution from it. Wen should confirm.

**Why it wasn't caught:**
- Acceptance rate is reported only in aggregate.
- Handlers aren't told when their responder is pinged.
- Two of the four affected handlers (Aunt Dot, Kip) filed no tickets. They
  mentioned it only in Sofia's September interviews.
- The seasonal explanation ("August is always soft") isn't supported: the
  week of 3 Aug was the best week in the data, and there is no year-ago data
  to compare against.

## 3. Solution

### Phase 1: stop the harm (config + data only, no new features)

| # | Action | Addresses | Needs |
| --- | --- | --- | --- |
| 1.1 | Set `OFFER_TIMEOUT_SECONDS` back to 90 | "Gone before I could answer" for everyone | Marcus approval (per `config.py`) |
| 1.2 | Reset recent-acceptance to `NEUTRAL_SCORE` (0.5) for Farlight, The Undertow, Vesper, Meteor Mite | The four stuck responders | Wen: how to do this safely in production |
| 1.3 | Personally contact Linda Pruitt, Desmond Okafor, Aunt Dot and Kip: what happened, what we changed | Trust; these handlers were told nothing | PM + Nadia Hoffmann |

1.1 alone is not enough: the four responders' scores are already at the
bottom and would stay there.

### Phase 2: fix the scoring (needs product decisions with Wen)

| # | Change | Open decision |
| --- | --- | --- |
| 2.1 | Score *missed* separately from *turned down* | Should a miss get a smaller penalty than a decline, or none? (TBD with Wen) |
| 2.2 | Let scores recover toward neutral over time (the 2019 TODO) | How fast? Should a responder who has truly stopped taking work stay low? (TBD) |
| 2.3 | Review the asymmetry (−0.12 / +0.08) | Keep, or make recovery as fast as loss? No rationale is recorded |
| 2.4 | Answer Marcus's 14 Aug question about whether the proximity change was meant to apply to responders who'd been turning jobs down | Document the decision either way |

### Phase 3: make it visible

| # | Change | Why |
| --- | --- | --- |
| 3.1 | Ravi reports pings per responder weekly and flags sudden drops | The aggregate rate hid this for a month |
| 3.2 | Handler console: show when a responder's ping volume has dropped, and alert the handler when their responder is pinged | Asked for directly: Aunt Dot ("something that tells me too"), Kip ("look less like a coincidence"), Mr. Ambrose (callout alert "harder to miss"). Needs Sofia's design input |
| 3.3 | Record when each ping is answered | Time-to-accept (a headline metric) can't be measured today, and neither can the right ping wait |
| 3.4 | Write the routing description Priya asked for (with Wen) | No written description exists |

### Not doing

- **Reverting all of 4.2.** It doesn't release the four stuck responders, it
  throws away a change responders asked for, and it would undo filter
  persistence.
- **Just changing a number and calling it handled.** Helen's note asks for a
  fix handlers can see. That's Phase 3.

## 4. Success measures

All targets are the pre-4.2 baseline (29 Jun – 9 Aug) from the Rook
database.

| Measure | Baseline | Now (wk of 31 Aug) | Target |
| --- | --- | --- | --- |
| Weekly acceptance rate | 75–78% | 73% | ≥ 75% |
| Weekly missed pings (all responders) | 2–6 | 21 | back within baseline range |
| Pings/week for the four affected responders | ~11–14 each | ~1 each | back to roughly baseline |
| Weekly support tickets | 5–8 | 25 | back within baseline range |
| "Gone quiet" tickets | 0 | ongoing | 0 |

## 5. Risks and checks

- **Longer ping wait.** When nobody answers, a callout waits 30s longer before
  moving on. This can't be quantified until 3.3 is done.
- **Rook Supply.** Supply reads the Responder Availability Record. These
  fixes change the acceptance score, not that record (`availability.py`), so
  the shape Supply depends on doesn't change. Separately, "Maintenance booked
  on a bad day" and "reminder came after the date" tickets appeared after
  4.2. They're worth checking with the Supply team; no link is established.
- **Other responders lose some pings** as the four come back up the list.
  Expected and fair, but watch The Gale's and Nightwell's volumes.

## 6. Also open (from the handoff)

- **Q3 roadmap:** all items still list Priya as owner, and the roadmap
  hasn't been reviewed since 30 Jun. Availability Confidence was committed
  to 4.2 but didn't ship. Confirm with Helen what's still committed.
- **Filter persistence:** about 16 tickets since 4.2 (filters reset or saved
  wrong). Mr. Ambrose reported resets too. Treat it as a reliability bug,
  not noise.

## 7. Next steps

1. Review this with Marcus and Wen, and agree Phase 1.
2. Take Phase 1 + Phase 2 decisions to Helen (committed roadmap changes go
   through Product).
3. Ship Phase 1, then contact the four handlers with Nadia.
4. Ravi starts per-responder reporting; re-check the measures in section 4
   weekly.
