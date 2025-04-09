from datetime import datetime, timedelta, timezone

def validateDate(datePublished: datetime) -> bool:
    if datePublished.tzinfo is not None:  # Si tiene zona horaria
        datePublished = datePublished.replace(tzinfo=None)
    if(datePublished):
        limit_date = datetime.now() - timedelta(days=2)
        return datePublished < limit_date
    return False

def convertDate(datePublished: str) -> datetime:
    try:
        if(datePublished):
            return datetime.strptime(datePublished, '%Y-%m-%dT%H:%M:%S%z')
    except:
        pass
    
    try:
        if(datePublished):
            return datetime.strptime(datePublished, '%B %d, %Y - %I:%M %p')
    except:
        pass

    return None


def cleanText(text: str)-> str:
    try:
        return text.strip() if text else ''
    except:
        pass
    return ''
