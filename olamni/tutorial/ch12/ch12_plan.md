# Ch 12 Plan (multi-agent + Flutter)

## Shared
- Project per use case: self/agent/network/actors/boot.glp.
- Flutter: copy [s3] → main_olamni_ch12_<use-case>.dart; retarget _projectDir.

## Use cases
- blocklace-consensus/: §12.3 blocklace (block(Round, Payload, Pointers); genesis(P, σ, Δ); depth/rounds/waves) + §12.4 wave (3-round candidates/endorsements/ratifications, finality = majority endorse + majority ratify, quiescent waves) + §12.5 dual-mode (low- and high-throughput modes; round-robin formal leader; Low↔High transitions; wait_for_leader timeout via `wait/1`) + §12.6 ordering function τ (incremental compute_tau via find_new_finalized + order_candidates + append) + §12.7 GLP implementation (state(Blocklace, Mode, CurrentRound, Finalized, Pending); agent/4 main loop; handle_event adds block, runs check_mode/advance_round/maybe_issue; 5-clause maybe_issue keyed on (mode, Round mod 3) covering low-throughput propose/endorse/ratify and high-throughput leader/timeout; leader/3 round-robin by wave number; is_finalized via endorsements_for + ratifications_for + is_majority; update_finalized appends newly finalized).
- complete-consensus-example/: §12.8 Alice/Bob/Carol scenario — `genesis([alice, bob, carol], 0.5, 1000)`; Wave 1 low-throughput (R1 Alice proposes tx_a; R2 all endorse; R3 all ratify; finalize [tx_a]); Wave 2 high-throughput (R4 Alice/Bob conflict tx_a2 vs tx_b; formal leader is Carol per round-robin, but with no transaction Carol delegates to first-received → all endorse Alice; R5–R6 finalize tx_a2); Wave 3 (R7 Bob retries tx_b alone, low-throughput; R8 endorse; R9 ratify); final Finalized = [tx_a, tx_a2, tx_b].
- useful-techniques.glp: 3-round wave structure; ordering function τ; `is_majority/2` simple-majority pattern (σ = 1/2 with attested agents per §12.1); `wait_for_leader/2` timeout idiom (clause 1 suspends on `wait(Timeout?)`, clause 2 succeeds on `known(Block?)` — first to fire wins).

## Test
- REPL each: load project; play_<name>. → succeeds.
- Flutter each: per-agent panels showing consensus rounds.
