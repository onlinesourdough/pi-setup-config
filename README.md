# pi-setup-config

Backup og bootstrap-guide til Gustavs PI setup.

Repoet spejler portable PI-konfigurationer: settings, lokale skills, extensions og themes. Det indeholder ikke auth, sessions, caches, `node_modules` eller API keys.

## Spejlet indhold

- `config/settings.json` — macOS-default og bagudkompatibel default.
- `config/macos/settings.json` — macOS setup:
  - provider/model: `openai-codex` / `gpt-5.5`
  - thinking: `low`
  - packages: `npm:context-mode`
- `config/windows/settings.json` — Windows setup:
  - provider/model: `openai-codex` / `gpt-5.5`
  - thinking: `low`
  - packages: `npm:context-mode`
- `config/skills/`
  - `vps-temporary-ssh`
- `config/extensions/` — lokale PI extensions, inkl. Superset hooks og smart voice notify.
- `config/themes/` — lokale/valgte themes.

Repoet undgår at spejle package-/git-installerede skills som `brave-search` og context-mode for at undgå skill-conflicts. De installeres/vedligeholdes af PI packages eller eksisterende skill sources.

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

## Ny Windows maskine

1. Installer PI, Git og Node.js.
2. Clone repoet og følg `SETUP_PROMPT.md`; vælg Windows.
3. Local/model-provider setup håndteres separat og spejles ikke længere i dette repo.

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
Remove-Item (Join-Path $target "themes") -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item (Join-Path $target "skills") -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item (Join-Path $target "extensions") -Recurse -Force -ErrorAction SilentlyContinue
Copy-Item .\config\themes (Join-Path $target "themes") -Recurse -Force
Copy-Item .\config\skills (Join-Path $target "skills") -Recurse -Force
Copy-Item .\config\extensions (Join-Path $target "extensions") -Recurse -Force

pi update --extensions
```

## Brave Search

`brave-search` spejles ikke som lokal skill i repoet for at undgå conflicts med eksisterende skill-installationer. Sæt kun API key lokalt på hver maskine, hvis du bruger Brave Search:

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
