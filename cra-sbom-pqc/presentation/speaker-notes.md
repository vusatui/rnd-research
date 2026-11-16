# Speaker notes: "24 hours to report, ten years to migrate" (EU Cyber Resilience Act, SBOMs and the post-quantum plan), about 35 minutes plus questions

These notes are written to be read aloud, word for word, at a calm pace of roughly 130 words per minute. Each slide has a heading with its number, title and time. Lines in italic brackets are short stage directions and are not spoken. Every number that is called "our measurement" comes from the workshop in this repository, from a fictional sample product on one machine on 16 November 2026, and is a small sample, not a benchmark.

The slides take 1, 1, 1.5, 1.5, 1.5, 2, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 2, 1.5, 1.5, 1.5, 1.5, 1 and 1 minutes, which is thirty-five minutes. Slide 25 is the question round, with ten prepared answers at the end of this file.

---

## Slide 01 · Title · 1 min

Hello everyone, and thank you for being here. Today's talk has a slightly dramatic title, which is twenty-four hours to report, ten years to migrate. The first half of that sentence is a legal deadline that already applies. The second half is a planning horizon that comes from standards bodies, and it is much softer. I want to show you both, side by side, because clients tend to ask for them in one breath. A typical request sounds like this: we need to report vulnerabilities within twenty-four hours, and we need a crypto inventory and a post-quantum plan.

I will keep this practical. We will look at what the European Cyber Resilience Act actually says, what a software bill of materials is and is not, how a scanner finding turns into a reporting decision, and how to start on post-quantum cryptography with an inventory and one measured pilot. Everything I show comes with a source in the repository, and I will tell you when something is a vendor claim, a secondary source, or only a forecast.

## Slide 02 · Read this first · 1 min

Please treat this slide as the most important one. What you will hear is general information, and it is not legal advice. I am an engineer, and this is an engineer's reading of public sources as they stood on the sixteenth of November 2026.

Whether your product is in scope of the regulation, whether your company counts as the manufacturer, what counts as being aware of a vulnerability, and what is enough to comply are legal questions. They are for your counsel and, in the end, for the authorities. Nothing in the workshop is a compliance certificate either. The sample product is fictional and deliberately outdated, the scripts are teaching tools, and the numbers are from one small run. If you take only one thing from this slide, take this one: use the talk to ask better questions of your lawyers and your engineers, not to replace them.

## Slide 03 · Monday, 09:00 · 1.5 min

Let me start with a small story. It is Monday, nine in the morning. A scanner runs over the software bill of materials of a product, and it prints a summary. In our fictional sample product it finds one hundred and fifty-six findings in fifteen packages. Sixteen of them are rated critical and seventy-nine high. That is noise most teams know how to live with.

But one line is different. An old version of the Pillow imaging library, which the product uses to create thumbnails of uploaded photos, carries a vulnerability in the WebP decoder, and the scanner says that this vulnerability is in the catalogue of known exploited vulnerabilities kept by the United States cyber agency. In other words, somebody has already used it against real systems.

Now the questions begin. Who decides whether this is reportable under European law? Who has the access to submit a report? And what is due tomorrow at nine in the morning? If nobody in the room can answer those three questions in a minute, you do not have a reporting process yet, you have a scanner. The rest of the first half of this talk is about turning that scanner line into a calm, rehearsed procedure.

## Slide 04 · The dates · 1.5 min

First, the dates, because they are easy to mix up. The Cyber Resilience Act is Regulation 2024 slash 2847. It entered into force in December 2024, and its main obligations apply from the eleventh of December 2027. That is the date most people have in their calendars.

But Article 71 of the regulation has an exception, and it is the one that matters for this talk. Article 14, the reporting obligations for manufacturers, applies from the eleventh of September 2026. That is already two months ago. In between, in June 2026, the rules on the bodies that assess conformity started to apply, which is why I show them on the slide, but they are not our topic today.

There is one more detail that surprised me when I read the text. Article 69 says that products placed on the market before December 2027 are normally outside the regulation unless they are substantially modified, but paragraph three makes an explicit exception, and says that the Article 14 obligations apply to all products in scope that were placed on the market earlier. So the reporting duty is not a future problem for your next product. It covers the products you already sell, if they are within the scope at all. And that scope question, again, is one for counsel.

## Slide 05 · What triggers a report · 1.5 min

Next, what actually triggers a report. It is not every vulnerability. The regulation names two triggers.

The first is an actively exploited vulnerability that is contained in your product. The definition in Article 3 says that there must be reliable evidence that a malicious actor has exploited it in a system without the permission of the system owner. So a high score in a database is not enough, and neither is a proof of concept on a blog. You need evidence of exploitation.

The second trigger is a severe incident that has an impact on the security of the product. Article 14 says an incident is severe if it negatively affects, or is capable of negatively affecting, the availability, authenticity, integrity or confidentiality of sensitive or important data or functions, or if it has led, or can lead, to malicious code being introduced or executed in the product or in the networks of its users.

I want to be careful about one thing. A listing in the known exploited catalogue is a strong public signal, and many teams will treat it as the practical trigger. But it is not the legal test, and the regulation does not mention that catalogue. Choose your evidence standard in advance, write it down, and have counsel read it. Whether your product is actually affected is the second half of the decision.

## Slide 06 · The clock · 2 min

Now the clock, which gives the talk its title. Once the manufacturer becomes aware of an actively exploited vulnerability, Article 14 asks for three submissions.

The first is an early warning, without undue delay and in any event within twenty-four hours of becoming aware. It is deliberately small. It says that something is happening, and it indicates the member states where the product is available.

The second is a vulnerability notification within seventy-two hours. It carries general information about the product, the general nature of the exploit and the vulnerability, the measures you have taken, the measures users can take, and how sensitive you consider the information to be.

The third is a final report, and here is a detail that people often miss. It is due no later than fourteen days after a corrective or a mitigating measure is available. So the clock for the final report can start before there is a full patch, as soon as you have a workaround that mitigates the problem.

For severe incidents the first two steps are the same, and the final report is due within one month after the seventy-two hour notification. The phrase in the text is without undue delay and in any event within these times, which means that the hours are an outer limit, not a target. Please also notice that the article counts hours, not working hours. A Friday evening awareness is a Saturday evening early warning.

## Slide 07 · One submission · 1.5 min

Who receives all this? Here the regulation is friendlier than many people fear. A manufacturer submits once, through a single reporting platform that ENISA, the European Union Agency for Cybersecurity, operates. The platform has been live since the eleventh of September 2026, and ENISA's page says it was upgraded to version one point three on the fourth of November.

The notification goes to the end point of the national computer security incident response team, the CSIRT, of the country where the manufacturer has its main establishment, and it is simultaneously accessible to ENISA. The main establishment is where the decisions about the cybersecurity of the products are predominantly taken, and there are fallback rules for manufacturers outside the Union, which use the member state of their authorised representative.

The team that first receives your report shares it with the other national teams where your product is available. In exceptional cases, on justified cybersecurity grounds, they may delay that sharing, and a delegated act specifies those grounds, according to the Commission's page. I have only read the page and not the act, so please treat that detail as second-hand.

One more practical point. The platform needs registered accounts and roles. ENISA publishes user guidance and a glossary of the data fields. We did not copy those fields into our workshop, so our drafts follow the legal minimum of the article, and you must map them to the real form before you rely on them.

## Slide 08 · Rehearse it · 1.5 min

So, rehearse it. In the workshop there is a small script that does the deadline arithmetic. You give it the moment of awareness, the current time and, when it exists, the time a mitigating measure became available, and it prints the three deadlines and their state.

On the slide you can see a run in which the team became aware at nine o'clock on Monday, and it is now ten o'clock on Tuesday. The early warning was due at nine, so it is overdue by an hour. The notification is open with just under two days left, and the final report is due on the second of December, fourteen days after a mitigation that we pretend became available on Wednesday afternoon.

The arithmetic has tests, including the unpleasant corner cases, such as a month-end for the incident case, where one month after the thirty-first of January is the end of February in our implementation. A legal reading may differ, which is exactly why I would like your counsel to look at that rule.

But, honestly, the arithmetic is the easy part. The hard part is the first line of the whole process, when you became aware. The text does not define it beyond the phrase itself. So write down who knows what and when, keep the record, and practise a drill with a real scanner finding at least once before the first real event.

## Slide 09 · SBOM: the legal minimum · 1.5 min

Let us move to the software bill of materials, the SBOM. What does the law require? Annex One, part two of the regulation asks manufacturers to identify and document vulnerabilities and components in their products, including by drawing up a software bill of materials in a commonly used and machine-readable format covering at the very least the top-level dependencies of the product.

That is all. The regulation does not name a format, and it does not list fields. The SBOM belongs to the technical documentation, and the market surveillance authority can ask for it with a reasoned request. Giving it to customers is optional, though if you do, the user information has to say where to find it. The Commission may specify format and elements later by an implementing act. I did not find one, and I flag that as unverified.

So where does the practical bar come from? From two guidance documents. The first is a technical guideline from the German BSI, which asks for CycloneDX version one point six or newer, or SPDX three point zero point one, and a long list of fields. It says itself that it is not binding and gives no presumption of conformity. The second is the July 2026 update of the minimum elements from the American CISA, signed by seventeen other agencies including the German and French ones. That is voluntary guidance as well. Both are good checklists, and neither one is the law.

## Slide 10 · Our SBOM scored · 1.5 min

How good is a typical SBOM against those checklists? We generated one with syft, a widely used open-source tool, for our sample product. It found seventy-two components in about a second.

Then we wrote a checker for the fields that can be decided from the file alone. On the German checklist, the components scored forty-six point six percent, and on the American one, forty-seven point nine percent. That is the raw output of a good tool, used as it comes.

Then we enriched the file, but only with facts that we really know. The lock file of the Node part of the product contains an integrity hash and a download address for each package, so we added those. We declared an author for the SBOM and the lifecycle phase, and we stated honestly that the Python part is incomplete, because it lists only the direct pins. After that, the German per-component score rose to sixty-seven percent and the American one to seventy point eight.

The slide shows both bars, and the lesson is not that we got to a hundred. The lesson is that part of the gap closes with five minutes of honest work in a pipeline, and part of it can never be closed by a tool, which is the next slide.

## Slide 11 · What no tool can invent · 1.5 min

Three columns are still at zero percent after our enrichment. The creator of each component, a contact for its supplier, and the address of its source code. A scanner reads files. It does not know who wrote a package or whom to call about it. The German guideline wants a contact for each component creator, an email address or at least a web address.

There are only two honest ways to fill those fields. One is to take them from the package registry metadata at build time, with the build tooling that knows the registry, and the other is to maintain them by hand for the components that matter. What you must not do is write invented values into the file so that a checker turns green. We deliberately did not.

There was a second gap, and it was a surprising one. Python's requirements file lists only the packages you pinned. Our SBOM therefore contained five Python packages. When we ran a second scanner, osv-scanner, directly on the same requirements file, it resolved the dependencies of those packages and found three more vulnerable ones, certifi, idna and urllib3, that the SBOM did not contain at all. That is not a scanner bug. It is a coverage statement that your SBOM should make explicitly, and the American guidance even has an element for that, called coverage, and another for explicitly identifying unknown information.

## Slide 12 · Two scanners · 1.5 min

Now to the scanning itself. We used two open-source engines on the same product. Grype read the SBOM and reported one hundred and fifty-six findings in fifteen packages. Osv-scanner read the lock files and reported two hundred and fifteen vulnerabilities in eighteen packages.

Those numbers are not comparable one-to-one, because the tools count aliases differently. The same weakness can have a CVE number and a GitHub advisory number, and one tool counts it once while the other counts twice. When we compared the identifiers, including aliases, everything grype found was also found by osv-scanner, and the extra findings came from the three transitive packages and from alias handling.

There are two lessons here. The first is that you should never quote a vulnerability count without saying which tool, which database and which day, because the databases move daily. We recorded the grype database build date, the fifteenth of November. The second lesson is that the overlap, not the total, is the stable part. Where two independent engines agree on a package, you have a very good reason to look at it first. I will also mention that we did not test commercial scanners or other open-source ones, and I cannot say anything about them.

## Slide 13 · VEX: not affected, in writing · 1.5 min

A hundred and fifty-six findings is a lot of work, and much of it is probably irrelevant for your product. VEX, the vulnerability exploitability exchange, is the way to say so in a structured form. It is a statement that says this vulnerability is not affecting this product, and why.

In the workshop we used a deliberately simple check. For each direct dependency we looked for an import in the first-party source code. Six direct dependencies were declared but never imported, for example a YAML parser and a template engine. For them we generated nineteen OpenVEX statements, and when grype read them, the findings fell from one hundred and fifty-six to one hundred and thirty-seven.

Look at what did not change. The actively exploited finding stays, because the Pillow library is imported by the product. That is the system working as intended.

Now the warning, which is also written in the first line of the script. A VEX statement is a claim by the manufacturer. An import check does not see transitive use, plugins, dynamic loading or configuration-driven code paths. Every statement in our file is marked as a candidate that needs human review. A wrong not-affected statement is worse than no statement, because it can end up in front of an auditor or, in a real incident, next to your name. Keep a sign-off and an expiry date on every claim.

## Slide 14 · Let a model draft the advisory? · 1.5 min

When the exploited finding arrives, you will also have to tell your users. Article 14 asks the manufacturer to inform the impacted users about the vulnerability and about mitigations, where appropriate in a structured, machine-readable form. It is tempting to ask a language model to write that customer advisory from the facts.

We tried it, with a free model on OpenRouter, giving it only the facts the reporting script knows. The component, the identifier, the fixed version, and the mitigation, which is blocking WebP uploads. We asked for ninety words in plain English, using only these facts.

In all four runs, the draft added claims that were not in the facts. Words such as critical, remote code execution, and immediately appeared in the text, although nothing in our input said that. The script now has a small guard that flags risk words in the output that are not in the input, and it flagged them every time.

I do not want to overstate this. It is four runs on one free model, which is a small sample, and a better model with a better prompt might behave differently. But the principle is general. Severity inflation in a document that goes to customers and sits next to a regulatory filing is a real risk. If you use a model, use it for a first draft, keep a guard, and let a human sign the final text.

## Slide 15 · The quantum dates · 1.5 min

Now to the second half of the title, the ten years. There are two sets of dates, and I would like you to keep them apart.

The first set is European. In June 2025, the Member States, supported by the Commission, adopted a coordinated implementation roadmap. It asks all Member States to start their transition by the end of 2026, to move high-risk use cases to post-quantum cryptography as soon as possible and no later than the end of 2030, and to finish as much as practically feasible by 2035. The roadmap also says that quantum-vulnerable public-key mechanisms should not be used stand-alone after the end of 2030 for high-risk use cases, and after 2035 for medium-risk ones. Please note who the addressee is. It is a document for Member States, not a legal obligation of your company.

The second set is American. NIST's report number 8547, final in October 2026, says that quantum-vulnerable public-key cryptography, so RSA, elliptic curves and Diffie-Hellman, will be deprecated after 2030 and disallowed after 2035 in NIST standards. That is a federal standards statement with global influence, but it is not a European law.

And what does the Cyber Resilience Act itself say? It asks for state of the art encryption in Annex One, nothing more specific. That the state of the art will move toward post-quantum cryptography is my inference, not a quotation.

## Slide 16 · Harvest now, decrypt later · 1.5 min

Why does the post-quantum topic have a deadline in the first place, when nobody knows when a powerful enough quantum computer will exist? The answer is on the slide, and the Commission's own page says it: an attacker can record encrypted traffic today and decrypt it later. The Commission page calls such attacks already likely occurring. I quote that as the Commission's statement. We did not measure it and I cannot verify it.

This changes how you prioritise. For key exchange, which protects the confidentiality of data in transit, the damage is done at recording time if the data must stay secret for a long time. So key exchange moves first.

Signatures are a different problem. A forged signature needs the quantum computer at the moment of forgery, not years earlier. So the urgent signature cases are the ones with very long lifetimes, such as the root keys that sign firmware, and devices in the field that you cannot update in time.

And when will such a computer exist? Nobody knows. That date is a forecast, experts disagree, and in our workshop it is deliberately a parameter that you set yourself, not a number we claim. I will show you that on slide eighteen.

## Slide 17 · Find your crypto · 1.5 min

Before you plan, you need an inventory. The industry word is a cryptographic bill of materials, and the CycloneDX format supports it since version one point six, with a component type for cryptographic assets.

Our workshop scanner is intentionally simple, a grep with opinions. It reads source and configuration files for the sample product and finds thirty-two uses of cryptography in five files, grouped into thirteen assets. Eight RSA uses, five Diffie-Hellman key agreements on elliptic curves, two ECDSA signatures, a few X25519 uses, and alongside them an MD5 and a SHA-1 hash, which are broken regardless of quantum computers. The output validates against the CycloneDX schema.

Now be honest about what this method cannot see. It does not see cryptography inside binaries or third-party libraries, hardware security modules, or encryption done by a service somewhere else. A real inventory combines several sources, source code, the dependency list, network probing of live endpoints, certificate stores and key management exports, and, most of all, the people who own each system. A list of algorithms without owners and without data lifetimes is a spreadsheet, not a plan, which leads to the next slide.

## Slide 18 · Rank by lifetime · 2 min

How do you decide what to migrate first? A widely used planning heuristic is called Mosca's inequality. If the time your data must stay secret, plus the time your migration will take, is longer than the time until a cryptographically relevant quantum computer exists, you have already lost the race for that asset. I should say that I cite it as common practice, and we did not check a primary source for it.

In the workshop, every cryptographic finding is joined with a business asset and two numbers that come from the system owners, how many years it must stay secure and how many years it takes to migrate. In our case those numbers are fictional.

The slide shows the result for three assumptions about the arrival of the quantum computer. If you assume eight years, five assets say migrate now. If you assume twelve, four assets do. If you assume fifteen, none does, because the largest sum in our example is exactly fifteen, and the inequality needs the sum to be bigger.

So the ranking depends on a number that nobody knows. That is exactly the point of showing it. Do not hide the assumption in a spreadsheet cell. Say your value out loud, write down why, and look at which assets change their verdict when it moves. The assets that stay on the list in every scenario, long-lived confidentiality and non-updatable signature keys, are the ones to start with.

## Slide 19 · The hybrid handshake · 1.5 min

Now to a pilot that you can run this week. The first thing that is practical is hybrid key exchange in TLS. It combines a classical exchange with ML-KEM, the key encapsulation standard in FIPS 203, so that an attacker has to break both. The IETF has published the TLS hybrid groups as RFC 10024 in August 2026, and OpenSSL 3.5 offers the group called X25519MLKEM768 by default.

We measured this on one machine, with OpenSSL 3.5.7, against local servers, thirty handshakes per configuration. A default client negotiated the hybrid group against a default server for all six certificate types we tried. The first message from the client grew from three hundred and thirty bytes to fifteen hundred and six, about one point two kilobytes. The server's answer grew by about one point one kilobyte. For example, with an elliptic-curve certificate it went from eight hundred and six to eighteen hundred and ninety-five bytes.

What about time? We could not see a difference. Each handshake took about ten and a half milliseconds, and most of that is the start of a process. So this tells you about bytes, not about latency in production. Please do not read it as a performance claim.

## Slide 20 · What breaks in practice · 1.5 min

What goes wrong in practice? We tested the two failures that we expect to bite during a migration.

In the first test a client offered only the hybrid group, and the server knew only the classical X25519. The result was zero successful handshakes out of five. The server answered with a handshake failure alert. In contrast, a default client, which also sends an X25519 key share, falls back and works every time. That is the reason hybrid deployments have been quiet so far, and also the reason a strict policy that says hybrid only can take down a connection to an old server.

In the second test a client offered only pure ML-KEM, or only the hybrid with the P-256 curve. The server was a default OpenSSL 3.5 server. Again zero out of five. The server does not enable those groups unless an administrator lists them. When we listed them explicitly, all of them worked.

What we did not test is as important. Real browsers, load balancers, firewalls that inspect the first message of a handshake, and old libraries that choke on a larger first message. Those are exactly the places where I would expect surprises, and I would measure them in a pilot before changing a policy.

## Slide 21 · Post-quantum signatures are heavy · 1.5 min

Signatures are the heavier half of the story. We created self-signed certificates for six algorithms and measured their sizes. An elliptic-curve P-256 certificate is three hundred and eighty-five bytes. An RSA two thousand and forty-eight bit certificate is seven hundred and eighty-one. The ML-DSA certificates, from the FIPS 204 standard, are three thousand nine hundred and eighty-one bytes at the smallest level, fifty-five hundred at the middle level, and seventy-four hundred and sixty-eight at the highest.

OpenSSL 3.5.7 negotiated TLS 1.3 with all of them, and the server's handshake data grew from about eight hundred bytes to about nine thousand bytes with the middle level. A real chain has more than one certificate, so the overhead can be bigger in practice.

Now the caveats, and there are several. We tested a self-signed certificate on a local server. We did not test public certificate authorities, browsers, or hardware security modules, and I do not make any claim about their support. NIST's other signature standard, FIPS 206, which is based on Falcon and would give smaller signatures, is not published yet according to NIST's own report, so please be careful with any product that says it supports it.

The practical conclusion is modest. Start with signatures where you control both ends, like firmware signing, and plan long-lived roots early, because those take years to replace.

## Slide 22 · Ninety days · 1.5 min

So what would I do in the next ninety days? Five things, in this order, because the order follows the law.

First, rehearse the twenty-four hour drill. Name the people, create the platform accounts, write down your evidence standard, and run one exercise with a real scanner finding. That is the one obligation with a date that has already passed.

Second, produce the SBOM from the build, not from a scan of a repository, check the fields in your pipeline against the German and American lists, and say explicitly what coverage you have.

Third, use two scanners, treat the overlap as your starting list, and write VEX statements only with a named human who signs them and a date when they expire.

Fourth, build the crypto inventory with owners and data lifetimes, and run the ranking with several assumptions about the quantum date.

Fifth, pilot hybrid TLS on one endpoint that you control. Measure the bytes and the failures, keep the classical fallback, and widen the rollout only after that.

None of this needs a big budget. Most of it needs an owner and a calendar. The repository contains a comparison guide that explains the tools and the trade-offs behind each step.

## Slide 23 · Honest limits · 1 min

Let me be explicit about the limits, because I would like you to trust what I showed.

This is not legal advice. Questions of scope, roles, awareness and evidence belong to counsel. The product is fictional and deliberately outdated, and the vulnerability counts will be different tomorrow, because the databases change daily.

Several things are open. We did not read the platform's form fields, the Commission guidance in full, or the delegated act on delaying dissemination. We did not verify whether harmonised standards have been cited in the Official Journal. A tracker says none yet, which is a secondary source. We did not research how the Commission's Digital Omnibus proposals might change reporting duties.

And a few things are not tested at all, namely browsers, certificate authorities, hardware modules, binary scanning, and commercial tools. Where we cite vendors or press, we say so in the research file with a marker. Please read that file before you quote anything from this talk.

## Slide 24 · Try it yourself · 1 min

Everything from today is in a public repository, which is vusatui slash rnd-research, in the folder called cra-sbom-pqc. You can scan the QR code on the slide.

The workshop has five labs, and each takes about twenty-five minutes. You can score an SBOM and see which fields are missing, scan and write a VEX statement, run the reporting clock and the drafts, rank cryptography by lifetime, and negotiate a hybrid post-quantum handshake with OpenSSL. There is a participant guide that was checked from a clean copy of the repository, and the free-model step is optional and uses only free models.

My invitation is simple. Take the sample product, break it, and then point the same scripts at something you own, even a small internal service. If you find something that is wrong in my reading, please tell me. The research file has a section with open items, and I would prefer to correct them than to repeat them.

## Slide 25 · Questions · Q&A, about 8 min

*[pause, then take questions; the prepared answers below are spoken, in case nobody asks]*

**Q1. Do we have to report every vulnerability within twenty-four hours?**

No. Reporting is triggered by an actively exploited vulnerability, meaning reliable evidence that someone exploited it without the owner's permission, or by a severe incident. Ordinary vulnerabilities fall under the vulnerability handling duties of Annex One, such as fixing without delay and disclosing fixed ones, but they do not start the twenty-four hour clock. Whether a specific case is actively exploited is a judgement that needs your evidence standard and counsel.

**Q2. When does the twenty-four hours start?**

When the manufacturer becomes aware. The article does not define that moment any further, so I cannot give you a rule. What you can do is document how and when your team learned about it, and decide in advance who is allowed to declare awareness, so that the moment is a decision and not an accident.

**Q3. Does the CRA require an SBOM to be published?**

No. The SBOM must exist, in a machine-readable and commonly used format, with at least the top-level dependencies, and it is part of the technical documentation that the authority can request. Giving it to customers is a manufacturer's choice, and if you do, the user information has to say where it can be found.

**Q4. Which SBOM format should we choose?**

If you want to follow the German guideline, CycloneDX version one point six or newer, or SPDX three point zero point one or newer. In our run, the tool we used produced CycloneDX one point seven by default, and SPDX two point three, which the German guideline no longer accepts. CycloneDX also carries cryptographic assets and vulnerability statements. That is a practical reason, not a legal one.

**Q5. Is VEX mandatory?**

The Cyber Resilience Act does not mention it, as far as we read. It is a practical tool for managing noise and for communicating with customers. The German guideline says an SBOM must not contain vulnerability data, so VEX is a separate document, which is another good reason to use it.

**Q6. Does the CRA force us to adopt post-quantum cryptography?**

Not by name. Annex One asks for state of the art protection of confidentiality, and the post-quantum timelines come from NIST and from the European roadmap for Member States. If your product has a long life, though, today's design choices will be judged against tomorrow's state of the art, and that is my inference, not a legal statement.

**Q7. Why hybrid and not pure post-quantum?**

The European roadmap recommends standardised and tested hybrid solutions where feasible and suitable, because a hybrid stays secure if either of the two components holds. NIST's report acknowledges hybrids and says they are typically expected to be temporary. Pure ML-KEM is smaller on the wire, and in our test it worked when we enabled it, but a default server did not accept it. Other national agencies may have different positions, and we did not read them.

**Q8. Is it safe to enable hybrid key exchange on our public endpoints today?**

I cannot answer that for your environment. In our local test it worked with default settings and a classical fallback, and the cost was about one kilobyte per direction. We did not test browsers, middleboxes or old clients. So pilot on one endpoint, watch the failure rate, and keep the fallback.

**Q9. When will a quantum computer break RSA?**

Nobody knows, and I will not give you a date. It is a forecast, and the experts disagree. That is why the workshop treats it as a parameter, and why the planning question is about your data lifetimes and migration time, not about the date.

**Q10. What should I do on Monday?**

Run the drill. Pick one scanner finding, pretend it is actively exploited, and see who can submit the early warning within twenty-four hours, with which account, using which text. Whatever breaks in that exercise is the first item of your backlog.
