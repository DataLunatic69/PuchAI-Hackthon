# src/agents/status_updates.py
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from src.agents.base_agent import BaseAgent, AgentResponse
from config.hostel_data import FacilityStatus
from src.utils.prompts import SystemPrompts
from typing import Dict, Any

class StatusQueryAnalysis(BaseModel):
    """Analysis of facility status query"""
    
    facility_type: str = Field(
        description="Type: power, water, internet, wifi, maintenance, general, or emergency"
    )
    query_scope: str = Field(
        description="Scope: current_status, scheduled_maintenance, outage_report, or general_info"
    )
    location_specific: str = Field(
        description="Specific location mentioned? building/block name or 'general'"
    )
    urgency_indicator: str = Field(
        description="Urgency: routine_check, service_needed, or emergency_situation"
    )

class StatusAgent(BaseAgent):
    def __init__(self):
        super().__init__("Status Monitor")
    
    def get_system_prompt(self) -> str:
        return SystemPrompts.get_status_updates_prompt()
    
    async def process_query(self, query: str, context: Dict[str, Any]) -> AgentResponse:
        # Analyze the status query
        analysis = await self._analyze_status_query(query, context)
        
        # Get current facility status
        current_status = FacilityStatus.get_current_status(
            analysis.facility_type, 
            analysis.location_specific
        )
        
        # Route based on query scope
        if analysis.query_scope == "current_status":
            return await self._provide_current_status(analysis, current_status)
        elif analysis.query_scope == "scheduled_maintenance":
            return await self._provide_maintenance_schedule(analysis)
        elif analysis.query_scope == "outage_report":
            return await self._handle_outage_report(analysis, current_status)
        else:
            return await self._provide_general_info(analysis)
    
    async def _analyze_status_query(self, query: str, context: Dict[str, Any]) -> StatusQueryAnalysis:
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.get_system_prompt()),
            ("human", "Status query: {query}")
        ])
        
        structured_llm = self.get_structured_llm(StatusQueryAnalysis)
        chain = prompt | structured_llm
        
        return await chain.ainvoke({"query": query})
    
    async def _provide_current_status(self, analysis: StatusQueryAnalysis, current_status: Dict) -> AgentResponse:
        status_info = current_status.get("status", "operational")
        location = analysis.location_specific if analysis.location_specific != "general" else "all areas"
        
        if status_info == "operational":
            content = f"""✅ **{analysis.facility_type.title()} Status - {location.title()}:**

**Current Status:** All systems operational

**Last Updated:** {current_status.get('last_updated', 'Recently')}

**Performance:**
- {analysis.facility_type.title()}: Working normally
- No reported issues in {location}
- All services available

**Next Scheduled Check:** {current_status.get('next_check', 'Within 24 hours')}"""
            
            urgency = "low"
            
        elif status_info == "maintenance":
            content = f"""🔧 **{analysis.facility_type.title()} Status - {location.title()}:**

**Current Status:** Scheduled maintenance in progress

**Affected Areas:** {current_status.get('affected_areas', location)}
**Expected Duration:** {current_status.get('duration', '2-4 hours')}
**Expected Completion:** {current_status.get('completion_time', 'This evening')}

**Alternative Arrangements:**
{current_status.get('alternatives', 'Check with hostel office for temporary solutions')}

**Updates:** Check back in 2 hours for progress updates"""
            
            urgency = "medium"
            
        else:  # outage or issues
            content = f"""⚠️ **{analysis.facility_type.title()} Status - {location.title()}:**

**Current Status:** {status_info.title()} reported

**Affected Areas:** {current_status.get('affected_areas', location)}
**Issue Started:** {current_status.get('start_time', 'Recently')}
**Estimated Resolution:** {current_status.get('estimated_fix', 'Working on it')}

**What we're doing:**
{current_status.get('action_taken', 'Technical team has been notified and is working on the issue')}

**Emergency Contact:** {current_status.get('emergency_contact', 'Hostel office - [phone]')}"""
            
            urgency = "high" if analysis.urgency_indicator == "emergency_situation" else "medium"
        
        return AgentResponse(content=content, urgency=urgency)
    
    async def _provide_maintenance_schedule(self, analysis: StatusQueryAnalysis) -> AgentResponse:
        schedule = FacilityStatus.get_maintenance_schedule(analysis.facility_type)
        
        content = f"""📅 **Scheduled Maintenance - {analysis.facility_type.title()}:**

**This Week's Schedule:**
{schedule.get('this_week', 'No scheduled maintenance this week')}

**Next Week:**
{schedule.get('next_week', 'Schedule to be announced')}

**Regular Maintenance:**
{schedule.get('regular_schedule', 'Monthly checks on first Sunday')}

**How you'll be notified:**
- Notices posted 48 hours in advance
- WhatsApp group announcements
- Email notifications (if registered)

**During maintenance:**
- Temporary disruptions expected
- Alternative arrangements provided
- Emergency services remain available"""
        
        return AgentResponse(content=content, urgency="low")
    
    async def _handle_outage_report(self, analysis: StatusQueryAnalysis, current_status: Dict) -> AgentResponse:
        content = f"""📝 **Reporting {analysis.facility_type.title()} Issue:**

**Current Known Status:**
{current_status.get('status', 'No current issues reported')}

**To report a new issue:**
1. Note the exact location and time
2. Describe the problem clearly
3. Check if neighbors have the same issue
4. Contact hostel office immediately

**Emergency Contacts:**
- Hostel Office: [phone number]
- Security (24/7): [phone number]
- Maintenance: [phone number]

**For {analysis.facility_type} specifically:**
{FacilityStatus.get_reporting_guide(analysis.facility_type)}

**After reporting:**
- You'll receive a reference number
- Updates provided every 2-4 hours
- Estimated resolution time given"""
        
        next_steps = [
            "Contact hostel office with details",
            "Get a complaint reference number",
            "Check for updates every few hours",
            "Use emergency contact if urgent"
        ]
        
        urgency = "urgent" if analysis.urgency_indicator == "emergency_situation" else "high"
        
        return AgentResponse(
            content=content,
            next_steps=next_steps,
            urgency=urgency
        )
    
    async def _provide_general_info(self, analysis: StatusQueryAnalysis) -> AgentResponse:
        content = f"""ℹ️ **{analysis.facility_type.title()} Service Information:**

**Service Hours:**
{FacilityStatus.get_service_hours(analysis.facility_type)}

**Normal Operations:**
{FacilityStatus.get_normal_operations(analysis.facility_type)}

**Common Issues & Solutions:**
{FacilityStatus.get_troubleshooting_tips(analysis.facility_type)}

**Who to Contact:**
{FacilityStatus.get_contact_info(analysis.facility_type)}

**Service Standards:**
{FacilityStatus.get_service_standards(analysis.facility_type)}

Need specific current status? Ask me "What's the current {analysis.facility_type} status?" """
        
        return AgentResponse(content=content, urgency="low")