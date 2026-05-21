# pi-setup-config

Backup og bootstrap-guide til Gustavs PI setup.

Repoet spejler portable PI-konfigurationer: settings, lokale skills, extensions og themes. Det indeholder ikke auth, sessions, caches, `node_modules` eller API keys.

## Spejlet indhold

- `config/settings.json` — macOS-default og bagudkompatibel default.
- `config/macos/settings.json` — macOS setup:
  - provider/model: `openai-codex` / `gpt-5.5`
  - thinking: `low`
  - packages: `npm:context-mode`
- `config/windows/settings.json` — Windows/local-model setup:
  - provider/model: `lemonade-local-thinking` / `Gemma-4-31B-it-GGUF`
  - thinking: `low`
  - packages: `npm:context-mode`
- `config/windows/models.json` — Windows local model provider config:
  - Lemonade/OpenAI-compatible endpoint: `http://127.0.0.1:13305/v1`
- `config/skills/`
  - `brave-search`
  - `vps-temporary-ssh`
  - context-mode skills: `context-mode`, `ctx-doctor`, `ctx-insight`, `ctx-purge`, `ctx-stats`, `ctx-upgrade`
- `config/extensions/` — lokale PI extensions, pt. Superset hooks.
- `config/themes/` — lokale/valgte themes.

`git:https://github.com/badlogic/pi-skills` er bevidst fjernet; repoet bruger den lokale `brave-search` skill i stedet.

## Ikke inkluderet

- `~/.pi/agent/auth*`, login, sessions, history og caches.
- `node_modules`, npm/git package caches og genererede filer.
- Secrets/API keys, fx `BRAVE_API_KEY`.

## Ny macOS maskine

```bash
brew install node git
npm install -g @earendil-works/pi-coding-agent

git clone https://github.com/gustavonline/pi-setup-config.git ~/Downloads/pi-setup-config
cd ~/Downloads/pi-setup-config
pi
```

I PI: bed den om at følge `SETUP_PROMPT.md` og vælge macOS.

## Ny Windows maskine med lokale modeller

1. Installer PI, Git og Node.js.
2. Start Lemonade/local OpenAI-compatible server på `http://127.0.0.1:13305/v1`.
3. Clone repoet og følg `SETUP_PROMPT.md`; vælg Windows.
4. Hvis endpoint/model ændrer sig, ret `~/.pi/agent/models.json` efter setup.

## Manuelt setup macOS

```bash
cd ~/Downloads/pi-setup-config

mkdir -p ~/.pi
[ -d ~/.pi/agent ] && cp -R ~/.pi/agent ~/.pi/agent.backup.$(date +%Y%m%d-%H%M%S)
mkdir -p ~/.pi/agent

cp config/macos/settings.json ~/.pi/agent/settings.json
rm -rf ~/.pi/agent/themes ~/.pi/agent/skills ~/.pi/agent/extensions
cp -R config/themes ~/.pi/agent/themes
cp -R config/skills ~/.pi/agent/skills
cp -R config/extensions ~/.pi/agent/extensions

pi update --extensions || pi update
find ~/.pi/agent/skills -type f -name "*.js" -exec chmod +x {} +
```

## Manuelt setup Windows

```powershell
cd $HOME\Downloads\pi-setup-config

$target = Join-Path $HOME ".pi\agent"
New-Item -ItemType Directory -Force -Path $target | Out-Null
Copy-Item .\config\windows\settings.json (Join-Path $target "settings.json") -Force
Copy-Item .\config\windows\models.json (Join-Path $target "models.json") -Force
Remove-Item (Join-Path $target "themes") -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item (Join-Path $target "skills") -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item (Join-Path $target "extensions") -Recurse -Force -ErrorAction SilentlyContinue
Copy-Item .\config\themes (Join-Path $target "themes") -Recurse -Force
Copy-Item .\config\skills (Join-Path $target "skills") -Recurse -Force
Copy-Item .\config\extensions (Join-Path $target "extensions") -Recurse -Force

pi update --extensions
```

## Brave Search

Sæt API key lokalt på hver maskine:

```bash
echo 'export BRAVE_API_KEY="your-api-key-here"' >> ~/.zprofile
source ~/.zprofile
```

## Opdater repoet fra denne maskine

```bash
cd ~/Downloads/pi-setup-config

cp ~/.pi/agent/settings.json config/macos/settings.json
cp ~/.pi/agent/settings.json config/settings.json
rm -rf config/themes config/skills config/extensions
cp -R ~/.pi/agent/themes config/themes
cp -R ~/.pi/agent/skills config/skills
cp -R ~/.pi/agent/extensions config/extensions

find config -name .DS_Store -delete
find config/skills -type d -name node_modules -prune -exec rm -rf {} +
find config/skills -type f -name .package-lock.json -delete

git add .
git commit -m "Update PI setup config"
git push
```
