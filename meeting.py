from datetime import datetime

class Meeting:
    
    def __init__(self, name, duration, room=None, start_time=None):
        self.name = name.strip()
        self.room = room
        if name != 'Lunch':
            self.duration = int(duration)
            
            if start_time is not None and not isinstance(start_time, datetime):
                raise TypeError("'start_time' must either be None or a datetime object")
                
            self.start_time = start_time
        else:
            self.duration = 60
            self.start_time = self.lunch_start = datetime(2016, 3, 3, 12)
            
    def __str__(self):
        if self.start_time is None:
            start_time = '--'
        else:
            start_time = self.start_time.strftime('%I:%M%p')
        
        if self.name == 'Lunch':
            output = "%s %s" % (start_time, self.name)
        else:
            output = "%s %s %smin" % (start_time, self.name, self.duration)
        return(output)
    
    def __repr__(self):
        output = "Meeting(name=%r, dur=%r, room=%r, start=%r)" % (self.name, self.duration, self.room, self.start_time)
        return(output)
