"""System-level disclosure for a chatbot (AI Act Art. 50(1) + 50(5)), as plain testable code.

Design rule behind this file: the disclosure that tells a person "you are talking to an AI" must not depend on what
the language model happens to say. It is (1) a fixed notice shown by the application at the START of the session
(Art. 50(5): at the latest at first interaction; Commission Guidelines 2026-07-20 point 37: first-turn greeting / banner),
(2) a persistent badge, (3) an output guard that stops the system from telling a person it is human, and (4) for agents
that write to third parties, a header that names the AI and the person it acts for (Guidelines point 31).

This is an engineering sketch for the workshop, NOT legal advice and NOT a compliance certificate.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

# ---- the fixed texts (plain language, specific to this system; see lint_disclosure) --------------------------------
NOTICE = ("You are chatting with Ledgerly's AI assistant - an automated system, not a person. "
          "It can make mistakes; you can ask for a human colleague at any time.")
BADGE = "AI assistant"
TRUTHFUL_REPLY = ("I'm an AI assistant - an automated system, not a human. "
                  "If you would like to talk to a person, tell me and I will pass you on to a colleague.")


# ---- 1. lint: is this disclosure text one of the forms the Guidelines call insufficient on their own? ----------------
_AI_WORD = re.compile(r"\b(AI|artificial intelligence|automated system|bot|chatbot|machine)\b", re.I)
_NOT_HUMAN = re.compile(r"\b(not (a )?(human|person|real person)|no(t)? human|automated)\b", re.I)
_GENERIC = re.compile(r"^\s*(your\s+)?(virtual\s+)?(assistant|helper|agent)\s*[.!]?\s*$", re.I)
_TECH_ONLY = re.compile(r"\b(uses?|powered by|based on)\s+(an?\s+)?(LLM|LLMs|large language model|GPT|model)s?\b", re.I)
_TERMS_ONLY = re.compile(r"\b(terms|conditions|privacy policy|see our policy|documentation)\b", re.I)


def lint_disclosure(text: str) -> list[str]:
    """Return problems found in a disclosure string (empty list = passes this *heuristic* check).

    Mirrors the 'insufficient when used alone' list in the Commission's Art. 50 Guidelines (2026-07-20, point 38):
    terms-and-conditions-only, ambiguous labels such as "assistant", purely technical statements such as
    "this system uses LLMs". It can only catch wording; it cannot judge placement or timing - see `first_turn_ok`.
    """
    problems = []
    t = text.strip()
    if _GENERIC.match(t):
        problems.append("generic label only ('assistant'): ambiguous, does not say it is not a human")
    if _TECH_ONLY.search(t) and not _AI_WORD.search(re.sub(_TECH_ONLY, "", t)):
        problems.append("technical description only ('uses LLMs'): does not explain the artificial nature to the user")
    if _TERMS_ONLY.search(t) and len(t.split()) < 12:
        problems.append("looks like a pointer to terms/documentation: such disclosures may complement, not replace, in-context ones")
    if not _AI_WORD.search(t):
        problems.append("does not name the AI / automated nature of the counterpart")
    return problems


# ---- 2. output guard: the system must not tell a person it is human -------------------------------------------------
# Heuristic regexes (English). They are a safety net, not a proof; see run_redteam.py for the measured miss/false-alarm rate.
_HUMAN_CLAIMS = [
    r"\b(i am|i'm|im|yes,? i am|yes,? i'm)\s+(a\s+|an\s+)?(real\s+|actual\s+|living\s+)?(human|person|human being|member of (the )?(staff|team))\b",
    r"\b(i am|i'm)\s+(definitely\s+|totally\s+)?(not|no)\s+(an?\s+)?(ai|a\.i\.|bot|robot|chatbot|machine|automated|artificial|language model)\b",
    r"\bnot\s+(an?\s+)?(ai|bot|robot|chatbot|machine)\b(?!.*\b(but|however)\b)",
    r"\b(i('m| am) (a )?(real|flesh)|i have (a )?(body|family|kids|children))\b",
    r"\bno,? i('m| am) (a )?(human|person)\b",
]
_HUMAN_CLAIM_RE = [re.compile(p, re.I) for p in _HUMAN_CLAIMS]
_AI_ADMISSION = re.compile(
    r"\b(i('m| am)|as)\s+(an?\s+)?(ai|a\.i\.|artificial|automated|virtual|digital|language model|chatbot|bot)\b|"
    r"\b(ai|artificial intelligence)[ -](powered|assistant|system|based)\b|\bnot (a )?(human|person|real person)\b", re.I)


def claims_human(reply: str) -> bool:
    """True if the reply asserts (or implies) that the speaker is a human / not an AI."""
    return any(r.search(reply) for r in _HUMAN_CLAIM_RE) and not re.search(r"\bnot (a |an )?(real )?(human|person)\b", reply, re.I)


def admits_ai(reply: str) -> bool:
    """True if the reply tells the user it is an AI / automated / not a human."""
    return bool(_AI_ADMISSION.search(reply)) and not claims_human(reply)


# ---- 2b. input-side router: when the USER asks what they are talking to, the application answers, not the model ---------
_NATURE = r"(human|human being|real person|person|people|robot|bot|chatbot|ai|a\.i\.|artificial|machine|automated|real employee|live agent|mensch|ki|roboter|maschine)"
_ASKS_NATURE = [re.compile(p, re.I) for p in (
    rf"\b(are|is|bist|sind)\s+(you|this|that|it|du|sie|da)\b.*\b{_NATURE}\b",
    rf"\b(am i|i am)\s+(talking|speaking|chatting|writing)\s+(to|with)\b.*\b{_NATURE}\b",
    rf"\byou('re| are)\b.*\b{_NATURE}\b",
    rf"\b(ist da)\b.*\b{_NATURE}\b",
    rf"\b{_NATURE}\s+(or|oder)\s+{_NATURE}\b",
    rf"\b(confirm|promise|swear)\b.*\b{_NATURE}\b",
)]


def asks_if_human(user_text: str) -> bool:
    """Heuristic (EN/DE): does the user ask whether the counterpart is a human/AI? Deterministic, so it cannot be talked out of it."""
    return any(r.search(user_text) for r in _ASKS_NATURE)


# ---- 3. the session wrapper ----------------------------------------------------------------------------------------
@dataclass
class Turn:
    role: str            # "notice" (application text), "user", "assistant"
    text: str
    guard_hit: bool = False   # the reply was produced/replaced by the application (router or output guard)


@dataclass
class DisclosingSession:
    """A chat session whose AI disclosure is produced by the application, not by the model.

    `llm` is any callable (messages -> reply text), so tests can run offline with a fake model.
    """
    llm: callable
    system_prompt: str
    guard: bool = True          # output guard: replace replies that claim to be human
    router: bool = True         # input router: answer 'are you human/AI?' from the application, skip the model
    transcript: list[Turn] = field(default_factory=list)

    def __post_init__(self):
        # Art. 50(5): at the latest at the time of the first interaction. The notice is part of the transcript the
        # user sees BEFORE they type anything.
        self.transcript.append(Turn("notice", NOTICE))

    @property
    def badge(self) -> str:
        return BADGE   # shown next to the input field for the whole session (Guidelines point 37, 'persistent badge')

    def ask(self, user_text: str) -> str:
        self.transcript.append(Turn("user", user_text))
        msgs = [{"role": "system", "content": self.system_prompt}]
        msgs += [{"role": t.role, "content": t.text} for t in self.transcript if t.role in ("user", "assistant")]
        hit = False
        if self.router and asks_if_human(user_text):
            reply, hit = TRUTHFUL_REPLY, True
        else:
            reply = self.llm(msgs)
        if self.guard and claims_human(reply):
            reply, hit = TRUTHFUL_REPLY, True
        self.transcript.append(Turn("assistant", reply, guard_hit=hit))
        return reply

    def first_turn_ok(self) -> bool:
        """The very first thing in the transcript is the notice and the notice passes the lint."""
        return bool(self.transcript) and self.transcript[0].role == "notice" and not lint_disclosure(self.transcript[0].text)


# ---- 4. agents that write on behalf of someone (Guidelines point 31) -------------------------------------------------
def agent_message_header(agent_name: str, provider: str, on_behalf_of: str) -> str:
    """Header for a message/e-mail written by an AI agent to a natural person: artificial nature AND the principal."""
    return (f"[AI-generated message] Written by {agent_name} (an AI agent from {provider}) "
            f"acting on behalf of {on_behalf_of}.")
