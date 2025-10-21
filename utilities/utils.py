def size_format(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
            
        size /= 1024
        
    return f"{size:.2f} PB"


def format_timeperiod(timeperiod):
    for unit in ["seconds", "minutes", "hours"]:
        if timeperiod < 60:
            return f"{timeperiod:.2f} {unit}"
        
        if unit == "hours":
            timeperiod /= 24
        else:
            timeperiod /= 60
