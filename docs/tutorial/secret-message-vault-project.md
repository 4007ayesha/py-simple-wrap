# Building a Secret Message Vault with Easy Base64 and Easy Hash

Combine **Easy Base64** and **Easy Hash** to disguise notes from casual reading and verify message integrity using digital fingerprints in just a few lines of Python.

## What we are building

Imagine you and a friend want to pass secret dispatches back and forth—such as game clues, mission briefings, or club codes. You want to disguise the text from casual eyes so someone glancing over your shoulder cannot immediately read it, while generating a digital fingerprint to verify that the message has not been altered or corrupted by comparing it against a trusted original checksum.

Base64 is an encoding format, not encryption—it obscures text from casual viewing but provides no confidentiality, as anyone can easily reverse it. Similarly, a regular hash allows a recipient to detect changes against a trusted original baseline, but cannot prevent an active attacker from modifying both the message and the hash if both are transmitted together over an untrusted channel.

Install the package:

```bash
python -m pip install py-simple-wrap
```

Save the following as `secret_vault.py`:

```python
from py_simple import (
    decode_text,
    encode_text,
    hash_text,
    hashes_match,
    is_base64,
)

# 1. Write the secret dispatch
secret_message = "Meet at midnight by the old oak tree. The password is: BLUEBERRY."

# 2. Scramble the message into Base64 and record a SHA-256 digital fingerprint
# Note: Base64 disguises text from casual glance, but provides no encryption/confidentiality.
vault_payload = encode_text(secret_message)
fingerprint = hash_text(vault_payload)

print("--- Outgoing Dispatch ---")
print(f"Scrambled: {vault_payload}")
print(f"SHA-256 fingerprint: {fingerprint}")

# 3. Simulate receiving and verifying the payload against the trusted original fingerprint
# Hashes verify data integrity by comparing against a known baseline.
print("\n--- Incoming Delivery ---")
if is_base64(vault_payload) and hashes_match(vault_payload, fingerprint):
    print("Integrity check: VERIFIED (Payload matches trusted fingerprint)")
    revealed = decode_text(vault_payload)
    print(f"Decoded message: {revealed}")
else:
    print("Integrity check: WARNING (Payload does not match expected fingerprint)")

# 4. What happens if the payload is altered in transit?
# If the payload is modified without the trusted original fingerprint matching, it alerts us.
tampered_payload = vault_payload[:-4] + "AAAA"
print("\n--- Tamper Test ---")
if not hashes_match(tampered_payload, fingerprint):
    print("Tampering alert: The payload does not match the trusted fingerprint!")
```

Run the script from your terminal:

```bash
python secret_vault.py
```

Example output:

```text
--- Outgoing Dispatch ---
Scrambled: TWVldCBhdCBtaWRuaWdodCBieSB0aGUgb2xkIG9hayB0cmVlLiBUaGUgcGFzc3dvcmQgaXM6IEJMVUVCRVJSWS4=
SHA-256 fingerprint: ae35c0900d3181cf57b07c0b7a7235eff5dbe756bafe99e97779697994134c18

--- Incoming Delivery ---
Integrity check: VERIFIED (Payload matches trusted fingerprint)
Decoded message: Meet at midnight by the old oak tree. The password is: BLUEBERRY.

--- Tamper Test ---
Tampering alert: The payload does not match the trusted fingerprint!
```

## What happened?

1. `encode_text(secret_message)` converts the plaintext string into a Base64-encoded ASCII string. Base64 is an encoding format, **not encryption**. While it obscures text from a casual glance and makes binary or formatted strings safe for storage and transmission, it provides **no confidentiality**—anyone who sees the encoded string can immediately decode it back to the original text.
2. `hash_text(vault_payload)` calculates a cryptographic SHA-256 checksum of the scrambled payload. Even if a single character is changed later, the hash will produce a completely different result.
3. `is_base64(vault_payload)` checks that the payload format is valid Base64 before attempting to decode it.
4. `hashes_match(vault_payload, fingerprint)` verifies that the payload still matches the trusted original checksum. Because the checksum matches our known baseline, we can verify that the text was not accidentally modified or corrupted in transit.
5. `decode_text(vault_payload)` converts the Base64 string back into readable plaintext.
6. In the tamper test, changing even a few characters in `tampered_payload` causes `hashes_match()` to return `False`, alerting the recipient that the payload differs from the original baseline.

## Understanding Security: Integrity vs. Confidentiality

When working with Base64 and hashes, it is essential to understand what these tools do—and what they do not do:

- **Base64 disguises, but does not encrypt:** Base64 is an encoding scheme, not encryption. It prevents someone glancing at a screen from immediately reading the text, but provides no actual confidentiality. Anyone with access to the encoded text can decode it with `decode_text()`. Never rely on Base64 alone to protect sensitive data or real secrets.
- **Hashes detect alterations against a trusted baseline:** A SHA-256 hash acts as a digital fingerprint used to verify data integrity. When compared against a **trusted original fingerprint** (such as one saved beforehand or shared across a secure channel), you can detect if the message was altered or corrupted.
- **Hashes alone are not "tamper-proof":** A regular hash does not prevent an active attacker from modifying the message if both the message and the hash are transmitted over the same untrusted channel. An attacker could alter the message, compute a brand new SHA-256 hash for the altered text, and replace both. To guard against an active attacker modifying both data and checksum in real-world systems, cryptographic tools like Hash-based Message Authentication Codes (HMAC) or digital signatures with private keys are used.

## Try it yourself

- **Save to disk:** Use `encode_file()` and `decode_to_file()` to disguise and save an entire secret file or clue sheet to disk.
- **Switch algorithms:** Pass `algorithm="md5"` or `algorithm="sha1"` to `hash_text()` and `hashes_match()` to see how different checksum algorithms look.
- **Interactive decipher tool:** Wrap the receiving step with Python's `input()` prompt so users can paste in scrambled dispatches and security keys to unlock them interactively.

## Why use these helpers?

Without `py-simple-wrap`, achieving this with Python's standard library requires several boilerplate steps:
- Converting strings back and forth to bytes using `.encode("utf-8")` and `.decode("ascii")` for `base64.b64encode()` and `base64.b64decode()`.
- Setting up `hashlib.sha256()`, feeding bytes to the hasher, and calling `.hexdigest()`.
- Handling decoding errors and validating strings manually with `try/except` blocks.

Combining `easy_base64` and `easy_hash` replaces repetitive byte conversions and hashing plumbing with intuitive, single-line functions.

For more examples and detailed function references, see [Easy Base64](easy_base64.md) and [Easy Hash](easy_hash.md).
