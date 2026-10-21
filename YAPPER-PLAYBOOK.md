# The AI Yapper Playbook

> **Living document.** This is the single source of truth for how we script, generate, cut and ship AI yapper ads. Every AI agent (Claude, Grok, OpenClaw, anything else) reads this before writing a yapper script. When we learn something, it goes in here, and the change goes in the [Changelog](#14-changelog).
>
> **Version:** 0.4 · **Last updated:** 2026-10-21 · **Owner:** Shabir Nudrat
> **Origin:** v0.1 is built from the @ladprofit "AI Yapper Playbook" breakdown (fictional £1 perfume subscription, 92 s, 34 cuts, $16 total), plus our own kie.ai Omni chaining work on whiteboard and VSL ads.

---

## Contents

1. [What a yapper is](#1-what-a-yapper-is)
2. [Why it works: the six moves](#2-why-it-works-the-six-moves)
3. [Archetypes](#3-archetypes)
4. [Beat skeletons](#4-beat-skeletons)
5. [Script writing rules](#5-script-writing-rules)
6. [The director sheet](#6-the-director-sheet)
7. [The job file (machine contract)](#7-the-job-file-machine-contract)
8. [The actor](#8-the-actor)
9. [The takes: locked prompt + chaining](#9-the-takes-locked-prompt--chaining)
10. [Edit](#10-edit)
11. [Sound](#11-sound)
12. [QA checklist](#12-qa-checklist) · [12b. The QC agent](#12b-the-qc-agent)
13. [Production notes, costs and known failures](#13-production-notes-costs-and-known-failures)
14. [Changelog](#14-changelog)
- [Appendix A: How to brief an agent](#appendix-a-how-to-brief-an-agent)
- [Appendix B: Full worked example](#appendix-b-full-worked-example)

---

## 1. What a yapper is

A **yapper** is a UGC-style video ad where **one person talks fast into a phone camera about a story they have**, with a jump cut every couple of seconds. It plays like a creator's post, not an ad.

An **AI yapper** is the same thing with an AI-generated actor, generated in chained takes, cut and mixed so it is indistinguishable in feel from a real phone video.

**Fixed traits (every yapper):**

| Trait | Rule |
|---|---|
| Camera | Phone selfie framing. Locked off. Never moves, never zooms. |
| Talent | One person, talking to the lens. |
| Setting | A real-life place: parked car, kitchen, bathroom mirror, bedroom, walk-in closet, office desk, clinic break room. |
| Pace | Fast. ~3 words per second. Jump cut every 2-3 s. |
| Visual selling | Stickers (review cards, comment replies, price, perks) do the selling on mute. No B-roll over the voice. |
| Length | 45-90 s for the main cut. 15-30 s cutdowns from the same takes. |

**What changes between yappers:** who is talking (archetype), why they are talking (the trigger), where they are, and the product.

---

## 2. Why it works: the six moves

These six moves are what make a yapper read as a post instead of an ad. **Every script must contain all six.** An agent writing a script should be able to point at the line that delivers each one.

1. **The disclosure is the hook.** Lead with who they are and their bias: "Employee has thoughts", "I'm a nurse and I have to say this", "My husband made me film this". Being upfront about the bias makes them more believable, and reads like insider gossip, not a sponsor tag.
2. **A reason to talk that isn't selling.** They are reacting to something: a review, a comment, a DM, something that happened today, a question their mum asked. The viewer is overhearing, not being pitched.
3. **The first proof kills the format's biggest fear.** Identify the #1 fear about this product category, and make the first proof answer it. Subscription → "I couldn't cancel" → a customer who stayed a year and wants to restart. Supplement → "it doesn't do anything" → a specific felt result with a timeframe.
4. **The objection comes from the audience.** A comment sticker asks the top objection, then a switch line ("Okay. Business mode.") flips them into facts: mechanism, reframe, how-to.
5. **The price shows up late, around 55-60% through.** The first half is content a fan would watch for free: taste talk, story, opinions.
6. **A personality beat every ~10 seconds.** A seat shimmy, a joke, a side-eye, a laugh at themselves. The stuff a friend would keep and a brand would cut.

**The close:** close against an anchor. Compare the ask to a bigger decision the viewer was already avoiding. ("Not an £80 bottle you're not sure about. One pound.") Then two-word imperatives ("Go. Try it.") and a human sign-off ("love ya, bye").

---

## 3. Archetypes

Pick one archetype per ad. The archetype decides the hook disclosure, the trigger and the setting.

| ID | Archetype | Disclosure hook | Typical trigger | Typical settings | Notes |
|---|---|---|---|---|---|
| `insider` | Employee / insider | "Employee has thoughts" / "I work here and…" | Reading reviews, a customer email, a launch | Car on lunch break, desk, warehouse | The original format. |
| `customer` | Customer story | "I've been using this for X months" | Someone asked, a before/after moment, a restock | Kitchen, bathroom, bedroom, car | Most flexible. Default for client brands. |
| `skeptic` | Skeptic converted | "I was so sure this was a scam" | Partner bought it, they lost a bet, a friend wouldn't shut up | Couch, car, bed | Objection IS the story. Price can come earlier. |
| `partner` | Partner / family POV | "My husband / mum / roommate…" | Watching someone else change | Kitchen, living room | Third-person proof. Great for sleep, snoring, energy. |
| `reactor` | Reacting to comments / reviews / a viral post | "Someone commented this and I need to respond" | A comment sticker on screen | Anywhere | The comment sticker is the hook. Strong for objection-led angles. |
| `authority` | Expert (doctor, nurse, nutritionist, trainer, pharmacist, coach) | "As a [role], this is the one thing I'd…" | Patient question, myth they see online, a study | Clinic break room, car in scrubs, home office | Highest trust lift. Give them a specific role and setting. |
| `day-in-life` | Routine yapper | "Get ready with me / my night routine" | Doing the routine on camera | Bathroom mirror, vanity, kitchen | Product is used on camera as a silent beat. |

**Choosing:** match the archetype to the angle's core fear. If the fear is "it's a scam" → `skeptic` or `reactor`. If the fear is "it won't work for me" → `customer` or `partner`. If the fear is "is it safe / is it legit" → `authority` or `insider`.

---

## 4. Beat skeletons

Timings assume a ~90 s ad. Scale proportionally for 45-60 s: keep the order, compress the middle.

### 4.1 Master skeleton (from the original `insider` ad)

| When | % | Beat | What it does |
|---|---|---|---|
| 0-4 s | 0-5% | **Status + reason to talk** | Disclosure + trigger. "I'm going through our reviews on my lunch break and I just… I need to talk about this." |
| 4-10 s | 5-11% | **Proof aimed at the core fear** | A real-feeling person's proof on a sticker (review card or comment). Kills the biggest fear first. |
| 10-27 s | 11-30% | **Product/taste talk** | One or two products or benefits, each bridged from something the viewer already knows and loves. One personality beat each. |
| 27-48 s | 30-53% | **Objection + business mode** | Comment sticker with the top objection. "Okay. Business mode." Mechanism, reframe, a how-to. |
| 48-72 s | 53-80% | **"This is exactly why X exists" + offer** | The offer lands here (~58%). One sticker per perk. |
| 72-90 s | 80-100% | **Honesty + anchor close** | "For full transparency, I work here. And I'm still on it." Anchor close, two-word imperatives, sign-off. Terms on screen. |

### 4.2 Archetype variations

Only the beats that change are listed. Everything else follows the master skeleton.

**`customer`**
- 0-4 s: "Okay I've had like 10 people ask me about this so here's the honest answer."
- 4-10 s: Own before-state, specific and slightly embarrassing.
- 72-90 s: "I'm not sponsored, I just…" is **banned** unless true. Use "I'm literally on my third one" instead.

**`skeptic`**
- 0-4 s: "I need to publicly apologise to my [partner/friend]."
- 4-27 s: Why they thought it was a scam. Make it the viewer's exact objection.
- 27-48 s: The moment it flipped. Specific, time-stamped ("day 4, I woke up and…").
- Price can come at 40-50%. The story carries it.

**`partner`**
- 0-4 s: "My husband doesn't know I'm filming this."
- Proof is what they observed in someone else. Their own reaction is the personality.

**`reactor`**
- 0-2 s: Comment sticker is on screen before they speak. First line reads it out or reacts to it.
- The whole ad is the answer to that comment. Business mode can start at 15-20%.

**`authority`**
- 0-4 s: Role + the myth/question. "I'm a nurse and I need to stop you buying the wrong thing."
- 4-27 s: The myth, why it's wrong, in plain words. No jargon soup.
- 27-48 s: Mechanism, the "what I actually tell people" beat.
- Product is introduced as "what I'd look for" → "this is the one that ticks those boxes".

**`day-in-life`**
- Product use is a silent action beat (no line spoken during it).
- Talk over the routine; the routine gives natural cut points.

---

## 5. Script writing rules

These are the rules an agent must follow when writing the words.

### 5.1 Spoken, not written

- Write how people talk: fragments, restarts, "like", "honestly", "okay so". But no more than one filler per take.
- Contractions always. No semicolons. No lists of three adjectives.
- Short sentences. A cut can land after any of them.
- No marketing words: "revolutionary", "game-changer", "elevate", "unlock", "transform".
- Specific > general. "Three weeks" not "a while". "£1" not "cheap". "Woke up at 6:40 without my alarm" not "better sleep".

### 5.2 Pace and length

- **~3 words per second** at fast gossip energy (Omni's measured rate).
- **8 s take = 20-24 words. 10 s take = 25-30 words.** Never go over: the model rushes or truncates. Never go much under: the model pads with filler ("and honestly, that is it").
- A 90 s ad ≈ 9-11 takes ≈ 260-300 words.

### 5.3 Cut marks

- `/` marks a planned jump cut. It is **never spoken**. It goes between phrases where a real creator would cut.
- 3-4 cut marks per 10 s take. One every 2-3 s.
- Never put a cut mark mid-phrase that needs to sound continuous ("one / pound").

### 5.4 Personality beats

- One per ~10 s (so one per take). Physical or verbal: a laugh, a shimmy, a side-eye, a whisper, a "wait, no", a joke at their own expense.
- Write it into the timed beats of the take, not into the words.

### 5.5 Stickers

Stickers are written in the script, not added as an afterthought. Each one is tied to a specific word in a specific take.

| Sticker type | Use for | Rule |
|---|---|---|
| Review card | First proof | Star rating + 1-2 lines + first name + initial. Must be a real review or clearly fictional brand. |
| Comment bubble | The objection | Platform-style comment with @handle. Appears before the switch line. |
| Price | The offer | Appears on the word where the price is spoken. |
| Perk | Each offer element | One sticker per perk, on its word. |
| Hook text | First 2-3 s | The big number or claim. Captions hide under it while it's up. |
| Fine print | Bottom of frame, last ~10 s or full length | Offer terms. |

### 5.6 Hard bans in dialogue

- **No celebrity or real public-figure names.** It gets the take blocked. First name only and carry the joke with a sticker.
- No competitor brand names (use "the £80 one", "the one everyone's using").
- No claims the brand can't legally make (health, earnings, cures). Pull approved claims from the brand brain.
- No "I'm not sponsored" / "this isn't an ad" lines.
- No words in the take prompt that appear as **rendered on-screen text** that could trip the safety filter. Grim or medical words are fine in speech, not as text.

---

## 6. The director sheet

**Write the full director sheet before generating anything.** This is the human-readable version of the script. Each row is one take.

The first version of the original ad used 26 one-line takes. Every one restarted from the same pose with fresh energy and a falling end-of-sentence voice, so every cut felt like a reset. The fix: **~9-10 takes of 8-10 seconds, written as takes, not lines.**

### 6.1 Format

```markdown
# [Ad ID] — [Brand] — [Archetype] — [Angle]

**Actor:** [actor ID]   **Setting:** [setting ID]   **Length target:** [s]
**Core fear:** [the #1 fear this ad kills]
**Anchor:** [the bigger decision we compare the price to]

| Take | Dur | Words (/ = cut) | Timed beats | Props in hand | Starts on | Stickers |
|---|---|---|---|---|---|---|
| t1 | 10 s | Okay, so my last video kind of blew up, / and every comment is asking the same thing. / Is the one pound thing actually real? / Yes. Let me explain. | 0-3 s leans in, palms up · 3-6 s glances down at the comments · 6-10 s finger up, firm nod | none | actor | Hook text "£1?? 🤨" on t1 0-3 s |
| t2 | 10 s | First month is one pound. / You get a travel spray of whatever just landed. / … | 0-3 s finger up · 3-6 s lifts the spray from her lap · 6-10 s counts on fingers | spray (from 3 s) | t1 last frame | Price "£1 first month" on "one pound" |
```

### 6.2 Column rules

- **Words:** 20-30 words, with `/` cut marks (§5).
- **Timed beats:** 3 segments per 10 s take (0-3, 3-6, 6-10). Every pose change lands on a cut mark. Copy mannerisms from the reference video's frames where we have one.
- **Never name an object in a beat unless it's a real prop in `props`.** Omni turns mimes into real objects: "cups hands like holding a book" put a book in his hands for two takes; "mimes scrolling a phone" will produce a phone. Describe only hand shapes and body: "both palms up close together, eyes drooping". `qc.py lint --fix` rewrites offending beats.
- **No hand-to-face gestures** ("rubs eyes"). They melt faces.
- **Props in hand:** track every prop. If she lifts the spray in t2, it's still in her hand at the start of t3, or t3 has a beat where she puts it down.
- **Starts on:** `actor` (the approved actor image) or `tN last frame`. Re-anchor to `actor` every 3-4 takes so the face can't drift.
- **Stickers:** which sticker, on which word.

### 6.3 Silent action beats

A product action (spraying, pouring, applying, lying down on the pillow) is its own **silent take** of 3-5 s between two spoken takes. Mark it in the sheet as `tNs` with `Words: (silent)` and describe the action in timed beats. It still starts from a chained frame or the actor image, never from a separately edited frame.

---

## 7. The job file (machine contract)

The director sheet is for humans. The **job file** is what pipelines execute. Any agent that writes a script outputs **both**: the director sheet (markdown) and the job file (YAML), with identical content.

Location: `jobs/<brand>/<ad-id>/job.yaml`

```yaml
id: VV-INS-001                  # <BRAND>-<ARCHETYPE>-<NNN>
brand: velvet-vial              # brand slug, matches brands/<slug>.md
fictional_brand: true
archetype: insider               # see §3
angle: "Is the £1 thing real?"
core_fear: "I'll get stuck in a subscription"
anchor: "an £80 bottle you're not sure about"
length_target_s: 90
aspect_ratio: "9:16"

model:
  video: gemini-omni-video       # kie.ai default (Omni)
  resolution: 1080p
  take_duration_s: 8             # 8 or 10, see §13
  image: nano-banana-pro         # actor edits

actor:
  id: ACT-007
  source_frame: library/actors/ACT-007/source.jpg     # the real phone frame
  approved_image: library/actors/ACT-007/approved.png
  description: "Brazilian woman, late 20s, messy bun, gold hoops, wired white earphones"

setting:
  id: SET-car-lunch
  prompt: "UGC iPhone selfie footage from the dashboard of a woman in the driver's seat of a parked car on her lunch break, wired white earphones in, daylight through the side window"

energy: "SUPER high energy, fast breathless gossip delivery, rising intonation, little laughs between phrases"

takes:
  - id: t1
    duration_s: 10
    words: "Okay, so my last video kind of blew up, / and every comment is asking the same thing. / Is the one pound thing actually real? / Yes. Let me explain."
    beats:
      - [0, 3, "leans in, palms up"]
      - [3, 6, "glances down at the comments"]
      - [6, 10, "finger up, firm nod"]
    props_start: []
    props_end: []
    starts_on: actor            # actor | t<N>_last
    stickers:
      - {type: hook_text, text: "£1?? 🤨", start_word: "Okay", end_word: "thing."}

  - id: t2s
    duration_s: 4
    silent: true
    beats:
      - [0, 4, "lifts the spray and spritzes her wrist, smells it, eyebrows up"]
    props_start: [spray]
    props_end: [spray]
    starts_on: t1_last

fine_print: "£1 first month, then £14/mo. Cancel anytime."
```

**Validation rules (pipeline enforces):**
- Word count per take within §5.2 limits for its duration.
- Every take that isn't `t1` starts on the previous take's last frame or on `actor`.
- No more than 3 consecutive chained takes before a re-anchor to `actor`.
- `props_start` of take N equals `props_end` of take N-1.
- No banned words (§5.6) in `words`.

---

## 8. The actor

### 8.1 Start from a real phone frame, never a generated face

AI UGC looks plastic when the face was generated from scratch. Video models animate what's in the image, and a perfect image has nothing real to animate. So the actor starts as **one real frame from a real phone video** (the grain, the window light, the car) and gets turned into a **completely different person**.

**Rules:**
1. **One edit, one prompt.** Change the person, the outfit and the details in a single Nano Banana Pro edit. Stacked edits leave seams that show the moment you animate.
2. **A genuinely different person.** Face shape, eyes, nose, skin. Never a lookalike of the source creator or anyone real.
3. **Looking into the lens, lips slightly parted.** Every take starts on this image, so it has to look mid-sentence.
4. **Outlier details.** Tattoos, gold hoops, a messy bun, wired earphones. Wired earphones also explain the clean audio.
5. **Need a change? Redo it from the original frame.** Attach the version you liked as "the target result: match it exactly, only the [X] changes". **Never edit on top of the generated image.**
6. **No quality words.** "Realistic", "pores", "4K", "ultra-detailed" make it waxy. Plain prompt.
7. **Remove all caption text** from the source frame in the same edit.

### 8.2 Actor edit prompt template

```
Change this person so she is now a different [nationality] woman in her [age] with [build]:
[face shape], [eye colour], [nose], [skin], [hair]. [Tattoos / jewellery].
She wears [outfit]. Keep the [wired white earphones], the [car], the [window] and the light.
She looks straight into the phone lens, lips slightly parted. Remove all the caption text.
```

### 8.3 Actor library

Every approved actor gets a folder: `library/actors/ACT-NNN/` with `source.jpg` (the real frame), `approved.png`, `prompt.txt`, and `card.md` (description, which setting, which brands have used them, voice notes). Reuse actors across ads for the same brand so the audience sees a recurring "creator".

---

## 9. The takes: locked prompt + chaining

### 9.1 One locked prompt

Every take uses the same prompt. **Only the beats and the words change between takes.** Change anything else and the voice and energy drift.

```
Static, locked-off shot, no camera movement. [SETTING PROMPT].
[He/She] stays seated, mouth moving naturally, direct eye contact, the camera never moves.
In this take: [TIMED BEATS].
[He/She] says: "[THE TAKE'S WORDS, CUT MARKS REMOVED]"
[He/She] speaks with [FIXED VOICE DESCRIPTION]. [ENERGY LINE].
A very animated face: eyebrows up and down, glances to the window and back.
Both hands gesture at chest height. [His/Her] hands never touch [his/her] face.
One take, no jump cuts. No captions or on-screen text.
```

- Strip `/` cut marks before sending the words.
- Keep one fixed voice description in every take (age, accent, pitch, texture). It holds the voice steady across takes.
- `pipeline/takes.py` builds this prompt from `job.yaml` and prefixes "Use the attached image as the exact opening frame".
- Silent takes: replace the `says:` line with "[He/She] does not speak in this take." and keep everything else.
- Keep "No captions or on-screen text." always. One take in the original burned its own line in as a caption.

### 9.2 Chaining

- **Each take starts on the frame where the last one ended.** No pose reset between cuts.
- Harvest the last frame of take N → upload → pass as the start image for take N+1.
- **Re-anchor to the approved actor image every 3-4 takes** so the face can't drift.
- Generate in order. If you regenerate take N, every chained take after it is invalid until you check the join (or re-anchor at N+1).
- Back up any approved take before regenerating anything downstream.

### 9.3 When a take goes wrong

| Problem | Fix |
|---|---|
| Camera pushes in mid-take | Lock the take back to its start frame in the edit (crop/scale), or regenerate if the drift is big. |
| Model pads with filler at the end | Cut it in the edit. If it's mid-take, the take was too short on words: add 3-5 words and regenerate. |
| Take truncates the line | Too many words. Cut 3-5 words. |
| Face drifts | Re-anchor this take to the actor image. |
| Prop vanishes or changes | Name the prop and its position explicitly in timed beats: "the small black spray bottle is still in her right hand". |
| Line burned in as caption | Regenerate. Check "No captions or on-screen text" is in the prompt. |
| Take blocked | Check for celebrity names, competitor names, or risky words in the dialogue. |
| "Internal Error" | Transient, clusters. Retry the same prompt up to 3x. |

---

## 10. Edit

### 10.1 Picture rules

- **The camera stays still.** No zoom-ins between cuts, no fake handheld shake.
- **Lip sync at all times.** No B-roll over the voice. Product actions are silent beats between lines.
- **Stickers do the selling on mute.** Review card, comment reply, price, each perk, each on its word.
- **Captions in the lower third.** Never over the face. Hide under hook text while it's up.
- **Fine print at the bottom:** offer terms.

### 10.2 Cutting

- **The cuts stay human.** Automated cutting at pauses felt off at the joins in the original build. A human cuts on a blink or a gesture, a few frames before the next word.
- **Workflow:** pipeline lays out the rough cut using word timestamps (Whisper) at each `/` mark, with full handles (±0.5 s) → exports an editable timeline (FCPXML / Premiere XML / CapCut-friendly) → human trims → pipeline renders the final from the trimmed cut.
- Never let a cut land inside a word.

### 10.3 Deliverables per ad

- Main cut (45-90 s), 9:16, with stickers, captions, fine print.
- Clean version (no captions) for platforms that auto-caption.
- 15 s and 30 s cutdowns: hook + proof + offer + close.
- Hook variants: swap t1 only (new first take, same rest). Cheapest test lever.

---

## 11. Sound

The consistency of the voice comes from **cleaning the audio**, not from swapping voices. A voice changer kept lip sync but the original AI voice still won.

Make it sound like **a phone in the setting** (a car, a kitchen):

1. **Strip the AI's background bed.** Each take arrives with its own rumble/ambience 12-20 dB under the voice, different every take. That's what makes the voice feel inconsistent and crackly. Denoise per take.
2. **Match the reference's phone-mic EQ.** Short room/cabin reflections. Never boost the low end (brings the rumble back).
3. **Level-match every take** to the same loudness and tone. Raw takes can be 7 dB apart. Target one integrated loudness across all takes before mixing.
4. **One quiet room tone under the whole ad,** about 35 dB below the voice, unbroken across cuts.
5. Final master: -14 LUFS integrated for Meta/TikTok, true peak ≤ -1 dBTP.

---

## 12. QA checklist

Run on every ad before it ships. The pipeline automates what it can; a human checks the rest.

**Script (before generation)**
- [ ] All six moves present (§2), each pointable to a line
- [ ] Core fear named and killed by the first proof
- [ ] Price lands at 50-60% (40-50% for `skeptic`/`reactor`)
- [ ] One personality beat per take
- [ ] Words per take within §5.2
- [ ] No banned words (§5.6)
- [ ] Claims match the brand's approved claims

**Takes (after generation)**
- [ ] Every take says its full line, and nothing extra (cut filler)
- [ ] Camera doesn't move in any take
- [ ] Props carry across cuts
- [ ] Earphones, outfit, hair, jewellery and light identical in every shot, silent beats included
- [ ] No captions or text burned into the video
- [ ] Face consistent across all takes

**Edit + sound**
- [ ] No cut lands inside a word
- [ ] No take louder, brighter or thinner than the rest
- [ ] Background well under the voice, no rumble or crackle
- [ ] Stickers on the right words, captions never over the face
- [ ] Fine print on screen

---

## 12b. The QC agent

The checklist above is what a human catches by eye. The QC agent does it automatically and fixes what it finds. It runs as `python3 pipeline/qc.py <job_dir> fix` and loops:

```
lint (free) → Gemini reviews every take → regenerate bad takes → re-cut with matched cuts → Gemini reviews the finished ad → QC-REPORT.md
```

**1. Lint, before any credits are spent.** Flags beats that name objects (Omni will materialise them), hand-to-face gestures, and word counts outside §5.2. `--fix` rewrites the beats with Gemini Flash into prop-free hand shapes.

**2. Take review (Gemini 3.1 Pro watches and listens).** Each take is sent with the approved actor image and a reference voice clip. Gemini returns timestamped issues in these categories: `prop`, `identity`, `outfit`, `hands`, `camera`, `text`, `voice`, `lipsync`, `delivery`, `continuity`, plus a 1-5 voice match and identity match. **Only issues inside the frames the edit actually uses count** (from the EDL), so junk in a trimmed tail costs nothing.

**3. Regenerate.** A take is redone when it has a high-severity issue in used frames, or a voice/identity score ≤ 2. The fix depends on the category:

| Category | Fix |
|---|---|
| prop | Beats rewritten prop-free + "hands completely empty". If the prop is already in the opening frame (inherited from the chain), restart from the actor image. |
| identity / outfit / voice | Restart from the actor image (drift came down the chain). |
| hands / camera / text | Same start frame + a fixed end-state line ("hands stay below the chin…", "the phone never moves…"). |
| delivery / lipsync / continuity | Same prompt, new roll. |

Max 2 attempts per take, max 8 regenerations per run (`--max-regens`). Rejected takes are kept in `takes/_rejected/`. Takes are fixed in order, so a fixed take re-seeds the next chained take.

**4. Matched cuts (in `cut.py`, every render).**
- A pause shorter than 0.45 s is **kept, not cut**. Tiny jump cuts read as glitches.
- At every real cut, the cutter searches up to 0.3 s on each side (never into a word) for the out-frame and in-frame whose pose matches best (hands/torso weighted), so hands don't teleport. Each join's cost is written to the EDL (`join_cost`).

**5. Final review.** Gemini watches the finished ad and lists jarring moments (teleporting cuts, audio jumps, captions over the face, wrong caption words) mapped back to takes. Anything still open goes in `qc/QC-REPORT.md` for a human.

**Calibration notes:** Gemini scores a take 3/5 on voice even against its own audio, so treat voice/identity scores as outlier detectors (≤ 2), not truth. Prop and glitch detection is reliable: it caught the book in both takes with correct timestamps.

## 13. Production notes, costs and known failures

### 13.1 Default stack

| Step | Default | Notes |
|---|---|---|
| Actor image | Nano Banana Pro (kie.ai or Gemini) | One edit from the real frame. |
| Takes | **kie.ai `gemini-omni-video` (Omni)**, 9:16, 1080p | `createTask` → poll `recordInfo`. Start image via `image_urls`. Our verified setting is `duration: "8"`; test 10 s before relying on it. |
| Transcription | mlx-whisper large-v3-turbo | Word timestamps for cut marks and the script-vs-transcript check. |
| Audio | ffmpeg (afftdn / arnndn, EQ, loudnorm) | Per-take clean, then level match. |
| Edit | Rough cut auto → human trim → auto render | FCPXML handoff. |
| Fallbacks | Google Flow (Veo), Higgsfield | Flow: ~45 credits for a 30 s / 3-take pilot (~$0.90 on Pro). |

### 13.2 Cost benchmarks

- Original ad: **$16** for a 92 s ad, all in, including every rejected attempt (Omni on kie at 1080p, actor images, test voices).
- Our Omni runs: ~105-250 kie credits per 8 s clip.
- IM8 driveway-dad pilot (2026-10-21): 18 × 8 s takes, 1080p, zero failures, ~3,700 kie credits all in. All 18 said their line; 2 needed an `edit_words` fix. Wall-clock ~45 min with 5 chains in parallel.
- Rough cut: ~2 min once takes exist.

### 13.3 Known failures (add to this list every time)

| Failure | Cause | Fix |
|---|---|---|
| Take blocked | Celebrity name in dialogue | First name only, joke on a sticker |
| Earphones lost in a silent beat | Silent shot generated from a separately edited frame | Every shot starts from the same actor image or a chained frame |
| Line burned in as caption | Prompt didn't forbid text | "No captions or on-screen text." in every prompt |
| Voice inconsistent / crackly | Different AI ambience per take | Strip bed, level-match, one room tone (§11) |
| Voice changer didn't help | Consistency comes from audio cleanup | Don't bother swapping voices |
| Every cut feels like a reset | One-line takes, each restarting pose and energy | 8-10 s takes, chained |
| Filler at end of take | Too few words for the duration | 3 words/s, cut filler in edit |
| Word silently dropped or garbled | Omni safety filter on **rendered text** (e.g. "blood") | Keep risky words in speech only; never ask for them as on-screen text |
| "Internal Error" | Transient | Retry same prompt up to 3x |
| Omni reorders or garbles a phrase (e.g. "the next night, etrial night") | Model drift inside a take | Don't regenerate a chained take for this: set `edit_words` on the take to what was actually said that you keep; the cutter drops the rest |
| Omni adds a few words mid-take ("I just had to prove her wrong") | Model improv | Keep it if it reads naturally: add it to `edit_words` |
| Long caption chunk runs off screen | One long word group | `cut.py` shrinks the caption font to fit |
| Sticker covers the face | Card placed in the upper third | Badges at `pos: top` (above the head); product cards at chest height with `hide_captions: true` |
| Regenerating a chain's tail broke good takes | Downstream takes depend on the changed frame | Only rerun when the defect is load-bearing; back up first; re-anchor to actor |

---

## 14. Changelog

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-10-21 | First version. Built from the @ladprofit AI Yapper Playbook + our kie.ai Omni chaining learnings. Archetypes, skeletons, director sheet, job file spec added. |
| 0.4 | 2026-10-21 | QC agent (`qc.py`): lint, Gemini take review, auto-regenerate, matched cuts, final review. Rule: never name objects in beats. |
| 0.3 | 2026-10-21 | First full pilot (18 takes). Added `pipeline/` (kie.py, takes.py, cut.py), a fixed voice line in the locked prompt, `edit_words`, cutdowns in `edit.yaml`, new known failures. |
| 0.2 | 2026-10-21 | Removed the compliance section and AI-disclosure fine print rules. Experimentation use. |

---

## Appendix A: How to brief an agent

Paste this to any agent (Claude, Grok, OpenClaw) along with this file.

```
You are writing an AI yapper ad. Read YAPPER-PLAYBOOK.md fully before writing.

Brand: [brand slug or "fictional: <description>"]
Product + offer: [product, price, offer terms]
Archetype: [insider | customer | skeptic | partner | reactor | authority | day-in-life]
Angle: [the one idea]
Core fear: [the #1 fear this ad kills]
Approved claims / VoC: [paste or link]
Length target: [s]
Take duration: [8 | 10]

Output, in this order:
1. A one-paragraph concept: who, where, why they're talking, the anchor.
2. The six moves (§2): quote the line that delivers each.
3. The director sheet (§6) as a markdown table.
4. The job file (§7) as YAML, identical content.
5. Self-QA: the "Script" section of the §12 checklist, ticked or flagged.
```

**What good output looks like:** every take is within word limits, every `/` sits at a natural breath, every take has 3 timed beats with one personality beat, props and starts_on are tracked, stickers are tied to words, and the fine print carries the offer terms.

---

## Appendix B: Full worked example

Illustrative rebuild of the original ad's structure (fictional brand `velvet-vial`, `insider`, £1 perfume subscription). Not the original transcript. Use it as the reference for tone, density and how the columns are filled.

**Concept:** A brand employee films herself in her parked car on her lunch break, wired earphones in, laptop on her lap. Her last video blew up and everyone asked if the £1 first month is real. She answers, gets distracted gushing about two scents, switches to business mode for the cancel objection, lays out the offer, and closes with "I work here and I'm still on it".

| Take | Dur | Words (/ = cut) | Timed beats | Props | Starts on | Stickers |
|---|---|---|---|---|---|---|
| t1 | 10 s | Okay, so my last video kind of blew up, / and every comment is asking the same thing. / Is the one pound thing actually real? / Yes. Let me explain. | 0-3 leans in, palms up · 3-6 glances down at comments · 6-10 finger up, firm nod | — | actor | Hook "£1 perfume?? 🤨" |
| t2 | 10 s | But first, / someone left this review and I actually screamed. / She's been with us a full year, / cancelled to save money, / and is now begging to come back. | 0-3 hand on chest · 3-6 points down at the review · 6-10 mock-sobs, laughs | — | t1 last | Review card ★★★★★ on "this review" |
| t3 | 10 s | Okay so if you love that warm vanilla thing / from the expensive brand, / our Velvet one is that, / but somehow better. / I wore it to a date. / He asked. | 0-3 eyes closed, sniffs the air · 3-6 counts off on fingers · 6-10 seat shimmy, side-eye | — | t2 last | — |
| t4s | 4 s | (silent) | 0-4 lifts the travel spray from her lap, spritzes wrist, smells it, eyebrows up | spray | t3 last | — |
| t5 | 10 s | And the fresh one? / Clean laundry, / but like, / rich clean laundry. / I'm obsessed. / My desk neighbour thinks I'm unwell. | 0-3 holds spray up · 3-6 waves hand, laughs · 6-10 whispers to camera | spray | actor (re-anchor) | — |
| t6 | 10 s | Anyway. / Someone said "I bet you can't cancel." / Okay. Business mode. / You cancel in two taps. / In the app. / No phone call, no email. | 0-3 puts spray down · 3-6 reads comment, raises eyebrow · 6-10 finger counts, serious face | — (put down at 0-2 s) | t5 last | Comment bubble "@lou.k I bet you can't cancel" |
| t7 | 10 s | Here's how it works. / You pick your scent every month, / or skip a month, / whatever. / And if you hate one, / you swap it. / Done. | 0-3 palms out · 3-6 counts on fingers · 6-10 shrug, smile | — | t6 last | — |
| t8 | 10 s | This is exactly why we did the one pound thing. / First month is one pound. / You get a travel spray / of whatever just landed. / Then it's fourteen a month. | 0-3 points at camera · 3-6 holds up one finger · 6-10 small happy bounce | — | t7 last | Price "£1 first month" · Perk "Travel spray" |
| t9 | 10 s | For full transparency, / I work here. / And I'm still on it. / Not an eighty pound bottle you're not sure about. / One pound. / Go. Try it. / Love ya, bye. | 0-3 hand up, honest face · 3-6 shakes head, smirks · 6-10 waves, reaches to stop recording | — | actor (re-anchor) | Fine print |

**Fine print:** `£1 first month, then £14/mo. Cancel anytime in the app.`
