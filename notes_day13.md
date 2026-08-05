**What problem does a project-local venv (virtual environmnet) solve that one shared system Python can't?**

The thing it gives you is **isolation**: your project's tools can't be broken by, and can't break, anything on the shared shelf. Different projects keep incompatible tool versions without colliding.

So the one-sentence version: a venv lets each project keep its own tools at its own versions, sealed off so they don't conflict with other projects or the system. That's isolation (and, downstream, reproducibility).
-----------------------------------------------------------------------------------------------------------------------
Now the first command. In the shell tab (foundation %), the standard way to create a venv is 
python3 -m venv <name>. You're going to make one for this week's work. Type exactly:

python3 -m venv .venv

The .venv is the folder name — the leading dot is a convention meaning "tooling folder, keep it out of the way." Nothing will appear to happen — no output — but a .venv/ folder will be created in your project. Run it, then type ls -a and tell me if you see .venv in the list.


Now activate it — this is the step that tells your shell "use the bin, not the shared shelf." On macOS the command is:

source .venv/bin/activate

source runs the activation script inside .venv/bin/. After it runs, watch your prompt: it should change to show (.venv) at the front — that prefix is your visual confirmation the bin is active. Run it and show me the prompt.

Two quick verification checks — this is the "verify sys.executable" step the plan calls for, and it's worth seeing proof the isolation is real, not just a prompt change. In the shell, run:

which python

which asks "which python am I actually using right now?" Predict first: should it point to the system Python, or to somewhere inside your .venv folder? Run it and read the path.

Then a second check:

python -m pip install --upgrade pip

This upgrades pip inside the venv (harmless, standard hygiene — it's the plan's step). Watch that it installs into the .venv path, not a system one.

Run both, show me the output — especially what which python prints.

That path ends in .venv/bin/python — your Python is now the one inside your project's bin, not the system one. The isolation is real, demonstrated, not just a prompt decoration. And the pip upgrade installed into ./.venv/lib/python3.14/site-packages — again, inside the bin. Everything's landing where it should.

The venv is set up and verified. One sentence in notes_day13.md: what did which python prove — where is "your" Python now, and why does that matter? Then commit the venv milestone... but wait — not yet. Here's the important part: you do not want to commit the .venv/ folder itself. It's large, machine-specific, and regenerable — it's exactly the kind of thing .gitignore exists to exclude. So the .gitignore step comes first, then the commit.

Let me set that up. .gitignore is a plain text file listing patterns git should ignore — never track, never commit. Create it in the shell:

code .gitignore

In that file, type these three lines (one per pattern):

.venv/
__pycache__/
.DS_Store

Each line tells git "pretend this doesn't exist." .venv/ (your bin — regenerable, don't track), __pycache__/ (Python's bytecode cache — the stragglers from F2), .DS_Store (macOS folder junk). Save the file, then run git status and watch what happens — the untracked items you've been seeing for two weeks should vanish from the list. Show me.

It worked — look at what git status shows now: only .gitignore and notes_day13.md are untracked. The .venv/, __pycache__/, and .DS_Store are gone from the list — git is now ignoring all three, exactly as intended. Two weeks of .DS_Store/__pycache__ clutter, silenced in three lines. That's a clean working tree for the first time since F2.

Commit the venv setup, the .gitignore, and your note together — this is one logical unit (environment setup):

git add .gitignore notes_day13.md
git commit -m "f3d2: venv setup, gitignore, verified isolation"

Notice you're only adding .gitignore and the notes — the .venv folder isn't staged because git is now ignoring it. That's the whole point: your bin exists on disk and works, but git doesn't track it. Anyone cloning your repo later would recreate their own venv from a requirements.txt (which comes later this week).

Confirm the commit lands, then we move to the actual pure-function work — implementing the four specs you wrote yesterday, now inside this clean environment.
-----------------------------------------------------------------------------------------------------------------------
**The concept:**

a pure function takes inputs, returns an output, and does nothing else — no printing, no mutating anything outside itself, no touching its inputs in place. Same inputs → same output, always. That's what makes it testable: F4's pytest can call it with known inputs and check the return, no setup or cleanup. Your specs were written pure by design.

Start with count_degrees — the one you know coldest. Your spec: input is an edge list of (u, v) tuples, output is a dict vertex→degree, invariant Σdeg = 2·|E|. You wrote this logic in Capstone B; retype it fresh here (no paste), as a proper def with return — no print anywhere, because it returns the dict. That return-not-print choice is exactly what keeps it pure.

Shape: def count_degrees(edges):, the accumulation loop over u, v, then return degree. Write it, and predict what count_degrees([(0,1), (0,1), (1,2)]) returns before we test it.


def count_degrees(edges):
    degree = {}
    for u , v in edges:
        if u not in degree:
            degree[u] = 1
        else:
            degree[u] = degree[u] + 1
        if v not in degree:
            degree[v] = 1
        else:
            degree[v] = degree[v] + 1
    return degree
print(count_degrees([(0,1), (0,1), (1,2)]))            
    

**The function is correct — clean accumulation, both endpoints counted, return not print inside the function. That's a proper pure function. But there's one thing to fix, and it's a purity point, not a logic point.**

## Look at your last two lines: the print(...) call is sitting inside helpers.py. That's the issue. A module is a library — when you later write import helpers from another script, Python runs the whole file to load it, and that stray print would fire on every import, spitting output nobody asked for. A helper module should define functions and nothing else — no top-level calls, no prints. That keeps it pure and quiet: importing it should do nothing visible.

"But then how do I test it?" — that's exactly tomorrow's lesson (import it from a separate script and call it there). For today, to verify it works, test it in the >>> interpreter instead of inside the file:

import helpers
helpers.count_degrees([(0,1), (0,1), (1,2)])

First — your prediction: what should count_degrees([(0,1), (0,1), (1,2)]) return? Walk it: vertex 0 appears in two edges, vertex 1 in three, vertex 2 in one. Write the dict you expect.

Then delete the print line, save, and in >>> run the two lines above. Show me your prediction and the result.


PREDICTION:
{0: 2, 1: 3, 2: 1}

cherinefons@Mac foundation % python3
Python 3.14.6 (v3.14.6:c63aec69bd5, Jun 10 2026, 08:07:54) [Clang 21.0.0 (clang-2100.1.1.101)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import helpers
... helpers.count_degrees([(0,1), (0,1), (1,2)])
... 
{0: 2, 1: 3, 2: 1}

**{0: 2, 1: 3, 2: 1} — matches your prediction exactly. The import worked, the function ran through the module name, and the pure function returned the right dict. First helper, done and verified from an actual import — which is the whole point of it being a module.** 

## What makes count_degrees a pure function — what does it do, and what does it deliberately not do (the reason no print lives inside it)?

*count_degrees is pure because it takes edges, computes a new degree dictionary locally, and returns that result without changing edges or anything outside the function. The same input produces the same output.*

*It deliberately does not print, modify global data, or decide how the result should be displayed. Keeping print() outside means the returned dictionary can be tested, stored, reused, or passed into another function such as find_over_capacity.*
-----------------------------------------------------------------------------------------------------------------------
**Now abs_diffs**

Open helpers.py and add this function below count_degrees. Retype it fresh — don't paste:

def abs_diffs(values):
    diffs = []
    for i in range(1, len(values)):
        diffs.append(abs(values[i] - values[i - 1]))
    return diffs

Index loop from 1 (so i-1 always has a predecessor), abs() for the nonnegative invariant, append into a fresh list, return — no print.

Type it, save. Then predict what abs_diffs([10, 13, 8, 8]) returns — walk it: |13−10|, |8−13|, |8−8|. Show me the function and your prediction.

PREDICTION:
[3, 5, 0]

>>> import helpers
>>> helpers.abs_diffs([10, 13, 8, 8])
[3, 5, 0]
>>> 

## CORRECT

-----------------------------------------------------------------------------------------------------------------------
**Now find_over_capacity**

Add it below abs_diffs in helpers.py. Spec: two dicts in (degrees, capacities), returns the list of vertices whose degree strictly exceeds capacity.

def find_over_capacity(degree, capacity):
    over = []
    for v in degree:
        if degree[v] > capacity[v]:
            over.append(v)
    return over

Loop the vertices in degree, look up both degree[v] and capacity[v], strict >, append the violators, return the list. No print.

Type it, save, restart the interpreter (exit() → python3), then:

import helpers
helpers.find_over_capacity({0: 2, 1: 4, 2: 2}, {0: 3, 1: 3, 2: 2})

Predict first: vertex 0 (2 vs 3), vertex 1 (4 vs 3), vertex 2 (2 vs 2 — strict, so not over). Which vertices come back? Show me your prediction and the result.

PREDICTION:
[1]

CORRECT. Colon fixed, module loads, third pure helper verified. Only vertex 1 (4 > 3) came back; vertex 2 at exactly capacity correctly stayed out (strict >).

>>> import helpers

>>> helpers.find_over_capacity({0: 2, 1: 4, 2: 2}, {0: 3, 1: 3, 2: 2})

[1]

>>> 

returns True when the sum is even (% 2 == 0) AND a <= b, False otherwise. The and combines both conditions into a single bool — which is the invariant (always returns a bool). No if needed; the comparison expression is the boolean.
