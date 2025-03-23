from datetime import datetime, timedelta

priority_map = {"ASAP": 1, "Urgent": 2, "Normal": 3, "Flexible": 4}

def sort_tasks(tasks):
    return sorted(tasks, key=lambda t: (not t["fixed"], priority_map[t["priority"]]))

def schedule_tasks(tasks):
    scheduled = []
    for task in sort_tasks(tasks):
        if task["fixed"]:
            scheduled.append(task)
        else:
            start_hour = 8
            while start_hour < 20:
                potential_start = datetime.now().replace(hour=start_hour, minute=0, second=0, microsecond=0)
                potential_end = potential_start + timedelta(minutes=task["duration"])
                conflict = any(
                    t["start_time"] < potential_end and
                    (t["start_time"] + timedelta(minutes=t["duration"])) > potential_start
                    for t in scheduled
                )
                if not conflict:
                    task["start_time"] = potential_start
                    task["end_time"] = potential_end
                    scheduled.append(task)
                    break
                start_hour += 1
    return scheduled
