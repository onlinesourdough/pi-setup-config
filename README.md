# pi-setup-config

Backup og bootstrap-guide til Gustavs PI setup.

Formålet er: på en ny maskine installerer du PI, cloner dette repo, og beder PI om at følge `SETUP_PROMPT.md`. Repoet indeholder kun konfiguration og egne skills/themes — ikke auth, sessions, caches, installerede `node_modules` eller API keys.

## Hvad der er spejlet her

- `config/settings.json` — nuværende PI settings:
  - provider/model: `openai-codex` / `gpt-5.5`
  - thinking: `off`
  - theme: `pi-desktop-catppuccin-light`
  - packages/extensions der skal hentes af PI:
    - `git:https://github.com/badlogic/pi-skills`
    - `npm:context-mode`
    - `npm:pi-schedule-prompt`
- `config/themes/` — custom/valgte themes, inkl. aktivt `pi-desktop-catppuccin-light`.
- `config/skills/` — egne lokale skills, fx `brave-search` og `vps-temporary-ssh`.

## Det der bevidst ikke er med

- `~/.pi/agent/auth*`, login, sessions, history og caches.
- `node_modules` og andre genererede dependencies.
- API keys/secrets, fx `BRAVE_API_KEY`.
- Allerede installerede package-kopier under `~/.pi/agent/git` eller npm cache. De bliver hentet igen via `settings.json`/`pi install`.

## Ny macOS maskine: fra nul til samme setup

### 1. Installer forudsætninger

```bash
# hvis Node/npm mangler, installer fx via Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install node git

# installer PI
npm install -g @earendil-works/pi-coding-agent
```

### 2. Start PI og log ind

```bash
pi
/login
```

Vælg den provider/login-metode du vil bruge. Auth bliver kun på maskinen og skal ikke committes.

### 3. Clone dette setup-repo

```bash
cd ~/Downloads
git clone https://github.com/gustavonline/pi-setup-config.git
cd pi-setup-config
```

### 4. Giv repoet til PI

Start PI i repoet og indsæt prompten fra `SETUP_PROMPT.md`:

```bash
pi
```

Eller sig kort:

> Følg `SETUP_PROMPT.md` og sæt min PI config op fra dette repo.

PI skal kun røre `settings`, `themes` og `skills` — ikke auth/session-filer.

### 5. Secrets/API keys pr. maskine

Hvis du bruger `brave-search`, skal Brave Search API key sættes lokalt:

```bash
echo 'export BRAVE_API_KEY="your-api-key-here"' >> ~/.zprofile
source ~/.zprofile
```

Opret key her: https://api-dashboard.search.brave.com/register

### 6. Genstart PI

Luk og start `pi` igen, så packages/extensions/themes/skills loader friskt.

## Manuelt setup uden assistant

Hvis du vil gøre det selv:

```bash
cd ~/Downloads/pi-setup-config

mkdir -p ~/.pi
[ -d ~/.pi/agent ] && cp -R ~/.pi/agent ~/.pi/agent.backup.$(date +%Y%m%d-%H%M%S)

mkdir -p ~/.pi/agent
cp config/settings.json ~/.pi/agent/settings.json
rm -rf ~/.pi/agent/themes ~/.pi/agent/skills
cp -R config/themes ~/.pi/agent/themes
cp -R config/skills ~/.pi/agent/skills

# Installer PI packages/extensions fra settings.json
pi update --extensions || pi update

# Installer deps for lokale skills, hvis de har package.json
find ~/.pi/agent/skills -name package.json -not -path '*/node_modules/*' -print0 | while IFS= read -r -d '' pkg; do
  d="$(dirname "$pkg")"
  (
    cd "$d"
    if [ -f package-lock.json ]; then npm ci --omit=dev; else npm install --omit=dev; fi
  )
done

find ~/.pi/agent/skills -type f -name "*.js" -exec chmod +x {} +
```

## Windows / PowerShell

```powershell
cd $HOME\Downloads
git clone https://github.com/gustavonline/pi-setup-config.git
cd .\pi-setup-config

$target = Join-Path $HOME ".pi\agent"
New-Item -ItemType Directory -Force -Path $target | Out-Null
Copy-Item .\config\settings.json (Join-Path $target "settings.json") -Force
Remove-Item (Join-Path $target "themes") -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item (Join-Path $target "skills") -Recurse -Force -ErrorAction SilentlyContinue
Copy-Item .\config\themes (Join-Path $target "themes") -Recurse -Force
Copy-Item .\config\skills (Join-Path $target "skills") -Recurse -Force

pi update --extensions

Get-ChildItem (Join-Path $target "skills") -Recurse -Filter package.json | ForEach-Object {
  $dir = $_.Directory.FullName
  Push-Location $dir
  if (Test-Path "package-lock.json") { npm ci --omit=dev } else { npm install --omit=dev }
  Pop-Location
}
```

## Hold repoet opdateret

Efter ændringer i dit lokale PI setup:

```bash
cd ~/Downloads/pi-setup-config

cp ~/.pi/agent/settings.json config/settings.json
rm -rf config/themes config/skills
cp -R ~/.pi/agent/themes config/themes
cp -R ~/.pi/agent/skills config/skills

find config/skills -type d -name node_modules -prune -exec rm -rf {} +
find config/skills -type f -name .package-lock.json -delete
find config/skills -type f -name "*.js" -exec chmod +x {} +

git add .
git commit -m "Update PI setup config"
git push
```

## Hurtig prompt til næste gang

Se `SETUP_PROMPT.md`.
