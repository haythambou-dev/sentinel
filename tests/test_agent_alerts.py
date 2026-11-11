import pytest
from notifications.phone_alerts import TelegramNotifier
from investigator.security_agent import SecurityAgent
from core.incident_manager import IncidentManager

def test_telegram_notifier():
    notifier = TelegramNotifier()
    notifier.queue_notification("Test security alert message")
    queue = notifier._load_queue()
    assert len(queue) >= 1

def test_security_agent():
    mgr = IncidentManager()
    mgr.clear_incidents()
    mgr.create_incident("WINDOWS_LOGIN_FAILURE", "HIGH", {"attempts_count": 3})

    agent = SecurityAgent()
    analysis = agent.analyze_incidents()
    assert "confirmed_facts" in analysis
    assert len(analysis["confirmed_facts"]) > 0
    assert "strong_indications" in analysis
    assert "uncertainties" in analysis
    assert "recommendations" in analysis
