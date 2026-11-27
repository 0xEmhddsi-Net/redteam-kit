# Multi-turn chains

The current automated tests are single request/response cases. Real applications can
accumulate state across turns, so an authorization or trust decision in one turn may be
misapplied later.

When adapting these cases to a multi-turn application, preserve the same controls:

1. Start with a harmless baseline turn.
2. Introduce only synthetic untrusted content in a later turn.
3. Check that the application maintains instruction priority and data boundaries.
4. Record the full, sanitized sequence and a reproducible run identifier.

Do not treat a multi-turn pass as proof that tool use is safe. Tool authorization,
argument validation, and side-effect confirmation require separate tests.
