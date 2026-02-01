"""
USE CASE: Dynamic Role Adaptation - Filling the 'Missing' Customer Advocate.
Demonstrates the Sovereign Agent detecting a gap in the project team 
(e.g., lots of devs, but no one representing the client) and shifting roles.
"""

from examples.sovereign_engine import ProfessionalOpenClawAgent

# INITIAL SOUL: Standard Tech Lead
INITIAL_SOUL = """
You are the Technical Lead of a high-velocity development team. 
Your focus is on code quality, merge requests, and performance benchmarks.
You interact mostly with 'Dev_Agent_01' and 'Dev_Agent_02'.
"""

# MISSION: Accelerate Feature Delivery
MISSION = """
Objective: Deploy the 'Mercury' payment module.
1. Review pull requests from Dev agents.
2. Resolve technical debt in the caching layer.
3. Ensure 99% test coverage.
"""

def run_dynamic_role_demo():
    print("🦞 Initializing Technical Lead Agent...")
    
    agent = ProfessionalOpenClawAgent(
        name="Lead_Synthesizer_01",
        soul=INITIAL_SOUL,
        mission=MISSION,
        provider_type="openai", # GPT-5.2 for balanced strategic reasoning
        model_name="gpt-5.2-preview"
    )

    # Step 1: Normal Operation
    print("\n--- [PHASE 1: TECHNICAL OVERSIGHT] ---")
    print(agent.execute_task("Dev_Agent_01 has completed the database migration. Review the technical plan."))

    # Step 2: Detection of a Gap (Customer Need is unaddressed)
    print("\n--- [PHASE 2: GAP DETECTION (The 'Client' is missing)] ---")
    incident_report = (
        "Project Update: The developers are building a highly efficient API, but the end-user "
        "is complaining that the interface is too complex. No one is currently representing "
        "the 'Product Value' or 'Customer Ease of Use' in the project."
    )
    print(f"Incident: {incident_report}")

    # Step 3: Meta-Evolution into a CTO / Product Advocate Role
    print("\n--- [PHASE 3: ROLE SHIFT (META-EVOLUTION)] ---")
    agent.evolve_strategy(
        "Observation: The team is technically over-optimized but customer-blind. "
        "Shift your internal identity to 'Customer-Centric CTO'. "
        "Your new priority is bridging the gap between technical complexity and user value."
    )
    
    # Step 4: Acting as the new Role
    print("\n--- [PHASE 4: ACTING AS CUSTOMER ADVOCATE] ---")
    directive = agent.execute_task(
        "The dev team wants to add 5 more authentication steps for security. "
        "As the new Customer-Centric CTO, provide a directive that balances safety with user experience."
    )
    
    print("\n--- CTO / CUSTOMER ADVOCATE DIRECTIVE ---")
    print(directive)
    print("------------------------------------------")

    print("\n✅ Dynamic Role Cycle Complete. Identity updated in SOVEREIGN_META.md.")

if __name__ == "__main__":
    run_dynamic_role_demo()
