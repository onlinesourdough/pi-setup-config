---
name: vps-temporary-ssh
description: Prepare project-local SSH keys and copyable commands for authorized temporary VPS access, with verified OpenSSH server-side key expiry and exact-key revocation.
---

# Temporary VPS SSH access

Resolve authorized host, account, intended access and lifetime before generating keys or preparing a grant. Never assume root. Existing explicit authorization suffices; ask only for missing scope. Preparing files does not authorize connecting or changing a server.

## Prepare and verify

- Resolve the intended project root; nearest parent containing `.pi` is usable only if it is that project. Store artifacts in `<project>/.pi/tmp/ssh`, never the global Pi directory. Ensure this private directory is excluded from version control; stop if already tracked. Use a unique filename, directory mode 700 and `umask 077`.
- Generate an agent-side Ed25519 pair with `ssh-keygen -t ed25519 -N "" -f "$KEY" -C "$TAG"` when authorized. Never overwrite a key, print private content or commit it. Private key mode must be 600. Read public key and fingerprint with `ssh-keygen -lf "$KEY.pub"`.
- Establish target account's effective authorized-key source, ownership and permissions from authorized evidence. Do not assume a root path or change server-wide SSH configuration. Preserve separate working administrative access and verify the host key; never bypass host-key checking.
- Verify installed server support for expiry-time using its version and corresponding server documentation, and confirm server clock/time zone. Client version or sshd configuration validation alone does not prove an authorized-key option works. If support or effective key source is unresolved, do not issue an unbounded grant or promise expiry.

[OpenSSH documentation](https://man.openbsd.org/sshd.8#AUTHORIZED_KEYS_FILE_FORMAT) specifies `expiry-time="YYYYMMDDHHMMSSZ"` for an absolute UTC deadline. Use verified server time and the requested lifetime (30 minutes if unspecified), computing at installation or regenerating if delayed. Never use background sleep as an expiry mechanism. Expiry rejects subsequent authentication; it does not remove the line or terminate established sessions.

## Copyable grant and proof

Prepare a target-specific command that checks account/path, backs up the affected key file, preserves existing entries/metadata and appends the exact public key with expiry only on success. Apply restrictions appropriate to authorized access; do not silently grant forwarding or broader privileges. Do not overwrite the file, append unrestricted duplicates, follow unexpected symlinks or claim success after failure. Quote values for the target shell and avoid nested background-job recipes.

Save the exact copyable command in `<key>.vps-command.txt` and human-readable `.md` beside it. Include target/account, public key, fingerprint, deadline, restrictions and exact-key cleanup instructions. Prefer file links over a long terminal line; offer a platform-appropriate clipboard command when useful.

Within authorized remote scope, verify a fresh connection uses only this identity (IdentitiesOnly=yes, no agent/password fallback or reused multiplexed connection). Verify rejection after expiry under the same constraints, distinguishing expiry from unrelated failure using server evidence. Until tested, report enforcement as configured but unverified. Continue already authorized work without a ceremonial stop; if the user must execute the grant, state that dependency.

## Exact-key cleanup

Identify entries by generated key type and base64 blob, never comment or shared pi-temp prefix. Review matching entries, including option-prefixed duplicates and other effective key sources, before removal. Preserve all other lines byte-for-byte.

This Ed25519 filter produces a candidate from bytes, accepting an optional quoted options field and ignoring comments. It does not validate OpenSSH option semantics; inspect malformed or unmatched entries manually:

```python
import re

def revoke_candidate(content, key_blob):
    if not re.fullmatch(rb"[A-Za-z0-9+/]+={0,2}", key_blob):
        raise ValueError("Invalid public key blob")
    field = rb'(?:[^\x20\t"\r\n]|"(?:[^"\\]|\\.)*")+'
    entry = re.compile(
        rb"^[ \t]*(?:" + field + rb"[ \t]+)?ssh-ed25519[ \t]+"
        + re.escape(key_blob) + rb"(?=[ \t\r\n]|$)"
    )
    return b"".join(
        line for line in content.splitlines(keepends=True)
        if line.lstrip().startswith(b"#") or not entry.match(line)
    )
```

This is a filter, not a live-file writer. For authorized cleanup, back up the exact file, inspect candidate diff, and replace only after confirming source has not changed, with concurrent writers excluded and ownership/mode preserved. Refuse symlinks. Verify matching entries are gone and unrelated bytes unchanged. Cleanup does not end existing sessions; close only sessions in scope. Retain public fingerprint/receipt and remove local private key when no longer needed under user retention instructions.
