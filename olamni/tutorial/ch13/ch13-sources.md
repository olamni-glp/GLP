# Ch 13 Sources (bonus, Python actors)

Scenario per Udi: 3 AI engineers (parents) each with 3 named AI agents (children) collaborating on shared work. Apply the parent-children CSSN protocol with a purpose/context-scoped authorization step.

1. `programs/cssn_modules/` (parent-children CSSN agent + boot + ui modules — primary protocol source).
2. `programs/typed_book/social_networks/play_child_safe.glp` (parent-approval play; embedded response-variable approval pattern).
3. `programs/typed_book/social_networks/group_formation.glp`, `group_messaging.glp` (for "specific groups of agents" authorization scope).
4. `glp_multiagent/lib/main_cssn_village.dart`, `glp_multiagent/lib/main_cssg_mad_modules.dart` (Dart-side multi-isolate templates — adapt to 3+9 isolate layout).
5. `glp_multiagent/lib/mad_router.dart`, `glp_multiagent/lib/isolate_protocol.dart` (model for the line-delimited JSON Python-bridge protocol).
6. `ch13_tutorial.md`
7. `../charter.md`
