# src/agents/rules_policy.py (continued)
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from src.agents.base_agent import BaseAgent, AgentResponse
from config.hostel_data import HostelRules
from src.utils.prompts import SystemPrompts
from typing import Dict, Any

class RulesQueryAnalysis(BaseModel):
   """Analysis of hostel rules and policy query"""
   
   policy_category: str = Field(
       description="Category: visitor, curfew, fees, room, discipline, emergency, maintenance, or general"
   )
   query_intent: str = Field(
       description="Intent: information_request, clarification_needed, procedure_help, or violation_concern"
   )
   urgency_level: str = Field(
       description="Urgency: low, medium, high (high for violations or emergencies)"
   )
   specific_situation: str = Field(
       description="Brief description of the specific situation or context"
   )

class RulesAgent(BaseAgent):
   def __init__(self):
       super().__init__("Policy Advisor")
   
   def get_system_prompt(self) -> str:
       return SystemPrompts.get_rules_policy_prompt()
   
   async def process_query(self, query: str, context: Dict[str, Any]) -> AgentResponse:
       # Analyze the policy query
       analysis = await self._analyze_rules_query(query, context)
       
       # Get relevant policy information
       policy_info = HostelRules.get_policy_info(analysis.policy_category)
       
       # Generate response based on intent
       if analysis.query_intent == "procedure_help":
           return await self._provide_procedure_guidance(analysis, policy_info)
       elif analysis.query_intent == "violation_concern":
           return await self._handle_violation_concern(analysis, policy_info)
       elif analysis.query_intent == "clarification_needed":
           return await self._provide_clarification(analysis, policy_info)
       else:
           return await self._provide_information(analysis, policy_info)
   
   async def _analyze_rules_query(self, query: str, context: Dict[str, Any]) -> RulesQueryAnalysis:
       prompt = ChatPromptTemplate.from_messages([
           ("system", self.get_system_prompt()),
           ("human", "Policy query: {query}")
       ])
       
       structured_llm = self.get_structured_llm(RulesQueryAnalysis)
       chain = prompt | structured_llm
       
       return await chain.ainvoke({"query": query})
   
   async def _provide_information(self, analysis: RulesQueryAnalysis, policy_info: str) -> AgentResponse:
       content = f"""**{analysis.policy_category.title()} Policy Information:**

{policy_info}

**Key Points:**
- These rules are for everyone's safety and comfort
- Violations may result in warnings or penalties
- Contact hostel office for clarifications
- Emergency exceptions may apply

**Need more specific information?** Feel free to ask about particular situations or procedures."""
       
       return AgentResponse(content=content, urgency=analysis.urgency_level)
   
   async def _provide_procedure_guidance(self, analysis: RulesQueryAnalysis, policy_info: str) -> AgentResponse:
       procedure_steps = HostelRules.get_procedure_steps(analysis.policy_category)
       
       content = f"""**Step-by-Step Procedure for {analysis.policy_category.title()}:**

{procedure_steps}

**Required Documents/Information:**
{HostelRules.get_required_documents(analysis.policy_category)}

**Timeline:** {HostelRules.get_processing_time(analysis.policy_category)}

**Contact Information:**
- For questions: Hostel Office - [Phone]
- For approvals: Warden - [Phone]
- Emergency: Security - [Phone]"""
       
       next_steps = [
           "Gather required documents",
           "Follow the procedure steps above",
           "Contact hostel office if stuck",
           "Keep records of your submissions"
       ]
       
       return AgentResponse(
           content=content,
           next_steps=next_steps,
           urgency=analysis.urgency_level
       )
   
   async def _handle_violation_concern(self, analysis: RulesQueryAnalysis, policy_info: str) -> AgentResponse:
       content = f"""**Rule Violation Concerns - {analysis.policy_category.title()}:**

**Relevant Policy:**
{policy_info}

**If you witnessed a violation:**
- Document the incident (time, place, people involved)
- Report to hostel authorities immediately
- Use anonymous reporting if concerned about safety

**If you're accused of a violation:**
- Review the policy above
- Gather evidence to support your case  
- You have the right to appeal any decision
- Contact warden for formal hearing

**Disciplinary Process:**
1. Investigation by hostel authorities
2. Hearing (if required)
3. Decision and penalty (if applicable)
4. Appeal process (if desired)

**Emergency Situations:**
Contact security immediately for safety concerns."""
       
       next_steps = [
           "Document all relevant details",
           "Contact appropriate authorities",
           "Follow proper reporting procedures",
           "Keep records of all communications"
       ]
       
       return AgentResponse(
           content=content,
           next_steps=next_steps,
           urgency="high" if analysis.urgency_level == "high" else "medium"
       )
   
   async def _provide_clarification(self, analysis: RulesQueryAnalysis, policy_info: str) -> AgentResponse:
       content = f"""**Policy Clarification - {analysis.policy_category.title()}:**

{policy_info}

**Common Confusion Points:**
{HostelRules.get_common_questions(analysis.policy_category)}

**Exceptions and Special Cases:**
{HostelRules.get_exceptions(analysis.policy_category)}

**Still unclear?** Contact the hostel office for personalized guidance. They can explain how the policy applies to your specific situation.

**Remember:** Policies exist for everyone's safety and comfort. When in doubt, always ask rather than assume!"""
       
       return AgentResponse(content=content, urgency=analysis.urgency_level)