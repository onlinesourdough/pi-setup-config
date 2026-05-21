# SETUP_PROMPT

Use this prompt with PI on a new machine after cloning this repo:

---

I cloned `~/Downloads/pi-setup-config`. Please set up my PI config from this repo.

Do this:

1. Ask me which platform profile to apply:
   - `macos` -> use `config/macos/settings.json`
   - `windows` -> use `config/windows/settings.json` for local models
   - if I do not answer, infer from OS and use macOS on Darwin, Windows on Windows
2. Verify these exist:
   - selected profile settings file
   - `config/themes`
   - `config/skills`
   - `config/extensions`
3. Read `README.md` so you understand what is intentionally included/excluded.
4. Back up my current config if it exists:
   - `~/.pi/agent` -> `~/.pi/agent.backup-<timestamp>`
5. Apply repo config to `~/.pi/agent`:
   - copy selected profile settings file to `~/.pi/agent/settings.json`
   - replace `~/.pi/agent/themes` with `config/themes`
   - replace `~/.pi/agent/skills` with `config/skills`
   - replace `~/.pi/agent/extensions` with `config/extensions`
6. Install/update PI packages from `settings.json`:
   - run `pi update --extensions` if available
   - if that fails, run `pi update`
   - do not manually copy package caches/git clones from another machine
7. Ensure skill scripts are executable on macOS/Linux:
   - run `find ~/.pi/agent/skills -type f -name "*.js" -exec chmod +x {} +`
8. If Windows/local models profile is selected:
   - confirm the local OpenAI-compatible server is running
   - default endpoint is `http://localhost:1234/v1`
   - remind me to set `LOCAL_OPENAI_MODEL`, `LOCAL_OPENAI_BASE_URL`, and `LOCAL_OPENAI_API_KEY` if needed
9. Confirm result:
   - show active theme from `~/.pi/agent/settings.json`
   - show provider/model/thinking level
   - list packages from `~/.pi/agent/settings.json`
   - list installed local skill folders, including brave-search, vps-temporary-ssh and ctx/context-mode skills
   - list installed extension files/folders
   - remind me to set `BRAVE_API_KEY` locally if I want to use `brave-search`
10. Give me a short summary.

Only touch settings/themes/skills/extensions/packages. Do not touch auth, login, session, history, or cache files except what PI itself updates while installing packages.
