Day 2 is being covered on the same day as Day 1, so today's date is Mon Jul 20th. This morning we covered:
the interpreter, values, types. This afternoon we are covering: Strings, input/output, conversions.
1. "ab" * 3 (my prediction was ab ab ab, but the output was ababab)
2. "7" + "2" (prediction: 7 + 2, output: 72)
3. len(""): counts the number of characters in a string . I did not know what len was so I googled. Output: 0
4. "hello"[0] : This asks Python for the character at index 0, meaning the first character of the string. Python starts counting positions from zero so my prediction on the output is h. Output was actually 'h' and not h.
5. "hello"[-1]: This asks Python for the character at index −1, meaning the last character of the string. Negative indexing counts backward from the end. Prediction: 'l'. Output: 'o'. My mstake was thinking it still started the count from 0 in the reverse direction. 

Conclusion of exercise 1 on what + and * did with strings vs numbers: With numbers, + adds and * multiplies.
With strings, + joins strings and * repeats a string.
So "7" + "2" joins into "72", while "ab" * 3 repeats "ab" three times.










2. f-strings: `f"{sets} x {reps} @ {weight_kg}kg"`. Rebuild Day 1's output with an f-string, formatted to one decimal place.
3. Conversions: `int("12")`, `float("12.5")`, `str(12)`. Deliberately trigger `int("12.5")` and `int("twelve")`; retype both tracebacks into `notes_day2.md` and annotate what each is telling you.
4. `day2_logline.py`: a script using `input()` to ask for exercise name, sets, reps, weight; prints one clean formatted training-log line. (Yes, `input()` returns a string. That is the whole lesson.)
5. Bug hunt — retype these by hand, run, diagnose, fix; one sentence each on the cause:
   - `weight = input("kg? ")` then `print(weight * 2.5)`
   - `print("total: " + 45)`
   - `name = "farmer's carry"` typed with a straight quote inside single quotes: `name = 'farmer's carry'`

**Done when:** you can say precisely what type `input()` returns and what to do about it.