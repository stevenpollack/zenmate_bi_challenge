import re
from meeting import Meeting
from meetingroom import MeetingRoom
from random import shuffle

def parse_input(input_file='test_input.txt'):    
    meetings = []
    with open(input_file) as f:
        for line in f:
            line_split = re.match('(.*) (\d+)min', line)
            if line_split:
                meetings.append(Meeting(line_split.group(1), line_split.group(2)))
    return(meetings)

def reset_and_shuffle(meetings):
    for meeting in meetings:
        meeting.room = None
    shuffle(meetings)

def set_agenda(meetings, room1, room2):        
    found_solution=True
    # go through each potential meeting and try and allocate to one
    # of the rooms (try the other if that fails):
    for meeting in meetings:
        if room1.add_meeting(meeting):
            continue
        elif not room2.add_meeting(meeting):
            found_solution=False
            break
    
    return(found_solution)

def organize_meetings(meetings_file='test_input.txt',
                      max_meeting_time=7*60*2,
                      max_attempts=100,
                      verbose=True):

    meetings = parse_input(meetings_file)

    # check to make sure we even have enough time...
    total_meeting_time = 0
    for meeting in meetings:
        total_meeting_time += meeting.duration

    if total_meeting_time / 60 > max_meeting_time:
        raise Exception('more meeting time required than allowed')

    if verbose:
        print("Total meeting time: %i minutes\n" % total_meeting_time)
        
    # initialize the two meeting rooms
    room1 = MeetingRoom("Room 1")
    room2 = MeetingRoom("Room 2")

    for attempt in range(max_attempts):
        if set_agenda(meetings, room1, room2):
            break
        else:
            reset_and_shuffle(meetings)
            set_agenda(meetings, room1, room2)

    if attempt > max_attempts:
        raise Exception("Couldn't find solution")
    
    if verbose:
        print("Found solution after %d attempts:\n" % attempt)
        print(room1, "\n")
        print(room2)
        
    return(room1, room2)

if __name__ == "__main__":
    organize_meetings()
