# 04 · X-Ray Vision — prompts

**Context:** You joined Rook two weeks ago as PM on Dispatch.
Release 4.2 shipped on 12 August, just before you arrived, and
landed badly. Last session the numbers showed you what happened: a
ping used to wait ninety seconds and now it waits sixty, people
missed pings they used to catch, and missing one counts the same as
turning one down — so four responders stopped hearing from us
altogether.

At the end of the session, type wrap up, and Claude Code saves the
prompts you wrote yourself below — not the starter prompt — updates
CLAUDE.md, and saves your work to GitHub. By Module 6 this file is a
prompt library built from your own questions.

---

### 1.

list all changes in the code since 4.2

### 2.

based on what you understood from the code "Based on what I found, the reason some responders are getting no pings at all is ___, because ___.
" can you answer it and provide a confident score to it ?

### 3.

can you create a visual diagram to explain the reason with an example

### 4.

what do you mean by reweight here ?

### 5.

so based on this what is the reason after 4.2 ?

### 6.

can you give the answer to "According to my findings in the code, for someone who's gone quiet, they would need to ___.
"

### 7.

what is your recommendations to fix this in the product ?

### 8.

can you show this visually "
▎ "Based on what I found, the reason some responders are getting no pings at all is that a burst of missed pings after 4.2 pushed their reliability score to the bottom, and the system gives them no way to climb back up, because the code punishes a missed ping exactly like a 'no' (−0.12), never restores a score on its own, and only buzzes one phone at a time, so someone at the back of the line is effectively never reached; with fewer pings they can't take a job, which is the only thing that raises their score."

### 9.

can you do a simulation to show how a quiet person to get back to normal
