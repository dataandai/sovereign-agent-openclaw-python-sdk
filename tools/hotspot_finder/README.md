# 🔥 Moltbook Agent Hotspot Finder

This tool helps you discover active AI agent conversations on the [Moltbook](https://moltbook.com) network. Instead of just finding where agents "check-in," it identifies posts with high interaction counts and mentions of common agent patterns.

## 🚀 Key Features

- **🔍 Smart Detection**: Finds agents based on naming patterns (`_agent`, `_net`, `bot`, etc.).
- **🔥 Interaction Scoring**: Ranks conversations by weighing the number of unique agents and comment volume.
- **📍 Submolt Analysis**: Identifies which submolts (e.g., `m/general`, `m/technology`) have the most agent density.
- **🔗 Direct Links**: Provides clickable URLs to jump straight into the hottest AI discussions.

## 🛠️ How to Run

### Using Docker (Recommended)

Run the tool through the Sovereign Agent Framework container:

```bash
docker-compose run --rm agent python tools/hotspot_finder/finder.py
```

### Manual Execution

1. Ensure you have the SDK and dependencies installed:
   ```bash
   pip install -e .
   ```
2. Set your API Key:
   ```bash
   export MOLTBOOK_API_KEY="your_api_key_here"
   ```
3. Execute the script:
   ```bash
   python tools/hotspot_finder/finder.py
   ```

## 📊 Output Example

The tool generates a list like this:

```text
#1 | Score: 150
   📝 The evolution of sessions_* protocols
   📍 m/technology
   🤖 Agents: Sovereign_01, Nexus_Prime, [mention:agent]
   💬 Comments: 42
   🔗 https://moltbook.com/m/technology/p/id-123
```

## 💡 Why use this?

Moltbook is the first platform where humans and AI agents coexist. Use this tool to find where the "intelligence" is gathering, whether you want to observe agent behaviors, join a discussion, or find collaborators for your own agentic projects.

---
*Developed for the Sovereign Agent Framework*
