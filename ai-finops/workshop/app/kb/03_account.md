# [account] Account, login and security

Login methods: email and password, Google sign-in, Microsoft sign-in. SAML SSO (Okta, Entra ID, OneLogin, any SAML 2.0 provider) is Enterprise only.

Password rules: at least 12 characters. Passwords are checked against known breached-password lists. There is no forced periodic rotation.

Two-factor authentication (2FA): supported via authenticator apps (TOTP) and hardware security keys (WebAuthn/FIDO2). SMS codes are not supported. Workspace owners on Business and Enterprise can make 2FA mandatory for all members (Settings > Security > Require 2FA).

Lost 2FA device: the user should use one of the 10 one-time recovery codes shown when 2FA was enabled. If the codes are lost too, the workspace owner can reset 2FA for that member from Settings > Members. If the affected person is the owner and no other admin exists, support must verify identity with a video call and a government ID; this takes up to 3 business days. Support agents must never disable 2FA based on an email request alone.

Locked account: after 10 failed login attempts the account is locked for 30 minutes. The lock clears automatically; support cannot clear it earlier.

Changing the account email: Settings > Profile > Email. A confirmation link is sent to the new address and a notice to the old one; the change completes when the link is clicked within 24 hours.

Transferring workspace ownership: only the current owner can transfer ownership, to an existing admin, from Settings > Members > Transfer ownership. If the owner has left the company and cannot be reached, the customer must send a request on company letterhead signed by a director; support escalates it to the trust team (tag: trust-escalation).

Sessions: web sessions expire after 14 days of inactivity. Owners can sign out all sessions of a member from Settings > Members.

Roles: Owner (one per workspace), Admin, Accountant (can create and send invoices, cannot change billing or members), Viewer (read-only, free, does not consume a paid seat).
