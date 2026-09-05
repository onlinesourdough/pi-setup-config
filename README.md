# pi-setup-config

Backup og scoped bootstrap-guide til Gustavs PI setup. Ingen auth, sessions, caches eller private API keys.

## Indhold og ejerskab

- `config/settings.json` er bagudkompatibel macOS-profil. `config/macos/settings.json` og `config/windows/settings.json` bruger begge `openai-codex` / `gpt-5.5`, thinking `low`: eksisterende brugervalg, ikke en modelmigration.
- Windows `models.json` tilbyder Lemonade på `http://127.0.0.1:13305/v1`, `Gemma-4-31B-it-GGUF`, til manuelt valg; lokal model er ikke default.
- `vps-temporary-ssh` er first-party. `brave-search` er en adapteret pi-skills-import. Backup mangler dens refererede `search.js`, `content.js` og `package.json`; installer den ikke som fungerende skill. Bevar eksisterende komplette installationer. Rekonstruktion fra verificeret upstream kræver særskilt scope.
- De seks importerede context-mode skills (`context-mode`, `ctx-doctor`, `ctx-insight`, `ctx-purge`, `ctx-stats`, `ctx-upgrade`) og fire referencer er legacy recovery/proveniens. Præcis importversion er ikke registreret. Bevar payloads uden lokale forks.
- `config/extensions/superset-hooks.ts` og individuelt valgte filer i `config/themes/` er øvrige mulige kopiemner.

## Onboarding og manuel recovery: macOS og Windows

Brug installeret PI, Git og Node.js, eller installer dem inden for autoriseret maskinopsætning. Clone fra `https://github.com/onlinesourdough/pi-setup-config.git` og følg [SETUP_PROMPT.md](SETUP_PROMPT.md). Samme scoped procedure gælder manuel opsætning på begge platforme:

1. Vælg profil fra brugerens valg eller OS. Destination er brugerens `~/.pi/agent` (Windows: `$HOME\.pi\agent`), medmindre en anden PI-konfigurationsrod er valgt. Oplist præcise settings-felter, pakker og filer til ændring.
2. Tag en unik, adgangsbeskyttet backup af berørte eksisterende filer uden for aktive discovery-rødder. Kontroller læsbarhed og lighed med originalen. Registrer også destinationer der ikke fandtes. Backups kan indeholde følsomme værdier og må ikke ind i repoet.
3. Sammenlign kilde/destination. Bevar ikke-valgte settings, modelvalg, pakker, skills, extensions og themes samt OSM-bridges, instruktioner og owner-ruter. Forbered diff for konflikter eller uklart ejerskab og afklar kun det uafklarede; eksisterende præcis autorisation kræver ingen ekstra godkendelsesrunde.
4. Merge valgte JSON-felter; overskriv aldrig hele eksisterende settings/models-filer. Bevar ukendte og nestede felter samt eksisterende pakkeindstillinger. En tom installation kan starte fra valgt profil. På Windows tilføjes kun valgte Lemonade-providerposter uden at overskrive eksisterende poster eller skifte default.
5. Kopier kun valgte konkrete owned filer/foldere. Slet eller erstat aldrig hele skills/extensions/themes-rødder. Afvis uventede symlinks eller destinationer uden for scope. Ingen rekursiv chmod over brugerens skills.

## Én context-mode distribution

Normal rute er profilens `npm:context-mode`. Kopier ikke de seks legacy skill-foldere, og tilføj ikke repoets samlede `config/skills` som discovery-sti. Kontroller eksisterende pakker og lokale skills før aktivering.

Ved eksisterende lokale kopier: verificer oprindelse og lokale ændringer; flyt kun identificerede, autoriserede dubletter til backup uden for aktive discovery-rødder før npm-ruten aktiveres. Ved uklarhed bevares eksisterende installation, og den nye aktiveres ikke. Legacy recovery er et eksplicit alternativ med npm-ruten deaktiveret og en komplet kompatibel runtime verificeret først; de kopierede skills alene er ikke en runtime.

Ved autoriseret pakkeinstallation/opdatering: brug installeret PI's hjælp til en operation begrænset til context-mode. Ingen bred update-fallback. Ved fejl rapporteres fejlen; aktiver ikke automatisk en alternativ distribution.

## Verifikation og recovery

Genlæs ændret JSON; kontroller aktive modelvalg, theme, pakker og discovery-kilder. Bekræft én context-mode-kilde og rapporter uverificeret runtime-adfærd. Sammenlign ikke-valgte filer/felter med førtilstanden, inklusive OSM.

Ved fejl gendannes kun ændrede owned filer/felter fra backup. Fjern kun nye emner registreret i denne kørsel, hvis de stadig matcher det skrevne indhold. Merge recovery ved efterfølgende brugerændringer. Rapporter pakkeinstallationens øvrige effekter og brug scoped package recovery, ikke blanket config-restore.

På Windows skal Lemonade køre før manuelt modelvalg; endpoint/model kan justeres lokalt. Brave kræver komplet installation og lokalt konfigureret `BRAVE_API_KEY`; kopier aldrig nøglen til repoet.

## Opdater backup-repoet

Sammenlign og importer kun valgte portable repo-ejede filer. Kopier aldrig hele brugerens skills/extensions/themes tilbage. Udelad OSM-data, auth, sessions, history, caches, node_modules og secrets. Bevar importproveniens og legacy-filer. Gennemgå diff og valider lokalt; commit, push og publicering kræver egen autorisation.
