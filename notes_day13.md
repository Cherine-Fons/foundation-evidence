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