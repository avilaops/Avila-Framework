"""
Sistema de KPIs e Monitoramento Multinacional Ávila Ops
Define indicadores-chave de performance para operações globais
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from enum import Enum

from on.core.on_metrics import (
    record_regional_operation,
    update_customer_count,
    update_sla_compliance,
    record_error
)
from on.core.on_logger import AgentLogger


class Region(Enum):
    """Regiões geográficas de operação"""
    AMERICAS = "americas"
    EUROPE = "europe"
    ASIA_PACIFIC = "asia_pacific"
    MIDDLE_EAST_AFRICA = "middle_east_africa"


class OperationType(Enum):
    """Tipos de operações globais"""
    ASSESSMENT = "assessment"
    CONSULTING = "consulting"
    IMPLEMENTATION = "implementation"
    SUPPORT = "support"
    TRAINING = "training"
    AUDIT = "audit"


@dataclass
class CountryMetrics:
    """Métricas por país"""
    country_code: str
    country_name: str
    region: Region
    active_customers: int = 0
    monthly_operations: int = 0
    sla_compliance: float = 0.0
    revenue_usd: float = 0.0
    last_updated: datetime = None


class GlobalMonitor:
    """
    Monitor global de operações Ávila
    Rastreia métricas de 70+ países
    """
    
    # Países de operação (70+)
    COUNTRIES = {
        # Américas (20)
        "US": ("United States", Region.AMERICAS),
        "CA": ("Canada", Region.AMERICAS),
        "MX": ("Mexico", Region.AMERICAS),
        "BR": ("Brazil", Region.AMERICAS),
        "AR": ("Argentina", Region.AMERICAS),
        "CL": ("Chile", Region.AMERICAS),
        "CO": ("Colombia", Region.AMERICAS),
        "PE": ("Peru", Region.AMERICAS),
        "VE": ("Venezuela", Region.AMERICAS),
        "EC": ("Ecuador", Region.AMERICAS),
        "BO": ("Bolivia", Region.AMERICAS),
        "PY": ("Paraguay", Region.AMERICAS),
        "UY": ("Uruguay", Region.AMERICAS),
        "CR": ("Costa Rica", Region.AMERICAS),
        "PA": ("Panama", Region.AMERICAS),
        "DO": ("Dominican Republic", Region.AMERICAS),
        "CU": ("Cuba", Region.AMERICAS),
        "GT": ("Guatemala", Region.AMERICAS),
        "HN": ("Honduras", Region.AMERICAS),
        "NI": ("Nicaragua", Region.AMERICAS),
        
        # Europa (25)
        "GB": ("United Kingdom", Region.EUROPE),
        "DE": ("Germany", Region.EUROPE),
        "FR": ("France", Region.EUROPE),
        "IT": ("Italy", Region.EUROPE),
        "ES": ("Spain", Region.EUROPE),
        "PT": ("Portugal", Region.EUROPE),
        "NL": ("Netherlands", Region.EUROPE),
        "BE": ("Belgium", Region.EUROPE),
        "CH": ("Switzerland", Region.EUROPE),
        "AT": ("Austria", Region.EUROPE),
        "SE": ("Sweden", Region.EUROPE),
        "NO": ("Norway", Region.EUROPE),
        "DK": ("Denmark", Region.EUROPE),
        "FI": ("Finland", Region.EUROPE),
        "PL": ("Poland", Region.EUROPE),
        "CZ": ("Czech Republic", Region.EUROPE),
        "HU": ("Hungary", Region.EUROPE),
        "RO": ("Romania", Region.EUROPE),
        "BG": ("Bulgaria", Region.EUROPE),
        "GR": ("Greece", Region.EUROPE),
        "IE": ("Ireland", Region.EUROPE),
        "HR": ("Croatia", Region.EUROPE),
        "SI": ("Slovenia", Region.EUROPE),
        "SK": ("Slovakia", Region.EUROPE),
        "RS": ("Serbia", Region.EUROPE),
        
        # Ásia-Pacífico (15)
        "CN": ("China", Region.ASIA_PACIFIC),
        "JP": ("Japan", Region.ASIA_PACIFIC),
        "KR": ("South Korea", Region.ASIA_PACIFIC),
        "IN": ("India", Region.ASIA_PACIFIC),
        "AU": ("Australia", Region.ASIA_PACIFIC),
        "NZ": ("New Zealand", Region.ASIA_PACIFIC),
        "SG": ("Singapore", Region.ASIA_PACIFIC),
        "MY": ("Malaysia", Region.ASIA_PACIFIC),
        "TH": ("Thailand", Region.ASIA_PACIFIC),
        "VN": ("Vietnam", Region.ASIA_PACIFIC),
        "PH": ("Philippines", Region.ASIA_PACIFIC),
        "ID": ("Indonesia", Region.ASIA_PACIFIC),
        "PK": ("Pakistan", Region.ASIA_PACIFIC),
        "BD": ("Bangladesh", Region.ASIA_PACIFIC),
        "LK": ("Sri Lanka", Region.ASIA_PACIFIC),
        
        # Oriente Médio e África (10)
        "SA": ("Saudi Arabia", Region.MIDDLE_EAST_AFRICA),
        "AE": ("United Arab Emirates", Region.MIDDLE_EAST_AFRICA),
        "IL": ("Israel", Region.MIDDLE_EAST_AFRICA),
        "TR": ("Turkey", Region.MIDDLE_EAST_AFRICA),
        "EG": ("Egypt", Region.MIDDLE_EAST_AFRICA),
        "ZA": ("South Africa", Region.MIDDLE_EAST_AFRICA),
        "NG": ("Nigeria", Region.MIDDLE_EAST_AFRICA),
        "KE": ("Kenya", Region.MIDDLE_EAST_AFRICA),
        "MA": ("Morocco", Region.MIDDLE_EAST_AFRICA),
        "GH": ("Ghana", Region.MIDDLE_EAST_AFRICA),
    }
    
    def __init__(self):
        self.logger = AgentLogger("GlobalMonitor")
        self.metrics: Dict[str, CountryMetrics] = {}
        self._initialize_countries()
        
    def _initialize_countries(self):
        """Inicializa métricas para todos os países"""
        for code, (name, region) in self.COUNTRIES.items():
            self.metrics[code] = CountryMetrics(
                country_code=code,
                country_name=name,
                region=region,
                last_updated=datetime.utcnow()
            )
        self.logger.log(f"? Monitoramento inicializado para {len(self.COUNTRIES)} países")
    
    def record_operation(
        self,
        country_code: str,
        operation_type: OperationType,
        success: bool = True
    ):
        """Registra operação realizada em um país"""
        if country_code not in self.COUNTRIES:
            self.logger.log(f"?? País desconhecido: {country_code}")
            return
        
        name, region = self.COUNTRIES[country_code]
        
        # Atualizar métricas locais
        if country_code in self.metrics:
            self.metrics[country_code].monthly_operations += 1
            self.metrics[country_code].last_updated = datetime.utcnow()
        
        # Registrar em telemetria
        record_regional_operation(
            region=region.value,
            country=name,
            operation_type=operation_type.value
        )
        
        if not success:
            record_error(
                agent="global_operations",
                error_type="operation_failed",
                severity="medium"
            )
    
    def update_customer_metrics(self, country_code: str, delta: int):
        """Atualiza contagem de clientes ativos"""
        if country_code not in self.COUNTRIES:
            return
        
        if country_code in self.metrics:
            self.metrics[country_code].active_customers += delta
            
        update_customer_count(country_code, delta)
    
    def update_sla(self, country_code: str, compliance: float):
        """Atualiza SLA compliance de um país"""
        if country_code not in self.COUNTRIES:
            return
        
        if country_code in self.metrics:
            self.metrics[country_code].sla_compliance = compliance
            
        update_sla_compliance(f"country_{country_code}", compliance)
    
    def get_regional_summary(self, region: Region) -> Dict:
        """Retorna resumo de uma região"""
        countries = [
            m for m in self.metrics.values()
            if m.region == region
        ]
        
        return {
            "region": region.value,
            "countries": len(countries),
            "total_customers": sum(c.active_customers for c in countries),
            "total_operations": sum(c.monthly_operations for c in countries),
            "avg_sla_compliance": sum(c.sla_compliance for c in countries) / len(countries) if countries else 0,
            "total_revenue_usd": sum(c.revenue_usd for c in countries)
        }
    
    def get_global_summary(self) -> Dict:
        """Retorna resumo global de todas as operações"""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "total_countries": len(self.COUNTRIES),
            "regions": {
                "americas": self.get_regional_summary(Region.AMERICAS),
                "europe": self.get_regional_summary(Region.EUROPE),
                "asia_pacific": self.get_regional_summary(Region.ASIA_PACIFIC),
                "middle_east_africa": self.get_regional_summary(Region.MIDDLE_EAST_AFRICA)
            },
            "global_totals": {
                "customers": sum(m.active_customers for m in self.metrics.values()),
                "operations": sum(m.monthly_operations for m in self.metrics.values()),
                "avg_sla": sum(m.sla_compliance for m in self.metrics.values()) / len(self.metrics),
                "revenue_usd": sum(m.revenue_usd for m in self.metrics.values())
            }
        }
    
    def get_top_countries(self, metric: str = "customers", limit: int = 10) -> List[Dict]:
        """Retorna top países por métrica"""
        metric_map = {
            "customers": lambda m: m.active_customers,
            "operations": lambda m: m.monthly_operations,
            "sla": lambda m: m.sla_compliance,
            "revenue": lambda m: m.revenue_usd
        }
        
        if metric not in metric_map:
            return []
        
        sorted_countries = sorted(
            self.metrics.values(),
            key=metric_map[metric],
            reverse=True
        )[:limit]
        
        return [
            {
                "country": c.country_name,
                "code": c.country_code,
                "region": c.region.value,
                "value": metric_map[metric](c)
            }
            for c in sorted_countries
        ]


# Instância global do monitor
global_monitor = GlobalMonitor()
