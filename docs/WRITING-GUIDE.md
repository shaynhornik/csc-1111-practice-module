# Writing guide for lessons, questions and programs

The course prepares a student for a one-attempt test-out exam, so questions must be exact, unambiguous and at exam level.

The topics come from the course master syllabus: the problem-solving process (input, processing, output); flowcharts, pseudocode and algorithms; variables, constants and data types; expressions; the three structures (sequence, selection, iteration); introduction to functions; one-dimensional arrays; testing and debugging; introduction to object-oriented programming. The course textbook's section list is the coverage checklist. **Write everything in your own words.** Never copy the textbook's questions, examples or prose.

## What to write
Each file in `units/` is one JSON document shaped like this:

```json
{"units": [{
  "id": "u4", "title": "Making decisions", "summary": "One sentence on what this unit covers.",
  "lessons": [{"id": "u4-l1", "title": "Relational operators and the if statement", "book": "Sections 4.1 to 4.3, pages 153 to 169",
               "html": "<p>...</p><pre><code>...</code></pre>"}],
  "questions": [{"id": "u4-q001", "lesson": "u4-l1", "type": "mc", "difficulty": 2,
                 "prompt": "...", "code": "optional snippet shown in a code block",
                 "choices": ["a", "b", "c", "d"], "answer": 2, "explain": "Why, in 1 to 3 sentences."}],
  "programs": [{"id": "u4-p1", "title": "...", "task": "What to write.", "stdin": "optional input", "sampleOutput": "exact stdout of the solution for that input", "solution": "complete program"}]
}]}
```

### Lessons
- 3 to 7 per unit, each 200 to 450 words of tight notes plus short code examples. Cover every section in your range between them.
- `book` names the sections and printed page numbers.
- HTML: only these tags: p, ul, ol, li, strong, em, code, pre, table, thead, tbody, tr, th, td, h4, br. Escape `<`, `>` and `&` inside code as `&lt;`, `&gt;`, `&amp;`.
- State rules precisely (operator precedence, what a loop tests and when, what happens on integer division, and so on). Include the traps an examiner likes.

### Questions
Four types:
- `mc`: exactly 4 distinct choices, `answer` is the 0-based index. Spread the correct answer evenly across positions 0 to 3. Distractors must be the mistakes a student really makes.
- `tf`: `answer` is true or false. Keep true and false roughly balanced.
- `fill`: a term or a short piece of code. `answer` is the canonical answer, `accept` is a list of every reasonable spelling (compared case-insensitively, whitespace-trimmed), and must include `answer`.
- `output`: "What does this print?" Needs `code` (what the student sees), `program` (a complete program that compiles and prints exactly the answer; it may be the same text as `code`), and `answer` (the exact stdout). Keep output to 6 lines or fewer.

For `mc`, `tf` and `fill` questions whose correct answer depends on what code does, add `program` and `expect` (exact stdout) so it is machine-checked. For "find the error" questions the snippet may not compile; then don't add `program`.

Every question needs `lesson` (an id from your lessons), `difficulty` (1 easy, 2 exam level, 3 tricky), and `explain` (teach in 1 to 3 sentences: why the right answer is right, and where relevant why the tempting wrong one is wrong).

Mix per unit, roughly: 35% mc, 15% tf, 15% fill, 35% output (concept-only units use fewer output and more mc/fill). At least 4 questions per lesson. Roughly 25% difficulty 1, 50% difficulty 2, 25% difficulty 3.

Coverage rules:
- Every numbered book section in your range gets at least one question; core sections get many.
- Every key term gets a definition question in at least one direction.
- Include every question style: define the term, name the symbol, trace the output, find the error, pick the correct statement, complete the code, "how many times does this loop run", "what is the value of x after", convert between pseudocode/flowchart description and code where it applies.
- No undefined or unspecified behavior as the thing being asked (no `i++ + ++i`, no printing uninitialized variables, no reading past an array). Questions ABOUT why those are wrong are fine, as concept questions.
- `output` answers must be deterministic. No random numbers, time, addresses or `sizeof` results.
- Standard C++17. Use `#include <iostream>` style headers and `using namespace std;` as the book does.

### Programs
Write-it-yourself exercises at exam level, each with a complete solution, the `stdin` used, and the exact `sampleOutput`.

## Things the app does that affect wording

- Multiple-choice options are shuffled every time. Never write "all of the above", "none of the above" or "both A and B", and never refer to a choice by its position or letter in a prompt or explanation.
- `prompt`, `explain` and `choices` are shown as plain text, with backticks marking inline code. Only lesson `html` is real HTML.
- Output answers ignore trailing spaces and a final blank line. Everything else counts, so wrap space-sensitive output in visible delimiters such as `[` and `]`.
- Fill-in answers ignore capital letters and spacing.

## Verify

```
python3 tools/verify_unit.py units/<file>.json
```

It checks the shape of the file and compiles and runs every `program` and `solution` with `g++ -std=c++17 -Wall`. Fix until it prints `RESULT: PASS`. Then re-read a sample of questions as a skeptical examiner: is exactly one choice correct, and is the explanation right?
