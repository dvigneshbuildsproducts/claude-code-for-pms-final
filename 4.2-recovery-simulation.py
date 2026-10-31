"""Simulation: how a quiet responder gets back to normal.

Replays the rules in 00-rook/code/dispatch-routing/ (ranking weights, one
phone at a time, +0.08 per take, -0.12 per no or miss, score kept in 0..1)
for one area: the quiet responder plus five competitors.

Behaviour comes from the pings table (rook-database):
  - Responders getting regular pings missed 2% at 90s and 12% at 60s,
    and turned down ~20%.
  - Responders who had gone quiet missed 55-64% and turned down ~24%
    at 60s (the four sidelined responders, 12 Aug - 6 Sep).
  - "Quiet" here = fewer than 5 pings the week before.
  - ASSUMPTION (no data): at 90s a quiet responder misses 25%.

Run:  python3 4.2-recovery-simulation.py
"""

import random
import statistics

WEEKS = 26
RUNS = 2000
CALLOUTS_PER_WEEK = 60      # tuned so a normal responder gets ~13 pings/week
COMPETITORS = 5
NORMAL_PINGS = 10           # "back to normal" = 10+ pings a week (before 4.2: 13-15)
QUIET_BELOW = 5             # fewer pings than this last week = "quiet"

# (miss chance, turn-down chance) by ping wait and whether they're quiet.
BEHAVIOUR = {
    (90, False): (0.02, 0.20),
    (60, False): (0.12, 0.20),
    (90, True): (0.25, 0.24),   # assumption
    (60, True): (0.60, 0.24),   # from the pings table
}

SCENARIOS = {
    "A. Today (60s, no fixes)":
        dict(wait=60, start=0.0, miss_pen=0.12, recover=0.0),
    "B. Ping wait back to 90s only":
        dict(wait=90, start=0.0, miss_pen=0.12, recover=0.0),
    "C. 90s + score reset to 0.5":
        dict(wait=90, start=0.5, miss_pen=0.12, recover=0.0),
    "D. 90s + small miss penalty + recovery over time (no reset)":
        dict(wait=90, start=0.0, miss_pen=0.02, recover=0.10),
    "E. C + D together":
        dict(wait=90, start=0.5, miss_pen=0.02, recover=0.10),
    "F. 90s + reset to pre-4.2 level (0.9)":
        dict(wait=90, start=0.9, miss_pen=0.12, recover=0.0),
    "G. E + fair share (quiet responder asked first on 1 in 5 callouts)":
        dict(wait=90, start=0.5, miss_pen=0.02, recover=0.10, fair_share=5),
    "H. G + handler alert/countdown (quiet responder misses like everyone else)":
        dict(wait=90, start=0.5, miss_pen=0.02, recover=0.10, fair_share=5,
             alert=True),
    "I. F + G + H (full fix, reset to 0.9)":
        dict(wait=90, start=0.9, miss_pen=0.02, recover=0.10, fair_share=5,
             alert=True),
}

W_PROX, W_ACC, W_CAP = 0.60, 0.25, 0.15
CREDIT, DECLINE_PEN = 0.08, 0.12


def clamp(x):
    return max(0.0, min(1.0, x))


def run_once(wait, start, miss_pen, recover, rng, fair_share=0, alert=False):
    n = COMPETITORS + 1
    scores = [start] + [0.9] * COMPETITORS          # index 0 = quiet responder
    last_week = [0] + [13] * COMPETITORS            # quiet responder starts quiet
    weekly = []
    for _ in range(WEEKS):
        this_week = [0] * n
        for c in range(CALLOUTS_PER_WEEK):
            # Closeness: travel time 10-30 min each, out of the 45-min range.
            prox = [1 - rng.uniform(10, 30) / 45 for _ in range(n)]
            order = sorted(range(n),
                           key=lambda i: W_PROX * prox[i] + W_ACC * scores[i] + W_CAP,
                           reverse=True)
            # Fair share: a quiet responder goes to the front every Nth callout.
            if fair_share and last_week[0] < QUIET_BELOW and c % fair_share == 0:
                order.remove(0)
                order.insert(0, 0)
            for i in order:                          # one phone at a time
                this_week[i] += 1
                quiet = last_week[i] < QUIET_BELOW and not alert
                miss_p, decline_p = BEHAVIOUR[(wait, quiet)]
                r = rng.random()
                if r < miss_p:
                    scores[i] = clamp(scores[i] - miss_pen)
                elif r < miss_p + decline_p:
                    scores[i] = clamp(scores[i] - DECLINE_PEN)
                else:
                    scores[i] = clamp(scores[i] + CREDIT)
                    break
        # Recovery over time: close part of the gap to 0.5 each week.
        if recover:
            scores = [s + (0.5 - s) * recover if s < 0.5 else s for s in scores]
        last_week = this_week
        weekly.append(this_week[0])
    return weekly


def main():
    rng = random.Random(42)
    print(f"{RUNS} runs x {WEEKS} weeks; 'normal' = {NORMAL_PINGS}+ pings/week\n")
    for name, cfg in SCENARIOS.items():
        runs = [run_once(rng=rng, **cfg) for _ in range(RUNS)]
        avg = [statistics.mean(r[w] for r in runs) for w in range(WEEKS)]
        hits = [next((w + 1 for w in range(WEEKS) if r[w] >= NORMAL_PINGS), None)
                for r in runs]
        made_it = [w for w in hits if w is not None]
        print(name)
        print("  avg pings/week by week:", [round(x, 1) for x in avg[:12]], "...",
              round(avg[-1], 1))
        print(f"  back to normal within 26 weeks: {100 * len(made_it) / RUNS:.0f}%")
        if made_it:
            print(f"  median weeks to get there: {statistics.median(made_it)}")
        print()


if __name__ == "__main__":
    main()
