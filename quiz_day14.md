## Day 14 Quiz

1. You have helpers.py and a separate use_helpers.py in the same folder. Write the two lines in use_helpers.py that import the module and call count_degrees on [(0,1),(2,3)], printing the result. What must come before the function name, and why?
2. Why does the print live in use_helpers.py (the script) and not inside helpers.py (the module)? What would go wrong if helpers.py had a top-level print?
3. The stale-import trap: you import helpers at >>>, edit a function in helpers.py, save, then call it again in the same session — and see the old behavior. One sentence: why? And what's the fix?
4. Interpreter vs script file — give one thing a script gives you that typing into >>> cannot. (Any one of the three we discussed.)
5. You edit helpers.py and a fresh import helpers fails with IndentationError — does any function in the module load, or none? Why? (Think about what import has to do before it can give you the functions.)
6. Predict the four printed lines from running this script:
import helpers
print(helpers.abs_diffs([4, 4, 9]))
print(helpers.count_degrees([(0,1),(0,1)]))
print(helpers.find_over_capacity({0: 5}, {0: 5}))
print(helpers.is_admissible(3, 5))

Take it, paste your answers, I'll mark it.
---------------------------------------------------------------------------------------------------------------

1. 
import helpers
print(helpers.count_degrees([(0, 1), (2, 3)]))

We must write helpers. before count_degrees because you imported the module, not the function directly. helpers.count_degrees means “use the count_degrees function that lives inside the helpers module.”

2. 
The print belongs in use_helpers.py because helpers.py should only define reusable functions and return results; the script decides when to display them.

If helpers.py had a top-level print, it would run automatically as soon as another file did:

import helpers

So simply importing the module would unexpectedly print something, which is an unwanted side effect.

## Note to self: “Top level” means code that sits directly in the file, not indented inside a function, loop, if, class, etc.

3. 
No—the current session keeps using the version of helpers it already loaded into memory, even though you changed the file on disk. Fix it by exiting the REPL with exit(), starting a fresh python3 session, and importing helpers again.

4. 
A script file gives you saved, repeatable code: you can run the same program again later without retyping every command at >>>.

5. 
None of the functions load. Python must first parse (python reads the code and checks that its structure and syntax make sense before it can run it)the entire helpers.py file successfully before it can create the module and give you its functions; an IndentationError prevents the import from completing at all.

6. 
[0, 5]
{0: 2, 1: 2}
[]
True

-----------------------------------------------------------------------------------------------------------

6/6 — clean, and again every answer carries the why, which is what actually matters. Marking:

1. Correct. helpers.count_degrees explained precisely — "use the function that lives inside the helpers module." You've got dot-access cold. ✓

2. Correct, and your note-to-self defining "top level" (directly in the file, not indented inside a function/loop/class) is exactly right and worth having written down — that's the concept that makes the whole module/script separation click. ✓✓

3. Correct — old version stays in memory, disk change doesn't touch it, restart reloads. ✓

4. Correct — saved, repeatable, no retyping. ✓

5. This is the standout. "Python must first parse the entire file successfully before it can create the module" — that's the precise mechanism, and it's why one bad line kills the whole import, not just the broken function. You reasoned from "what does import have to do" to the right answer. That's understanding the machinery, not memorizing a rule. ✓✓

6. All four correct:

abs_diffs([4, 4, 9]) → [0, 5] ✓ (|4−4|=0, |9−4|=5)
count_degrees([(0,1),(0,1)]) → {0: 2, 1: 2} ✓ (double edge, each endpoint twice)
find_over_capacity({0: 5}, {0: 5}) → [] ✓ (5 > 5 is False, strict boundary)
is_admissible(3, 5) → True ✓ (sum 8 even, 3 ≤ 5)