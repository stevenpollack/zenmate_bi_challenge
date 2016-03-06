import re
from meeting import Meeting
from meetingroom import MeetingRoom
from random import shuffle
import argparse

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
                      verbose=False):

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

    solution_found=False
    for attempt in range(max_attempts):
        solution_found = set_agenda(meetings, room1, room2)
        print(attempt, solution_found)
        if solution_found:
            break
        else:
            print(room1)
            print(room2)
            reset_and_shuffle(meetings)

    if solution_found:
        print("Couldn't find solution within %i attempts." % max_attempts)
        return(None)
    
    if verbose:
        print("Found solution after %s attempts:\n" % str(attempt+1))

    print(room1, "\n")
    print(room2)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("meeting_file", 
                        help="the path to the file containing meeting names and lengths.")
    parser.add_argument("-m", "--max-attempts", 
                        default=100,
                        type=int,
                        help="the maximum number of attempts to be performed. Default is 100.")
    parser.add_argument("-v", "--verbose",
                        help="print extra information about meetings and scheduling attempts.",
                        action="store_true")
    args = parser.parse_args()

    organize_meetings(meetings_file=args.meeting_file, 
                      max_attempts=args.max_attempts,
                      verbose=args.verbose)
