"""
Observability & Tracing Module
================================

Provides comprehensive logging, tracing, and monitoring for agents and systems.
Tracks: decisions, tool calls, token usage, latency, reasoning paths, errors.

Integration points:
- LangSmith/LangFuse (when available)
- Local JSON/CSV export
- Real-time dashboards (future)
"""

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Callable
from enum import Enum
import json
import logging
import time
from datetime import datetime


logger = logging.getLogger(__name__)


class EventLevel(Enum):
    """Event severity levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class EventType(Enum):
    """Types of observable events"""
    # Execution events
    TASK_START = "task_start"
    TASK_END = "task_end"
    TASK_ERROR = "task_error"
    
    # Agent events
    AGENT_REASONING = "agent_reasoning"
    AGENT_ACTION = "agent_action"
    AGENT_REFLECTION = "agent_reflection"
    
    # Tool events
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    
    # Memory events
    MEMORY_STORE = "memory_store"
    MEMORY_RETRIEVE = "memory_retrieve"
    MEMORY_CONSOLIDATE = "memory_consolidate"
    
    # Reasoning events
    REASONING_START = "reasoning_start"
    REASONING_STEP = "reasoning_step"
    REASONING_END = "reasoning_end"
    
    # Decision events
    DECISION_MADE = "decision_made"
    DECISION_ALTERNATIVE = "decision_alternative"
    
    # Error tracking
    ERROR_OCCURRED = "error_occurred"
    WARNING_ISSUED = "warning_issued"


@dataclass
class ObservableEvent:
    """Base event for tracing and monitoring"""
    event_type: EventType
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    actor: str = "system"  # Agent/component name
    level: EventLevel = EventLevel.INFO
    message: str = ""
    duration_ms: Optional[float] = None  # For timed operations
    
    # Contextual data
    context: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # For errors
    error: Optional[str] = None
    stack_trace: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data['event_type'] = self.event_type.value
        data['level'] = self.level.value
        return data
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), default=str)


@dataclass
class ExecutionTrace:
    """Complete trace of a task execution"""
    task_id: str
    start_time: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    end_time: Optional[str] = None
    events: List[ObservableEvent] = field(default_factory=list)
    
    # Aggregated metrics
    total_duration_ms: float = 0.0
    total_tokens: int = 0
    tool_calls: int = 0
    errors: int = 0
    
    def add_event(self, event: ObservableEvent) -> None:
        """Add event to trace"""
        self.events.append(event)
        if event.duration_ms:
            self.total_duration_ms += event.duration_ms
    
    def finalize(self) -> None:
        """Mark trace as complete"""
        self.end_time = datetime.utcnow().isoformat()
        self.total_duration_ms = (
            datetime.fromisoformat(self.end_time) - 
            datetime.fromisoformat(self.start_time)
        ).total_seconds() * 1000
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "task_id": self.task_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "total_duration_ms": self.total_duration_ms,
            "total_tokens": self.total_tokens,
            "tool_calls": self.tool_calls,
            "errors": self.errors,
            "event_count": len(self.events),
            "events": [e.to_dict() for e in self.events]
        }


class Tracer:
    """
    Central tracing and observability system.
    
    Usage:
        tracer = Tracer(name="MyAgent")
        with tracer.trace("task_123"):
            tracer.log_reasoning(thought="...")
            tracer.log_tool_call(tool="calculator", args={...})
    """
    
    def __init__(self, name: str = "system", export_json: bool = False, export_path: str = "./traces"):
        self.name = name
        self.export_json = export_json
        self.export_path = export_path
        self.current_trace: Optional[ExecutionTrace] = None
        self.traces: Dict[str, ExecutionTrace] = {}
        self._timers: Dict[str, float] = {}  # For duration tracking
        
        self.logger = logging.getLogger(f"trace.{name}")
    
    def start_trace(self, task_id: str) -> ExecutionTrace:
        """Start a new execution trace"""
        trace = ExecutionTrace(task_id=task_id)
        self.current_trace = trace
        self.traces[task_id] = trace
        
        event = ObservableEvent(
            event_type=EventType.TASK_START,
            actor=self.name,
            message=f"Starting task: {task_id}"
        )
        self.log_event(event)
        
        return trace
    
    def end_trace(self) -> Optional[ExecutionTrace]:
        """Finalize current trace"""
        if not self.current_trace:
            return None
        
        trace = self.current_trace
        trace.finalize()
        
        event = ObservableEvent(
            event_type=EventType.TASK_END,
            actor=self.name,
            message=f"Task completed: {trace.task_id}",
            duration_ms=trace.total_duration_ms
        )
        self.log_event(event)
        
        if self.export_json:
            self._export_trace(trace)
        
        self.current_trace = None
        return trace
    
    def log_event(self, event: ObservableEvent) -> None:
        """Log an observable event"""
        if self.current_trace:
            self.current_trace.add_event(event)
        
        # Also log to Python logger
        level = getattr(logging, event.level.value)
        self.logger.log(level, f"[{event.event_type.value}] {event.message}")
    
    def log_reasoning(self, thought: str, step: int = 0, confidence: float = 1.0) -> None:
        """Log agent reasoning"""
        event = ObservableEvent(
            event_type=EventType.AGENT_REASONING,
            actor=self.name,
            message=f"Reasoning step {step}",
            context={
                "thought": thought,
                "step": step,
                "confidence": confidence
            }
        )
        self.log_event(event)
    
    def log_action(self, action: str, tool: Optional[str] = None, args: Optional[Dict] = None) -> None:
        """Log agent action"""
        event = ObservableEvent(
            event_type=EventType.AGENT_ACTION,
            actor=self.name,
            message=f"Action: {action}",
            context={
                "action": action,
                "tool": tool,
                "args": args or {}
            }
        )
        self.log_event(event)
    
    def log_reflection(self, reflection: str, success: bool = True) -> None:
        """Log agent reflection/self-critique"""
        event = ObservableEvent(
            event_type=EventType.AGENT_REFLECTION,
            actor=self.name,
            message=f"Reflection: {reflection[:100]}...",
            level=EventLevel.INFO if success else EventLevel.WARNING,
            context={
                "reflection": reflection,
                "success": success
            }
        )
        self.log_event(event)
    
    def log_tool_call(self, tool_name: str, args: Dict[str, Any], result: Optional[Any] = None) -> None:
        """Log tool invocation"""
        event = ObservableEvent(
            event_type=EventType.TOOL_CALL,
            actor=self.name,
            message=f"Tool call: {tool_name}",
            context={
                "tool_name": tool_name,
                "args": args,
                "result": result
            }
        )
        self.log_event(event)
        
        if self.current_trace:
            self.current_trace.tool_calls += 1
    
    def log_memory_operation(self, operation: str, key: str, value_summary: str = "") -> None:
        """Log memory store/retrieve operations"""
        event_type_map = {
            "store": EventType.MEMORY_STORE,
            "retrieve": EventType.MEMORY_RETRIEVE,
            "consolidate": EventType.MEMORY_CONSOLIDATE
        }
        
        event = ObservableEvent(
            event_type=event_type_map.get(operation, EventType.MEMORY_STORE),
            actor=self.name,
            message=f"Memory {operation}: {key}",
            context={
                "operation": operation,
                "key": key,
                "value_summary": value_summary
            }
        )
        self.log_event(event)
    
    def log_decision(self, decision: str, alternatives: Optional[List[str]] = None, reasoning: str = "") -> None:
        """Log decision made by agent"""
        event = ObservableEvent(
            event_type=EventType.DECISION_MADE,
            actor=self.name,
            message=f"Decision: {decision}",
            context={
                "decision": decision,
                "reasoning": reasoning,
                "alternatives": alternatives or []
            }
        )
        self.log_event(event)
    
    def log_error(self, error: str, stack_trace: Optional[str] = None) -> None:
        """Log error"""
        event = ObservableEvent(
            event_type=EventType.ERROR_OCCURRED,
            actor=self.name,
            message=error,
            level=EventLevel.ERROR,
            error=error,
            stack_trace=stack_trace
        )
        self.log_event(event)
        
        if self.current_trace:
            self.current_trace.errors += 1
    
    def start_timer(self, timer_name: str) -> None:
        """Start timing an operation"""
        self._timers[timer_name] = time.time()
    
    def end_timer(self, timer_name: str) -> float:
        """End timing and return duration in ms"""
        if timer_name not in self._timers:
            return 0.0
        
        duration_ms = (time.time() - self._timers[timer_name]) * 1000
        del self._timers[timer_name]
        return duration_ms
    
    def _export_trace(self, trace: ExecutionTrace) -> None:
        """Export trace to JSON"""
        import os
        
        os.makedirs(self.export_path, exist_ok=True)
        
        filename = f"trace_{trace.task_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(self.export_path, filename)
        
        with open(filepath, 'w') as f:
            json.dump(trace.to_dict(), f, indent=2, default=str)
        
        self.logger.info(f"Trace exported to {filepath}")
    
    def get_trace(self, task_id: str) -> Optional[ExecutionTrace]:
        """Retrieve a completed trace"""
        return self.traces.get(task_id)
    
    def get_all_traces(self) -> Dict[str, ExecutionTrace]:
        """Get all completed traces"""
        return self.traces.copy()
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics"""
        if not self.traces:
            return {"traces": 0, "total_duration_ms": 0}
        
        total_duration = sum(t.total_duration_ms for t in self.traces.values())
        total_errors = sum(t.errors for t in self.traces.values())
        total_tools = sum(t.tool_calls for t in self.traces.values())
        
        return {
            "traces": len(self.traces),
            "total_duration_ms": total_duration,
            "total_errors": total_errors,
            "total_tool_calls": total_tools,
            "avg_duration_ms": total_duration / len(self.traces) if self.traces else 0
        }


# Global tracer instance
_global_tracer: Optional[Tracer] = None


def get_tracer(name: str = "global") -> Tracer:
    """Get or create global tracer"""
    global _global_tracer
    if _global_tracer is None:
        _global_tracer = Tracer(name=name, export_json=True)
    return _global_tracer


def configure_tracer(name: str = "system", export_json: bool = True, export_path: str = "./traces") -> Tracer:
    """Configure and return global tracer"""
    global _global_tracer
    _global_tracer = Tracer(name=name, export_json=export_json, export_path=export_path)
    return _global_tracer


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.DEBUG)
    
    # Create tracer
    tracer = Tracer(name="MyAgent", export_json=True, export_path="./example_traces")
    
    # Start tracing
    print("Starting agent trace example...")
    trace = tracer.start_trace("task_001")
    
    # Simulate agent work
    tracer.log_reasoning(thought="Problem requires analysis", step=1, confidence=0.85)
    tracer.log_action(action="analyze_data", tool="analyzer")
    tracer.log_tool_call("analyzer", {"input": "data.csv"}, result="Analysis complete")
    tracer.log_reflection(reflection="Analysis successful, found 3 patterns", success=True)
    tracer.log_decision(
        decision="use_pattern_1",
        alternatives=["use_pattern_2", "use_pattern_3"],
        reasoning="Pattern 1 has highest confidence"
    )
    
    # End trace
    time.sleep(0.1)  # Simulate work
    result = tracer.end_trace()
    
    # Display summary
    print(f"\nTrace Summary:")
    print(f"  Task ID: {result.task_id}")
    print(f"  Duration: {result.total_duration_ms:.1f}ms")
    print(f"  Events: {len(result.events)}")
    print(f"  Tool calls: {result.tool_calls}")
    print(f"  Errors: {result.errors}")
    
    print(f"\nGlobal Summary:")
    print(f"  {tracer.get_summary()}")
    
    print("\n✅ Observability module initialized!")
    print("   Each agent can now log all activities for debugging and analysis.")
