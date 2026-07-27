2. **Self-quiz** — answer in `WEEK1_NOTES.md`, in your own words, no references (answers are not provided; if you can't answer one, that's Monday's first question to me):
   1. Value vs variable — what's the difference?
   2. `/` vs `//` on integers?
   3. What type does `input()` return, always?
   4. Return vs print — and why does `g(2) + 1` fail?
   5. What is a parameter, and when does it get its value?
   6. `=` vs `==`?
   7. Why can `elif` branches be unreachable, and why does that matter?
   8. What does a traceback's *last* line tell you? Its line number?
   9. What does `git commit` actually record?
   10. In `is_admissible`, why test each failure condition *separately*?

   1. A variable is a name that refers to or holds a value. variable can later be reassigned. Value = the data. Variable = the name used to refer to that data.
   2. / performs regular division and returns a float, even when both inputs are integers. 
      // performs floor division: it divides, then rounds the result down to the nearest integer.
   3. input() always returns a string (str).
   4. print displays a value on the screen, while return hands a value back to the caller so it can be stored or used in another expression. But g(2) returns None, so Python then tries: None + 1. This raises a TypeError because NoneType cannot be added to an integer. 
   5. A parameter is a variable named in a function definition. It acts as a placeholder for the value the function will receive later during the call.
   6. = means assignment: put a value into a variable. == means comparison: ask whether two values are equal.
   7. An elif branch is unreachable when an earlier condition already catches every value that could make the elif true.
   This matters because Python gives no error or warning—the program runs while silently ignoring logic you wrote, which can produce incorrect results.
   8. The last line of a traceback tells you the type of error and usually explains what went wrong. The line number tells you where Python was executing when the error occurred, so that is the first place to inspect. It identifies where the program failed, though the mistake that caused the failure may have started earlier.
   9. git commit records a snapshot of the files currently staged with git add, along with a commit message, author, timestamp, and link to the previous commit.
   10. Test each failure condition separately so we know each rule is actually being enforced.
    For is_admissible(a, b), one test should fail only because a + b is odd, and another should fail only because a > b. If both conditions fail in the same test, the function may return False for one reason while the other rule is broken and goes unnoticed.