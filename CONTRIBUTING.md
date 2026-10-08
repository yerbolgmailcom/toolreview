# Contributing

Keep the executable self-contained. Change embedded assets using tools/assets.py
and run ./toolreview test. If a change affects authorization or scope, include a
regression case that demonstrates the failure and the corrected behavior.

Use synthetic fixtures. Never submit personal prompts, model call recordings,
credentials, machine addresses or private configuration. Keep model behavior
claims tied to a named version, configuration and evaluation; mock tests are not
model accuracy results.

Use feature branches and small commits. Describe the observable change and how
it was validated. Do not run live-provider evaluations from CI or pull requests.
