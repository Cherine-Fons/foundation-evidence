**Day 8 Warm-Up (index loops from yesterday)**

1. nums = [5, 12, 8, 20]. Write the loop that builds gaps, the list of day-over-day absolute differences. Then say what range you loop over and why it starts where it does.
For that same nums, what does nums[i] - nums[i-1] equal when i = 3? Give the two elements you're subtracting and the result. Read the list above — use those exact values.
2. data = [100, 100, 100]. Predict exactly what gaps (the absolute-differences list) contains after the loop runs. How many elements, and what are they?


1) We are building a new list called gaps. The goal to compare each number with the number before it. We do not compare 5 with anything because it is the first value and has no previous value. 

**STEP 1**
Create the original list: 
nums = [5, 12, 8, 20]

The indexes (positions) are 0 that has value 5, 1 that has value 12, 2 that has value 8 and 3 that has value 20.

**STEP 2**
Create an empty result list:
gaps = []

This is where we will store each absolute difference.

**STEP 3**
Choose the indexes for the loop:
for i in range(1, len(nums)):

So len(nums) is 4, therefore range(1, 4) which gives 1,2,3. I loop over range(1, len(nums)) because each calculation compares the current number with the number immediately before it. The loop starts at index 1 because index 0 is the first item and has no previous item to compare with; starting at 0 would incorrectly use index -1, then nums[i - 1] which is nums[-1], which refers to the last item in the list.

**STEP 4**
Calculate each absolute difference. Inside the loop we write:
diff = abs(nums[i] - nums[i-1])

So the loop works like this:
i = 1: abs(nums[1] - nums[0]) = abs(12 - 5)  = 7
i = 2: abs(nums[2] - nums[1]) = abs(8 - 12)  = 4
i = 3: abs(nums[3] - nums[2]) = abs(20 - 8)  = 12

**STEP5**
Add each result to gaps:
gaps.append(diff)

So after each pass this is what we get:
After i = 1: gaps = [7]
After i = 2: gaps = [7, 4]
After i = 3: gaps = [7, 4, 12]

Complete program:

nums = [5, 12, 8, 20]
gaps = []
for i in range(1, len(nums)):
    diff = abs(nums[i] - nums[i-1])
    gaps.append(diff)
print(gaps)

2) data = [100, 100, 100]
   gaps = []
   for i in range(1, len(data)):
       diff = abs(date[i] - data[i-1])
       gaps.append(diff)
   print(gaps)

The loop runs for i = 1 and i = 2
i = 1: abs(data[1] - data[0]) = abs(100 - 100) = 0
i = 2: abs(data[2] - data[1]) = abs(100 - 100) = 0

I predict that gap contains: 
   [0,0]    
