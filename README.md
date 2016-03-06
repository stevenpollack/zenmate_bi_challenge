# zenmate_bi_challenge
This code requires python 3 to be run, and can be executed from the command line:
```
python organize_meetings.py /path/to/meetings.txt
```
You can always run the `organize_meetings.py` with `-h` to see the various flags
and arguments.

***Note:*** the input to `organize_meetings.py` is assumed to have the same
structure as the .txt provided in the coding challenge ([test_input.txt](test_input.txt)). 
The output of the .py is a schedule, as depicted in the coding challenge. E.g.,
```bash
$ python organize_meetings.py test_input.txt

Room 1:
09:00AM All Hands meeting 60min
10:00AM Marketing presentation 30min
10:30AM Product team sync 30min
11:00AM Ruby vs Go presentation 45min
12:00PM Lunch
01:00PM New app design presentation 45min
01:45PM Customer support sync 30min
02:15PM Front-end coding interview 60min
03:15PM Skype Interview A 30min
03:45PM Skype Interview B 30min
04:15PM Project Bananaphone Kickoff 45min

Room 2:
09:00AM Developer talk 60min
10:00AM API Architecture planning 45min
10:45AM Android app presentation 45min
12:00PM Lunch
01:00PM Back-end coding interview A 60min
02:00PM Back-end coding interview B 60min
03:00PM Back-end coding interview C 60min
04:00PM Sprint planning 45min
```

----------
*edit (after the challenge is over)*
## Design considerations and notes:
I realize I should probably write a note or two about what this code is doing.

I couldn't think of a simple (deterministic) way to schedule meetings
between rooms, for the simple fact that meetings have no obvious relation
or ordering amongst themselves. For example, "Back-end coding interview A",
doesn't, _a priori_, need to be in the same room, or even precede (or proceed)
"Sprint Planning". Hence, a candidate scheduling algorithm can be
- _greedy_, in that we can assign as many meetings to one room as possible before
considering the allocation of a meeting to the other, and
- _random_, in that we can shuffle our stack of meetings should our greedy attempt
at allocation fail.

### Object Design
The code has two data structures:
- *Meetings* -- an abstraction of the problem input. These objects have
attributes to represent the meeting name, the room the meeting will take place in,
the time the meeting will start, and the duration of the meeting.
- *Meeting Rooms* -- an abstraction of a meeting room, as you'd see it posted on an
office calendar. A meeting room has a collection of meetings associated to it (for a
given day), an attribute tracking the next available time when the room is free,
as well as attributes representing the various problem constraints (e.g.,
the times when the room is available) and a method to (greedily) add a meeting to
the room's schedule (if possible), `add_meeting`.

The logic in `add_meeting` is (perhaps too) simple:

1. If the next free time is before lunch, check that the proposed meeting can start
   and conclude before lunch.
    - If it cannot conclude before lunch, set the next free time to the end of lunch
      and try again. If we can schedule the meeting, return `True`.
2. If the next free time is after lunch, check that the proposed meeting can start
   and conclude before the end of the work day.
   - If it it cannot, return `False`.

### Algorithm Design
The algorithm, on its face, is rather inelegant: we

1. Start with a stack of meetings.
2. Pop a meeting off the top.
3. Attempt to allocate the meeting to the first room with `add_meeting`.
    - if that fails, we attempt to allocate it to the second room
4. If both attempts fail, we (re)shuffle the stack of meetings, and start over at step 1.
   If either attempt succeeds, we repeat steps 2 and 3 until the stack is empty.

Hence, this algorithm requires a metaparameter, `max_attempts`, which limits the number
of times the stack will be shuffled and the algorith re-run. With the test input, convergence
seems to happen with near certainty when `max_attempts` is set to 100, but convergence has
been observed in as few as 3 (or even 1) attempts. However, I cannot guarantee that a 
malicious manager won't show up with a list of meetings whose allocation scheme is computational
infeasible. In which case, it doesn't matter what `max_attempts` is set to: the algorithm will
never converge on a solution.
