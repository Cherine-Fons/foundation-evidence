# DAY 23
# warm-up — three from last week, in your own words:

1. Multiplicity-aware degrees: why + e.multiplicity and not +1? What specifically does +1 break?
2. pip freeze > requirements.txt — what does it capture, and why do we regenerate it right after installing a new package (which is exactly what we're about to do)?
3. __str__ vs __repr__ — which one fires on print(obj) versus typing obj bare at >>>, and who's the intended audience for each?


# Answers
1. We use + e.multiplicity because one Edge object can represent several parallel copies of the same edge. Each of those copies contributes to the degree of both endpoints. If I used +1, I would count the Edge object only once instead of counting all the edges it represents, so any edge with multiplicity greater than 1 would make the vertex degrees too small.

2. `pip freeze > requirements.txt` records the packages currently installed in my active virtual environment, including their exact versions, and writes that list into `requirements.txt`. I regenerate it after installing a new package so the file stays synchronized with the environment I am actually using. That way, someone else — or future me on a new machine — can recreate the same setup with the same dependencies instead of guessing what needs to be installed.**

3. 
print(obj) uses __str__. It is meant for human-readable output — concise and pleasant to display.

Typing obj bare at >>> uses __repr__. It is meant for developers/debugging — more complete and precise about what the object actually contains.

Using the Quote example:

print(q)
# AAPL: 150.0/150.2

That is __str__.

But:

>>> q
Quote(ticker='AAPL', bid=150.0, ask=150.2, timestamp='2026-08-08')

That is __repr__.

So the easiest way to remember it is:

__str__ = “How should this look to a person?”
__repr__ = “What is this object exactly?”


# Correction
3/3 — clean across the board.

1. Exactly right, and you named the failure mode precisely: +1 counts the object, not the copies it stands for, so every parallel bundle collapses to one and degrees come out too small. That's the whole reason the solver's instance shape carries multiplicity on the edge.
2. Correct — snapshot of the active venv with pinned versions, regenerated so the file never drifts from reality. Which is why it's step two today, right after the install.
3. Correct, and your mnemonic is the right one. One thing to bank alongside it: __str__ falls back to __repr__ if you don't define it, but never the other way around — so if you only write one, write __repr__.

----------------------------------------------------------------------------------------------------------------
 
# Now the install. First, look at your foundation % prompt and confirm (.venv) is showing — inside the venv, plain pip is the project's pip, and installing into the wrong Python is the one way this goes sideways.

If (.venv) is there, run this at foundation %:

pip install numpy
----------------------------------------------------

Now step two, and predict before you freeze. requirements.txt currently holds the pytest line and its dependencies from Day 20. After this install, pip freeze > requirements.txt will regenerate the whole snapshot.

Predict for me first: how many new lines does numpy add — exactly one, or one plus some dependencies? Commit to an answer before you look.

Then run these at foundation %:

pip freeze > requirements.txt
cat requirements.txt

Tell me your prediction and what cat actually shows.
-----------------------------------------------------
IN SHELL:

(.venv) cherinefons@Mac foundation % pip install numpy
Collecting numpy
  Downloading numpy-2.5.2-cp314-cp314-macosx_14_0_arm64.whl.metadata (6.6 kB)
Downloading numpy-2.5.2-cp314-cp314-macosx_14_0_arm64.whl (5.4 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5.4/5.4 MB 21.5 MB/s  0:00:00
Installing collected packages: numpy
Successfully installed numpy-2.5.2
(.venv) cherinefons@Mac foundation % successfully installed
zsh: command not found: successfully
(.venv) cherinefons@Mac foundation % pip freeze > requirements.txt
(.venv) cherinefons@Mac foundation % cat requirements.txt
iniconfig==2.3.0
numpy==2.5.2
packaging==26.3
pluggy==1.6.0
Pygments==2.20.0
pytest==9.1.1
(.venv) cherinefons@Mac foundation % 
-----------------------------------------------------
# Q
Now the prediction payoff. numpy added exactly one line — just numpy==2.5.2. The other five (iniconfig, packaging, pluggy, Pygments, pytest) were already there from Day 20.

Here's the drill, and it's a real reasoning question, not something you can read off the screen: back on Day 20, installing pytest added five lines — itself plus iniconfig, pluggy, packaging, Pygments. Today, installing numpy added one. Same pip install, wildly different footprint. Why? What's different about what these two packages need to run?
------------------------------------------------------
# A

Because pip install installs not only the package you asked for, but also any runtime dependencies that package declares it needs.

pytest is built on several separate Python packages. To run, it relies on things like pluggy, iniconfig, packaging, and Pygments, so pip had to install those alongside pytest. That is why one request produced five entries in requirements.txt.

numpy is different. The NumPy wheel you installed is essentially self-contained at runtime for your platform: its core functionality comes packaged inside NumPy itself, including compiled numerical code, so it did not require additional Python packages to be installed with it. Therefore:

pip install pytest
→ pytest + its dependencies

pip install numpy
→ numpy only

The important idea is:

The number of packages pip installs depends on the dependency tree of the package, not on the pip install command itself.

Small technical nuance: NumPy does have machinery and dependencies involved if it must be built from source, but because pip installed a ready-made wheel for your system, those are not additional runtime packages showing up in your pip freeze.

Some packages depend on other packages; some are mostly self-contained. Pip installs the whole dependency chain automatically.

That is why the same command can add a very different number of lines to requirements.txt.
----------------------------------------------------------