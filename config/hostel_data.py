# config/hostel_data.py (continued)
class MessData:
   @staticmethod
   def get_menu_info(meal_type: str) -> str:
       menus = {
           "breakfast": """**Today's Breakfast (7:00 AM - 9:00 AM):**
- Aloo Paratha with Curd
- Poha with Tea/Coffee
- Bread, Butter, Jam
- Seasonal Fruits""",
           
           "lunch": """**Today's Lunch (12:00 PM - 2:00 PM):**
- Rice with Dal Tadka
- Mixed Vegetable Curry
- Roti/Chapati
- Pickle and Salad""",
           
           "dinner": """**Today's Dinner (7:00 PM - 9:00 PM):**
- Rajma with Rice
- Aloo Gobi
- Roti/Chapati
- Sweet Dish""",
           
           "all": """**Full Day Menu:**
**Breakfast:** Paratha, Poha, Bread & Tea
**Lunch:** Rice, Dal, Sabzi, Roti
**Dinner:** Rice, Curry, Roti, Sweet"""
       }
       return menus.get(meal_type.lower(), menus["all"])

class HostelRules:
   @staticmethod
   def get_policy_info(category: str) -> str:
       policies = {
           "visitor": """**Visitor Policy:**
- Visiting hours: 10:00 AM - 8:00 PM
- All visitors must register at reception
- Valid ID required for entry
- Maximum 2 visitors per student at a time
- Overnight stays not permitted without prior approval
- Visitors cannot access mess without permission""",
           
           "curfew": """**Entry/Exit Timings:**
- Hostel gates close at 10:30 PM
- Late entry requires permission slip
- Emergency late entry: Contact security
- Weekend curfew extended to 11:30 PM
- Special occasions: Check with warden for extensions""",
           
           "fees": """**Fee Payment Policy:**
- Mess fees due by 5th of each month
- Room rent due by 1st of each month
- Late payment penalty: ₹50 per day after due date
- Payment methods: Online, cash at office
- Refunds processed within 15 working days""",
           
           "room": """**Room Allocation & Transfer:**
- Room changes allowed once per semester
- Transfer requests require valid reason
- New room allocation within 7 days of approval
- Room sharing: Maximum 2 students per room
- Student responsible for room maintenance""",
           
           "discipline": """**Disciplinary Policy:**
- First violation: Verbal warning
- Second violation: Written warning
- Third violation: Fine or temporary suspension
- Serious violations: Immediate action
- Appeal process: Submit within 7 days to warden""",
           
           "emergency": """**Emergency Procedures:**
- Fire alarm: Evacuate immediately via nearest exit
- Medical emergency: Contact security (24/7)
- Security issues: Alert security immediately
- Power outage: Contact maintenance
- Emergency contacts posted in all common areas"""
       }
       return policies.get(category.lower(), "Policy information not available. Contact hostel office.")
   
   @staticmethod
   def get_procedure_steps(category: str) -> str:
       procedures = {
           "visitor": """1. Visitor brings valid ID to reception
2. Student comes to reception to verify
3. Visitor fills registration form
4. Security issues visitor pass
5. Student escorts visitor to room/common area
6. Visitor returns pass before leaving""",
           
           "room": """1. Submit room transfer application to warden
2. Provide valid reason (medical, academic, personal)
3. Pay transfer fee (if applicable)
4. Wait for approval (3-5 working days)
5. Receive new room allocation
6. Complete room handover process""",
           
           "fees": """1. Receive fee payment notice
2. Calculate total amount due
3. Pay via online portal or cash at office
4. Collect payment receipt
5. Verify payment reflects in your account"""
       }
       return procedures.get(category.lower(), "Contact hostel office for specific procedures.")
   
   @staticmethod
   def get_required_documents(category: str) -> str:
       docs = {
           "visitor": "Valid government ID (Aadhar, PAN, License)",
           "room": "Medical certificate (if applicable), Parent consent form",
           "fees": "Previous payment receipts, Fee structure copy"
       }
       return docs.get(category.lower(), "Check with hostel office for required documents.")
   
   @staticmethod
   def get_processing_time(category: str) -> str:
       times = {
           "visitor": "Immediate (if documents are valid)",
           "room": "3-5 working days",
           "fees": "Payment processed immediately"
       }
       return times.get(category.lower(), "Contact office for timeline information.")
   
   @staticmethod
   def get_common_questions(category: str) -> str:
       questions = {
           "visitor": """• Can visitors eat in mess? (Only with prior permission)
- Can visitors stay overnight? (Not without approval)
- What ID is acceptable? (Government issued photo ID)""",
           
           "curfew": """• What if I have a medical emergency? (Contact security immediately)
- Can I get late entry for work? (Yes, with employer letter)
- Weekend timings different? (Yes, extended to 11:30 PM)""",
           
           "fees": """• What if payment is 1 day late? (₹50 penalty applies)
- Can I pay in installments? (Contact office for payment plan)
- How to get payment receipt? (Available online or at office)"""
       }
       return questions.get(category.lower(), "Ask hostel office for clarifications.")
   
   @staticmethod
   def get_exceptions(category: str) -> str:
       exceptions = {
           "visitor": "Emergency situations, parent visits, official purposes may have relaxed restrictions",
           "curfew": "Medical emergencies, family emergencies, work requirements with documentation",
           "fees": "Financial hardship cases may get payment plan options"
       }
       return exceptions.get(category.lower(), "Speak with warden about special circumstances.")

class FacilityStatus:
   @staticmethod
   def get_current_status(facility_type: str, location: str = "general") -> Dict[str, str]:
       # Simulated current status - in real implementation, this would fetch from actual monitoring systems
       statuses = {
           "power": {
               "status": "operational",
               "last_updated": "30 minutes ago",
               "next_check": "Every 6 hours",
               "affected_areas": "None",
               "emergency_contact": "Electrician: +91-XXXXXXXXXX"
           },
           "water": {
               "status": "operational", 
               "last_updated": "1 hour ago",
               "next_check": "Every 4 hours",
               "affected_areas": "None",
               "emergency_contact": "Plumber: +91-XXXXXXXXXX"
           },
           "internet": {
               "status": "operational",
               "last_updated": "15 minutes ago", 
               "next_check": "Every 2 hours",
               "affected_areas": "None",
               "emergency_contact": "IT Support: +91-XXXXXXXXXX"
           }
       }
       return statuses.get(facility_type.lower(), {
           "status": "unknown",
           "last_updated": "Check with office",
           "emergency_contact": "Hostel Office: +91-XXXXXXXXXX"
       })
   
   @staticmethod
   def get_maintenance_schedule(facility_type: str) -> Dict[str, str]:
       schedules = {
           "power": {
               "this_week": "• Sunday 6:00 AM - 8:00 AM: Generator testing\n• No other scheduled work",
               "next_week": "• Wednesday 2:00 PM - 4:00 PM: Electrical panel maintenance",
               "regular_schedule": "Monthly generator maintenance, Weekly electrical checks"
           },
           "water": {
               "this_week": "• Monday 5:00 AM - 7:00 AM: Water tank cleaning (Block A)\n• No disruption expected",
               "next_week": "• Thursday 6:00 AM - 10:00 AM: Pump maintenance",
               "regular_schedule": "Weekly tank cleaning rotation, Monthly pump servicing"
           },
           "internet": {
               "this_week": "• No scheduled maintenance",
               "next_week": "• Saturday 11:00 PM - 1:00 AM: Server updates",
               "regular_schedule": "Monthly router updates, Quarterly network optimization"
           }
       }
       return schedules.get(facility_type.lower(), {
           "this_week": "No information available",
           "next_week": "Check with office",
           "regular_schedule": "Contact office for schedule"
       })
   
   @staticmethod
   def get_service_hours(facility_type: str) -> str:
       hours = {
           "power": "24/7 availability, Maintenance team: 8:00 AM - 8:00 PM",
           "water": "24/7 supply, Plumber available: 7:00 AM - 9:00 PM",
           "internet": "24/7 connectivity, IT support: 9:00 AM - 6:00 PM"
       }
       return hours.get(facility_type.lower(), "Contact office for service hours")
   
   @staticmethod
   def get_reporting_guide(facility_type: str) -> str:
       guides = {
           "power": """• Note which lights/outlets not working
- Check if neighbors have same issue
- Don't touch exposed wires
- Report immediately if sparks/burning smell""",
           
           "water": """• Check if issue is in your room only or building-wide
- Note water pressure level
- Report leaks immediately
- Don't attempt repairs yourself""",
           
           "internet": """• Test on multiple devices
- Note error messages
- Check if WiFi shows up in available networks
- Try restarting your device first"""
       }
       return guides.get(facility_type.lower(), "Contact office with detailed description")
   
   @staticmethod
   def get_troubleshooting_tips(facility_type: str) -> str:
       tips = {
           "power": """• Check main switch in your room
- Verify other rooms have power
- Check circuit breaker panel
- Don't overload outlets""",
           
           "water": """• Check if taps in other areas work
- Verify water motor is running
- Check for visible leaks
- Clean tap filters regularly""",
           
           "internet": """• Restart WiFi router if accessible
- Check device WiFi settings
- Try connecting closer to router
- Clear browser cache"""
       }
       return tips.get(facility_type.lower(), "Contact technical support for help")
   
   @staticmethod
   def get_contact_info(facility_type: str) -> str:
       contacts = {
           "power": "Electrician: +91-XXXXXXXXXX, Hostel Office: +91-XXXXXXXXXX",
           "water": "Plumber: +91-XXXXXXXXXX, Hostel Office: +91-XXXXXXXXXX", 
           "internet": "IT Support: +91-XXXXXXXXXX, Network Admin: +91-XXXXXXXXXX"
       }
       return contacts.get(facility_type.lower(), "Hostel Office: +91-XXXXXXXXXX")
   
   @staticmethod
   def get_service_standards(facility_type: str) -> str:
       standards = {
           "power": "• 99.5% uptime target\n• Emergency repairs within 2 hours\n• Planned outages with 48hr notice",
           "water": "• 24/7 supply commitment\n• Pressure maintained 20-40 PSI\n• Quality testing monthly",
           "internet": "• 50 Mbps minimum speed\n• 99% uptime target\n• Support response within 4 hours"
       }
       return standards.get(facility_type.lower(), "Contact office for service standards")