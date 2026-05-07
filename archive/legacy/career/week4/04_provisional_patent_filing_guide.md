# 🪪 Provisional Patent Filing Guide — Decision + How-To

> One file. Three paths. Decide, then execute.

---

## 🎯 Big-picture decision tree

```
                    Did CSUEB Tech Transfer accept?
                            ┌─────┐
                            │     │
                            ▼     ▼
                          YES    NO / NO REPLY
                            │     │
                            ▼     ▼
              They file       You decide:
              everything.       │
              You do nothing.   ├──> Self-file provisional ($75)
              GO TO §A          │       GO TO §B
                                │
                                └──> Drop the patent angle
                                        GO TO §C
```

Make the call by **Friday May 30**. Don't carry the indecision into Week 5.

---

## §A — CSUEB Tech Transfer accepted (best case)

Congratulations. Almost zero work for you.

### What they do
- File the provisional patent (USPTO) on the university's behalf
- Cover the filing fee (typically $75-$300)
- Negotiate inventor terms in writing — usually some royalty share to you
- Handle the **12-month conversion to non-provisional** if the work warrants it
- Manage prior-art search, claim drafting, prosecution

### What you do
1. Sign the **Inventor Assignment** they send you
2. Provide any technical clarifications they ask for
3. Continue publishing — but check with them before any *new* technical disclosure (some claims need to be filed before public disclosure)
4. **Update LinkedIn:**

   ```
   Quick milestone: working with Cal State East Bay's Office of
   Technology Transfer on a provisional patent application
   covering the SHAP-conditioned RAG architecture inside AttriSense.

   Filing in progress — open source code stays MIT.

   Grateful to [Faculty / Tech Transfer contact] for the support.
   ```

### LinkedIn signal value
Substantial. "Patent pending via [University] Tech Transfer" reads as both *technical novelty* and *institutional validation*. Recruiters notice.

---

## §B — Self-file provisional via USPTO ($75 path)

CSUEB passed (or didn't reply). You still want patent protection. The DIY route is real and reasonable.

### What a provisional patent gives you
- A 12-month placeholder priority date
- The legal right to say "**Patent Pending**" on every artifact
- Time to convert to a non-provisional (full) patent or let it lapse
- Cost: **$75** for a *micro-entity* (which you qualify for as a student)

### What it does NOT give you
- ❌ Any enforceable right by itself — only a non-provisional grants enforcement
- ❌ A guarantee of issuance — that comes from the eventual examination
- ❌ Free conversion — non-provisional in 12 months is ~$5K-$15K with attorney

### Step-by-step (~3 hours, one Saturday)

#### 1. Determine you qualify as a micro-entity
- ✅ Income < ~$200K (yes)
- ✅ Filed fewer than 4 prior US applications (yes)
- ✅ Not assigned to a large entity (yes — CSUEB passed)

#### 2. Write a "specification" (~2 hours)

A provisional doesn't require formal claims. It just needs an "enabling disclosure" — a technical write-up complete enough that someone skilled in the art could reproduce the invention.

You **already have this**. It's your IEEE paper.

Format the provisional as:

```
TITLE: A Multi-Modal Framework for Employee Flight-Risk Prediction
       Combining SHAP-Conditioned Retrieval and Verified Natural-
       Language SQL Querying

INVENTOR(S): Sharada Dogiparthi

FIELD OF INVENTION
[1 paragraph — applied ML for HR analytics]

BACKGROUND
[2-3 paragraphs — same as paper Section II]

SUMMARY OF INVENTION
[1 page — describe the 3 layers + the novel SHAP→RAG conditioning
loop. This is the heart of what's patentable.]

DETAILED DESCRIPTION
[5-15 pages — paste in the relevant paper sections, expanded with
implementation specifics. Include the architecture diagram.]

EXAMPLES / EMBODIMENTS
[2 pages — 2-3 example workflows showing how a manager would
interact with the system]

DRAWINGS
[Architecture diagram. Workflow diagrams. Screenshots of dashboard.]
```

#### 3. File via USPTO Patent Center

- Go to https://patentcenter.uspto.gov
- Create a free account
- "New Submission" → "Provisional Application for Patent"
- Upload your specification PDF
- Upload drawings as separate PDFs
- Pay the **$75 micro-entity fee**
- You receive a **Provisional Application Number** instantly

That's it. You are now legally allowed to say **"Patent Pending"** on every public artifact.

#### 4. Update everything that mentions the architecture

- README.md — add "🪪 Patent Pending (USPTO Provisional)" at the top
- Paper acknowledgments
- LinkedIn featured section
- Resume — add a "Patents" section

### LinkedIn signal value
Less than university-backed, but still real. The "patent pending" line is a credible technical signal.

```
Quick milestone: just filed a USPTO provisional patent on the
SHAP-conditioned RAG architecture inside AttriSense.

The novel piece — that I haven't seen elsewhere — is using SHAP
attributions as the *retrieval query* for RAG context, not just
as a UI explanation. So the rationale a manager reads is grounded
in what the model actually thinks is driving the score.

Open source stays MIT — patent only covers the architectural
combination. Happy to chat with anyone building similar things.
```

---

## §C — Drop the patent angle

Sometimes the right call is to skip it.

### When this makes sense
- ⚠ Tech Transfer says "this isn't patentable" with reasons
- ⚠ You've already disclosed the architecture publicly without filing first (one-year US grace period applies but international rights may be lost)
- ⚠ Energy budget is full and you'd rather ship the next feature
- ⚠ You're not planning to commercialize — open source forever

### How to drop it gracefully

Don't say anything publicly about why you didn't file. The absence of a patent isn't a story.

If anyone asks why you released as MIT instead of patenting:

> *"The architecture is most useful in the open. Patent would have constrained adoption — and the goal was to put usable HR analytics in front of more practitioners, not fewer."*

That's a positive framing of "I chose not to" — which is its own respectable answer.

---

## 🚦 Decision matrix

| Situation | Path |
|---|---|
| Tech Transfer accepted | §A — sign their forms |
| Tech Transfer declined, you have $75 + a Saturday | §B — self-file |
| Tech Transfer declined, you're exhausted | §C — drop, no shame |
| Tech Transfer ghosted, you self-file anyway | §B — fine |
| You haven't even contacted Tech Transfer | Send the email TODAY (`week1/05_csueb_tech_transfer_email.md`) and decide next week |

---

## ⚠️ Common pitfalls

- **Don't disclose anything new publicly** between now and filing if you're going §A or §B. Existing disclosures are fine (one-year US grace period).
- **Don't promise a patent will issue** — only "patent pending" is honest while pending.
- **Don't oversell** — recruiters know provisionals are placeholders. Calling it "my patent" before issuance is a red flag.
- **Save EVERY receipt** if you self-file. The $75 is tax-deductible as professional development.

---

## 💡 The honest framing

A provisional patent at the start of your career is mostly **a story device**, not a money-making asset.

What it does:

1. ✅ Demonstrates you understand IP
2. ✅ Signals technical novelty to non-technical hiring stakeholders
3. ✅ Creates a defensible "we got there first" timestamp
4. ✅ Forces you to articulate what's actually novel — clarifies your own thinking

What it does NOT do:

1. ❌ Make you money (until/unless converted, examined, issued, and licensed — years away)
2. ❌ Stop competitors meaningfully (provisional is unenforceable on its own)
3. ❌ Replace publication (you should still publish)

So treat it as **part of the credibility stack**, not as the prize itself.
