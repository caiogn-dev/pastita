"""
Session Management Service for WhatsApp Automation

Gerencia o estado da sessão do cliente durante fluxos de:
- Pedidos
- Pagamentos
- Carrinho
"""
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


class SessionContext:
    """Contexto de sessão para fluxos de conversação."""
    
    def __init__(self, session=None):
        from apps.automation.models import CustomerSession
        self.session = session
        self.current_flow = None  # 'order', 'payment', 'cart', etc
        self.flow_step = 0
        self.temp_data = {}  # Dados temporários do fluxo
        self.CustomerSession = CustomerSession
    
    def is_in_flow(self) -> bool:
        """Verifica se está em algum fluxo ativo"""
        if not self.session:
            return False
        return self.session.status in [
            'cart_created',
            'checkout',
            'payment_pending',
        ]
    
    def start_order_flow(self):
        """Inicia fluxo de pedido"""
        self.current_flow = 'order'
        self.flow_step = 1
        if self.session:
            self.session.status = 'cart_created'
            self.session.save()
    
    def start_payment_flow(self):
        """Inicia fluxo de pagamento"""
        self.current_flow = 'payment'
        self.flow_step = 1
        if self.session:
            self.session.status = 'payment_pending'
            self.session.save()
    
    def complete_flow(self):
        """Completa o fluxo atual"""
        if self.session:
            self.session.status = 'completed'
            self.session.save()
        self.current_flow = None
        self.flow_step = 0
        self.temp_data = {}
    
    def reset(self):
        """Reseta o contexto"""
        if self.session:
            self.session.status = 'active'
            self.session.cart_data = {}
            self.session.cart_total = 0
            self.session.cart_items_count = 0
            self.session.save()
        self.current_flow = None
        self.flow_step = 0
        self.temp_data = {}


class SessionManager:
    """Gerenciador de sessões de clientes."""
    
    def __init__(self):
        self._sessions: Dict[str, SessionContext] = {}
    
    def get_or_create_session(
        self,
        phone_number: str,
        account=None,
        company=None
    ) -> SessionContext:
        """Obtém ou cria uma sessão para o cliente."""
        from apps.automation.models import CustomerSession
        
        # Busca sessão existente ativa
        session = CustomerSession.objects.filter(
            phone_number=phone_number,
            status__in=['active', 'cart_created', 'checkout', 'payment_pending']
        ).order_by('-updated_at').first()
        
        if not session:
            # Cria nova sessão
            defaults = {'status': 'active', 'session_id': f'sess_{phone_number}'}
            if company:
                defaults['company'] = company
            
            session = CustomerSession.objects.create(
                phone_number=phone_number,
                **defaults
            )
        
        context = SessionContext(session)
        self._sessions[phone_number] = context
        return context
    
    def get_session(self, phone_number: str) -> Optional[SessionContext]:
        """Obtém sessão existente."""
        return self._sessions.get(phone_number)
    
    def clear_session(self, phone_number: str):
        """Limpa sessão da memória."""
        if phone_number in self._sessions:
            del self._sessions[phone_number]


# Instância global
_session_manager: Optional[SessionManager] = None


def get_session_manager() -> SessionManager:
    """Retorna instância singleton do SessionManager."""
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager
