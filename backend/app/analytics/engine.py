from datetime import datetime
from typing import Dict, List, Optional
import json
from loguru import logger

class MetricsCollector:
    def __init__(self):
        self.metrics = {}
        
    async def record_response_time(self, endpoint: str, duration: float):
        if 'response_times' not in self.metrics:
            self.metrics['response_times'] = {}
        if endpoint not in self.metrics['response_times']:
            self.metrics['response_times'][endpoint] = []
        self.metrics['response_times'][endpoint].append({
            'timestamp': datetime.now().isoformat(),
            'duration': duration
        })
        
    async def record_error(self, endpoint: str, error: str):
        if 'errors' not in self.metrics:
            self.metrics['errors'] = {}
        if endpoint not in self.metrics['errors']:
            self.metrics['errors'][endpoint] = []
        self.metrics['errors'][endpoint].append({
            'timestamp': datetime.now().isoformat(),
            'error': error
        })
        
    async def record_interaction(self, user_id: str, interaction_type: str, details: Dict):
        if 'interactions' not in self.metrics:
            self.metrics['interactions'] = []
        self.metrics['interactions'].append({
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'type': interaction_type,
            'details': details
        })

class ReportGenerator:
    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics_collector = metrics_collector
        
    async def generate_performance_report(self, timeframe: str) -> Dict:
        metrics = self.metrics_collector.metrics
        report = {
            'generated_at': datetime.now().isoformat(),
            'timeframe': timeframe,
            'response_times': {},
            'error_rates': {},
            'total_interactions': 0
        }
        
        if 'response_times' in metrics:
            for endpoint, times in metrics['response_times'].items():
                avg_time = sum(t['duration'] for t in times) / len(times)
                report['response_times'][endpoint] = avg_time
                
        if 'errors' in metrics:
            for endpoint, errors in metrics['errors'].items():
                report['error_rates'][endpoint] = len(errors)
                
        if 'interactions' in metrics:
            report['total_interactions'] = len(metrics['interactions'])
            
        return report

class SystemMonitor:
    def __init__(self):
        self.health_status = "healthy"
        self.last_check = datetime.now()
        
    async def check_system_health(self) -> Dict:
        self.last_check = datetime.now()
        return {
            'status': self.health_status,
            'last_check': self.last_check.isoformat(),
            'components': {
                'database': 'operational',
                'ai_service': 'operational',
                'cache': 'operational'
            }
        }
        
    async def update_health_status(self, status: str):
        self.health_status = status
        logger.info(f"System health status updated to: {status}")

class AnalyticsEngine:
    def __init__(self):
        self.metrics = MetricsCollector()
        self.reporter = ReportGenerator(self.metrics)
        self.monitor = SystemMonitor()
        
    async def track_interaction(self, user_id: str, interaction_type: str, details: Dict):
        await self.metrics.record_interaction(user_id, interaction_type, details)
        
    async def track_response_time(self, endpoint: str, duration: float):
        await self.metrics.record_response_time(endpoint, duration)
        
    async def track_error(self, endpoint: str, error: str):
        await self.metrics.record_error(endpoint, error)
        
    async def get_system_health(self) -> Dict:
        return await self.monitor.check_system_health()
        
    async def generate_report(self, timeframe: str) -> Dict:
        return await self.reporter.generate_performance_report(timeframe) 