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
    
    return(found_solution, room1, room2)

def organize_meetings(meetings_file,
                      max_meeting_time,
                      max_attempts,
                      verbose=False):

    meetings = parse_input(meetings_file)

    # check to make sure we even have enough time...
    total_meeting_time = 0
    for meeting in meetings:
        total_meeting_time += meeting.duration

    if verbose:
        print("Total meeting time: %i minutes\n" % total_meeting_time)
     
    if total_meeting_time > max_meeting_time:
        print('Error: more meeting time required than allowed...')
        return(None)

    # initialize the two meeting rooms
    room1 = MeetingRoom("Room 1")
    room2 = MeetingRoom("Room 2")

    solution_found=False
    for attempt in range(max_attempts):
        
        solution_found, room1, room2 = set_agenda(meetings, room1, room2)

        if solution_found:
            break
        else:
            # shuffle meetings and clear the meeting rooms' schedules
            reset_and_shuffle(meetings)
            room1 = MeetingRoom("Room 1")
            room2 = MeetingRoom("Room 2")

    if not solution_found:
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
    parser.add_argument("-t", "--max-meeting-time",
                        type=int,
                        default=60*7*2,
                        help="the maximum number of minutes allowed for \
                        meeting, across both meeting rooms. Default is 60*7*2, \
                        which represents 14 hours across both rooms.")
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
                      max_meeting_time=args.max_meeting_time,
                      verbose=args.verbose)
