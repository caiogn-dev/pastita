# -*- coding: utf-8 -*-
"""
Pastita Automation Services

Novo orquestrador 100% - sem compatibilidade legada.
"""

# Novo Orquestrador Completo
from .pastita_orchestrator import (
    PastitaOrchestrator,
    IntentType,
    ResponseSource,
    OrchestratorResponse,
    IntentDetector,
)

# Serviços de sessão
from .session_manager import SessionManager, SessionContext, get_session_manager

# Mensagens unificadas
from .unified_messaging import UnifiedMessagingService

# Legacy - lazy import to avoid AppRegistryNotReady
def AutomationService():
    """Lazy import for AutomationService to avoid AppRegistryNotReady."""
    from .automation_service import AutomationService as _AutomationService
    return _AutomationService()

__all__ = [
    # Novo Orquestrador
    'PastitaOrchestrator',
    'IntentType',
    'ResponseSource',
    'OrchestratorResponse',
    'IntentDetector',
    # Sessão
    'SessionManager',
    'SessionContext',
    'get_session_manager',
    # Legacy
    'AutomationService',
    # Messaging
    'UnifiedMessagingService',
]
