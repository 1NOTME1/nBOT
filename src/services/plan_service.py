from src.domain.plan_item import PlanItem

def create_plan_item(trip_id, title, date, time):
    if not isinstance(trip_id, int) or isinstance(trip_id, bool) or trip_id < 1:
        raise ValueError("Invalid trip_id")
    
    if not isinstance(title, str) or title.strip() == "":
        raise ValueError("Invalid title")
    
    if not isinstance(date, str) or date.strip() == "":
            raise ValueError("Invalid date")
        
    if not isinstance(time, str) or time.strip() == "":
                raise ValueError("Invalid time")
    
    return PlanItem(
        trip_id=trip_id,
        title=title.strip(),
        date=date.strip(),
        time=time.strip()
    )
