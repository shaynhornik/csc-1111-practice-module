# CSC 1111 practice module

A self-contained study course for testing out of **CSC 1111, Introduction to Problem Solving and Computer Programming** (Sinclair College), which is taught in C++.

Open `index.html` in a browser. It runs offline from that one file; there is nothing to install.

## What is in it

| | |
|---|---|
| Units | 9 |
| Lessons | 55 |
| Practice questions | 717 |
| Programs to write | 32, each with a worked solution |

The units follow the course's master syllabus:

1. How programs get made (the programming process, flowcharts, pseudocode, algorithms)
2. C++ basics (program structure, variables, data types, constants)
3. Expressions and interactivity (input, arithmetic, type conversion, formatting output)
4. Making decisions (selection)
5. Loops (iteration)
6. Functions
7. Arrays
8. Introduction to objects
9. Testing and debugging

Each lesson names the sections of the course textbook it covers (Tony Gaddis, *Starting Out with C++: From Control Structures through Objects*, 10th edition). The textbook itself is not part of this repository, and all lesson text and questions here are original.

## How the course works

- **Lessons** are short notes with code examples.
- **Practice** gives the answer and the reason after every question. Anything missed comes back a few questions later, and again under "Review my misses", until it is answered correctly.
- **Four question types:** multiple choice, true/false, fill in the blank, and "what does this print" (typed exactly).
- **Mock exams** are timed, drawn from every unit, and give no feedback until the end.
- **Programs to write** are exam-level exercises to type, compile and compare against a sample run.
- **The dashboard** tracks progress and shows a four-point readiness checklist.

Progress is stored in the browser's local storage on the computer you use. It does not sync.

## How the answers were checked

- Every question that shows code and asks what it prints, and every program solution, is compiled and run by `tools/verify_unit.py` with `g++ -std=c++17 -Wall`. The stored answer must match the real output.
- Every question was then audited by a second reviewer who worked out each answer independently, compiling wherever the answer depends on what code does.
- Coverage was checked chapter by chapter against the textbook's section list and end-of-chapter review topics.
- The text was compared with the textbook so that no passage repeats its wording.

This is a study aid built from the syllabus and the textbook. It is not the college's exam, and the college does not publish that exam's length or format.

This project is not affiliated with or endorsed by Sinclair College, Pearson, or the textbook's author. Textbook section and page numbers are given only as references for further reading.

## Repository layout

```
index.html              the built course (open this)
src/app-template.html   the app: lessons, practice engine, mock exams, dashboard
units/*.json            lessons, questions and programs, one file per group of units
tools/build.py          merges units into the template and writes index.html
tools/verify_unit.py    validates a unit file and compiles and runs all of its C++
docs/WRITING-GUIDE.md   the format and rules for writing lessons and questions
test/smoke.js           a browser test of the built course
```

## Changing or adding questions

1. Edit a file in `units/`, following `docs/WRITING-GUIDE.md`.
2. Check it: `python3 tools/verify_unit.py units/<file>.json` (needs `g++`). It must print `RESULT: PASS`.
3. Rebuild: `python3 tools/build.py`.

To practice the programming exercises:

```
g++ -std=c++17 -Wall prog.cpp -o prog && ./prog
```

## License

MIT. See `LICENSE`.
