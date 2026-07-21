Day 2 is being covered on the same day as Day 1, so today's date is Mon Jul 20th. This morning we covered:
the interpreter, values, types. This afternoon we are covering: Strings, input/output, conversions.
EXERCISE 1  String warm-up in the interpreter 
1. "ab" * 3 (my prediction was ab ab ab, but the output was ababab)
2. "7" + "2" (prediction: 7 + 2, output: "72")
3. len(""): counts the number of characters in a string . I did not know what len was so I googled. Output: 0
4. "hello"[0] : This asks Python for the character at index 0, meaning the first character of the string. Python starts counting positions from zero so my prediction on the output is h. Output was actually 'h' and not h.
5. "hello"[-1]: This asks Python for the character at index −1, meaning the last character of the string. Negative indexing counts backward from the end. Prediction: 'l'. Output: 'o'. My mstake was thinking it still started the count from 0 in the reverse direction. 

Conclusion of exercise 1 on what + and * did with strings vs numbers: With numbers, + adds and * multiplies.
With strings, + joins strings and * repeats a string.
So "7" + "2" joins into "72", while "ab" * 3 repeats "ab" three times.


EXERCISE 2 f-strings
Def: An f-string builds a string with live values dropped into it
The exercise: rebuild Day 1's volume output as an f-string like f"{sets} x {reps} @ {weight_kg}kg", formatted to one decimal place. The concept to format a number to one decimal inside an f-string, you write {value:.1f} — the :.1f part means "one digit after the decimal."

note on an f-string: stuff inside {} = Python looks it up or computes it; stuff outside {} = printed literally as text.

My input : >>> sets=5
>>> reps=8
>>> weight_kg=20
>>> volume= f"{sets} x {reps} @ {weight_kg:.1f}"
>>> volume
my prediction: 800 but output was :'5 x 8 @ 20.0'

Conclusion: an f-string doesn't compute a total — it builds a piece of text by dropping values into a template.
I was also wrong to place .1f inside the weight_kg since I already assigned this value myself. Therefore, the right value to format up to 1 decimal is the result (volume)

Correction: 
Put the actual computation inside a brace since anything inside {} gets computed. So {sets * reps * weight_kg} inside an f-string would drop the result 800 into my text. And {sets * reps * weight_kg:.1f} would drop in 800.0. 

EXERCISE 3 Conversions, and deliberately breaking them
1. int("12") : prediction is 12, output is 12
2. float("12.5") : prediction is 12.5, output is 12.5
3. str(12): prediction is 12, output was '12'
4. int("12.5"): prediction was either 12 or error, output wss error. ( invalid literal for int() )
5. int("twelve"): prediction is error, output is error.(  invalid literal for int() )

Conclusion: The lesson: int() converts a value into a whole-number integer but it can't convert a string with a decimal point, and it definitely can't convert a word.

EXERCISE 4 
New tool: input() pauses the program and waits for the user to type something. input() always returns a string.
In `day2_logline.py`: I need to write a script using `input()` that prints one clean formatted training-log line.
some notes: mv ~/Desktop/"Career Plan"/day2_logline.py .
mv means "move," then the file's current Desktop location, then . (a single dot) meaning "to here, the folder I'm currently in." The quotes around "Career Plan" are needed because the folder name has a space in it. This picks the file up from Career Plan and drops it into foundation.

EXERCISE 5 debug
I was given: `weight = input("kg? ")` then `print(weight * 2.5)`
I typed : >>> weight = input("kg?")
kg?2
>>> print(weight * 2.5)
Traceback (most recent call last):
  File "<python-input-64>", line 1, in <module>
    print(weight * 2.5)
          ~~~~~~~^~~~~
TypeError: can't multiply sequence by non-int of type 'float'

correction: weight = float(input("kg?"))
print(weight * 2.5)
5.0

I was given: print("total: " + 45)
fix: print("total:" + str(45))

I was given: `name = "farmer's carry"`
fix: >>> name = "farmer's carry"
>>> name
"farmer's carry"