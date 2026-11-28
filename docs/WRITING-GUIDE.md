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
A lesson must teach someone who does not know the topic yet. It is not a summary sheet.
- 3 to 7 per unit. Usually 600 to 1300 words plus code: as long as the topic needs, with no padding. Cover every section in your range between them.
- `book` names the sections and printed page numbers.
- Shape, adapted to the topic:
  1. Start from the idea in plain words: what problem the feature solves and one picture to hold in mind. Reuse that picture through the lesson.
  2. Teach each point with a small example and trace it: values before, what the statement does, values after.
  3. State the exact rules (operator precedence, what a loop tests and when, integer division, and so on) after the reader has seen them work. Say why a rule holds and when it does not apply.
  4. Show the traps an examiner likes, each with the wrong and the right version.
  5. End with `<h4>Mistakes students make</h4>` and `<h4>What to remember for the test</h4>`.
- Define every technical term the first time it appears. Never rely on a term from a later lesson.
- Every question attached to the lesson must be answerable from the lesson text alone.
- Run every code example that shows output.
- HTML: only these tags: p, ul, ol, li, strong, em, code, pre, table, thead, tbody, tr, th, td, h4, br. Escape `<`, `>` and `&` inside code as `&lt;`, `&gt;`, `&amp;`. Keep code lines short enough for a phone.
- `units/a2-basics.json`, lesson `u3-l5`, is the model to follow.

### Questions
Four types:
- `mc`: exactly 4 distinct choices, `answer` is the 0-based index. Spread the correct answer evenly across positions 0 to 3. Distractors must be the mistakes a student really makes.
- `tf`: `answer` is true or false. Keep true and false roughly balanced.
- `fill`: a term or a short piece of code. `answer` is the canonical answer, `accept` is a list of every reasonable spelling (compared case-insensitively, whitespace-trimmed), and must include `answer`.
- `output`: "What does this print?" Needs `code` (what the student sees), `program` (a complete program that compiles and prints exactly the answer; it may be the same text as `code`), and `answer` (the exact stdout). Keep output to 6 lines or fewer.

For `mc`, `tf` and `fill` questions whose correct answer depends on what code does, add `program` and `expect` (exact stdout) so it is machine-checked. For "find the error" questions the snippet may not compile; then don't add `program`.

Every question needs `lesson` (an id from your lessons), `difficulty` (1 easy, 2 exam level, 3 tricky), and `explain`.

`explain` is shown right after the answer and matters most when the answer was wrong, so it must teach:
- Walk through how to reach the answer. For output and value questions, trace the code step by step.
- Multiple choice: say why the right choice is right and what mistake each wrong choice represents.
- True/false: say what makes it true, or name what is false and give the correct statement.
- Name the tempting wrong answer and why it is wrong.
- 2 to 7 sentences or a short trace. Easy definition questions can be shorter.
- Plain text. Backticks mark inline code, a fenced ``` block (fences on their own lines) holds a trace or code, and a blank line starts a new paragraph.

Never change the `id` of a lesson or question once it has been published: saved progress is keyed on ids.

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
- `prompt`, `explain` and `choices` are shown as plain text, with backticks marking inline code. `explain` may also use fenced code blocks and blank-line paragraphs. Only lesson `html` is real HTML.
- Output answers ignore trailing spaces and a final blank line. Everything else counts, so wrap space-sensitive output in visible delimiters such as `[` and `]`.
- Fill-in answers ignore capital letters and spacing.

## Verify

```
python3 tools/verify_unit.py units/<file>.json
```

It checks the shape of the file and compiles and runs every `program` and `solution` with `g++ -std=c++17 -Wall`. Fix until it prints `RESULT: PASS`. Then re-read a sample of questions as a skeptical examiner: is exactly one choice correct, and is the explanation right?
