# zenmate_bi_challenge
This code requires python 3 to be run, and can be executed from the command line:
```
python organize_meetings.py /path/to/meetings.txt
```
You can always run the `organize_meetings.py` with `-h` to see the various flags
and arguments.

***Note:*** the input to `organize_meetings.py` is assume to have the same
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
