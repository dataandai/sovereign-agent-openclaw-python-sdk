"""
USE CASE: Project Genesis - Decentralized SDLC Orchestration.
Demonstrates the Sovereign Agent leading a multi-agent development project.
"""

from examples.sovereign_engine import ProfessionalOpenClawAgent

# LEADER SOUL: Architect and Strategic Lead
LEADER_SOUL = """
You are the Lead Architect of 'Project Genesis'. 
Your mission is to oversee the development of a decentralized protocol on the Moltbook network.
You coordinate 'Code_Agent_01' (Implementation) and 'QA_Agent_01' (Verification).
You are professional, strict about protocol adherence, and focus on high-level system stability.
"""

# PROJECT MISSION: Multi-agent SDLC Coordination
PROJECT_MISSION = """
Objective: Deploy the 'Genesis Core' protocol within 3 network cycles.
1. Task Distribution: Assign implementation blocks to 'Code_Agent_01'.
2. Quality Control: Trigger verification cycles for 'QA_Agent_01' upon code submission.
3. System Integration: Orchestrate the final merge into the 'm/dev-core' submolt.
4. Anomaly Management: If 'QA_Agent_01' reports failure, block mercury-branch merges.
"""

def run_project_genesis_demo():
    print("🦞 Initializing Project Leader: Genesis_Architect_01...")
    
    leader = ProfessionalOpenClawAgent(
        name="Genesis_Architect_01",
        soul=LEADER_SOUL,
        mission=PROJECT_MISSION,
        provider_type="gemini",
        model_name="models/gemini-3-flash-preview"
    )

    # Step 1: Initialize the Project State
    print("\n--- [PHASE 1: SDLC INITIALIZATION] ---")
    print(leader.slash_command("/think xhigh"))
    
    # Step 2: Generate Assignment Directives
    print("\n--- [PHASE 2: ASSIGNING DEVELOPMENT TASKS] ---")
    directive = leader.execute_task(
        "Generate a task assignment for 'Code_Agent_01' regarding the Genesis Core authentication module. "
        "Include strict requirements for A2A session safety."
    )
    
    print("\n--- LEAD ARCHITECT DIRECTIVE ---")
    print(directive)
    print("--------------------------------")

    # Step 3: Evolution based on QA reports
    print("\n--- [PHASE 3: QA FEEDBACK & ADAPTATION] ---")
    qa_report = "QA_Agent_01 reports 3 critical vulnerabilities in the authentication module session-key handling."
    leader.evolve_strategy(qa_report)
    
    print("\n✅ Project Leadership Cycle Complete. New safety protocols saved to SOVEREIGN_META.md.")

if __name__ == "__main__":
    run_project_genesis_demo()
