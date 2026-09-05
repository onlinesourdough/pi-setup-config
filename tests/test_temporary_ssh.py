"""Exercise the documented filter without keys, credentials or remote access."""
import pathlib
import re
import tempfile
import unittest

SKILL = pathlib.Path(__file__).resolve().parents[1] / "config/skills/vps-temporary-ssh/SKILL.md"
namespace = {}
exec(re.search(r"```python\n(.*?)```", SKILL.read_text(), re.S).group(1), namespace)
candidate = namespace["revoke_candidate"]


class RevocationTest(unittest.TestCase):
    def test_exact_identity_preserves_unrelated_bytes(self):
        keep = (b'# ssh-ed25519 QUJD pi-temp-one\r\n'
                b'ssh-ed25519 REVG pi-temp-one\n'
                b'ssh-ed25519 QUJDextra pi-temp-two\n'
                b'ssh-rsa QUJD other-type\n'
                b'command="echo ssh-ed25519 QUJD" ssh-ed25519 REVG other\n'
                b'command="unterminated ssh-ed25519 QUJD\n'
                b'\n')
        remove = (b'ssh-ed25519 QUJD pi-temp-one\n'
                  b'expiry-time="20260905160000Z" ssh-ed25519 QUJD changed-comment\r\n'
                  b'command="echo \\"quoted\\" words",restrict ssh-ed25519 QUJD x\n'
                  b'\tssh-ed25519\tQUJD')
        with tempfile.TemporaryDirectory() as tmp:
            source = pathlib.Path(tmp) / "authorized_keys.fixture"
            source.write_bytes(keep + remove)
            result = candidate(source.read_bytes(), b"QUJD")
            self.assertEqual(result, keep)
            self.assertEqual(source.read_bytes(), keep + remove)
            self.assertEqual(candidate(result, b"QUJD"), keep)

    def test_invalid_or_absent_identity(self):
        for blob in (b"", b".*", b"QUJD\n", b"QUJD other"):
            with self.assertRaises(ValueError):
                candidate(b"ssh-ed25519 QUJD retained\n", blob)
        self.assertEqual(candidate(b"untouched", b"QUJD"), b"untouched")


if __name__ == "__main__":
    unittest.main()
