# Chapter 12 — Constitutional Consensus *(multi-participant → Flutter)*

Companion files for *The Art of Grassroots Logic Programming*, Chapter 12.

Per Udi's direction, ch 12 follows the same template as ch 7–11.

## Use cases

### `ch12/blocklace-consensus/` — Use case 1 (§12.3–§12.7)

Blocklace structure (`block(Round, Payload, Pointers)`), three-round wave structure (candidates → endorsements → ratifications), dual-mode operation (low- and high-throughput with automatic transitions and timeout via `wait/1`), ordering function τ, and the §12.7 GLP implementation: agent state record `state(Blocklace, Mode, CurrentRound, Finalized, Pending)`, the main agent loop processing block events, a 5-clause `maybe_issue` dispatch keyed on (mode, round mod 3), round-robin leader selection by wave number, finality detection via majority endorsement + majority ratification. Deployed as a three-participant multi-agent play.

### `ch12/complete-consensus-example/` — Use case 2 (§12.8)

The §12.8 Alice/Bob/Carol example as a runnable scenario. The genesis block establishes `([alice, bob, carol], σ=0.5, Δ=1000ms)`. Wave 1 finalizes Alice's tx_a in low-throughput mode (propose → endorse → ratify in one wave, 3δ). Wave 2 detects an Alice/Bob conflict (tx_a2 vs tx_b); all switch to high-throughput; Carol is the round-robin formal leader but delegates to the first-received block, so all endorse Alice's; tx_a2 finalizes. Wave 3 returns to low-throughput as Bob retries tx_b alone. Final output: `Finalized = [tx_a, tx_a2, tx_b]`.

## Useful techniques

### `ch12/useful-techniques.glp`

Three-round wave structure; ordering function τ (incremental `compute_tau`); `is_majority/2` simple-majority pattern (σ = 1/2 with attested agents per §12.1); `wait_for_leader/2` timeout idiom (suspending clause `wait(Timeout?)` racing against immediate clause `known(Block?)`).

## How to run

```bash
cd glp_runtime/bin
dart run glp_repl.dart
```

```
load ../../olamni/tutorial/ch12/<use-case>
play.
```

```bash
cd glp_multiagent
flutter run -d windows -t lib/main_olamni_ch12_<use-case>.dart
```

## Pattern source in the repo

`programs/typed_book/constitutional_consensus/` (consensus.glp, play_agents.glp, play_high_throughput.glp, play_low_throughput.glp, test_blocklace.glp, test_waves.glp).
