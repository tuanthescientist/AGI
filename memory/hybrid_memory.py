"""
Hybrid Memory System for AGI
Combines: Vector DB (semantic), Graph DB (knowledge), Episodic, Procedural, Working
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import logging
import json
import numpy as np
from collections import defaultdict

logger = logging.getLogger(__name__)


@dataclass
class Memory:
    """Base memory entry"""
    key: str
    content: Any
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[np.ndarray] = None
    reflection: Optional[str] = None


@dataclass
class Episode:
    """Episodic memory: trajectory with reflection"""
    episode_id: str
    steps: List[Dict[str, Any]]
    outcome: str
    timestamp: datetime = field(default_factory=datetime.now)
    reflection: Optional[str] = None
    success: bool = True


class VectorMemory:
    """Semantic memory with vector embeddings (simulated - use Chroma/Qdrant in prod)"""
    
    def __init__(self, embedding_dim: int = 768):
        self.embedding_dim = embedding_dim
        self.memories: Dict[str, Memory] = {}
        self.embeddings_index = {}  # key -> embedding
        
    def store(self, key: str, content: Any, embedding: Optional[np.ndarray] = None,
             metadata: Optional[Dict] = None):
        """Store semantic memory"""
        if embedding is None:
            # Simulate embedding (in prod: use real embedder)
            embedding = np.random.randn(self.embedding_dim)
        
        memory = Memory(
            key=key,
            content=content,
            embedding=embedding,
            metadata=metadata or {}
        )
        self.memories[key] = memory
        self.embeddings_index[key] = embedding
        logger.info(f"Stored semantic memory: {key}")
    
    def search_similar(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Tuple[str, float]]:
        """Semantic search"""
        similarities = []
        for key, emb in self.embeddings_index.items():
            # Cosine similarity
            sim = np.dot(query_embedding, emb) / (np.linalg.norm(query_embedding) * np.linalg.norm(emb) + 1e-8)
            similarities.append((key, sim))
        
        return sorted(similarities, key=lambda x: x[1], reverse=True)[:top_k]
    
    def retrieve(self, key: str) -> Optional[Memory]:
        """Retrieve by key"""
        return self.memories.get(key)
    
    def consolidate(self):
        """Consolidate memories (remove duplicates, merge similar)"""
        logger.info(f"Consolidating {len(self.memories)} semantic memories")
        # Could implement clustering, deduplication, etc.


class GraphMemory:
    """Knowledge graph memory (using dict structure, can integrate Neo4j)"""
    
    def __init__(self):
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: List[Dict[str, Any]] = []
        self.relationships: defaultdict = defaultdict(list)
        
    def add_concept(self, concept: str, properties: Dict[str, Any]):
        """Add concept to knowledge graph"""
        self.nodes[concept] = properties
        logger.info(f"Added concept: {concept}")
    
    def add_relationship(self, source: str, target: str, relation_type: str, 
                        properties: Optional[Dict] = None):
        """Add relationship between concepts"""
        edge = {
            'source': source,
            'target': target,
            'type': relation_type,
            'properties': properties or {},
            'timestamp': datetime.now()
        }
        self.edges.append(edge)
        self.relationships[source].append((target, relation_type))
        logger.info(f"Added relation: {source} --[{relation_type}]--> {target}")
    
    def infer(self, concept: str, max_depth: int = 2) -> Dict[str, List[str]]:
        """Graph-based inference/traversal"""
        results = {}
        visited = set()
        
        def traverse(node: str, depth: int):
            if depth > max_depth or node in visited:
                return
            visited.add(node)
            
            for target, rel_type in self.relationships[node]:
                if rel_type not in results:
                    results[rel_type] = []
                results[rel_type].append(target)
                traverse(target, depth + 1)
        
        traverse(concept, 0)
        return results
    
    def get_neighbors(self, concept: str) -> List[Tuple[str, str]]:
        """Get immediate neighbors"""
        return self.relationships.get(concept, [])


class EpisodicMemory:
    """Episodic memory: experiences with reflection"""
    
    def __init__(self):
        self.episodes: Dict[str, Episode] = {}
        self.trajectory_history: List[Episode] = []
        
    def record_episode(self, episode_id: str, steps: List[Dict], 
                      outcome: str, success: bool = True, reflection: Optional[str] = None):
        """Record a complete episode/trajectory"""
        episode = Episode(
            episode_id=episode_id,
            steps=steps,
            outcome=outcome,
            success=success,
            reflection=reflection
        )
        self.episodes[episode_id] = episode
        self.trajectory_history.append(episode)
        logger.info(f"Recorded episode: {episode_id} (success={success})")
    
    def retrieve_by_outcome(self, outcome: str) -> List[Episode]:
        """Retrieve episodes by outcome"""
        return [ep for ep in self.trajectory_history if outcome in ep.outcome]
    
    def get_success_rate(self) -> float:
        """Calculate success rate"""
        if not self.trajectory_history:
            return 0.0
        successful = sum(1 for ep in self.trajectory_history if ep.success)
        return successful / len(self.trajectory_history)
    
    def reflect_on_episode(self, episode_id: str) -> str:
        """Generate reflection on episode"""
        if episode_id not in self.episodes:
            return ""
        
        episode = self.episodes[episode_id]
        reflection = f"Episode {episode_id}: {len(episode.steps)} steps, Outcome: {episode.outcome}, Success: {episode.success}"
        return reflection


class ProceduralMemory:
    """Procedural memory: skills, tool usage, and success patterns"""
    
    def __init__(self):
        self.skills: Dict[str, Dict[str, Any]] = {}
        self.tool_usage: Dict[str, Dict[str, Any]] = {}
        
    def register_skill(self, skill_name: str, procedure: str, success_rate: float = 0.0):
        """Register a skill/procedure"""
        self.skills[skill_name] = {
            'procedure': procedure,
            'usage_count': 0,
            'success_count': 0,
            'success_rate': success_rate,
            'learned_at': datetime.now()
        }
        logger.info(f"Registered skill: {skill_name}")
    
    def record_tool_usage(self, tool_name: str, success: bool, execution_time: float = 0.0):
        """Record tool usage"""
        if tool_name not in self.tool_usage:
            self.tool_usage[tool_name] = {
                'usage_count': 0,
                'success_count': 0,
                'total_time': 0.0,
                'last_used': None
            }
        
        self.tool_usage[tool_name]['usage_count'] += 1
        if success:
            self.tool_usage[tool_name]['success_count'] += 1
        self.tool_usage[tool_name]['total_time'] += execution_time
        self.tool_usage[tool_name]['last_used'] = datetime.now()
    
    def get_best_tools(self, top_k: int = 5) -> List[Tuple[str, float]]:
        """Get most reliable tools"""
        tool_scores = []
        for tool_name, stats in self.tool_usage.items():
            if stats['usage_count'] > 0:
                success_rate = stats['success_count'] / stats['usage_count']
                tool_scores.append((tool_name, success_rate))
        
        return sorted(tool_scores, key=lambda x: x[1], reverse=True)[:top_k]


class WorkingMemory:
    """Short-term/working memory: current context"""
    
    def __init__(self, capacity: int = 10):
        self.capacity = capacity
        self.context: List[Dict[str, Any]] = []
        
    def add(self, item: Dict[str, Any]):
        """Add to working memory"""
        self.context.append(item)
        if len(self.context) > self.capacity:
            self.context.pop(0)  # FIFO eviction
    
    def get_context(self) -> str:
        """Get current context as string"""
        if not self.context:
            return ""
        return "\n".join([str(item) for item in self.context])
    
    def clear(self):
        """Clear working memory"""
        self.context = []


class HybridMemorySystem:
    """Unified hybrid memory system"""
    
    def __init__(self, vector_dim: int = 768, working_memory_capacity: int = 10):
        self.semantic = VectorMemory(embedding_dim=vector_dim)
        self.knowledge_graph = GraphMemory()
        self.episodic = EpisodicMemory()
        self.procedural = ProceduralMemory()
        self.working = WorkingMemory(capacity=working_memory_capacity)
        
        self.consolidation_interval = 100  # Consolidate every N operations
        self.operation_count = 0
        
    def store_semantic(self, key: str, content: Any, embedding: Optional[np.ndarray] = None,
                      metadata: Optional[Dict] = None):
        """Store in semantic memory"""
        self.semantic.store(key, content, embedding, metadata)
        self._check_consolidation()
    
    def store_knowledge(self, concept: str, properties: Dict[str, Any]):
        """Add to knowledge graph"""
        self.knowledge_graph.add_concept(concept, properties)
    
    def add_relation(self, source: str, target: str, relation_type: str,
                    properties: Optional[Dict] = None):
        """Add relationship in knowledge graph"""
        self.knowledge_graph.add_relationship(source, target, relation_type, properties)
    
    def record_experience(self, episode_id: str, steps: List[Dict], 
                         outcome: str, success: bool = True):
        """Record episodic experience"""
        self.episodic.record_episode(episode_id, steps, outcome, success)
        self._check_consolidation()
    
    def search_memories(self, query: str, search_type: str = "semantic",
                       top_k: int = 5) -> List[Any]:
        """Search across memory systems"""
        if search_type == "semantic":
            # Simulate: in prod would embed query
            query_emb = np.random.randn(768)
            results = self.semantic.search_similar(query_emb, top_k)
            return [self.semantic.retrieve(key) for key, _ in results]
        
        elif search_type == "episodic":
            return self.episodic.retrieve_by_outcome(query)
        
        return []
    
    def get_memory_status(self) -> Dict[str, Any]:
        """Get memory system status"""
        return {
            'semantic_memories': len(self.semantic.memories),
            'knowledge_concepts': len(self.knowledge_graph.nodes),
            'knowledge_relations': len(self.knowledge_graph.edges),
            'episodes': len(self.episodic.episodes),
            'skills': len(self.procedural.skills),
            'tool_usage_tracked': len(self.procedural.tool_usage),
            'episodic_success_rate': self.episodic.get_success_rate(),
            'working_memory_size': len(self.working.context),
            'timestamp': datetime.now()
        }
    
    def _check_consolidation(self):
        """Periodically consolidate memories"""
        self.operation_count += 1
        if self.operation_count % self.consolidation_interval == 0:
            logger.info("Triggering memory consolidation...")
            self.semantic.consolidate()
    
    def save_snapshot(self, filepath: str):
        """Save memory snapshot to disk"""
        snapshot = {
            'timestamp': datetime.now().isoformat(),
            'semantic_count': len(self.semantic.memories),
            'knowledge_concepts': len(self.knowledge_graph.nodes),
            'episodic_episodes': len(self.episodic.episodes),
            'status': self.get_memory_status()
        }
        
        with open(filepath, 'w') as f:
            json.dump(snapshot, f, indent=2, default=str)
        
        logger.info(f"Memory snapshot saved to {filepath}")


if __name__ == "__main__":
    # Example usage
    memory = HybridMemorySystem()
    
    # Add some knowledge
    memory.store_knowledge("AGI", {"definition": "Artificial General Intelligence"})
    memory.add_relation("AGI", "reasoning", "has_capability")
    
    # Record an episode
    memory.record_experience(
        episode_id="ep_001",
        steps=[
            {"action": "think", "result": "formulated problem"},
            {"action": "plan", "result": "created strategy"}
        ],
        outcome="success",
        success=True
    )
    
    # Check status
    print("Memory Status:")
    print(json.dumps(memory.get_memory_status(), indent=2, default=str))
