from ics import Calendar, Event
import os
import datetime

def create_ics_event(summary, start_time_iso, duration_minutes=60):
    c = Calendar()
    e = Event()
    e.name = summary
    
    try:
        start_dt = datetime.datetime.fromisoformat(start_time_iso)
        e.begin = start_dt
        e.duration = datetime.timedelta(minutes=duration_minutes)
        
        c.events.add(e)
        
        filename = f"event_{start_dt.strftime('%Y%m%d_%H%M')}.ics"
        with open(filename, 'w') as f:
            f.writelines(c)
            
        print(f"Created file: {filename}")
        
        os.startfile(filename) 
        return True
    except Exception as ex:
        print(f"Error creating event: {ex}")
        return False