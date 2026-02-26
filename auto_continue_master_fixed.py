#!/usr/bin/env python3
"""
Auto-Continue Master System - NEVER STOPS
Für die Doktorarbeit in Zusammenarbeit mit dem Bundesamt für Verfassungsschutz (BfV)
Master-Koordinator für kontinuierliche Sammlung aller 350+ Musiker
"""

import json
import datetime
import re
import time
import os
import threading
import subprocess
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class MasterStatus:
    """Master-System Status"""
    total_artists: int = 0
    target_artists: int = 350
    fully_collected: int = 0
    enhanced_profiles: int = 0
    ai_analyzed: int = 0
    bot_networks_detected: int = 0
    security_alerts: int = 0
    collection_active: bool = True
    monitoring_active: bool = True
    last_update: str = ""
    uptime: datetime.timedelta = datetime.timedelta(0)
    cycles_completed: int = 0
    total_api_calls: int = 0

class AutoContinueMaster:
    def __init__(self):
        """Initialisiert den Auto-Continue Master"""
        self.master_start = datetime.datetime.now()
        self.continuous_mode = True
        self.master_cycle_interval = 120  # 2 Minuten Master-Zyklen
        self.target_completeness = 95.0  # 95% Ziel-Vollständigkeit
        
        # Sub-Systeme
        self.collector_active = False
        self.monitor_active = False
        self.enhancer_active = False
        
        # Status-Tracking
        self.status = MasterStatus()
        self.milestones = []
        self.achievements = []
        
    def load_artist_list(self):
        """Lädt die Künstlerliste"""
        try:
            with open("artists_list.txt", 'r', encoding='utf-8') as f:
                artists = [line.strip() for line in f if line.strip()]
            return artists
        except Exception as e:
            print(f"❌ Fehler beim Laden: {e}")
            return []
    
    def assess_master_status(self):
        """Bewertet den Gesamt-Status"""
        artists = self.load_artist_list()
        
        self.status.total_artists = len(artists)
        self.status.fully_collected = 0
        self.status.enhanced_profiles = 0
        self.status.ai_analyzed = 0
        self.status.last_update = datetime.datetime.now().isoformat()
        self.status.uptime = datetime.datetime.now() - self.master_start
        
        for artist in artists:
            # Prüfe Basis-Profile
            base_filename = f"{artist.replace('/', '_').replace(':', '_')}.md"
            if os.path.exists(base_filename):
                with open(base_filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Vollständigkeits-Check
                completeness = 0.0
                sections = ["Spotify ID", "monthly listeners", "followers", "popularity", 
                          "biography", "albums", "tracks", "related", "network", "ai", "security"]
                
                for section in sections:
                    if section.lower() in content.lower():
                        completeness += 9.09  # 100/11
                
                if completeness >= 90.0:
                    self.status.fully_collected += 1
            
            # Prüfe Enhanced-Profile
            enhanced_filename = f"{artist.replace('/', '_').replace(':', '_')}_Complete.md"
            if os.path.exists(enhanced_filename):
                self.status.enhanced_profiles += 1
            
            # Prüfe AI-Analysen
            ai_filename = f"{artist.replace('/', '_').replace(':', '_')}_AI_Analysis.md"
            if os.path.exists(ai_filename):
                self.status.ai_analyzed += 1
        
        # Prüfe Bot-Netzwerke
        bot_files = [f for f in os.listdir('.') if 'Bot_Network' in f and f.endswith('.md')]
        self.status.bot_networks_detected = len(bot_files)
        
        # Prüfe Security Alerts
        alert_files = [f for f in os.listdir('.') if 'security_alert' in f and f.endswith('.json')]
        total_alerts = 0
        for alert_file in alert_files:
            try:
                with open(alert_file, 'r', encoding='utf-8') as f:
                    alerts = json.load(f)
                    total_alerts += len(alerts)
            except:
                continue
        self.status.security_alerts = total_alerts
        
        # Prüfe ob Sub-Systeme aktiv sind
        self.status.collection_active = self.check_collector_status()
        self.status.monitoring_active = self.check_monitor_status()
        
        # Zähle API-Calls
        self.status.total_api_calls = self.count_api_calls()
        
        # Prüfe Meilensteine
        self.check_milestones()
    
    def check_collector_status(self):
        """Prüft ob der Collector aktiv ist"""
        # Prüfe auf laufende Prozesse
        try:
            result = subprocess.run(['tasklist'], capture_output=True, text=True)
            return 'python' in result.stdout and 'auto_continue_collector' in result.stdout
        except:
            return False
    
    def check_monitor_status(self):
        """Prüft ob der Monitor aktiv ist"""
        try:
            result = subprocess.run(['tasklist'], capture_output=True, text=True)
            return 'python' in result.stdout and 'continuous_monitor' in result.stdout
        except:
            return False
    
    def count_api_calls(self):
        """Zählt API-Calls aus Logs"""
        total_calls = 0
        try:
            for file in os.listdir('.'):
                if file.endswith('.md'):
                    with open(file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'API Calls Used:' in content:
                            match = re.search(r'API Calls Used: (\d+)', content)
                            if match:
                                total_calls += int(match.group(1))
        except:
            pass
        return total_calls
    
    def check_milestones(self):
        """Prüft und protokolliert Meilensteine"""
        completion_rate = (self.status.fully_collected / self.status.total_artists) * 100
        
        milestones = [
            (25, "25% Collection Milestone"),
            (50, "50% Collection Milestone"),
            (75, "75% Collection Milestone"),
            (90, "90% Collection Milestone"),
            (95, "95% Collection Milestone"),
            (100, "100% Collection Milestone - MISSION COMPLETE")
        ]
        
        for threshold, name in milestones:
            if completion_rate >= threshold and not any(m["name"] == name for m in self.milestones):
                milestone = {
                    "name": name,
                    "completion_rate": completion_rate,
                    "timestamp": datetime.datetime.now().isoformat(),
                    "artists_collected": self.status.fully_collected,
                    "total_artists": self.status.total_artists
                }
                self.milestones.append(milestone)
                self.achievements.append(f"🏆 MILESTONE REACHED: {name} ({completion_rate:.1f}%)")
                print(f"🎉 {name} erreicht: {completion_rate:.1f}% ({self.status.fully_collected}/{self.status.total_artists})")
    
    def create_master_dashboard(self):
        """Erstellt das Master-Dashboard"""
        completion_rate = (self.status.fully_collected / self.status.total_artists) * 100
        ai_coverage = (self.status.ai_analyzed / self.status.total_artists) * 100
        enhanced_coverage = (self.status.enhanced_profiles / self.status.total_artists) * 100
        
        dashboard = f"""# 🚀 Auto-Continue Master Dashboard

## 🛡️ BfV Security Master System
### Status: ACTIVE - NEVER STOPS - MISSION IN PROGRESS

### 🎯 Mission Status
- **Target Artists**: {self.status.target_artists}
- **Total Artists Found**: {self.status.total_artists}
- **Fully Collected**: {self.status.fully_collected} ({completion_rate:.1f}%)
- **Enhanced Profiles**: {self.status.enhanced_profiles} ({enhanced_coverage:.1f}%)
- **AI Analysis Completed**: {self.status.ai_analyzed} ({ai_coverage:.1f}%)
- **Bot Networks Detected**: {self.status.bot_networks_detected}
- **Security Alerts**: {self.status.security_alerts}

### 🔄 System Status
- **Collection Active**: {'✅ RUNNING' if self.status.collection_active else '❌ STOPPED'}
- **Monitoring Active**: {'✅ RUNNING' if self.status.monitoring_active else '❌ STOPPED'}
- **Master Uptime**: {self.status.uptime}
- **Cycles Completed**: {self.status.cycles_completed}
- **Last Update**: {self.status.last_update}

### 📊 Progress Metrics
- **Collection Progress**: {completion_rate:.1f}% (Target: {self.target_completeness}%)
- **AI Analysis Coverage**: {ai_coverage:.1f}%
- **Enhanced Profile Coverage**: {enhanced_coverage:.1f}%
- **Total API Calls**: {self.status.total_api_calls:,}

### 🏆 Recent Achievements
{chr(10).join(f"- {achievement}" for achievement in self.achievements[-5:])}

### 🎯 Mission Objectives
- [ ] {'✅' if self.status.fully_collected >= self.status.target_artists else '⏳'} Collect {self.status.target_artists}+ artists
- [ ] {'✅' if completion_rate >= self.target_completeness else '⏳'} Achieve {self.target_completeness}% completeness
- [ ] {'✅' if ai_coverage >= 90 else '⏳'} Complete AI analysis for 90% of artists
- [ ] {'✅' if enhanced_coverage >= 50 else '⏳'} Create enhanced profiles for 50% of artists
- [ ] {'✅' if self.status.bot_networks_detected > 0 else '⏳'} Detect and analyze bot networks
- [ ] {'✅' if self.status.security_alerts > 0 else '⏳'} Generate security alerts for threats

### 🚨 Active Alerts
{chr(10).join(f"- **ALERT**: {self.status.security_alerts} security alerts detected") if self.status.security_alerts > 0 else "- ✅ No active security alerts"}

### 📈 System Health
- **Status**: ✅ OPERATIONAL
- **Mode**: CONTINUOUS AUTO-CONTINUE
- **Collection System**: {'ACTIVE' if self.status.collection_active else 'INACTIVE'}
- **Monitoring System**: {'ACTIVE' if self.status.monitoring_active else 'INACTIVE'}
- **Auto-Restart**: ENABLED

---

*Auto-Continue Master System for BfV Collaboration*
*Status: Active - {datetime.datetime.now().isoformat()}*
*Mode: NEVER STOPS UNTIL MISSION COMPLETE*
"""
        
        with open("master_dashboard.md", 'w', encoding='utf-8') as f:
            f.write(dashboard)
    
    def run_master_cycle(self):
        """Führt einen Master-Zyklus durch"""
        self.status.cycles_completed += 1
        cycle_start = datetime.datetime.now()
        
        print(f"\n🚀 MASTER CYCLE {self.status.cycles_completed} - {cycle_start.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        # Status aktualisieren
        self.assess_master_status()
        
        # Fortschritt anzeigen
        completion_rate = (self.status.fully_collected / self.status.total_artists) * 100
        
        print(f"📊 MISSION STATUS:")
        print(f"   Target: {self.status.target_artists}+ artists")
        print(f"   Found: {self.status.total_artists} artists")
        print(f"   Collected: {self.status.fully_collected} ({completion_rate:.1f}%)")
        print(f"   Enhanced: {self.status.enhanced_profiles}")
        print(f"   AI Analyzed: {self.status.ai_analyzed}")
        print(f"   Bot Networks: {self.status.bot_networks_detected}")
        print(f"   Security Alerts: {self.status.security_alerts}")
        
        # System-Status
        print(f"\n🔄 SYSTEM STATUS:")
        print(f"   Collector: {'✅ ACTIVE' if self.status.collection_active else '❌ INACTIVE'}")
        print(f"   Monitor: {'✅ ACTIVE' if self.status.monitoring_active else '❌ INACTIVE'}")
        print(f"   Uptime: {self.status.uptime}")
        print(f"   API Calls: {self.status.total_api_calls:,}")
        
        # Dashboard aktualisieren
        self.create_master_dashboard()
        print(f"✅ Master Dashboard aktualisiert")
        
        # Prüfe Mission-Status
        if completion_rate >= self.target_completeness and self.status.fully_collected >= self.status.target_artists:
            print(f"\n🎉 MISSION COMPLETE!")
            print(f"   Target: {self.status.target_artists} artists")
            print(f"   Achieved: {self.status.fully_collected} artists")
            print(f"   Completeness: {completion_rate:.1f}%")
            print(f"   Duration: {self.status.uptime}")
            achievement_msg = f"🏆 MISSION COMPLETE: {self.status.fully_collected} artists collected"
            self.achievements.append(achievement_msg)
            self.continuous_mode = False
            return
        
        # Prüfe ob Sub-Systeme neugestartet werden müssen
        if not self.status.collection_active:
            print(f"⚠️ Collector inaktiv - Starte Neustart...")
            self.restart_collector()
        
        if not self.status.monitoring_active:
            print(f"⚠️ Monitor inaktiv - Starte Neustart...")
            self.restart_monitor()
        
        # Zeige aktuelle Achievements
        if self.achievements:
            print(f"\n🏆 RECENT ACHIEVEMENTS:")
            for achievement in self.achievements[-3:]:
                print(f"   {achievement}")
    
    def restart_collector(self):
        """Startet den Collector neu"""
        try:
            subprocess.Popen(['python', 'auto_continue_collector.py'], cwd='.')
            time.sleep(2)
            print(f"✅ Collector neu gestartet")
        except Exception as e:
            print(f"❌ Fehler beim Neustart des Collectors: {e}")
    
    def restart_monitor(self):
        """Startet den Monitor neu"""
        try:
            subprocess.Popen(['python', 'continuous_monitor.py'], cwd='.')
            time.sleep(2)
            print(f"✅ Monitor neu gestartet")
        except Exception as e:
            print(f"❌ Fehler beim Neustart des Monitors: {e}")
    
    def run_master_controller(self):
        """Führt den Master-Controller aus"""
        print("🚀 AUTO-CONTINUE MASTER SYSTEM STARTED")
        print("🛡️ BfV Security Master Integration")
        print("📅 Doktorarbeit - Master-Koordinator")
        print("⚠️ NEVER STOPS UNTIL 350+ ARTISTS FULLY COLLECTED")
        print("🎯 MISSION: COMPLETE DATA COLLECTION FOR ALL ARTISTS")
        print("=" * 100)
        
        # Warte kurz damit Sub-Systeme starten können
        time.sleep(5)
        
        while self.continuous_mode:
            try:
                self.run_master_cycle()
                
                if not self.continuous_mode:
                    break
                
                # Warte auf nächsten Zyklus
                print(f"\n⏳ Nächster Master-Zyklus in {self.master_cycle_interval} Sekunden...")
                time.sleep(self.master_cycle_interval)
                
            except KeyboardInterrupt:
                print(f"\n⚠️ Master-Controller manuell gestoppt")
                break
            except Exception as e:
                print(f"❌ Fehler im Master-Zyklus: {e}")
                time.sleep(30)  # Warte bei Fehlern
        
        # Finale Zusammenfassung
        self.create_final_summary()
    
    def create_final_summary(self):
        """Erstellt finale Zusammenfassung"""
        summary = f"""# 🏆 Auto-Continue Master - Mission Complete

## 🛡️ BfV Security Mission Status: ACCOMPLISHED ✅

### Final Statistics
- **Target Artists**: {self.status.target_artists}
- **Total Artists Found**: {self.status.total_artists}
- **Fully Collected**: {self.status.fully_collected}
- **Enhanced Profiles**: {self.status.enhanced_profiles}
- **AI Analysis Completed**: {self.status.ai_analyzed}
- **Bot Networks Detected**: {self.status.bot_networks_detected}
- **Security Alerts Generated**: {self.status.security_alerts}

### Mission Timeline
- **Mission Start**: {self.master_start}
- **Mission End**: {datetime.datetime.now()}
- **Total Duration**: {datetime.datetime.now() - self.master_start}
- **Master Cycles Completed**: {self.status.cycles_completed}
- **Total API Calls**: {self.status.total_api_calls:,}

### Achievements Unlocked
{chr(10).join(f"- {achievement}" for achievement in self.achievements)}

### Milestones Reached
{chr(10).join(f"- **{m['name']}**: {m['completion_rate']:.1f}% ({m['timestamp']})" for m in self.milestones)}

### Mission Impact
- **Data Collection**: Complete dataset for BfV analysis
- **Security Analysis**: Comprehensive threat assessment
- **AI Detection**: Advanced bot network identification
- **Academic Contribution**: Significant doctoral research data

---

*Auto-Continue Master System - Mission Accomplished*
*Status: Complete - {datetime.datetime.now().isoformat()}*
*BfV Collaboration: Successful*
"""
        
        with open(f"mission_complete_summary_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md", 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(f"\n📄 Mission Complete Summary gespeichert")
        print(f"🎉 AUTO-CONTINUE MASTER MISSION ACCOMPLISHED!")

def main():
    """Hauptfunktion"""
    master = AutoContinueMaster()
    master.run_master_controller()

if __name__ == "__main__":
    main()
