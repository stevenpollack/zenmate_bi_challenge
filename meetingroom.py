class MeetingRoom:
    
    def __init__(self, name):
        self.meetings = [Meeting('Lunch', 60, name)]
        self.name = name
        self.day_start = datetime(2016, 3, 3, 9)
        self.lunch_start = datetime(2016, 3, 3, 12)
        self.lunch_end = datetime(2016, 3, 3, 13)
        self.day_end = datetime(2016, 3, 3, 17)
        self.next_open_slot = copy(self.day_start)
    
    def __str__(self):
        self.meetings.sort(key = lambda x: x.start_time)
        output = self.name + ":\n"
        output += "\n".join([meeting.__str__() for meeting in self.meetings])
        return(output)
    
    def add_meeting(self, meeting):
        # meeting needs to be of type Meeting
        if not isinstance(meeting, Meeting):
            raise TypeError("'meeting' must be a Meeting object")
        
        if meeting.room is not None:
            # meeting is already scheduled
            return(False)
            
        # 2 issues:
        # - meeting either runs into lunch, or
        # - meeting runs outside of business hours.
        
        meeting_start = copy(self.next_open_slot)
        meeting_end = meeting_start + timedelta(minutes=meeting.duration)
        
        if self.next_open_slot <= self.lunch_start:
            # see if we can schedule before lunch            
            if meeting_end <= self.lunch_start:
                # meeting doesn't run through lunch...
                meeting.room = self.name
                meeting.start_time = meeting_start
                self.meetings.append(meeting)
                self.next_open_slot = meeting_end
                return(True)
            else:
                # meeting will run into lunch, so try again
                # with next_open_slot at lunch's end
                self.next_open_slot = self.lunch_end
                return(self.add_meeting(meeting))
        else:
            # next_open_slot >= lunch_end
            if meeting_end <= self.day_end:
                meeting.room = self.name
                meeting.start_time = meeting_start
                self.meetings.append(meeting)
                self.next_open_slot = meeting_end
                return(True)
            else:
                # meeting will run out of business hours,
                # so we cannot schedule this meeting.
                return(False)