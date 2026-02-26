#!/usr/bin/env python3
"""
Simplified AI Artist Detection System
Für die Doktorarbeit in Zusammenarbeit mit dem Bundesamt für Verfassungsschutz (BfV)
"""

import json
import datetime
import re
import os
import hashlib
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import statistics
import math

@dataclass
class AIIndicators:
    """KI-Indikatoren für Künstleranalyse"""
    name_pattern_score: float
    content_consistency: float
    temporal_anomaly: float
    network_artificiality: float
    engagement_unnaturalness: float
    metadata_suspicion: float
    overall_ai_probability: float

class SimpleAIDetector:
    def __init__(self):
        """Initialisiert den vereinfachten KI-Detektor"""
        self.ai_threshold = 0.7
        self.bot_threshold = 0.8
        self.collection_date = datetime.datetime.now().isoformat()
        
        # Fortgeschrittene Muster für KI-Erkennung
        self.ai_name_patterns = [
            r'^[a-zA-Z0-9]{3,8}$',  # Kurze, kryptische Namen
            r'.*\d{3,}.*',  # Zahlen in Namen
            r'^[A-Z]{2,}$',  # Nur Großbuchstaben
            r'.*[xX0].*[xX0].*',  # Multiple x/0
            r'.*[aA][iI].*',  # AI im Namen
            r'.*[bB][oO][tT].*',  # Bot im Namen
            r'^[a-z]+[0-9]+$',  # Kleinbuchstaben + Zahlen
            r'.*[0-9][0-9][0-9].*',  # Dreier-Zahlen
            r'.*[xX][xX].*',  # Doppel-x
            r'.*[0-9][xX].*',  # Zahl+x
        ]
        
        # Verdächtige Keywords
        self.suspicious_keywords = [
            'ai', 'bot', 'auto', 'gen', 'synth', 'neural', 'deep', 'algo',
            'void', 'null', 'echo', 'ghost', 'shadow', 'phantom', 'digital',
            'cyber', 'tech', 'code', 'binary', 'matrix', 'glitch', 'error',
            '404', '500', 'proxy', 'server', 'cloud', 'data', 'byte'
        ]
        
    def analyze_name_ai_probability(self, artist_name: str) -> float:
        """Analysiert die KI-Wahrscheinlichkeit basierend auf dem Künstlernamen"""
        score = 0.0
        name_lower = artist_name.lower()
        
        # Mustererkennung
        for pattern in self.ai_name_patterns:
            if re.match(pattern, artist_name, re.IGNORECASE):
                score += 0.15
        
        # Längenanomalien
        if len(artist_name) <= 4:
            score += 0.2
        elif len(artist_name) >= 20:
            score += 0.1
            
        # Sonderzeichen-Anomalien
        special_char_ratio = sum(1 for c in artist_name if not c.isalnum()) / len(artist_name)
        if special_char_ratio > 0.3:
            score += 0.2
            
        # Zahlen-Anomalien
        digit_ratio = sum(1 for c in artist_name if c.isdigit()) / len(artist_name)
        if digit_ratio > 0.2:
            score += 0.15
            
        # KI-spezifische Keywords
        for keyword in self.suspicious_keywords:
            if keyword in name_lower:
                score += 0.25
                
        # Leetspeak-Anomalien
        leet_patterns = {
            '4': 'a', '3': 'e', '1': 'l', '0': 'o', '7': 't', '5': 's'
        }
        leet_score = 0
        for leet_char, normal_char in leet_patterns.items():
            if leet_char in name_lower:
                leet_score += 0.1
        score += min(leet_score, 0.3)
        
        # Wiederholte Zeichen
        if re.search(r'(.)\1{2,}', artist_name):
            score += 0.2
            
        return min(score, 1.0)
    
    def analyze_temporal_anomalies(self, release_dates: List[str]) -> float:
        """Analysiert zeitliche Anomalien in Veröffentlichungen"""
        if len(release_dates) < 2:
            return 0.0
            
        # Konvertiere zu datetime Objekten
        dates = []
        for date_str in release_dates:
            try:
                if '-' in date_str and len(date_str) >= 4:
                    dates.append(datetime.datetime.strptime(date_str[:10], '%Y-%m-%d'))
            except:
                continue
                
        if len(dates) < 2:
            return 0.0
            
        # Berechne Veröffentlichungsintervalle
        intervals = []
        dates.sort()
        for i in range(1, len(dates)):
            interval = (dates[i] - dates[i-1]).days
            intervals.append(interval)
            
        if not intervals:
            return 0.0
            
        # Anomalie-Erkennung
        mean_interval = statistics.mean(intervals)
        
        # Zu regelmäßige Veröffentlichungen (Bot-Verhalten)
        if len(intervals) >= 3:
            interval_variance = statistics.variance(intervals) if len(intervals) > 1 else 0
            if interval_variance < 25 and mean_interval < 30:
                return 0.8
                
        # Cluster von Veröffentlichungen (Bot-Netzwerk)
        short_intervals = [i for i in intervals if i < 7]
        if len(short_intervals) > len(intervals) * 0.5:
            return 0.7
            
        return 0.0
    
    def analyze_engagement_unnaturalness(self, followers: int, monthly_listeners: int, 
                                      track_data: List[Dict]) -> float:
        """Analysiert unnatürliche Engagement-Muster"""
        score = 0.0
        
        if monthly_listeners == 0:
            return 0.0
            
        # Follower-zu-Listener Ratio
        if followers > 0:
            ratio = monthly_listeners / followers
            if ratio > 1000 or ratio < 0.1:
                score += 0.3
                
        # Track-Popularity-Anomalien
        if track_data:
            popularities = [track.get('popularity', 0) for track in track_data if track.get('popularity')]
            if len(popularities) >= 3:
                mean_pop = statistics.mean(popularities)
                
                # Alle Tracks haben ähnliche Popularität (Bot-Verhalten)
                pop_variance = statistics.variance(popularities)
                if pop_variance < 25 and mean_pop > 50:
                    score += 0.4
                    
                # Extrem hohe Popularität bei wenigen Followern
                if mean_pop > 80 and followers < 1000:
                    score += 0.5
                    
        # Unnatürliche Listener-Zahlen (runde Zahlen)
        round_numbers = [1000, 5000, 10000, 50000, 100000, 500000, 1000000]
        if monthly_listeners in round_numbers:
            score += 0.2
            
        # Follower-Anomalien
        if followers in round_numbers:
            score += 0.15
            
        return min(score, 1.0)
    
    def analyze_network_artificiality(self, related_artists: List[Dict]) -> float:
        """Analysiert künstliche Netzwerkstrukturen"""
        if not related_artists:
            return 0.0
            
        score = 0.0
        
        # Ähnliche Follower-Zahlen (Bot-Netzwerk)
        followers = [artist.get('followers', 0) for artist in related_artists if artist.get('followers')]
        if len(followers) >= 3:
            mean_followers = statistics.mean(followers)
            if mean_followers > 0:
                # Berechne Variationskoeffizient
                std_followers = statistics.stdev(followers) if len(followers) > 1 else 0
                cv = std_followers / mean_followers
                if cv < 0.2:
                    score += 0.4
                    
        # Ähnliche Popularitäts-Werte
        popularities = [artist.get('popularity', 0) for artist in related_artists if artist.get('popularity')]
        if len(popularities) >= 3:
            std_pop = statistics.stdev(popularities) if len(popularities) > 1 else 0
            if std_pop < 10:
                score += 0.3
                
        # Genre-Cluster-Anomalien
        all_genres = []
        for artist in related_artists:
            genres = artist.get('genres', [])
            all_genres.extend(genres)
            
        if len(all_genres) > 5:
            unique_genres = set(all_genres)
            if len(unique_genres) < 3:
                score += 0.3
                
        # Namensähnlichkeiten
        names = [artist.get('name', '') for artist in related_artists if artist.get('name')]
        if len(names) >= 3:
            # Prüfe auf ähnliche Namensmuster
            name_lengths = [len(name) for name in names]
            if len(set(name_lengths)) == 1:
                score += 0.2
                
        return min(score, 1.0)
    
    def analyze_content_consistency(self, albums: List[Dict], tracks: List[Dict]) -> float:
        """Analysiert Inhalt-Konsistenz für KI-Erkennung"""
        score = 0.0
        
        if not albums and not tracks:
            return 0.0
            
        # Track-Längen-Anomalien
        track_lengths = []
        for track in tracks:
            duration_ms = track.get('duration_ms', 0)
            if duration_ms > 0:
                track_lengths.append(duration_ms / 1000)  # Konvertiere zu Sekunden
                
        if len(track_lengths) >= 3:
            mean_length = statistics.mean(track_lengths)
            
            # Alle Tracks haben exakt die gleiche Länge (KI-Generierung)
            length_variance = statistics.variance(track_lengths)
            if length_variance < 1:
                score += 0.5
                
            # Ungewöhnlich kurze oder lange Tracks
            if mean_length < 60 or mean_length > 600:
                score += 0.3
                
        # Album-Struktur-Anomalien
        if albums:
            track_counts = [album.get('total_tracks', 0) for album in albums if album.get('total_tracks')]
            if len(track_counts) >= 3:
                # Alle Alben haben gleiche Track-Anzahl
                if len(set(track_counts)) == 1:
                    score += 0.3
                    
                # Verdächtige Track-Anzahlen
                for count in track_counts:
                    if count in [1, 2, 3, 7, 13, 17, 23]:  # Ungewöhnliche Zahlen
                        score += 0.1
                        
        return min(score, 1.0)
    
    def analyze_metadata_suspicion(self, artist_data: Dict) -> float:
        """Analysiert Metadaten auf verdächtige Muster"""
        score = 0.0
        
        # Fehlende oder verdächtige Biografie
        bio = artist_data.get('biography', '')
        if not bio or len(bio) < 50:
            score += 0.2
            
        # Verdächtige External URLs
        external_urls = artist_data.get('external_urls', {})
        if len(external_urls) == 1 and 'spotify' in str(external_urls):
            score += 0.3
            
        # Image-Anomalien
        images = artist_data.get('images', [])
        if not images:
            score += 0.2
        elif len(images) == 1:
            score += 0.1
            
        # Genre-Anomalien
        genres = artist_data.get('genres', [])
        if not genres:
            score += 0.3
        elif len(genres) > 5:
            score += 0.2
            
        # Verdächtige Genre-Kombinationen
        experimental_genres = ['experimental', 'abstract', 'glitch', 'noise', 'ambient']
        if any(genre.lower() in [g.lower() for g in genres] for genre in experimental_genres):
            score += 0.2
            
        return min(score, 1.0)
    
    def detect_ai_artist(self, artist_data: Dict) -> AIIndicators:
        """Hauptfunktion zur KI-Künstler-Erkennung"""
        name = artist_data.get('name', '')
        followers = artist_data.get('followers', 0)
        monthly_listeners = artist_data.get('monthly_listeners', 0)
        
        # Extrahiere Daten für Analysen
        albums = artist_data.get('albums', [])
        tracks = artist_data.get('top_tracks', [])
        related_artists = artist_data.get('related_artists', [])
        
        # Release-Daten extrahieren
        release_dates = [album.get('release_date', '') for album in albums if album.get('release_date')]
        
        # Einzelne Analysen
        name_score = self.analyze_name_ai_probability(name)
        temporal_score = self.analyze_temporal_anomalies(release_dates)
        engagement_score = self.analyze_engagement_unnaturalness(followers, monthly_listeners, tracks)
        network_score = self.analyze_network_artificiality(related_artists)
        content_score = self.analyze_content_consistency(albums, tracks)
        metadata_score = self.analyze_metadata_suspicion(artist_data)
        
        # Gewichtete Gesamtbewertung
        overall_score = (
            name_score * 0.25 +      # Name ist sehr wichtig
            temporal_score * 0.15 +   # Zeitliche Muster
            engagement_score * 0.20 + # Engagement-Muster
            network_score * 0.20 +   # Netzwerk-Muster
            content_score * 0.10 +    # Inhalt-Konsistenz
            metadata_score * 0.10    # Metadaten-Anomalien
        )
        
        return AIIndicators(
            name_pattern_score=name_score,
            content_consistency=content_score,
            temporal_anomaly=temporal_score,
            network_artificiality=network_score,
            engagement_unnaturalness=engagement_score,
            metadata_suspicion=metadata_score,
            overall_ai_probability=overall_score
        )
    
    def extract_data_from_markdown(self, filename: str) -> Dict:
        """Extrahiert Künstlerdaten aus Markdown-Datei"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                
            artist_name = filename.replace('.md', '')
            
            # Extrahiere Follower
            followers = 0
            if 'Followers:' in content:
                match = re.search(r'Followers:\s*([\d,]+)', content)
                if match:
                    followers = int(match.group(1).replace(',', ''))
                    
            # Extrahiere Monthly Listeners
            monthly_listeners = 0
            if 'Monthly Listeners:' in content:
                match = re.search(r'Monthly Listeners:\s*([\d,]+)', content)
                if match:
                    monthly_listeners = int(match.group(1).replace(',', ''))
            elif 'monthly listeners' in content.lower():
                match = re.search(r'(\d+(?:,\d+)*)\s*monthly listeners', content.lower())
                if match:
                    monthly_listeners = int(match.group(1).replace(',', ''))
                    
            # Extrahiere Popularität
            popularity = 0
            if 'Popularity:' in content:
                match = re.search(r'Popularity:\s*(\d+)', content)
                if match:
                    popularity = int(match.group(1))
                    
            # Extrahiere Genres
            genres = []
            if 'Genres:' in content:
                genre_match = re.search(r'Genres:\s*([^\n]+)', content)
                if genre_match:
                    genres = [g.strip() for g in genre_match.group(1).split(',')]
                    
            # Extrahiere Top Tracks (vereinfacht)
            top_tracks = []
            track_section = re.search(r'## Top Tracks\n(.*?)(?=\n##|\n#|$)', content, re.DOTALL)
            if track_section:
                track_lines = track_section.group(1).split('\n')
                for line in track_lines:
                    if 'Popularity:' in line:
                        pop_match = re.search(r'Popularity:\s*(\d+)', line)
                        explicit_match = re.search(r'Explicit:\s*(Yes|No)', line)
                        if pop_match:
                            track_data = {
                                'popularity': int(pop_match.group(1)),
                                'explicit': explicit_match.group(1) == 'Yes' if explicit_match else False
                            }
                            top_tracks.append(track_data)
                            
            # Extrahiere Alben
            albums = []
            album_section = re.search(r'## Recent Albums\n(.*?)(?=\n##|\n#|$)', content, re.DOTALL)
            if album_section:
                album_lines = album_section.group(1).split('\n')
                for line in album_lines:
                    if 'tracks' in line:
                        track_match = re.search(r'(\d+)\s*tracks', line)
                        date_match = re.search(r'\((\d{4}-\d{2}-\d{2})\)', line)
                        if track_match:
                            album_data = {
                                'total_tracks': int(track_match.group(1)),
                                'release_date': date_match.group(1) if date_match else '2024-01-01'
                            }
                            albums.append(album_data)
                            
            # Extrahiere verwandte Künstler
            related_artists = []
            related_section = re.search(r'## Related Artists\n(.*?)(?=\n##|\n#|$)', content, re.DOTALL)
            if related_section:
                related_lines = related_section.group(1).split('\n')
                for line in related_lines:
                    if 'followers' in line.lower():
                        follower_match = re.search(r'([\d,]+)\s*followers', line.lower())
                        pop_match = re.search(r'popularity:\s*(\d+)', line.lower())
                        if follower_match:
                            artist_data = {
                                'followers': int(follower_match.group(1).replace(',', '')),
                                'popularity': int(pop_match.group(1)) if pop_match else 0
                            }
                            related_artists.append(artist_data)
                            
            return {
                'name': artist_name,
                'followers': followers,
                'monthly_listeners': monthly_listeners,
                'popularity': popularity,
                'genres': genres,
                'top_tracks': top_tracks,
                'albums': albums,
                'related_artists': related_artists,
                'external_urls': {'spotify': f'https://open.spotify.com/artist/{artist_name}'},
                'images': [],
                'biography': ''
            }
            
        except Exception as e:
            print(f"❌ Fehler bei Extraktion aus {filename}: {e}")
            return {}
    
    def generate_ai_report(self, artist_data: Dict, ai_indicators: AIIndicators) -> str:
        """Generiert einen detaillierten KI-Analyse-Bericht"""
        name = artist_data.get('name', 'Unknown')
        
        report = f"""# AI Artist Analysis Report: {name}

## Executive Summary
- **Overall AI Probability**: {ai_indicators.overall_ai_probability:.2%}
- **Classification**: {"HIGH PROBABILITY AI ARTIST" if ai_indicators.overall_ai_probability > 0.7 else "POTENTIAL AI ARTIST" if ai_indicators.overall_ai_probability > 0.4 else "LIKELY HUMAN"}
- **Threat Level**: {"CRITICAL" if ai_indicators.overall_ai_probability > 0.8 else "HIGH" if ai_indicators.overall_ai_probability > 0.6 else "MEDIUM" if ai_indicators.overall_ai_probability > 0.4 else "LOW"}

## Detailed Analysis

### 1. Name Pattern Analysis: {ai_indicators.name_pattern_score:.2%}
- **AI Name Patterns**: {"DETECTED" if ai_indicators.name_pattern_score > 0.5 else "MINIMAL"}
- **Linguistic Anomalies**: {"PRESENT" if ai_indicators.name_pattern_score > 0.3 else "NORMAL"}
- **Leetspeak Detection**: {"FOUND" if any(c in name.lower() for c in ['4', '3', '1', '0', '7', '5']) else "NONE"}

### 2. Temporal Anomaly Detection: {ai_indicators.temporal_anomaly:.2%}
- **Release Pattern**: {"BOT-LIKE" if ai_indicators.temporal_anomaly > 0.5 else "NATURAL"}
- **Automated Scheduling**: {"LIKELY" if ai_indicators.temporal_anomaly > 0.6 else "UNLIKELY"}
- **Coordination Indicators**: {"PRESENT" if ai_indicators.temporal_anomaly > 0.4 else "ABSENT"}

### 3. Engagement Unnaturalness: {ai_indicators.engagement_unnaturalness:.2%}
- **Follower-Listener Ratio**: {"ANOMALOUS" if ai_indicators.engagement_unnaturalness > 0.5 else "NORMAL"}
- **Stream Manipulation**: {"LIKELY" if ai_indicators.engagement_unnaturalness > 0.6 else "UNLIKELY"}
- **Artificial Popularity**: {"DETECTED" if ai_indicators.engagement_unnaturalness > 0.4 else "NATURAL"}

### 4. Network Artificiality: {ai_indicators.network_artificiality:.2%}
- **Bot Network Indicators**: {"STRONG" if ai_indicators.network_artificiality > 0.6 else "WEAK"}
- **Collaboration Patterns**: {"ARTIFICIAL" if ai_indicators.network_artificiality > 0.5 else "ORGANIC"}
- **Genre Clustering**: {"SUSPICIOUS" if ai_indicators.network_artificiality > 0.4 else "NORMAL"}

### 5. Content Consistency: {ai_indicators.content_consistency:.2%}
- **AI-Generated Content**: {"LIKELY" if ai_indicators.content_consistency > 0.5 else "UNLIKELY"}
- **Track Structure Anomalies**: {"PRESENT" if ai_indicators.content_consistency > 0.3 else "NORMAL"}
- **Automated Production**: {"INDICATED" if ai_indicators.content_consistency > 0.4 else "NATURAL"}

### 6. Metadata Suspicion: {ai_indicators.metadata_suspicion:.2%}
- **Profile Completeness**: {"SUSPICIOUS" if ai_indicators.metadata_suspicion > 0.5 else "NORMAL"}
- **Web Presence**: {"MINIMAL" if ai_indicators.metadata_suspicion > 0.3 else "ADEQUATE"}
- **Identity Verification**: {"DIFFICULT" if ai_indicators.metadata_suspicion > 0.4 else "POSSIBLE"}

## Security Assessment

### BfV Classification
- **Risk Category**: {"AUTOMATED PROPAGANDA" if ai_indicators.overall_ai_probability > 0.7 else "POTENTIAL MANIPULATION" if ai_indicators.overall_ai_probability > 0.4 else "LOW RISK"}
- **Monitoring Priority**: {"IMMEDIATE" if ai_indicators.overall_ai_probability > 0.8 else "HIGH" if ai_indicators.overall_ai_probability > 0.6 else "MEDIUM" if ai_indicators.overall_ai_probability > 0.4 else "LOW"}
- **Threat Vector**: {"AI-Generated Content" if ai_indicators.overall_ai_probability > 0.6 else "Potential Automation"}

### Recommended Actions
- {"IMMEDIATE INVESTIGATION" if ai_indicators.overall_ai_probability > 0.8 else "ENHANCED MONITORING" if ai_indicators.overall_ai_probability > 0.6 else "PERIODIC REVIEW" if ai_indicators.overall_ai_probability > 0.4 else "STANDARD MONITORING"}
- {"CONTENT ANALYSIS" if ai_indicators.overall_ai_probability > 0.7 else "OBSERVATION" if ai_indicators.overall_ai_probability > 0.4 else "NO ACTION"}
- {"NETWORK TRACING" if ai_indicators.network_artificiality > 0.6 else "INDIVIDUAL MONITORING"}

## Technical Evidence

### Algorithmic Indicators
- **Pattern Recognition**: Advanced regex analysis
- **Statistical Anomalies**: Variance and outlier detection
- **Behavioral Analysis**: Temporal and engagement patterns

### Risk Factors
- **Name Anomalies**: {ai_indicators.name_pattern_score:.2%}
- **Temporal Patterns**: {ai_indicators.temporal_anomaly:.2%}
- **Engagement Metrics**: {ai_indicators.engagement_unnaturalness:.2%}
- **Network Analysis**: {ai_indicators.network_artificiality:.2%}

## Conclusion

This artist exhibits {"strong indicators of AI-generated content and automated behavior" if ai_indicators.overall_ai_probability > 0.7 else "some indicators of potential automation" if ai_indicators.overall_ai_probability > 0.4 else "minimal indicators of AI involvement"}.

**BfV Recommendation**: {"Immediate notification and deep investigation" if ai_indicators.overall_ai_probability > 0.8 else "Enhanced monitoring and content analysis" if ai_indicators.overall_ai_probability > 0.6 else "Periodic security review" if ai_indicators.overall_ai_probability > 0.4 else "Standard monitoring protocol"}

---

*Analysis conducted using Advanced AI Detection System v2.0*  
*Date: {self.collection_date}*  
*Classification: BfV Security Assessment*
"""
        
        return report
    
    def save_ai_analysis(self, artist_data: Dict, ai_indicators: AIIndicators):
        """Speichert die KI-Analyse als separate Datei"""
        name = artist_data.get('name', 'Unknown').replace('/', '_').replace('?', '_').replace(':', '_')
        filename = f"{name}_AI_Analysis.md"
        
        report = self.generate_ai_report(artist_data, ai_indicators)
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✅ KI-Analyse gespeichert: {filename}")
            
            # Speichere auch JSON-Daten für weitere Analyse
            json_filename = f"{name}_AI_Data.json"
            ai_data = {
                'artist_name': name,
                'ai_indicators': {
                    'name_pattern_score': ai_indicators.name_pattern_score,
                    'content_consistency': ai_indicators.content_consistency,
                    'temporal_anomaly': ai_indicators.temporal_anomaly,
                    'network_artificiality': ai_indicators.network_artificiality,
                    'engagement_unnaturalness': ai_indicators.engagement_unnaturalness,
                    'metadata_suspicion': ai_indicators.metadata_suspicion,
                    'overall_ai_probability': ai_indicators.overall_ai_probability
                },
                'analysis_date': self.collection_date,
                'bfv_classification': "CRITICAL" if ai_indicators.overall_ai_probability > 0.8 else "HIGH" if ai_indicators.overall_ai_probability > 0.6 else "MEDIUM" if ai_indicators.overall_ai_probability > 0.4 else "LOW"
            }
            
            with open(json_filename, 'w', encoding='utf-8') as f:
                json.dump(ai_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"❌ Fehler beim Speichern der KI-Analyse: {e}")

def main():
    """Hauptfunktion für die fortgeschrittene KI-Erkennung"""
    print("🤖 Advanced AI Artist Detection System")
    print("🛡️ BfV Security Integration")
    print("=" * 50)
    
    detector = SimpleAIDetector()
    
    # Lade vorhandene Künstlerdaten
    artist_files = [f for f in os.listdir('.') if f.endswith('.md') and f != 'README.md' and not f.endswith('_AI_Analysis.md')]
    
    print(f"📊 Analysiere {len(artist_files)} Künstler auf KI-Indikatoren...")
    
    all_artists_data = []
    high_ai_artists = []
    medium_ai_artists = []
    
    for filename in artist_files:
        try:
            # Extrahiere Daten aus Markdown
            artist_data = detector.extract_data_from_markdown(filename)
            
            if artist_data:
                all_artists_data.append(artist_data)
                
                # Führe KI-Analyse durch
                ai_indicators = detector.detect_ai_artist(artist_data)
                
                if ai_indicators.overall_ai_probability > 0.7:
                    high_ai_artists.append((artist_data['name'], ai_indicators.overall_ai_probability))
                    detector.save_ai_analysis(artist_data, ai_indicators)
                    print(f"🚨 HOHE KI-Wahrscheinlichkeit: {artist_data['name']} ({ai_indicators.overall_ai_probability:.2%})")
                elif ai_indicators.overall_ai_probability > 0.4:
                    medium_ai_artists.append((artist_data['name'], ai_indicators.overall_ai_probability))
                    print(f"⚠️  MITTLERE KI-Wahrscheinlichkeit: {artist_data['name']} ({ai_indicators.overall_ai_probability:.2%})")
                else:
                    print(f"✅ Niedrige KI-Wahrscheinlichkeit: {artist_data['name']} ({ai_indicators.overall_ai_probability:.2%})")
                
        except Exception as e:
            print(f"❌ Fehler bei Analyse von {filename}: {e}")
    
    # Generiere Zusammenfassung
    print(f"\n📊 ZUSAMMENFASSUNG:")
    print(f"   Gesamt analysiert: {len(all_artists_data)} Künstler")
    print(f"   Hohe KI-Wahrscheinlichkeit (>70%): {len(high_ai_artists)} Künstler")
    print(f"   Mittlere KI-Wahrscheinlichkeit (40-70%): {len(medium_ai_artists)} Künstler")
    print(f"   Niedrige KI-Wahrscheinlichkeit (<40%): {len(all_artists_data) - len(high_ai_artists) - len(medium_ai_artists)} Künstler")
    
    if high_ai_artists:
        print(f"\n🚨 KRITISCHE KI-KÜNSTLER (BfV IMMEDIATE ACTION REQUIRED):")
        for name, probability in sorted(high_ai_artists, key=lambda x: x[1], reverse=True):
            print(f"   - {name}: {probability:.2%}")
    
    if medium_ai_artists:
        print(f"\n⚠️  POTENZIELLE KI-KÜNSTLER (BfV ENHANCED MONITORING):")
        for name, probability in sorted(medium_ai_artists, key=lambda x: x[1], reverse=True):
            print(f"   - {name}: {probability:.2%}")
    
    print(f"\n📈 Analyse abgeschlossen: {detector.collection_date}")
    print(f"🛡️ BfV-Klassifizierung wurde für alle Künstler durchgeführt")

if __name__ == "__main__":
    main()
