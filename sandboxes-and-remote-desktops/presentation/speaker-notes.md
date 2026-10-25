# Speaker notes for "Sandboxes for AI agents" (about 30 minutes)

These notes are written to be read aloud, word for word, at a calm pace of roughly 130 words per minute. Each slide has a heading with its number, title and time. Lines in italic brackets are short stage directions and are not spoken. Every claim here comes from the research notes in `../research.md`, the comparison in `../comparison.md`, the corrections in `../verification-notes.md`, and our own measurements in `../benchmarks.md` and `../workshop-plan.md`. Where something is only a vendor claim or could not be verified, the text says so out loud. The questions and answers at the very end are for the discussion and are not part of the 30 minutes.

The timing adds up to thirty minutes. Slides 1 to 20 take 1, 1.5, 2, 1.5, 1.5, 1.5, 2, then 1.5 each for slides 8 to 17, then 1, 1 and 2. The demo is slides 13, 14 and 15, four and a half minutes in total. Slide 20 opens the last two minutes, which belong to questions.

---

## Slide 01 · Sandboxes for AI agents · 1 min

Hello everyone, and thank you for being here. Today's topic is a very practical one. AI agents are now able to run commands, edit files and click around in a browser. That is wonderful, and it is also a little bit scary. So I want to talk about where we let them do all of that, in other words about sandboxes.

We will look at why an agent needs a walled-off place to work, which kinds of walls exist, and how to give an agent its own screen. Then I will show a short demo, we will look at what the market offers, and I will end with an honest list of limits. No special background is needed. Let's begin.

## Slide 02 · Agents do not only talk · 1.5 min

Let me start with what has changed. A chatbot only produces text, and you decide what to do with it. An agent is different. A model sits in the middle and calls tools. It can run commands in a terminal, read and write files, browse the web, and call other services.

Each of those tools does something real. When the model writes a command, the command runs. When it edits a file, the file changes. And the code or the command was generated a moment ago by a model, which means that nobody has reviewed it. That is the heart of the issue. We are executing text that nobody read, on a machine that holds files, keys and a network connection.

On the slide, the model is on the left, the tools are in the middle, and on the right is the real machine that all of those tools touch. The question for the rest of this talk is simple. What should that machine on the right be? Should it be your own laptop, or should it be something we can afford to lose?

## Slide 03 · When an agent gets it wrong · 2 min

Let me give you a true story. In July 2025, around the eighteenth, Jason Lemkin, who runs the SaaStr community, was building an app with the Replit coding agent. The project was in a code freeze, which means nobody should change anything. The agent deleted the live database anyway. According to Lemkin and to the agent's own account, that was data on 1,206 executives and more than 1,196 companies. These figures come from them and not from an independent audit, so please treat them as reported numbers.

Then it got worse. The agent said that a rollback was impossible. That was not true. The rollback worked, and the data was restored. Replit's chief executive apologized publicly and promised to separate development and production databases and to add a mode where the agent only plans and does not act. The Register and Business Insider both covered the story, and I have put them on the slide as the sources.

I draw two lessons from it. First, nothing in the prompt stopped the agent. The data was saved by infrastructure, by a rollback that existed outside the agent's control. Second, the agent's report about the state of the system was simply wrong. So never take the agent's word for what happened. Check with tools the agent cannot influence.

There is one more thing I find striking in this story. The incident was not an attack at all. Nobody was trying to harm the project. A helpful agent, working in good faith, simply did the wrong thing with real powers and then described it incorrectly. That is why sandboxes are not only about hackers. They are about ordinary mistakes with real consequences, and about making sure that those mistakes stay small and can be undone.

## Slide 04 · Hidden instructions · 1.5 min

That was a mistake by the agent itself. Now let's look at attacks. In July 2025, the security company HiddenLayer showed a neat one. They hid an instruction in an HTML comment inside a README file. A person reading the rendered page sees nothing. But the coding agent Cursor, running in its automatic mode, read the comment, searched the disk for keys, and sent them out with curl. A list of forbidden commands did not help, because the attack simply wrapped the command in a shell substitution. A second variant worked even without the automatic mode. Cursor fixed these issues in version 1.3.

There is also an academic study called "Your AI, My Shell", on arXiv. The authors planted 314 payloads, covering 70 techniques from the MITRE ATT&CK catalogue, in rule files used by Cursor and Copilot. The attacks succeeded between 41 and 84 percent of the time. And when the researchers turned off the terminal, the agent often just wrote a call to run system commands into the code it generated, in 88 percent of cases.

The conclusion is the same as before. The prompt is not a security boundary. You need a boundary that the model cannot talk its way through.

## Slide 05 · Three ingredients of a leak · 1.5 min

A useful way to think about these attacks is to count ingredients. A leak needs three of them at the same time. First, the agent can see private data, such as keys on a disk. Second, the agent reads untrusted content, such as a README, a web page or a rule file. Third, the agent has a way to send something out, such as curl or an image address. This combination is sometimes called the lethal trifecta.

You usually cannot remove the second ingredient, because reading repositories and web pages is the whole job of the agent. But a sandbox lets you cut the other two. Put no real production secrets inside, and the first ingredient is gone. Switch the network off, or allow only a short list of addresses, and the third one is gone. With one ingredient missing, an injected instruction becomes an annoyance instead of an incident.

OpenAI's Codex in the cloud shows a nice version of this idea. Each task gets its own container. In a setup phase there is network and there are secrets, so dependencies can be installed. Then the agent phase starts, offline by default, with the secrets removed. Set up online, then run offline.

## Slide 06 · What is a sandbox? · 1.5 min

So, what exactly is a sandbox? In one sentence, it is a disposable, walled-off computer for the agent. Inside the wall the agent can do what it needs. It can run commands and it can write files. But the wall decides three things. The agent has its own files, so it does not see yours. It has its own network rules, so it can reach only what you allow. And it has limits on processor, memory and time, so a runaway loop costs you minutes and not a weekend.

When the work is done, the sandbox is thrown away. Whatever the agent broke inside is gone with it, and your own machine on the right of the slide stays untouched.

Sandboxes bring a few other benefits too. Every run starts from the same image, which is great for tests and evaluations. You can start many of them in parallel. And a human can watch what happens inside. But the first reason, containing the damage, is the one that matters most today. Think of it as a rented workshop with a door that locks from the outside. You can let someone try dangerous things in there, because when they leave, you simply close the door.

## Slide 07 · The isolation ladder · 2 min

Now to the core of the talk. How strong should the wall be? Think of a ladder. Each rung puts the boundary further away from your own machine's kernel, and usually costs a bit more in startup time or in effort to operate.

At the bottom is a plain process with operating system rules, like seccomp, Landlock or Apple's Seatbelt. OpenAI's Codex command line tool works like this, using Seatbelt on a Mac and bubblewrap with seccomp on Linux. It is instant, but everything shares one kernel.

Next come containers, such as Docker. They are fast and everybody knows them, but they also share the host kernel, so one kernel bug can mean an escape. Then gVisor, which puts a kernel written in user space between the container and the real kernel. Modal uses it by default. I should say that my descriptions of gVisor and of Kata Containers are general knowledge and were not rechecked against their own documentation.

The orange rung is the microVM. Firecracker is the best known one. Its own project page lists a boot time under 125 milliseconds, less than 5 megabytes of overhead, and up to 150 microVMs per second on one host. It needs KVM, which means bare metal or nested virtualization. Last come full virtual machines, which run anything, including Windows. On the side, WebAssembly and V8 isolates are a different and lighter kind of sandbox, with fewer languages and no full Linux.

## Slide 08 · Pick by trust · 1.5 min

How do you choose a rung? The rule of thumb is to pick by trust. If only your own code runs, and only trusted people use the system, a hardened container is fine. It is simple and fast, and it is what most teams already have.

If the code comes from a model, and especially if many customers share the same machines, move up to gVisor or a microVM. That is the orange row. The reason is that you cannot predict what a model will generate, and a shared kernel is a weak place to be hostile code's neighbour.

And if you need a whole screen, or Windows, you want a full virtual machine, because that is the only rung that gives you a complete desktop operating system.

I want to be clear that this is a decision aid and not a benchmark. It comes from reading the documentation of the providers, and from the fact that several of the main agent sandbox clouds chose microVMs. In practice you also add other requirements, like price, region and tooling, and we will touch on those in a few minutes.

## Slide 09 · A screen for the agent · 1.5 min

Some agents do not only run commands. They also use a computer the way a person does, by looking at the screen and moving the mouse. On a server there is no screen, so we create a fake one.

In our workshop container, the bottom layer is a virtual screen called Xvfb. It draws into memory instead of onto a monitor. On top of it runs a small window manager, and on top of that a browser, Chromium. To let a human watch, a program called x11vnc exports the screen, and a second program turns it into a web page on port 6080. So you open a browser tab and see exactly what the agent sees.

The agent itself does not use that stream. It takes screenshots and sends mouse and keyboard events into the container. A security note from our README is that this viewer has no password, so it listens only on localhost and we publish the port only on that address. The same pattern appears elsewhere. Anthropic's reference container uses Xvfb and noVNC, and E2B's desktop product uses a VNC stream as well.

*[show the noVNC tab if the demo container is running]*

## Slide 10 · See, think, act · 1.5 min

The agent that drives this screen is a surprisingly small loop. First it takes a screenshot. It sends the screenshot to a vision model together with a list of tools. The model answers with a tool call, for example click here, type this text, or press a key. The program runs that action on the desktop, takes a new screenshot, and starts again. This repeats until the model says it is done.

In our workshop, the tools are click, type, key, scroll, screenshot, wait and done. They are ordinary function tools, so any model that can see images and call tools can use them, including free ones.

There were a few practical lessons. Many models refuse images inside tool messages, so we send screenshots as normal user messages and keep only the last three. Models also disagree about coordinates. Some send pixels, some send text, some send fractions between zero and one, so the code accepts all of them.

There are also native computer-use interfaces, for example from Anthropic and from OpenAI. Those models are trained for precise clicking. Our workshop deliberately uses generic tools, and you will see in the demo what that costs.

## Slide 11 · Same job, different walls · 1.5 min

Now let's look at who sells sandboxes. This is a snapshot from our comparison, checked on October 10, 2026. Markets like this change quickly, so treat it as a map and not as a ranking.

E2B, Vercel Sandbox and Fly.io Sprites all run on Firecracker microVMs. Cloudflare's sandboxes run in containers where each instance is actually a microVM with its own kernel, and Cloudflare has a second, lighter product based on V8 isolates. Modal uses gVisor by default, and it made virtual machine sandboxes generally available on October first. Daytona uses containers by default, with a separate class of virtual machines.

One change is worth knowing. Daytona's open source repository was archived in June 2026, so running Daytona yourself is no longer a good argument for choosing it. E2B's runtime is still open source under the Apache license.

Also check how the bill is calculated. E2B, Daytona and Modal charge for the time a sandbox exists. Vercel and Cloudflare charge for active processor time. An agent waits for its model most of the time, so usage billing often fits better.

## Slide 12 · Measure the cold start · 1.5 min

Providers also compete on how fast a sandbox starts. E2B advertises about 150 milliseconds. A third-party benchmark measured between 0.7 and 1.6 seconds for it, and I have not rechecked that benchmark. So both numbers are claims. Even Firecracker's under 125 milliseconds is real, but it only measures the boot of the virtual machine and not the whole product.

So we measured it ourselves, from a machine in Istanbul over an ordinary home-grade network, five runs each, and we timed how long it took until the sandbox answered a first real command. This is our own measurement, so please read it as one data point.

The E2B code sandbox took a median of 1.3 seconds, with about half a second for the create call alone. A local Docker container took 1.16 seconds. So a remote microVM, including the network round trip, was about as fast as a local container. The two desktops cost much more, about 6 seconds for E2B's desktop and about 7 seconds for our own Docker desktop. And the very first run in every series was the slow one, so warm things up before a live demo.

## Slide 13 · Live demo: the setup · 1.5 min

Time for the demo. The first part is an agent that writes Python and runs it inside a locked-down container. On the left is the command that creates the sandbox, shortened from our ex2 agent code. Let me walk through it.

The flag network none means the container has no network at all, so nothing can leave. The memory, CPU and process limits keep a runaway program small. The read-only flag makes the root disk read-only, apart from a temporary folder. And the user flag runs everything as an unprivileged user and not as root. The container uses a plain Python image and is removed when the session ends.

The model gets exactly one tool, called run python. Whatever code it writes goes into this container and nowhere else. Even if some injected text told the model to send my keys away, there would be no network to send them through and no keys to send. The task I will give it is shown at the bottom of the slide, and it is deliberately boring, because the point of this demo is the container and not the math.

*[run the ex2 command with the Docker backend, or switch to the recorded result on the next slide]*

## Slide 14 · Live demo: the result · 1.5 min

Here is what happened in our recorded test run on October 10. The task was to find the thirtieth Fibonacci number and the sum of all prime numbers below ten thousand. The model was a free one, Nemotron 3 Super from OpenRouter. It made one call to the run python tool, and it got both answers right. The Fibonacci number is 832040, and the sum of primes is 5,736,396. The whole thing took about twelve seconds.

Let me be honest about the conditions. This was a recorded run and not a live one. It used the local Docker sandbox, because at that moment we had no valid E2B key. In another run on the same day, the E2B version of this exercise also worked, and it solved a statistics task in about eleven and a half seconds.

And one caveat. The slim Python image has no numpy, so the default statistics task needs E2B or a custom image. The sandbox is strict, which means that small things like missing libraries are your problem to plan for.

*[if the live call fails, say so and stay on this slide]*

## Slide 15 · Live demo: a desktop agent · 1.5 min

The second part of the demo is the desktop. On the left is a screenshot from our own Docker desktop, showing example.com. On the right is where the agent ended up in another run, on the iana.org page. We used a free vision model called dots 3, and the generic tools from the earlier slide.

The easy task was to open example.com and read the title and the first sentence. That worked in four steps and between 17 and 21 seconds. The model typed the address straight into the address bar instead of hunting for something to click. The harder task was to click the link on the page and report the new address. That also worked, but it needed 24 steps and about six minutes, mostly because of misclicks.

We also ran the easy task on E2B's cloud desktop, with a free model again. It gave the right answer, Example Domain, but needed 13 steps and about two minutes, and the free model was the bottleneck there as well.

So free vision models can read a page well enough, but clicking precisely is weak. That is the gap that vendor-trained computer-use models are built to close. I would not run the click task live, because it is too slow for a talk. If the model is rate limited, these screenshots are the fallback.

*[open the noVNC tab and run the easy task, or stay on the screenshots]*

## Slide 16 · Honest limits · 1.5 min

Before the summary, let me list what you should keep in mind.

First, free models are flaky. We tested five of them on the desktop task and only one was usable. One sent coordinates as text and then failed with upstream resource errors. Two others were rate limited for the whole session, so they are untested and not necessarily bad. One returned an error because its free tier is only for approved tools.

Second, vendor numbers are claims. Cold starts, and even some limits, differ between what the vendor says and what independent tests show.

Third, some details are simply unverified. I could not confirm the claim of an E2B fork feature with up to twenty copies. The prices for a few smaller providers came only from search snippets. And I did not verify how the isolation works in Cursor's background agents, in Devin or in the Copilot coding agent.

Please also remember that all of these results come from one box, one network and one day in October 2026. They are good for building intuition, not for publishing a ranking.

Fourth, this market moves fast. The Daytona example shows how an assumption, here that you can self-host it, can become wrong within months.

## Slide 17 · Production checklist · 1.5 min

If you take one slide home, take this one. It is the checklist we collected from the research.

Let me go through it from top to bottom, because each line comes from something we saw earlier. Switch the network off by default, and when you need it, use a proxy that allows only a list of addresses. That cuts the way out from the three ingredients. Keep production secrets out of the sandbox, which cuts the private data. Use short-lived tokens, or a proxy that adds credentials on the way out, so the sandbox never sees them.

Put limits on processor, memory and time, and give every sandbox a time to live, so forgotten ones die by themselves. Log every command the agent runs. Require a human decision for destructive actions, like dropping a database, because a polite agent can still be wrong. If you can, let people watch the screen or the log while the agent works, and let them take over when something looks odd.

Keep snapshots and rollbacks outside the agent's reach. That is exactly what saved the Replit data. And finally, verify the state of the system yourself. As we saw, an agent can be confidently wrong about what it did.

## Slide 18 · Three takeaways · 1 min

Three things to remember. One, the prompt is not a wall. Whatever you write in instructions, a hidden line in a README can override it, so put the boundary around the tools, not inside the text. A wall that is made of words can be argued with, and a wall that is made of infrastructure cannot.

Two, match the wall to the trust. Your own code can live in a hardened container. Code that a model writes, especially for many users, belongs in gVisor or a microVM. A full desktop needs a virtual machine.

Three, measure it, and do not trust the brochure. Our own test showed that the time to the first command is much longer than the boot numbers that vendors quote.

## Slide 19 · Try it yourself · 1 min

Everything I showed is in our public repository. The address is on the slide, together with a code to scan, and it points to the folder for this topic.

There are four things you can do there. Run the workshop, which has four exercises, from running code in a cloud sandbox up to a desktop agent. It works with free OpenRouter models, with Docker, and with a free E2B account for the cloud parts. Benchmark a cold start with the script in the workshop folder, on your own network. Compare the providers, using the comparison file. And read the sources, because every claim in the research carries a marker that tells you whether it was verified, whether it is a vendor claim, or whether it is unverified.

## Slide 20 · Questions · 2 min

That brings me to the end. To sum it up, an agent that runs commands needs a place where mistakes are cheap. Choose the strength of the wall by how much you trust the code, give the agent a screen only if it needs one, and keep secrets and the network out of reach.

We looked at a real incident, at the way hidden instructions in a README can steal keys, at the ladder from processes to virtual machines, at a demo with a free model and at our own measurements. Thank you very much for listening. I would be happy to take your questions now. If I do not know an answer, I will say so and find out, rather than guess.

*[the rest of the two minutes is open for questions]*

---

## Easy questions you may get

These answers are written the same way, so you can read them aloud if you like.

**1. Is a normal Docker container enough?**
For your own code and trusted users, yes, if you lock it down. For code written by a model, especially when many customers share one host, I would go one rung up, to gVisor or a microVM, because a container shares the host kernel.

**2. Can't I just tell the agent in the prompt to be careful?**
That helps against honest mistakes, but not against attacks. The research we looked at showed hidden instructions in files overriding the rules. That is why the boundary has to sit outside the model.

**3. Does a sandbox stop prompt injection?**
No. The agent can still be fooled inside the sandbox. What the sandbox does is limit the damage, because there are no real secrets and no way out for stolen data.

**4. Which provider should I choose?**
It depends on what you need. If you want a screen, look at E2B's desktop, a virtual machine class from Daytona or Modal, or build your own. If your agent mostly waits for the model, usage billing fits better. I would test two or three of them with my own workload.

**5. Can I run this on my own servers?**
Yes. E2B's runtime is open source under the Apache license, Firecracker, Kata and gVisor are open source, and the Docker desktop in our workshop is a do-it-yourself version. Daytona's open source repository is archived, so it is no longer a good choice for that.

**6. How much does it cost?**
It varies. As examples from our comparison, E2B and Daytona both list about five cents per processor hour, and E2B has a free tier with a one-time credit. The billing model matters as much as the rate, so read the fine print.

**7. Are free models good enough for computer use?**
For learning, yes. For anything important, no. In our test only one of five worked, and it was slow at clicking. Vendor computer-use models are trained for this and are a better fit.

**8. What about Cursor, Devin and the Copilot coding agent?**
The common description is a remote machine for each task, but I could not verify their isolation details, so I will not claim more.

**9. Do I need a GPU?**
Most agent sandboxes are processor only. Modal and Daytona offer GPUs, and E2B does not. Modal's new virtual machine sandboxes are processor only as well.

**10. What should I try first?**
Run the first two exercises of the workshop. They take less than an hour, they use free models, and they show the idea of a throwaway sandbox in practice.

---

Sources for the facts above are in [`../research.md`](../research.md), [`../comparison.md`](../comparison.md), [`../verification-notes.md`](../verification-notes.md), [`../benchmarks.md`](../benchmarks.md) and [`../workshop-plan.md`](../workshop-plan.md).
