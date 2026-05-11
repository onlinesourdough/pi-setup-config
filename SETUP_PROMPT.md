# SETUP_PROMPT

Use this prompt with PI on a new machine after cloning this repo:

---

I cloned `~/Downloads/pi-setup-config`.
Please set up my PI config from this repo.

Do this:

1. Verify these exist:
   - `config/settings.json`
   - `config/themes`
   - `config/skills`
2. Read `README.md` so you understand what is intentionally included/excluded.
3. Back up my current config if it exists:
   - `~/.pi/agent` -> `~/.pi/agent.backup-<timestamp>`
4. Apply repo config to `~/.pi/agent`:
   - copy `config/settings.json` to `~/.pi/agent/settings.json`
   - replace `~/.pi/agent/themes` with `config/themes`
   - replace `~/.pi/agent/skills` with `config/skills`
5. Install/update PI packages from `settings.json`:
   - run `pi update --extensions` if available
   - if that fails, run `pi update`
   - do not manually copy package caches/git clones from another machine
6. Install dependencies in each local skill folder with `package.json`:
   - use `npm ci --omit=dev` if `package-lock.json` exists
   - otherwise `npm install --omit=dev`
7. Ensure skill scripts are executable on macOS:
   - run `find ~/.pi/agent/skills -type f -name "*.js" -exec chmod +x {} +`
8. Confirm result:
   - show active theme from `~/.pi/agent/settings.json`
   - show provider/model/thinking level
   - list packages from `~/.pi/agent/settings.json`
   - list installed local skill folders
   - remind me to set `BRAVE_API_KEY` locally if I want to use `brave-search`
9. Give me a short summary.

Only touch settings/themes/skills/packages. Do not touch auth, login, session, history, or cache files except what PI itself updates while installing packages.
