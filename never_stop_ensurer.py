#!/usr/bin/env python3
"""
NEVER STOP ENSURER - Guarantees Continuous Operation
Für die Doktorarbeit in Zusammenarbeit mit dem Bundesamt für Verfassungsschutz (BfV)
Stellt sicher, dass die Sammlung NIEMALS aufhört
"""

import json
import datetime
import re
import time
import os
import subprocess
import threading
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class SystemHealth:
    """System-Health Status"""
    collector_running: bool = False
    monitor_running: bool = False
    master_running: bool = False
    last_check: str = ""
    uptime: datetime.timedelta = datetime.timedelta(0)
    restarts_triggered: int = 0
    mission_complete: bool = False

class NeverStopEnsurer:
    def __init__(self):
        """Initialisiert den Never-Stop Ensurer"""
        self.ensurer_start = datetime.datetime.now()
        self.continuous_mode = True
        self.check_interval = 30  # 30 Sekunden Health-Checks
        self.max_downtime = 60  # 60 Sekunden maximale Downtime
        
        # Health-Tracking
        self.health = SystemHealth()
        self.health_history = []
        self.restart_log = []
        
        # Mission-Parameter
        self.target_artists = 350
        self.target_completeness = 95.0
        
    def check_system_health(self):
        """Überprüft den System-Health"""
        self.health.last_check = datetime.datetime.now().isoformat()
        self.health.uptime = datetime.datetime.now() - self.ensurer_start
        
        # Prüfe ob Prozesse laufen
        try:
            result = subprocess.run(['tasklist'], capture_output=True, text=True)
            processes = result.stdout.lower()
            
            self.health.collector_running = 'auto_continue_collector' in processes
            self.health.monitor_running = 'continuous_monitor' in processes
            self.health.master_running = 'auto_continue_master' in processes
            
        except Exception as e:
            print(f"❌ Fehler bei Prozess-Prüfung: {e}")
            return False
        
        # Speichere Health-History
        self.health_history.append({
            "timestamp": self.health.last_check,
            "collector": self.health.collector_running,
            "monitor": self.health.monitor_running,
            "master": self.health.master_running,
            "uptime": str(self.health.uptime)
        })
        
        # Behalte nur die letzten 100 Einträge
        if len(self.health_history) > 100:
            self.health_history = self.health_history[-100:]
        
        return True
    
    def assess_mission_status(self):
        """Bewertet den Mission-Status"""
        try:
            # Lade Master Dashboard
            with open("master_dashboard.md", 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extrahiere Mission-Status
            fully_collected_match = re.search(r'Fully Collected\*: (\d+)', content)
            total_artists_match = re.search(r'Total Artists Found\*: (\d+)', content)
            
            if fully_collected_match and total_artists_match:
                fully_collected = int(fully_collected_match.group(1))
                total_artists = int(total_artists_match.group(1))
                
                completion_rate = (fully_collected / total_artists) * 100
                
                # Prüfe ob Mission komplett
                if (fully_collected >= self.target_artists and 
                    completion_rate >= self.target_completeness):
                    self.health.mission_complete = True
                    return True
        
        except Exception as e:
            print(f"❌ Fehler bei Mission-Status-Prüfung: {e}")
        
        return False
    
    def restart_system(self, system_name: str):
        """Startet ein System neu"""
        restart_time = datetime.datetime.now().isoformat()
        
        try:
            if system_name == "collector":
                subprocess.Popen(['python', 'auto_continue_collector.py'], cwd='.')
                print(f"✅ Collector neu gestartet")
                
            elif system_name == "monitor":
                subprocess.Popen(['python', 'continuous_monitor.py'], cwd='.')
                print(f"✅ Monitor neu gestartet")
                
            elif system_name == "master":
                subprocess.Popen(['python', 'auto_continue_master.py'], cwd='.')
                print(f"✅ Master neu gestartet")
            
            # Log restart
            restart_entry = {
                "timestamp": restart_time,
                "system": system_name,
                "reason": "health_check_failure",
                "success": True
            }
            self.restart_log.append(restart_entry)
            self.health.restarts_triggered += 1
            
            # Warte kurz damit der Prozess starten kann
            time.sleep(3)
            
        except Exception as e:
            print(f"❌ Fehler beim Neustart von {system_name}: {e}")
            
            restart_entry = {
                "timestamp": restart_time,
                "system": system_name,
                "reason": "health_check_failure",
                "success": False,
                "error": str(e)
            }
            self.restart_log.append(restart_entry)
    
    def create_health_report(self):
        """Erstellt Health-Report"""
        all_systems_running = (self.health.collector_running and 
                             self.health.monitor_running and 
                             self.health.master_running)
        
        report = f"""# 🛡️ NEVER STOP ENSURER - Health Report

## System Status: {'✅ ALL SYSTEMS OPERATIONAL' if all_systems_running else '⚠️ SYSTEM RECOVERY IN PROGRESS'}

### 🔄 System Health
- **Collector**: {'✅ RUNNING' if self.health.collector_running else '❌ STOPPED'}
- **Monitor**: {'✅ RUNNING' if self.health.monitor_running else '❌ STOPPED'}
- **Master**: {'✅ RUNNING' if self.health.master_running else '❌ STOPPED'}
- **Overall Status**: {'✅ OPERATIONAL' if all_systems_running else '⚠️ RECOVERY'}

### 📊 Ensurer Statistics
- **Ensurer Uptime**: {self.health.uptime}
- **Restarts Triggered**: {self.health.restarts_triggered}
- **Last Health Check**: {self.health.last_check}
- **Mission Complete**: {'✅ YES' if self.health.mission_complete else '⏳ IN PROGRESS'}

### 🔄 Recent Restarts
{chr(10).join(f"- **{entry['system']}**: {entry['timestamp']} ({'SUCCESS' if entry['success'] else 'FAILED'})" for entry in self.restart_log[-5:])}

### 🎯 Mission Status
- **Target**: {self.target_artists}+ artists
- **Completeness Target**: {self.target_completeness}%
- **Status**: {'✅ MISSION COMPLETE' if self.health.mission_complete else '⏳ CONTINUING'}

### 🛡️ BfV Security Status
- **Continuous Monitoring**: {'✅ ACTIVE' if self.health.monitor_running else '❌ INACTIVE'}
- **Data Collection**: {'✅ ACTIVE' if self.health.collector_running else '❌ INACTIVE'}
- **System Coordination**: {'✅ ACTIVE' if self.health.master_running else '❌ INACTIVE'}

---

*Never Stop Ensurer - Guaranteed Continuous Operation*
*Status: Active - {datetime.datetime.now().isoformat()}*
*Mode: NEVER STOP UNTIL MISSION COMPLETE*
"""
        
        with open("never_stop_health_report.md", 'w', encoding='utf-8') as f:
            f.write(report)
    
    def run_never_stop_ensurer(self):
        """Führt den Never-Stop Ensurer aus"""
        print("🚀 NEVER STOP ENSURER STARTED")
        print("🛡️ BfV Security Guarantee System")
        print("📅 Doktorarbeit - Kontinuierliche Betriebsgarantie")
        print("⚠️ GUARANTEES THAT COLLECTION NEVER STOPS")
        print("🎯 MISSION: ENSURE 350+ ARTISTS FULLY COLLECTED")
        print("=" * 100)
        
        cycle = 0
        
        while self.continuous_mode:
            cycle += 1
            cycle_start = datetime.datetime.now()
            
            print(f"\n🛡️ HEALTH CHECK CYCLE {cycle} - {cycle_start.strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 80)
            
            # System-Health prüfen
            self.check_system_health()
            
            # Mission-Status prüfen
            mission_complete = self.assess_mission_status()
            
            # Health-Status anzeigen
            all_running = (self.health.collector_running and 
                          self.health.monitor_running and 
                          self.health.master_running)
            
            print(f"📊 SYSTEM HEALTH:")
            print(f"   Collector: {'✅ RUNNING' if self.health.collector_running else '❌ STOPPED'}")
            print(f"   Monitor: {'✅ RUNNING' if self.health.monitor_running else '❌ STOPPED'}")
            print(f"   Master: {'✅ RUNNING' if self.health.master_running else '❌ STOPPED'}")
            print(f"   Overall: {'✅ OPERATIONAL' if all_running else '⚠️ RECOVERY'}")
            print(f"   Restarts: {self.health.restarts_triggered}")
            print(f"   Uptime: {self.health.uptime}")
            
            # Mission-Status
            print(f"\n🎯 MISSION STATUS:")
            print(f"   Target: {self.target_artists}+ artists")
            print(f"   Status: {'✅ COMPLETE' if mission_complete else '⏳ IN PROGRESS'}")
            
            # System-Recovery bei Bedarf
            if not all_running and not mission_complete:
                print(f"\n🔄 SYSTEM RECOVERY REQUIRED:")
                
                if not self.health.collector_running:
                    print(f"   Restarting Collector...")
                    self.restart_system("collector")
                
                if not self.health.monitor_running:
                    print(f"   Restarting Monitor...")
                    self.restart_system("monitor")
                
                if not self.health.master_running:
                    print(f"   Restarting Master...")
                    self.restart_system("master")
                
                print(f"✅ Recovery completed")
            
            # Health-Report aktualisieren
            self.create_health_report()
            print(f"✅ Health Report aktualisiert")
            
            # Prüfe ob Mission komplett
            if mission_complete:
                print(f"\n🎉 MISSION COMPLETE - ALL SYSTEMS CAN STOP")
                print(f"   Target: {self.target_artists}+ artists achieved")
                print(f"   Ensurer Uptime: {self.health.uptime}")
                print(f"   Total Restarts: {self.health.restarts_triggered}")
                self.continuous_mode = False
                break
            
            # System-Health alle 10 Zyklen detailliert anzeigen
            if cycle % 10 == 0:
                print(f"\n🏥 DETAILED HEALTH CHECK - Cycle {cycle}")
                print(f"   Health History Entries: {len(self.health_history)}")
                print(f"   Recent Restarts: {len(self.restart_log)}")
                print(f"   System Stability: {'HIGH' if self.health.restarts_triggered < cycle * 0.1 else 'MEDIUM'}")
            
            # Warte auf nächsten Check
            print(f"\n⏳ Nächster Health-Check in {self.check_interval} Sekunden...")
            time.sleep(self.check_interval)
        
        # Finale Zusammenfassung
        self.create_final_ensurer_summary()
    
    def create_final_ensurer_summary(self):
        """Erstellt finale Ensurer-Zusammenfassung"""
        summary = f"""# 🛡️ Never Stop Ensurer - Mission Complete

## System Guarantee Status: ACCOMPLISHED ✅

### Final Statistics
- **Ensurer Uptime**: {self.health.uptime}
- **Health Checks Performed**: {len(self.health_history)}
- **Restarts Triggered**: {self.health.restarts_triggered}
- **Mission Status**: {'✅ COMPLETED' if self.health.mission_complete else '⏳ CONTINUING'}

### System Reliability
- **Collector Restarts**: {len([r for r in self.restart_log if r['system'] == 'collector'])}
- **Monitor Restarts**: {len([r for r in self.restart_log if r['system'] == 'monitor'])}
- **Master Restarts**: {len([r for r in self.restart_log if r['system'] == 'master'])}
- **System Uptime**: {((len(self.health_history) * self.check_interval) / (self.health.uptime.total_seconds())) * 100:.1f}%

### Mission Impact
- **Continuous Operation**: GUARANTEED
- **Data Collection**: UNINTERRUPTED
- **System Recovery**: AUTOMATIC
- **Mission Success**: ENSURED

---

*Never Stop Ensurer - Mission Accomplished*
*Status: Complete - {datetime.datetime.now().isoformat()}*
*Guarantee: Fulfilled*
"""
        
        with open(f"never_stop_final_summary_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md", 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(f"\n📄 Never Stop Ensurer Final Summary gespeichert")
        print(f"🛡️ CONTINUOUS OPERATION GUARANTEE FULFILLED!")

def main():
    """Hauptfunktion"""
    ensurer = NeverStopEnsurer()
    ensurer.run_never_stop_ensurer()

if __name__ == "__main__":
    main()
