#!/usr/bin/env python3
"""
Advanced Bot Network Detection System
Für die Doktorarbeit in Zusammenarbeit mit dem Bundesamt für Verfassungsschutz (BfV)
Spezialisiert auf fortgeschrittene Bot-Netzwerke und KI-Künstler-Erkennung
"""

import json
import datetime
import re
import os
import hashlib
import math
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from collections import defaultdict, Counter
import itertools

@dataclass
class BotNetworkIndicators:
    """Bot-Netzwerk-Indikatoren"""
    network_id: str
    artists: List[str]
    size: int
    coordination_strength: float
    temporal_synchronization: float
    engagement_artificiality: float
    naming_convention_score: float
    genre_convergence_score: float
    overall_threat_level: float
    is_ai_generated: bool
    bot_probability: float

class AdvancedBotNetworkDetector:
    def __init__(self):
        """Initialisiert den fortgeschrittenen Bot-Netzwerk-Detektor"""
        self.collection_date = datetime.datetime.now().isoformat()
        self.bot_networks = []
        self.ai_clusters = []
        
        # Fortgeschrittene Bot-Muster
        self.bot_naming_patterns = [
            # Zahlen-basierte Muster
            r'^[a-zA-Z]+[0-9]{3,}$',  # Buchstaben + 3+ Zahlen
            r'^[0-9]{3,}[a-zA-Z]+$',  # 3+ Zahlen + Buchstaben
            r'.*[0-9]{4,}.*',  # 4+ Zahlen im Namen
            
            # Symbol-basierte Muster
            r'.*[xX0][xX0].*',  # Doppel-x/0
            r'.*[xX][0-9].*',  # x + Zahl
            r'.*[0-9][xX].*',  # Zahl + x
            r'^[a-zA-Z]{1,2}[0-9]{1,3}$',  # Kurz + Zahlen
            
            # Leetspeak-Muster
            r'.*[4][a-zA-Z].*',  # 4 statt a
            r'.*[3][a-zA-Z].*',  # 3 statt e
            r'.*[1][a-zA-Z].*',  # 1 statt l
            r'.*[0][a-zA-Z].*',  # 0 statt o
            r'.*[7][a-zA-Z].*',  # 7 statt t
            r'.*[5][a-zA-Z].*',  # 5 statt s
            
            # KI-spezifische Muster
            r'.*[aA][iI].*',  # AI im Namen
            r'.*[bB][oO][tT].*',  # Bot im Namen
            r'.*[gG][eE][nN].*',  # Gen im Namen
            r'.*[sS][yY][nN][tT][hH].*',  # Synth im Namen
            
            # Verdächtige Kombinationen
            r'^[a-z]+[0-9]+[a-z]*$',  # Kleinbuchstaben + Zahlen
            r'^[A-Z]+[0-9]+$',  # Großbuchstaben + Zahlen
            r'.*[0-9][0-9][0-9].*',  # Dreier-Zahlen
        ]
        
        # Bot-Netzwerk Keywords
        self.bot_keywords = [
            'void', 'null', 'echo', 'ghost', 'shadow', 'phantom', 'digital',
            'cyber', 'tech', 'code', 'binary', 'matrix', 'glitch', 'error',
            '404', '500', 'proxy', 'server', 'cloud', 'data', 'byte',
            'neural', 'deep', 'algo', 'auto', 'synth', 'gen', 'ai', 'bot'
        ]
        
        # Verdächtige Genre-Kombinationen für Bot-Netzwerke
        self.bot_genre_combinations = [
            {'trap', 'phonk', 'hyperpop'},
            {'experimental', 'electronic', 'abstract'},
            {'ambient', 'glitch', 'noise'},
            {'trap', 'drill', 'phonk'},
            {'hyperpop', 'experimental', 'electronic'},
            {'phonk', 'electronic', 'trap'},
        ]
        
    def extract_artist_data(self, filename: str) -> Dict:
        """Extrahiert erweiterte Künstlerdaten aus Markdown-Datei"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                
            artist_name = filename.replace('.md', '')
            
            # Extrahiere Followers
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
                    genres = [g.strip().lower() for g in genre_match.group(1).split(',')]
                    
            # Extrahiere Top Tracks mit erweiterten Daten
            top_tracks = []
            track_section = re.search(r'## Top Tracks\n(.*?)(?=\n##|\n#|$)', content, re.DOTALL)
            if track_section:
                track_lines = track_section.group(1).split('\n')
                for line in track_lines:
                    if 'Popularity:' in line:
                        pop_match = re.search(r'Popularity:\s*(\d+)', line)
                        explicit_match = re.search(r'Explicit:\s*(Yes|No)', line)
                        duration_match = re.search(r'(\d+):(\d+)', line)
                        
                        track_data = {
                            'popularity': int(pop_match.group(1)) if pop_match else 0,
                            'explicit': explicit_match.group(1) == 'Yes' if explicit_match else False,
                            'duration_seconds': 0
                        }
                        
                        if duration_match:
                            minutes = int(duration_match.group(1))
                            seconds = int(duration_match.group(2))
                            track_data['duration_seconds'] = minutes * 60 + seconds
                            
                        top_tracks.append(track_data)
                        
            # Extrahiere Alben mit Release-Daten
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
    
    def analyze_naming_conventions(self, artist_names: List[str]) -> float:
        """Analysiert Namenskonventionen für Bot-Netzwerke"""
        if len(artist_names) < 3:
            return 0.0
            
        score = 0.0
        
        # Längen-Anomalien
        lengths = [len(name) for name in artist_names]
        length_variance = sum((l - sum(lengths)/len(lengths))**2 for l in lengths) / len(lengths)
        
        if length_variance < 2:  # Sehr ähnliche Längen
            score += 0.3
            
        # Zeichen-Muster-Analyse
        all_chars = set()
        for name in artist_names:
            all_chars.update(name.lower())
            
        # Begrenzte Zeichen-Vielfalt
        if len(all_chars) < 15:
            score += 0.2
            
        # Gemeinsame Präfixe/Suffixe
        prefixes = [name[:3].lower() for name in artist_names if len(name) >= 3]
        suffixes = [name[-3:].lower() for name in artist_names if len(name) >= 3]
        
        prefix_counter = Counter(prefixes)
        suffix_counter = Counter(suffixes)
        
        if any(count > len(artist_names) * 0.4 for count in prefix_counter.values()):
            score += 0.3
            
        if any(count > len(artist_names) * 0.4 for count in suffix_counter.values()):
            score += 0.3
            
        # Zahlen-Muster
        names_with_numbers = [name for name in artist_names if any(c.isdigit() for c in name)]
        if len(names_with_numbers) / len(artist_names) > 0.5:
            score += 0.4
            
        # Symbol-Muster
        symbol_chars = ['x', 'X', '0', '1', '3', '4', '5', '7']
        names_with_symbols = [name for name in artist_names if any(c in name for c in symbol_chars)]
        if len(names_with_symbols) / len(artist_names) > 0.3:
            score += 0.3
            
        return min(score, 1.0)
    
    def analyze_temporal_synchronization(self, albums_data: List[List[Dict]]) -> float:
        """Analysiert zeitliche Synchronisation für Bot-Netzwerke"""
        if len(albums_data) < 3:
            return 0.0
            
        all_dates = []
        for albums in albums_data:
            for album in albums:
                if album.get('release_date'):
                    try:
                        date = datetime.datetime.strptime(album['release_date'][:10], '%Y-%m-%d')
                        all_dates.append(date)
                    except:
                        continue
                        
        if len(all_dates) < 5:
            return 0.0
            
        # Gruppiere nach Monaten
        month_groups = defaultdict(list)
        for date in all_dates:
            month_key = f"{date.year}-{date.month:02d}"
            month_groups[month_key].append(date)
            
        # Finde Cluster von Veröffentlichungen
        max_cluster_size = max(len(group) for group in month_groups.values())
        
        # Hohe Konzentration in bestimmten Monaten
        if max_cluster_size > len(all_dates) * 0.4:
            return 0.8
            
        # Wöchentliche Muster
        weekday_distribution = Counter(date.weekday() for date in all_dates)
        max_weekday_count = max(weekday_distribution.values())
        
        if max_weekday_count > len(all_dates) * 0.3:
            return 0.6
            
        return 0.0
    
    def analyze_engagement_artificiality(self, artists_data: List[Dict]) -> float:
        """Analysiert künstliche Engagement-Muster"""
        if len(artists_data) < 3:
            return 0.0
            
        score = 0.0
        
        # Follower-Anomalien
        followers = [artist.get('followers', 0) for artist in artists_data]
        if followers:
            # Runde Zahlen
            round_followers = [f for f in followers if f in [1000, 5000, 10000, 50000, 100000]]
            if len(round_followers) / len(followers) > 0.3:
                score += 0.4
                
            # Ähnliche Follower-Zahlen
            if len(followers) >= 3:
                mean_followers = sum(followers) / len(followers)
                variance = sum((f - mean_followers)**2 for f in followers) / len(followers)
                if variance < (mean_followers * 0.1)**2:  # Weniger als 10% Varianz
                    score += 0.5
                    
        # Monthly Listeners Anomalien
        listeners = [artist.get('monthly_listeners', 0) for artist in artists_data]
        if listeners:
            # Runde Zahlen
            round_listeners = [l for l in listeners if l in [1000, 5000, 10000, 50000, 100000, 500000, 1000000]]
            if len(round_listeners) / len(listeners) > 0.3:
                score += 0.4
                
            # Ähnliche Listener-Zahlen
            if len(listeners) >= 3:
                mean_listeners = sum(listeners) / len(listeners)
                variance = sum((l - mean_listeners)**2 for l in listeners) / len(listeners)
                if variance < (mean_listeners * 0.1)**2:
                    score += 0.5
                    
        # Follower-zu-Listener Ratios
        ratios = []
        for artist in artists_data:
            followers = artist.get('followers', 0)
            listeners = artist.get('monthly_listeners', 0)
            if followers > 0 and listeners > 0:
                ratios.append(listeners / followers)
                
        if len(ratios) >= 3:
            mean_ratio = sum(ratios) / len(ratios)
            ratio_variance = sum((r - mean_ratio)**2 for r in ratios) / len(ratios)
            if ratio_variance < (mean_ratio * 0.2)**2:  # Weniger als 20% Varianz
                score += 0.4
                
        return min(score, 1.0)
    
    def analyze_genre_convergence(self, genres_data: List[List[str]]) -> float:
        """Analysiert Genre-Konvergenz für Bot-Netzwerke"""
        if len(genres_data) < 3:
            return 0.0
            
        score = 0.0
        
        # Alle Genres sammeln
        all_genres = []
        for genres in genres_data:
            all_genres.extend(genres)
            
        if not all_genres:
            return 0.0
            
        genre_counter = Counter(all_genres)
        
        # Hohe Konzentration auf wenige Genres
        if len(genre_counter) < 5 and len(all_genres) > 10:
            score += 0.4
            
        # Verdächtige Genre-Kombinationen
        genre_set = set(all_genres)
        for bot_combo in self.bot_genre_combinations:
            if bot_combo.issubset(genre_set):
                score += 0.6
                break
                
        # Jeder Künstler hat die gleichen Genres
        unique_genre_sets = set()
        for genres in genres_data:
            unique_genre_sets.add(tuple(sorted(genres)))
            
        if len(unique_genre_sets) == 1 and len(genres_data) > 2:
            score += 0.5
            
        return min(score, 1.0)
    
    def detect_bot_networks(self, artists_data: List[Dict]) -> List[BotNetworkIndicators]:
        """Erkennt Bot-Netzwerke durch Cluster-Analyse"""
        if len(artists_data) < 5:
            return []
            
        bot_networks = []
        
        # Erstelle mögliche Cluster basierend auf verschiedenen Kriterien
        clusters = []
        
        # Cluster nach Namensähnlichkeit
        name_clusters = defaultdict(list)
        for artist in artists_data:
            name = artist.get('name', '').lower()
            
            # Gruppiere nach Namensmustern
            for pattern in self.bot_naming_patterns:
                if re.match(pattern, name):
                    cluster_id = f"pattern_{hash(pattern) % 10000}"
                    name_clusters[cluster_id].append(artist)
                    break
                    
        # Cluster nach Genre-Ähnlichkeit
        genre_clusters = defaultdict(list)
        for i, artist1 in enumerate(artists_data):
            for j, artist2 in enumerate(artists_data[i+1:], i+1):
                genres1 = set(artist1.get('genres', []))
                genres2 = set(artist2.get('genres', []))
                
                if genres1 and genres2:
                    jaccard = len(genres1.intersection(genres2)) / len(genres1.union(genres2))
                    if jaccard > 0.6:  # Hohe Genre-Ähnlichkeit
                        cluster_id = f"genre_{hash(tuple(sorted(genres1.intersection(genres2)))) % 10000}"
                        genre_clusters[cluster_id].extend([artist1, artist2])
                        
        # Cluster nach Engagement-Ähnlichkeit
        engagement_clusters = defaultdict(list)
        for i, artist1 in enumerate(artists_data):
            for j, artist2 in enumerate(artists_data[i+1:], i+1):
                followers1 = artist1.get('followers', 0)
                followers2 = artist2.get('followers', 0)
                listeners1 = artist1.get('monthly_listeners', 0)
                listeners2 = artist2.get('monthly_listeners', 0)
                
                if followers1 > 0 and followers2 > 0 and listeners1 > 0 and listeners2 > 0:
                    ratio1 = listeners1 / followers1
                    ratio2 = listeners2 / followers2
                    
                    if abs(ratio1 - ratio2) < 0.1:  # Sehr ähnliche Ratios
                        cluster_id = f"engagement_{int(ratio1 * 100)}"
                        engagement_clusters[cluster_id].extend([artist1, artist2])
                        
        # Kombiniere Cluster
        all_clusters = {}
        
        for cluster_id, artists in name_clusters.items():
            if len(artists) >= 3:
                # Entferne Duplikate basierend auf Künstlername
                unique_artists = {}
                for artist in artists:
                    name = artist.get('name', '')
                    if name and name not in unique_artists:
                        unique_artists[name] = artist
                all_clusters[cluster_id] = list(unique_artists.values())
                
        for cluster_id, artists in genre_clusters.items():
            if len(artists) >= 3:
                # Entferne Duplikate basierend auf Künstlername
                unique_artists = {}
                for artist in artists:
                    name = artist.get('name', '')
                    if name and name not in unique_artists:
                        unique_artists[name] = artist
                all_clusters[cluster_id] = list(unique_artists.values())
                
        for cluster_id, artists in engagement_clusters.items():
            if len(artists) >= 3:
                # Entferne Duplikate basierend auf Künstlername
                unique_artists = {}
                for artist in artists:
                    name = artist.get('name', '')
                    if name and name not in unique_artists:
                        unique_artists[name] = artist
                all_clusters[cluster_id] = list(unique_artists.values())
                
        # Analysiere jedes Cluster
        for cluster_id, cluster_artists in all_clusters.items():
            if len(cluster_artists) >= 3:
                # Berechne Indikatoren
                artist_names = [artist.get('name', '') for artist in cluster_artists]
                naming_score = self.analyze_naming_conventions(artist_names)
                
                albums_data = [artist.get('albums', []) for artist in cluster_artists]
                temporal_score = self.analyze_temporal_synchronization(albums_data)
                
                engagement_score = self.analyze_engagement_artificiality(cluster_artists)
                
                genres_data = [artist.get('genres', []) for artist in cluster_artists]
                genre_score = self.analyze_genre_convergence(genres_data)
                
                # Gesamtbewertung
                coordination_strength = (
                    naming_score * 0.3 +
                    temporal_score * 0.2 +
                    engagement_score * 0.3 +
                    genre_score * 0.2
                )
                
                # KI-Generierungswahrscheinlichkeit
                ai_keywords_count = sum(1 for name in artist_names 
                                      for keyword in self.bot_keywords 
                                      if keyword in name.lower())
                ai_probability = min(ai_keywords_count / len(artist_names), 1.0)
                
                # Bot-Wahrscheinlichkeit
                bot_probability = coordination_strength
                
                # Overall Threat Level
                threat_level = max(coordination_strength, ai_probability)
                
                network_indicators = BotNetworkIndicators(
                    network_id=cluster_id,
                    artists=artist_names,
                    size=len(cluster_artists),
                    coordination_strength=coordination_strength,
                    temporal_synchronization=temporal_score,
                    engagement_artificiality=engagement_score,
                    naming_convention_score=naming_score,
                    genre_convergence_score=genre_score,
                    overall_threat_level=threat_level,
                    is_ai_generated=ai_probability > 0.5,
                    bot_probability=bot_probability
                )
                
                bot_networks.append(network_indicators)
                
        # Sortiere nach Bedrohungslevel
        bot_networks.sort(key=lambda x: x.overall_threat_level, reverse=True)
        
        return bot_networks
    
    def generate_bot_network_report(self, network: BotNetworkIndicators) -> str:
        """Generiert einen detaillierten Bot-Netzwerk-Bericht"""
        report = f"""# Bot Network Analysis Report: {network.network_id}

## Executive Summary
- **Network ID**: {network.network_id}
- **Network Size**: {network.size} artists
- **Overall Threat Level**: {network.overall_threat_level:.2%}
- **Classification**: {"CRITICAL BOT NETWORK" if network.overall_threat_level > 0.8 else "HIGH-RISK NETWORK" if network.overall_threat_level > 0.6 else "SUSPICIOUS NETWORK" if network.overall_threat_level > 0.4 else "LOW-RISK NETWORK"}
- **AI Generated**: {"YES" if network.is_ai_generated else "NO"}
- **Bot Probability**: {network.bot_probability:.2%}

## Network Members
{chr(10).join(f"- {artist}" for artist in network.artists)}

## Detailed Analysis

### 1. Coordination Strength: {network.coordination_strength:.2%}
- **Naming Conventions**: {network.naming_convention_score:.2%}
- **Temporal Synchronization**: {network.temporal_synchronization:.2%}
- **Engagement Artificiality**: {network.engagement_artificiality:.2%}
- **Genre Convergence**: {network.genre_convergence_score:.2%}

### 2. Naming Convention Analysis: {network.naming_convention_score:.2%}
- **Pattern Consistency**: {"HIGH" if network.naming_convention_score > 0.6 else "MEDIUM" if network.naming_convention_score > 0.3 else "LOW"}
- **Character Similarity**: {"DETECTED" if network.naming_convention_score > 0.5 else "MINIMAL"}
- **Automated Generation**: {"LIKELY" if network.naming_convention_score > 0.7 else "POSSIBLE" if network.naming_convention_score > 0.4 else "UNLIKELY"}

### 3. Temporal Synchronization: {network.temporal_synchronization:.2%}
- **Release Coordination**: {"COORDINATED" if network.temporal_synchronization > 0.6 else "PARTIAL" if network.temporal_synchronization > 0.3 else "NATURAL"}
- **Automated Scheduling**: {"HIGH PROBABILITY" if network.temporal_synchronization > 0.7 else "POSSIBLE" if network.temporal_synchronization > 0.4 else "LOW"}
- **Bot Activity Patterns**: {"PRESENT" if network.temporal_synchronization > 0.5 else "ABSENT"}

### 4. Engagement Artificiality: {network.engagement_artificiality:.2%}
- **Follower Manipulation**: {"LIKELY" if network.engagement_artificiality > 0.6 else "POSSIBLE" if network.engagement_artificiality > 0.3 else "UNLIKELY"}
- **Stream Inflation**: {"DETECTED" if network.engagement_artificiality > 0.7 else "SUSPECTED" if network.engagement_artificiality > 0.4 else "NATURAL"}
- **Artificial Metrics**: {"HIGH" if network.engagement_artificiality > 0.5 else "MEDIUM" if network.engagement_artificiality > 0.3 else "LOW"}

### 5. Genre Convergence: {network.genre_convergence_score:.2%}
- **Genre Manipulation**: {"EVIDENT" if network.genre_convergence_score > 0.6 else "SUSPECTED" if network.genre_convergence_score > 0.3 else "NATURAL"}
- **Algorithm Gaming**: {"DETECTED" if network.genre_convergence_score > 0.7 else "POSSIBLE" if network.genre_convergence_score > 0.4 else "UNLIKELY"}
- **Targeted Placement**: {"ACTIVE" if network.genre_convergence_score > 0.5 else "PASSIVE"}

## Security Assessment

### BfV Classification
- **Threat Category**: {"ORGANIZED BOT NETWORK" if network.overall_threat_level > 0.8 else "COORDINATED MANIPULATION" if network.overall_threat_level > 0.6 else "SUSPICIOUS ACTIVITY" if network.overall_threat_level > 0.4 else "MONITORING REQUIRED"}
- **Priority Level**: {"IMMEDIATE ACTION" if network.overall_threat_level > 0.8 else "HIGH PRIORITY" if network.overall_threat_level > 0.6 else "MEDIUM PRIORITY" if network.overall_threat_level > 0.4 else "LOW PRIORITY"}
- **AI Involvement**: {"CONFIRMED" if network.is_ai_generated else "SUSPECTED" if network.bot_probability > 0.5 else "UNLIKELY"}

### Recommended Actions
- {"IMMEDIATE NETWORK DISRUPTION" if network.overall_threat_level > 0.8 else "ENHANCED MONITORING" if network.overall_threat_level > 0.6 else "PERIODIC REVIEW" if network.overall_threat_level > 0.4 else "STANDARD SURVEILLANCE"}
- {"FULL NETWORK ANALYSIS" if network.overall_threat_level > 0.7 else "TARGETED INVESTIGATION" if network.overall_threat_level > 0.4 else "OBSERVATION"}
- {"COORDINATED TAKEDOWN" if network.bot_probability > 0.8 else "SELECTIVE REMOVAL" if network.bot_probability > 0.5 else "MONITORING"}

## Technical Evidence

### Network Characteristics
- **Cluster Size**: {network.size} artists
- **Coordination Patterns**: {"HIGHLY COORDINATED" if network.coordination_strength > 0.7 else "MODERATELY COORDINATED" if network.coordination_strength > 0.4 else "LOOSELY ASSOCIATED"}
- **Automation Level**: {"HIGH" if network.bot_probability > 0.7 else "MEDIUM" if network.bot_probability > 0.4 else "LOW"}

### Manipulation Indicators
- **Naming Patterns**: {"AUTOMATED" if network.naming_convention_score > 0.6 else "SEMI-AUTOMATED" if network.naming_convention_score > 0.3 else "MANUAL"}
- **Temporal Patterns**: {"BOT-LIKE" if network.temporal_synchronization > 0.6 else "SUSPICIOUS" if network.temporal_synchronization > 0.3 else "NATURAL"}
- **Engagement Patterns**: {"ARTIFICIAL" if network.engagement_artificiality > 0.6 else "MANIPULATED" if network.engagement_artificiality > 0.3 else "ORGANIC"}

## Conclusion

This network exhibits {"strong evidence of coordinated bot activity" if network.overall_threat_level > 0.7 else "indications of potential manipulation" if network.overall_threat_level > 0.4 else "minimal coordination indicators"}.

**BfV Recommendation**: {"Immediate network disruption and investigation" if network.overall_threat_level > 0.8 else "Enhanced monitoring and partial disruption" if network.overall_threat_level > 0.6 else "Periodic security review" if network.overall_threat_level > 0.4 else "Standard monitoring protocol"}

---

*Analysis conducted using Advanced Bot Network Detection System v3.0*  
*Date: {self.collection_date}*  
*Classification: BfV Security Assessment*
"""
        
        return report
    
    def save_bot_network_analysis(self, network: BotNetworkIndicators):
        """Speichert die Bot-Netzwerk-Analyse"""
        filename = f"Bot_Network_{network.network_id}_Analysis.md"
        
        report = self.generate_bot_network_report(network)
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✅ Bot-Netzwerk-Analyse gespeichert: {filename}")
            
            # Speichere auch JSON-Daten
            json_filename = f"Bot_Network_{network.network_id}_Data.json"
            network_data = {
                'network_id': network.network_id,
                'artists': network.artists,
                'size': network.size,
                'coordination_strength': network.coordination_strength,
                'temporal_synchronization': network.temporal_synchronization,
                'engagement_artificiality': network.engagement_artificiality,
                'naming_convention_score': network.naming_convention_score,
                'genre_convergence_score': network.genre_convergence_score,
                'overall_threat_level': network.overall_threat_level,
                'is_ai_generated': network.is_ai_generated,
                'bot_probability': network.bot_probability,
                'analysis_date': self.collection_date,
                'bfv_classification': "CRITICAL" if network.overall_threat_level > 0.8 else "HIGH" if network.overall_threat_level > 0.6 else "MEDIUM" if network.overall_threat_level > 0.4 else "LOW"
            }
            
            with open(json_filename, 'w', encoding='utf-8') as f:
                json.dump(network_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"❌ Fehler beim Speichern der Bot-Netzwerk-Analyse: {e}")

def main():
    """Hauptfunktion für die Bot-Netzwerk-Erkennung"""
    print("🕸️ Advanced Bot Network Detection System")
    print("🛡️ BfV Security Integration")
    print("=" * 50)
    
    detector = AdvancedBotNetworkDetector()
    
    # Lade vorhandene Künstlerdaten
    artist_files = [f for f in os.listdir('.') if f.endswith('.md') and f != 'README.md' and not f.endswith('_AI_Analysis.md') and not f.endswith('Analysis.md')]
    
    print(f"📊 Analysiere {len(artist_files)} Künstler auf Bot-Netzwerk-Muster...")
    
    all_artists_data = []
    
    for filename in artist_files:
        try:
            artist_data = detector.extract_artist_data(filename)
            if artist_data:
                all_artists_data.append(artist_data)
        except Exception as e:
            print(f"❌ Fehler bei Verarbeitung von {filename}: {e}")
    
    # Erkenne Bot-Netzwerke
    print("\n🔍 Erkenne Bot-Netzwerke...")
    bot_networks = detector.detect_bot_networks(all_artists_data)
    
    # Speichere Analysen für verdächtige Netzwerke
    critical_networks = []
    high_risk_networks = []
    suspicious_networks = []
    
    for network in bot_networks:
        if network.overall_threat_level > 0.8:
            critical_networks.append(network)
            detector.save_bot_network_analysis(network)
            print(f"🚨 KRITISCHES BOT-NETZWERK: {network.network_id} ({network.overall_threat_level:.2%}) - {network.size} Künstler")
        elif network.overall_threat_level > 0.6:
            high_risk_networks.append(network)
            detector.save_bot_network_analysis(network)
            print(f"⚠️  HOHRISIKO BOT-NETZWERK: {network.network_id} ({network.overall_threat_level:.2%}) - {network.size} Künstler")
        elif network.overall_threat_level > 0.4:
            suspicious_networks.append(network)
            detector.save_bot_network_analysis(network)
            print(f"🔍 VERDÄCHTIGES NETZWERK: {network.network_id} ({network.overall_threat_level:.2%}) - {network.size} Künstler")
    
    # Generiere Zusammenfassung
    print(f"\n📊 BOT-NETZWERK ZUSAMMENFASSUNG:")
    print(f"   Gesamt analysiert: {len(all_artists_data)} Künstler")
    print(f"   Erkannte Netzwerke: {len(bot_networks)}")
    print(f"   Kritische Netzwerke (>80%): {len(critical_networks)}")
    print(f"   Hochrisiko-Netzwerke (60-80%): {len(high_risk_networks)}")
    print(f"   Verdächtige Netzwerke (40-60%): {len(suspicious_networks)}")
    
    if critical_networks:
        print(f"\n🚨 KRITISCHE BOT-NETZWERKE (BfV IMMEDIATE ACTION):")
        for network in critical_networks:
            print(f"   - {network.network_id}: {network.overall_threat_level:.2%} ({network.size} Künstler)")
            print(f"     Künstler: {', '.join(network.artists[:5])}{'...' if len(network.artists) > 5 else ''}")
    
    if high_risk_networks:
        print(f"\n⚠️  HOHRISIKO BOT-NETZWERKE (BfV ENHANCED MONITORING):")
        for network in high_risk_networks:
            print(f"   - {network.network_id}: {network.overall_threat_level:.2%} ({network.size} Künstler)")
            print(f"     Künstler: {', '.join(network.artists[:5])}{'...' if len(network.artists) > 5 else ''}")
    
    print(f"\n📈 Bot-Netzwerk-Analyse abgeschlossen: {detector.collection_date}")
    print(f"🛡️ BfV-Klassifizierung wurde für alle Netzwerke durchgeführt")

if __name__ == "__main__":
    main()
