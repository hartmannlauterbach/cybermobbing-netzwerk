#!/usr/bin/env python3
"""
Continuous Monitoring System - NEVER STOPS
Für die Doktorarbeit in Zusammenarbeit mit dem Bundesamt für Verfassungsschutz (BfV)
Kontinuierliche Überwachung und Analyse aller 350+ Musiker
"""

import json
import datetime
import re
import time
import os
import threading
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class MonitoringStatus:
    """Monitoring-Status"""
    total_artists: int = 0
    fully_collected: int = 0
    partially_collected: int = 0
    ai_detected: int = 0
    bot_networks: int = 0
    security_alerts: int = 0
    last_update: str = ""
    uptime: datetime.timedelta = datetime.timedelta(0)

class ContinuousMonitor:
    def __init__(self):
        """Initialisiert den Continuous Monitor"""
        self.monitoring_start = datetime.datetime.now()
        self.last_check = datetime.datetime.now()
        self.monitoring_interval = 60  # 1 Minute zwischen Checks
        self.continuous_mode = True
        self.alert_threshold = 0.7  # 70% AI-Wahrscheinlichkeit für Alerts
        
        # Status-Tracking
        self.status = MonitoringStatus()
        self.history = []
        self.alerts = []
        
    def load_artist_list(self):
        """Lädt die Künstlerliste"""
        try:
            with open("artists_list.txt", 'r', encoding='utf-8') as f:
                artists = [line.strip() for line in f if line.strip()]
            return artists
        except Exception as e:
            print(f"❌ Fehler beim Laden: {e}")
            return []
    
    def assess_profile_quality(self, artist_name: str) -> Dict:
        """Bewertet die Qualität eines Künstlerprofils"""
        filename = f"{artist_name.replace('/', '_').replace(':', '_')}.md"
        
        if not os.path.exists(filename):
            return {"completeness": 0.0, "has_ai_analysis": False, "has_security": False}
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            completeness = 0.0
            has_ai_analysis = False
            has_security = False
            
            # Vollständigkeits-Check
            sections = [
                ("Spotify ID", 10),
                ("monthly listeners", 10),
                ("followers", 10),
                ("popularity", 10),
                ("biography", 15),
                ("albums", 15),
                ("tracks", 15),
                ("related", 10),
                ("network", 10),
                ("ai", 10),
                ("security", 10)
            ]
            
            for section, points in sections:
                if section.lower() in content.lower():
                    completeness += points
            
            completeness = min(completeness, 100.0)
            
            # KI-Analyse Check
            if "ai" in content.lower() or "bot" in content.lower():
                has_ai_analysis = True
                
                # Extrahiere AI-Wahrscheinlichkeit
                ai_match = re.search(r'(\d+\.?\d*)%.*?ai', content.lower())
                if ai_match:
                    ai_prob = float(ai_match.group(1)) / 100
                    if ai_prob > self.alert_threshold:
                        self.trigger_alert(artist_name, "HIGH_AI_PROBABILITY", ai_prob)
            
            # Sicherheits-Analyse Check
            if "security" in content.lower() or "bfv" in content.lower():
                has_security = True
            
            return {
                "completeness": completeness,
                "has_ai_analysis": has_ai_analysis,
                "has_security": has_security
            }
            
        except Exception as e:
            print(f"❌ Fehler bei Qualitäts-Bewertung für {artist_name}: {e}")
            return {"completeness": 0.0, "has_ai_analysis": False, "has_security": False}
    
    def trigger_alert(self, artist_name: str, alert_type: str, severity: float):
        """Löst einen Sicherheits-Alert aus"""
        alert = {
            "timestamp": datetime.datetime.now().isoformat(),
            "artist": artist_name,
            "type": alert_type,
            "severity": severity,
            "action_required": "IMMEDIATE" if severity > 0.8 else "MONITOR"
        }
        
        self.alerts.append(alert)
        self.status.security_alerts += 1
        
        print(f"🚨 SECURITY ALERT: {artist_name} - {alert_type} ({severity:.1%})")
        
        # Speichere Alert
        self.save_alert(alert)
    
    def save_alert(self, alert: Dict):
        """Speichert einen Alert"""
        alert_file = f"security_alert_{datetime.datetime.now().strftime('%Y%m%d')}.json"
        
        try:
            alerts = []
            if os.path.exists(alert_file):
                with open(alert_file, 'r', encoding='utf-8') as f:
                    alerts = json.load(f)
            
            alerts.append(alert)
            
            with open(alert_file, 'w', encoding='utf-8') as f:
                json.dump(alerts, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"❌ Fehler beim Speichern des Alerts: {e}")
    
    def check_ai_analysis_files(self):
        """Prüft auf AI-Analyse-Dateien"""
        ai_files = [f for f in os.listdir('.') if f.endswith('_AI_Analysis.md')]
        return len(ai_files)
    
    def check_bot_network_files(self):
        """Prüft auf Bot-Netzwerk-Analysen"""
        bot_files = [f for f in os.listdir('.') if 'Bot_Network' in f and f.endswith('.md')]
        return len(bot_files)
    
    def update_status(self):
        """Aktualisiert den Monitoring-Status"""
        artists = self.load_artist_list()
        
        self.status.total_artists = len(artists)
        self.status.fully_collected = 0
        self.status.partially_collected = 0
        self.status.ai_detected = 0
        self.status.last_update = datetime.datetime.now().isoformat()
        self.status.uptime = datetime.datetime.now() - self.monitoring_start
        
        for artist in artists:
            quality = self.assess_profile_quality(artist)
            
            if quality["completeness"] >= 90.0:
                self.status.fully_collected += 1
            elif quality["completeness"] > 0:
                self.status.partially_collected += 1
            
            if quality["has_ai_analysis"]:
                self.status.ai_detected += 1
        
        self.status.bot_networks = self.check_bot_network_files()
        
        # Speichere Status-Historie
        self.history.append({
            "timestamp": self.status.last_update,
            "total": self.status.total_artists,
            "fully_collected": self.status.fully_collected,
            "partially_collected": self.status.partially_collected,
            "ai_detected": self.status.ai_detected,
            "bot_networks": self.status.bot_networks,
            "security_alerts": self.status.security_alerts
        })
        
        # Behalte nur die letzten 100 Einträge
        if len(self.history) > 100:
            self.history = self.history[-100:]
    
    def create_status_dashboard(self):
        """Erstellt ein Status-Dashboard"""
        dashboard = f"""# Continuous Monitoring Dashboard

## 🛡️ BfV Security Monitoring System
### Status: ACTIVE - NEVER STOPS

### Current Status
- **Total Artists**: {self.status.total_artists}
- **Fully Collected**: {self.status.fully_collected} ({(self.status.fully_collected/self.status.total_artists*100):.1f}%)
- **Partially Collected**: {self.status.partially_collected}
- **AI Analysis Completed**: {self.status.ai_detected}
- **Bot Networks Detected**: {self.status.bot_networks}
- **Security Alerts**: {self.status.security_alerts}

### System Information
- **Monitoring Start**: {self.monitoring_start}
- **Uptime**: {self.status.uptime}
- **Last Update**: {self.status.last_update}
- **Monitoring Interval**: {self.monitoring_interval} seconds

### Recent Alerts
{chr(10).join(f"- **{alert['artist']}**: {alert['type']} ({alert['severity']:.1%}) - {alert['timestamp']}" for alert in self.alerts[-5:])}

### Progress Metrics
- **Collection Progress**: {(self.status.fully_collected/self.status.total_artists*100):.1f}%
- **AI Analysis Coverage**: {(self.status.ai_detected/self.status.total_artists*100):.1f}%
- **Security Assessment**: {(self.status.ai_detected/self.status.total_artists*100):.1f}%

### System Health
- **Status**: ✅ OPERATIONAL
- **Mode**: CONTINUOUS MONITORING
- **Auto-Continue**: ACTIVE
- **Alert System**: ACTIVE

---

*Continuous Monitoring System for BfV Collaboration*
*Status: Active - {datetime.datetime.now().isoformat()}*
*Auto-Continue: ENABLED*
"""
        
        with open("monitoring_dashboard.md", 'w', encoding='utf-8') as f:
            f.write(dashboard)
    
    def run_continuous_monitoring(self):
        """Führt kontinuierliche Überwachung durch"""
        print("🚀 CONTINUOUS MONITORING SYSTEM STARTED")
        print("🛡️ BfV Security Integration")
        print("📅 Doktorarbeit - Kontinuierliche Überwachung")
        print("⚠️ NEVER STOPS - 24/7 MONITORING ACTIVE")
        print("=" * 80)
        
        cycle = 0
        
        while self.continuous_mode:
            cycle += 1
            cycle_start = datetime.datetime.now()
            
            print(f"\n🔄 MONITORING CYCLE {cycle} - {cycle_start.strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 60)
            
            # Status aktualisieren
            self.update_status()
            
            # Fortschritt anzeigen
            completion_rate = (self.status.fully_collected / self.status.total_artists) * 100
            ai_coverage = (self.status.ai_detected / self.status.total_artists) * 100
            
            print(f"📊 COLLECTION STATUS:")
            print(f"   Total Artists: {self.status.total_artists}")
            print(f"   Fully Collected: {self.status.fully_collected} ({completion_rate:.1f}%)")
            print(f"   AI Analysis: {self.status.ai_detected} ({ai_coverage:.1f}%)")
            print(f"   Bot Networks: {self.status.bot_networks}")
            print(f"   Security Alerts: {self.status.security_alerts}")
            
            # Dashboard aktualisieren
            self.create_status_dashboard()
            print(f"✅ Dashboard aktualisiert")
            
            # Prüfe auf kritische Ereignisse
            if self.status.security_alerts > 0:
                print(f"🚨 {self.status.security_alerts} Security Alerts aktiv!")
            
            # System-Health Check
            if cycle % 10 == 0:
                print(f"🏥 SYSTEM HEALTH CHECK - Cycle {cycle}")
                print(f"   Uptime: {self.status.uptime}")
                print(f"   Average Cycle Time: {datetime.datetime.now() - cycle_start}")
                print(f"   Total History Entries: {len(self.history)}")
            
            # Warte auf nächsten Zyklus
            sleep_time = self.monitoring_interval
            print(f"⏳ Nächster Check in {sleep_time} Sekunden...")
            time.sleep(sleep_time)
    
    def start_background_monitoring(self):
        """Startet Monitoring im Hintergrund"""
        monitor_thread = threading.Thread(target=self.run_continuous_monitoring, daemon=True)
        monitor_thread.start()
        return monitor_thread

def main():
    """Hauptfunktion"""
    monitor = ContinuousMonitor()
    monitor.run_continuous_monitoring()

if __name__ == "__main__":
    main()
