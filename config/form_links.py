# config/form_links.py
class FormLinks:
    # Complaint Forms
    ELECTRICAL = "https://forms.gle/electrical123"
    PLUMBING = "https://forms.gle/plumbing123"
    FURNITURE = "https://forms.gle/furniture123"
    ROOM_ISSUES = "https://forms.gle/room123"
    INTERNET = "https://forms.gle/internet123"
    GENERAL_COMPLAINT = "https://forms.gle/general123"
    
    # Lost & Found
    LOST_ITEM = "https://forms.gle/lost123"
    FOUND_ITEM = "https://forms.gle/found123"
    
    # Mess
    MESS_FEEDBACK = "https://forms.gle/mess123"
    MESS_COMPLAINT = "https://forms.gle/messcomplaint123"
    
    @classmethod
    def get_complaint_form(cls, issue_type: str) -> str:
        mapping = {
            "electrical": cls.ELECTRICAL,
            "plumbing": cls.PLUMBING,
            "furniture": cls.FURNITURE,
            "room": cls.ROOM_ISSUES,
            "internet": cls.INTERNET,
            "wifi": cls.INTERNET
        }
        return mapping.get(issue_type.lower(), cls.GENERAL_COMPLAINT)