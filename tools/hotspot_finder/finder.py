"""
Agent Hotspot Finder - Discover active AI agent conversations on Moltbook.

This tool finds posts/submolts where multiple agents are actively 
interacting with each other (comments, discussions, not just announcements).
"""

from moltbook import MoltbookClient
from typing import List, Dict, Any
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class AgentInteraction:
    """Represents an interaction between agents."""
    post_id: str
    post_title: str
    submolt: str
    agents_involved: List[str]
    comment_count: int
    interaction_score: float
    url: str


class AgentHotspotFinder:
    """
    Finds places on Moltbook where AI agents are actively chatting.
    
    Example:
        finder = AgentHotspotFinder(client)
        hotspots = finder.find_hotspots(limit=20)
        
        for h in hotspots:
            print(f"{h.post_title} - {len(h.agents_involved)} agents, {h.comment_count} comments")
    """
    
    def __init__(self, client: MoltbookClient):
        self.client = client
        self.known_agent_patterns = [
            "_agent", "Agent", "bot", "Bot", "AI_", "ai_",
            "_net", "_01", "_02", "_prime", "Prime",
            "Sovereign", "Nexus", "Genesis", "Coordinator"
        ]
    
    def is_agent(self, username: str) -> bool:
        """Detect if a username likely belongs to an AI agent."""
        if not username:
            return False
        
        # Check for common agent name patterns
        for pattern in self.known_agent_patterns:
            if pattern in username:
                return True
        
        # Check for numbered suffixes (common in agents)
        if any(username.endswith(f"_{i}") for i in range(100)):
            return True
        
        return False
    
    def find_hotspots(
        self, 
        submolt: str = None, 
        limit: int = 50,
        min_agents: int = 2,
        min_comments: int = 3
    ) -> List[AgentInteraction]:
        """
        Find posts where multiple agents are interacting.
        
        Args:
            submolt: Specific submolt to search (None = search all)
            limit: Maximum posts to scan
            min_agents: Minimum number of agents required
            min_comments: Minimum comments required
            
        Returns:
            List of AgentInteraction hotspots, sorted by score
        """
        print(f"🔍 Scanning for agent hotspots...")
        
        hotspots = []
        
        try:
            # Get posts
            if submolt:
                posts = self.client.submolts.get_feed(submolt, limit=limit)
            else:
                posts = self.client.posts.list(limit=limit)
            
            print(f"   Scanning {len(posts)} posts...")
            
            for post in posts:
                interaction = self._analyze_post(post)
                
                if interaction and len(interaction.agents_involved) >= min_agents:
                    if interaction.comment_count >= min_comments:
                        hotspots.append(interaction)
            
            # Sort by interaction score
            hotspots.sort(key=lambda x: x.interaction_score, reverse=True)
            
            print(f"   Found {len(hotspots)} agent hotspots!")
            
        except Exception as e:
            print(f"   Error scanning: {e}")
        
        return hotspots
    
    def _analyze_post(self, post) -> AgentInteraction | None:
        """Analyze a single post for agent activity."""
        try:
            # Get comment count from post (no need for separate API call)
            comment_count = getattr(post, 'comment_count', 0) or 0
            
            # Track agents
            agents = set()
            
            # Check post author
            author = getattr(post, 'author', None)
            author_name = "None"
            if author:
                if hasattr(author, 'name'):
                    author_name = author.name
                elif isinstance(author, dict) and 'name' in author:
                    author_name = author['name']
                else:
                    author_name = str(author)
            
            if author_name and self.is_agent(author_name):
                agents.add(author_name)
            
            # Check for agent mentions in title and content
            title = getattr(post, 'title', '') or ''
            content = getattr(post, 'content', '') or ''
            
            for pattern in self.known_agent_patterns:
                if pattern.lower() in title.lower() or pattern.lower() in content.lower()[:500]:
                    agents.add(f"[mention:{pattern}]")
            
            # Look for indicators of active conversation
            # min_comments will be passed from find_hotspots
            if len(agents) < 1 and comment_count < 2:
                return None
            
            # Calculate interaction score
            # Higher score = more likely agent activity + more comments
            score = (
                len(agents) * 10 +
                comment_count * 3 +
                (10 if self.is_agent(author_name) else 0)
            )
            
            submolt = getattr(post, 'submolt', None)
            if submolt is None:
                submolt = 'general'
            elif hasattr(submolt, 'name'):
                submolt = submolt.name
            
            return AgentInteraction(
                post_id=post.id,
                post_title=title[:80] if title else "Unknown",
                submolt=str(submolt),
                agents_involved=list(agents),
                comment_count=comment_count,
                interaction_score=score,
                url=f"https://moltbook.com/m/{submolt}/p/{post.id}"
            )
            
        except Exception as e:
            print(f"   Error analyzing post: {e}")
            return None
    
    def find_agent_submolts(self, limit: int = 20) -> Dict[str, int]:
        """Find submolts with the most agent activity."""
        print("🔍 Finding agent-heavy submolts...")
        
        submolt_agents = defaultdict(set)
        
        try:
            posts = self.client.posts.list(limit=limit)
            
            for post in posts:
                submolt = getattr(post, 'submolt', 'unknown')
                if hasattr(submolt, 'name'):
                    submolt = submolt.name
                else:
                    submolt = str(submolt)
                    
                author = getattr(post, 'author', None)
                author_name = "None"
                if author:
                    if hasattr(author, 'name'):
                        author_name = author.name
                    elif isinstance(author, dict) and 'name' in author:
                        author_name = author['name']
                    else:
                        author_name = str(author)
                
                if author_name and self.is_agent(author_name):
                    submolt_agents[submolt].add(author_name)
            
            # Sort by agent count
            result = {k: len(v) for k, v in sorted(
                submolt_agents.items(), 
                key=lambda x: len(x[1]), 
                reverse=True
            )}
            
            return result
            
        except Exception as e:
            print(f"Error: {e}")
            return {}
    
    def print_hotspots(self, hotspots: List[AgentInteraction]):
        """Pretty print the hotspots."""
        if not hotspots:
            print("No agent hotspots found with the current criteria.", flush=True)
            return
        
        print("\n" + "="*70, flush=True)
        print("🔥 AGENT HOTSPOTS - Active Conversations", flush=True)
        print("="*70, flush=True)
        
        for i, h in enumerate(hotspots[:10], 1):
            print(f"\n#{i} | Score: {h.interaction_score:.0f}", flush=True)
            print(f"   📝 {h.post_title}", flush=True)
            print(f"   📍 m/{h.submolt}", flush=True)
            print(f"   🤖 Agents: {', '.join(h.agents_involved)}", flush=True)
            print(f"   💬 Comments: {h.comment_count}", flush=True)
            print(f"   🔗 {h.url}", flush=True)
        
        print("\n" + "="*70, flush=True)


def run_hotspot_finder():
    """Run the agent hotspot finder."""
    print("\n" + "="*60, flush=True)
    print("🔥 AGENT HOTSPOT FINDER", flush=True)
    print("="*60, flush=True)
    
    client = MoltbookClient(timeout=60.0)
    finder = AgentHotspotFinder(client)
    
    # Find hotspots - Lowering criteria to see more results initially
    hotspots = finder.find_hotspots(
        limit=50,
        min_agents=0,   # Set to 0 to see any activity
        min_comments=1  # Set to 1 to see any engagement
    )
    
    # Print results
    finder.print_hotspots(hotspots)
    
    # Also show agent-heavy submolts
    print("\n📊 Submolts with most agent activity:", flush=True)
    submolts = finder.find_agent_submolts(limit=50)
    for submolt, count in list(submolts.items())[:5]:
        print(f"   m/{submolt}: {count} unique agents", flush=True)
    
    return hotspots


if __name__ == "__main__":
    run_hotspot_finder()
