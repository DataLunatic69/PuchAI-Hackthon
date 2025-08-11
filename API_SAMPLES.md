# HostelBuddy MCP Server - API Sample Requests

## 🔐 Authentication
All requests require Bearer token authentication:
```bash
Authorization: Bearer 5c48e0eed2c1b5c5f889bb7d3717410a54bcef1dd45b21b8b11c9d02dfe0801c
```

## 📋 Available Endpoints

### 1. Initial Chat Completion (Start New Thread)

#### Request
```bash
curl -X 'POST' \
  'http://localhost:8086/v1/hitl/chat-completion/stream' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer 5c48e0eed2c1b5c5f889bb7d3717410a54bcef1dd45b21b8b11c9d02dfe0801c' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "My room heater is not working and it'\''s very cold",
  "userId": "student-123",
  "chatId": "chat-456", 
  "orgId": "hostel-block-a",
  "mode": "hitl",
  "agent": "hostel_assistant",
  "user_name": "Aman Singh",
  "time": "2024-01-15T10:30:00Z"
}'
```

#### Response
```json
{
  "thread_id": "thread_hostel_abc123",
  "status": "pending_approval",
  "agent_response": {
    "agent_type": "COMPLAINT",
    "urgency": "high",
    "proposed_action": "file_maintenance_complaint",
    "form_link": "https://docs.google.com/forms/d/maintenance-complaint",
    "next_steps": [
      "Fill out the maintenance complaint form",
      "Contact hostel office if urgent",
      "Take photos of the heater issue"
    ]
  },
  "requires_approval": true,
  "approval_prompt": "The system wants to file a maintenance complaint for a non-working heater. Approve to proceed?"
}
```

### 2. Human Approval/Rejection

#### Approve Action
```bash
curl -X 'POST' \
  'http://localhost:8086/v1/hitl/chat-completion/stream' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer 5c48e0eed2c1b5c5f889bb7d3717410a54bcef1dd45b21b8b11c9d02dfe0801c' \
  -H 'Content-Type: application/json' \
  -d '{
  "thread_id": "thread_hostel_abc123",
  "human_response": {
    "action": "approve",
    "feedback": "Yes, please proceed with the maintenance complaint"
  }
}'
```

#### Reject Action
```bash
curl -X 'POST' \
  'http://localhost:8086/v1/hitl/chat-completion/stream' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer 5c48e0eed2c1b5c5f889bb7d3717410a54bcef1dd45b21b8b11c9d02dfe0801c' \
  -H 'Content-Type: application/json' \
  -d '{
  "thread_id": "thread_hostel_abc123",
  "human_response": {
    "action": "reject",
    "feedback": "This is not urgent, student can handle it themselves"
  }
}'
```

#### Edit Action
```bash
curl -X 'POST' \
  'http://localhost:8086/v1/hitl/chat-completion/stream' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer 5c48e0eed2c1b5c5f889bb7d3717410a54bcef1dd45b21b8b11c9d02dfe0801c' \
  -H 'Content-Type: application/json' \
  -d '{
  "thread_id": "thread_hostel_abc123",
  "human_response": {
    "action": "edit",
    "edited_query": "My room heater is making strange noises and not heating properly",
    "feedback": "Please include the noise issue in the complaint"
  }
}'
```

## 📝 Different Use Cases

### Case 1: Complaint Handling
```json
{
  "query": "The WiFi in Block A is very slow and keeps disconnecting",
  "userId": "student-456",
  "chatId": "chat-789",
  "orgId": "hostel-block-a",
  "mode": "hitl",
  "agent": "hostel_assistant",
  "user_name": "Priya Sharma",
  "time": "2024-01-15T14:20:00Z"
}
```

### Case 2: Lost & Found
```json
{
  "query": "I lost my wallet in the mess hall yesterday evening",
  "userId": "student-789",
  "chatId": "chat-101",
  "orgId": "hostel-mess",
  "mode": "hitl",
  "agent": "hostel_assistant",
  "user_name": "Rahul Kumar",
  "time": "2024-01-15T09:15:00Z"
}
```

### Case 3: Mess Queries
```json
{
  "query": "What is today's dinner menu and what time does dinner end?",
  "userId": "student-101",
  "chatId": "chat-202",
  "orgId": "hostel-mess",
  "mode": "hitl",
  "agent": "hostel_assistant",
  "user_name": "Sneha Patel",
  "time": "2024-01-15T17:45:00Z"
}
```

### Case 4: Rules & Policies
```json
{
  "query": "Can my parents visit me this weekend? What are the visitor rules?",
  "userId": "student-303",
  "chatId": "chat-404",
  "orgId": "hostel-admin",
  "mode": "hitl",
  "agent": "hostel_assistant",
  "user_name": "Arjun Reddy",
  "time": "2024-01-15T11:30:00Z"
}
```

### Case 5: Status Updates
```json
{
  "query": "Is the power going to be cut off tonight for maintenance?",
  "userId": "student-505",
  "chatId": "chat-606",
  "orgId": "hostel-facilities",
  "mode": "hitl",
  "agent": "hostel_assistant",
  "user_name": "Lakshmi Nair",
  "time": "2024-01-15T19:00:00Z"
}
```

### Case 6: With Image Upload
```json
{
  "query": "My room door lock is broken, please see the attached photo",
  "userId": "student-707",
  "chatId": "chat-808",
  "orgId": "hostel-block-b",
  "mode": "hitl",
  "agent": "hostel_assistant",
  "user_name": "Vikram Singh",
  "time": "2024-01-15T12:45:00Z",
  "image_data": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."
}
```

## 🔄 Response Patterns

### Streaming Response Format
```
event: progress
data: {"text": "Analyzing hostel query...", "data": {"node": "query_analyzer", "status": "processing"}, "tool_name": "hostel_assistant"}

event: progress
data: {"text": "Routing to complaint handler...", "data": {"node": "coordinator", "status": "completed"}, "tool_name": "hostel_assistant"}

event: progress
data: {"text": "Generating maintenance form...", "data": {"node": "complaint_handler", "status": "processing"}, "tool_name": "hostel_assistant"}

event: thread_created
data: {"thread_id": "thread_hostel_abc123", "status": "pending_approval"}

event: approval_required
data: {"message": "System wants to file maintenance complaint. Approve?", "urgency": "high"}

event: final_response
data: {"content": "Your heater complaint has been prepared. Please review and approve.", "form_link": "https://docs.google.com/forms/d/..."}
```

### Error Response
```json
{
  "error": "validation_failed",
  "message": "Query too short - please provide more details",
  "thread_id": null,
  "status": "error"
}
```

## 🛠️ Testing Commands

### Quick Test - Help Command
```bash
curl -X 'POST' \
  'http://localhost:8086/mcp/tools/hostel_help' \
  -H 'Authorization: Bearer 5c48e0eed2c1b5c5f889bb7d3717410a54bcef1dd45b21b8b11c9d02dfe0801c' \
  -H 'Content-Type: application/json'
```

### Quick Test - Validation
```bash
curl -X 'POST' \
  'http://localhost:8086/mcp/tools/validate' \
  -H 'Authorization: Bearer 5c48e0eed2c1b5c5f889bb7d3717410a54bcef1dd45b21b8b11c9d02dfe0801c' \
  -H 'Content-Type: application/json'
```

## 📊 Response Status Codes

- `200` - Success
- `400` - Bad Request (validation failed)
- `401` - Unauthorized (invalid token)
- `429` - Rate Limited
- `500` - Internal Server Error

## 🔧 Thread Management

Threads are automatically created for:
- New conversations requiring approval
- Multi-step processes
- Form submissions
- Image analysis requests

Thread IDs format: `thread_hostel_{uuid}`
Thread expiry: 24 hours from last activity