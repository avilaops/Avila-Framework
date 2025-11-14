"""
Message Bus - Pub/Sub system for agent communication
"""
import threading
import queue
import time
from typing import Dict, List, Callable, Any
from datetime import datetime
from collections import defaultdict


class MessageBus:
    """
    Publish-Subscribe message bus for agent communication.

    Enables:
    - Event-driven architecture
    - Async communication between agents
    - Message routing and filtering
    - Broadcast and targeted messages

    Example:
        bus = MessageBus()

        # Subscribe to events
        @bus.subscribe("task.completed")
        def on_task_done(event):
            print(f"Task {event['task_id']} completed!")

        # Publish events
        bus.publish("task.completed", {"task_id": "T-123"})
    """

    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self.message_queue = queue.Queue()
        self.running = False
        self.message_count = 0
        self._lock = threading.Lock()

        # Message history (last 100)
        self.history: List[Dict] = []
        self.max_history = 100

    def subscribe(self, event_type: str):
        """
        Decorator to subscribe function to event type.

        Example:
            @bus.subscribe("deploy.completed")
            def on_deploy(event):
                update_catalog(event['data'])
        """
        def decorator(func: Callable):
            with self._lock:
                self.subscribers[event_type].append(func)
            return func
        return decorator

    def subscribe_func(self, event_type: str, func: Callable):
        """Subscribe function to event type (non-decorator)"""
        with self._lock:
            self.subscribers[event_type].append(func)

    def unsubscribe(self, event_type: str, func: Callable):
        """Unsubscribe function from event type"""
        with self._lock:
            if event_type in self.subscribers:
                self.subscribers[event_type].remove(func)

    def publish(self, event_type: str, data: Any = None):
        """
        Publish event to all subscribers.

        Args:
            event_type: Type of event (e.g., "agent.started")
            data: Event data (dict, string, etc.)
        """
        message = {
            'type': event_type,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }

        self.message_queue.put(message)
        self.message_count += 1

        # Add to history
        self.history.append(message)
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

    def start(self):
        """Start message bus processing"""
        self.running = True

        while self.running:
            try:
                # Get message from queue (blocking with timeout)
                message = self.message_queue.get(timeout=0.1)

                # Get subscribers for this event type
                event_type = message['type']
                subscribers = self.subscribers.get(event_type, [])

                # Call all subscribers
                for subscriber in subscribers:
                    try:
                        subscriber(message['data'])
                    except Exception as e:
                        print(f"❌ Error in subscriber for {event_type}: {e}")

                self.message_queue.task_done()

            except queue.Empty:
                continue
            except Exception as e:
                print(f"❌ MessageBus error: {e}")

    def stop(self):
        """Stop message bus"""
        self.running = False

    def get_history(self, event_type: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """
        Get message history.

        Args:
            event_type: Filter by event type (optional)
            limit: Max messages to return

        Returns:
            List of messages
        """
        messages = self.history

        if event_type:
            messages = [m for m in messages if m['type'] == event_type]

        return messages[-limit:]

    def register_agent(self, agent):
        """Register agent with bus (for future agent-specific routing)"""
        pass

    def unregister_agent(self, agent):
        """Unregister agent from bus"""
        pass

    def get_stats(self) -> Dict:
        """Get bus statistics"""
        return {
            'total_messages': self.message_count,
            'active_subscriptions': sum(len(subs) for subs in self.subscribers.values()),
            'event_types': list(self.subscribers.keys()),
            'queue_size': self.message_queue.qsize(),
            'history_size': len(self.history)
        }
