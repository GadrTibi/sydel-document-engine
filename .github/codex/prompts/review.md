Review this pull request with the following repository constraints:

1. The engine must remain deterministic.
2. Do not introduce hidden AI generation logic in document production.
3. Flag any wording drift in legal text.
4. Check that the document lifecycle was respected before implementation.
5. Check that business constants are externalized and not hard-coded in multiple places.
6. Verify test coverage for helpers, conditions, and formatting-sensitive code.
7. Focus on high-severity problems first.
