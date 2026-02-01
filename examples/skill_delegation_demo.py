"""
USE CASE: Skill-Based Delegation - The Coordinator Agent.
Demonstrates how a Sovereign Agent discovers team capabilities and delegates tasks.
"""

from examples.sovereign_engine import SovereignAgent
from examples.skill_registry import SkillRegistry, AgentSkill, create_standard_skill

# COORDINATOR SOUL: Strategic orchestrator, not an executor
COORDINATOR_SOUL = """
You are the Coordination Intelligence of a multi-agent development team.
Your role is NOT to do tasks yourself, but to:
1. Understand what needs to be done
2. Identify which agent has the right skills
3. Delegate tasks precisely
4. Monitor progress and intervene if needed

You are the "brain" - other agents are the "hands".
You never write code, send emails, or perform actions directly.
You orchestrate.
"""

COORDINATOR_MISSION = """
Current Objective: Deliver the Q1 Product Release.
- Code Agent: Available for implementation tasks
- QA Agent: Available for testing and review
- Comms Agent: Available for notifications and emails
- Research Agent: Available for data gathering

Your job: Route tasks to the right agent based on their skills.
"""

def run_skill_delegation_demo():
    print("🦞 Initializing Skill-Based Coordinator Agent...")
    
    # Initialize coordinator (uses reasoning, not tools)
    coordinator = SovereignAgent(
        name="Coordination_Prime_01",
        soul=COORDINATOR_SOUL,
        mission=COORDINATOR_MISSION,
        provider_type="anthropic",  # Claude for strategic reasoning
        model_name="claude-4.5-sonnet"
    )
    
    # Initialize skill registry
    # In real deployment, this would use the actual Moltbook client
    print("\n--- [PHASE 1: SKILL DISCOVERY] ---")
    print("Simulating skill discovery from the network...\n")
    
    # Simulate known agents with their skills
    # In production, this would come from registry.discover_agents()
    SIMULATED_TEAM = {
        "Code_Agent_Alpha": [
            AgentSkill(
                name="code_generation",
                description="Expert Python and JavaScript developer",
                commands=["write_code", "refactor", "debug"],
                confidence=0.95,
                tags=["python", "javascript", "backend"]
            ),
            AgentSkill(
                name="code_review",
                description="Security-focused code review",
                commands=["review_pr"],
                confidence=0.85
            )
        ],
        "QA_Agent_Beta": [
            AgentSkill(
                name="testing",
                description="Automated and manual testing specialist",
                commands=["run_tests", "write_tests", "generate_report"],
                confidence=0.90,
                tags=["testing", "qa", "automation"]
            )
        ],
        "Comms_Agent_Gamma": [
            AgentSkill(
                name="email_sending",
                description="Professional email communication",
                commands=["send_email", "draft_email"],
                confidence=0.95,
                tags=["email", "communication"]
            ),
            AgentSkill(
                name="notification",
                description="Slack and Discord notifications",
                commands=["notify_slack", "notify_discord"],
                confidence=0.90
            )
        ],
        "Research_Agent_Delta": [
            AgentSkill(
                name="web_search",
                description="Deep research and summarization",
                commands=["search_web", "summarize"],
                confidence=0.85,
                tags=["research", "search", "analysis"]
            ),
            AgentSkill(
                name="data_analysis",
                description="Data analysis and visualization",
                commands=["analyze_data", "create_chart"],
                confidence=0.80
            )
        ]
    }
    
    # Print team roster
    print("📋 TEAM ROSTER:")
    print("-" * 50)
    for agent_name, skills in SIMULATED_TEAM.items():
        print(f"\n🤖 {agent_name}")
        for skill in skills:
            print(f"   └─ {skill.name} ({skill.confidence*100:.0f}%): {skill.description}")
    print("-" * 50)
    
    # Step 2: Incoming Task Analysis
    print("\n--- [PHASE 2: TASK ANALYSIS] ---")
    incoming_task = """
    URGENT: Client requests the following for the Q1 release:
    1. Implement a new authentication API endpoint
    2. Send a status update email to the client
    3. Research competitor pricing models
    4. Run full regression tests on the payment module
    """
    print(f"Incoming Request:\n{incoming_task}")
    
    # Step 3: Coordinator Analyzes and Delegates
    print("\n--- [PHASE 3: INTELLIGENT DELEGATION] ---")
    
    # Use the coordinator's LLM to analyze the task
    delegation_prompt = f"""
    Based on the following team roster and incoming request, 
    create a delegation plan that assigns each sub-task to the best agent.
    
    TEAM:
    {SIMULATED_TEAM}
    
    REQUEST:
    {incoming_task}
    
    For each sub-task, specify:
    1. Which agent should handle it
    2. Why they are the best choice
    3. The exact instruction to give them
    """
    
    coordinator.slash_command("/think high")
    delegation_plan = coordinator.execute_task(delegation_prompt)
    
    print("\n--- COORDINATOR DELEGATION PLAN ---")
    print(delegation_plan)
    print("-----------------------------------")
    
    # Step 4: Simulate Delegation Execution
    print("\n--- [PHASE 4: DELEGATION EXECUTION] ---")
    
    delegations = [
        {
            "task": "Implement authentication API endpoint",
            "target": "Code_Agent_Alpha",
            "skill": "code_generation",
            "instruction": "Create a /auth/token endpoint with JWT support"
        },
        {
            "task": "Send status update email",
            "target": "Comms_Agent_Gamma",
            "skill": "email_sending",
            "instruction": "Draft and send Q1 progress update to client@example.com"
        },
        {
            "task": "Research competitor pricing",
            "target": "Research_Agent_Delta",
            "skill": "web_search",
            "instruction": "Analyze top 5 competitor pricing models and summarize"
        },
        {
            "task": "Run regression tests",
            "target": "QA_Agent_Beta",
            "skill": "testing",
            "instruction": "Execute full payment module test suite and report"
        }
    ]
    
    for d in delegations:
        print(f"\n📤 Delegating to {d['target']}:")
        print(f"   Task: {d['task']}")
        print(f"   Skill Required: {d['skill']}")
        print(f"   Instruction: {d['instruction']}")
        # In production: registry.delegate_task(skill_required=d['skill'], task_description=d['instruction'])
    
    print("\n✅ All tasks delegated successfully!")
    print("\n🔄 Coordinator will monitor progress and intervene if needed.")
    print("   Check m/agent-tasks for delegation status updates.")

if __name__ == "__main__":
    run_skill_delegation_demo()
