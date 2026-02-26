#!/usr/bin/env python3
"""
Intelligent Stream Bot Detection System
Advanced algorithms for detecting coordinated streaming manipulation and bot networks
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from datetime import datetime, timedelta
import json
import re
from collections import defaultdict, Counter
import math
import random

@dataclass
class StreamEvent:
    """Individual stream event data structure"""
    timestamp: datetime
    user_id: str
    artist_id: str
    track_id: str
    duration_seconds: int
    completion_rate: float
    source: str  # playlist, algorithm, direct, etc.
    ip_address: str
    user_agent: str
    geographic_location: str

@dataclass
class UserProfile:
    """User profile for behavioral analysis"""
    user_id: str
    registration_date: datetime
    total_streams: int
    unique_artists: int
    avg_session_duration: float
    stream_frequency: float
    geographic_consistency: float
    device_fingerprint: str
    behavioral_score: float

class StreamBotDetector:
    """Advanced detection system for streaming manipulation"""
    
    def __init__(self):
        self.suspicious_patterns = {
            'perfect_completion': 0.98,  # 98%+ completion rate
            'identical_duration': 0.95,  # 95% identical session durations
            'max_daily_streams': 1000,   # Unrealistic daily stream count
            'min_unique_artists': 5,     # Too few unique artists
            'rapid_succession': 30,      # Streams within 30 seconds
            'geographic_jump_threshold': 1000,  # km between consecutive streams
        }
        
        self.bot_network_indicators = {
            'coordination_threshold': 0.8,  # 80% simultaneous activity
            'amplification_factor': 10,     # 10x normal engagement
            'temporal_consistency': 0.9,    # 90% timing consistency
        }
    
    def detect_perfect_completion_bots(self, stream_events: List[StreamEvent]) -> Dict:
        """Detect bots with unnaturally perfect completion rates"""
        user_completion_rates = defaultdict(list)
        
        for event in stream_events:
            user_completion_rates[event.user_id].append(event.completion_rate)
        
        suspicious_users = []
        for user_id, completion_rates in user_completion_rates.items():
            if len(completion_rates) < 10:  # Insufficient data
                continue
            
            avg_completion = np.mean(completion_rates)
            completion_std = np.std(completion_rates)
            
            # Perfect or near-perfect completion with low variance
            if (avg_completion >= self.suspicious_patterns['perfect_completion'] and 
                completion_std < 0.05):
                suspicious_users.append({
                    'user_id': user_id,
                    'avg_completion': avg_completion,
                    'completion_std': completion_std,
                    'total_streams': len(completion_rates),
                    'confidence': min(0.9, (avg_completion - 0.95) * 20),
                    'bot_type': 'PERFECT_COMPLETION_BOT'
                })
        
        return {
            'suspicious_users': suspicious_users,
            'total_analyzed': len(user_completion_rates),
            'detection_rate': len(suspicious_users) / len(user_completion_rates) if user_completion_rates else 0
        }
    
    def analyze_temporal_patterns(self, stream_events: List[StreamEvent]) -> Dict:
        """Detect coordinated temporal patterns indicating bot networks"""
        # Group events by hour
        hourly_activity = defaultdict(int)
        user_hourly_activity = defaultdict(lambda: defaultdict(int))
        
        for event in stream_events:
            hour = event.timestamp.replace(minute=0, second=0, microsecond=0)
            hourly_activity[hour] += 1
            user_hourly_activity[event.user_id][hour] += 1
        
        # Detect coordinated activity spikes
        activity_hours = sorted(hourly_activity.items())
        if len(activity_hours) < 24:
            return {'status': 'insufficient_data'}
        
        # Calculate baseline activity
        activity_values = [count for _, count in activity_hours]
        baseline_mean = np.mean(activity_values)
        baseline_std = np.std(activity_values)
        
        # Find significant spikes
        spike_threshold = baseline_mean + 2 * baseline_std
        coordinated_spikes = []
        
        for hour, count in activity_hours:
            if count > spike_threshold:
                # Check which users were active during this spike
                active_users = []
                for user_id, user_hours in user_hourly_activity.items():
                    if user_hours.get(hour, 0) > 0:
                        active_users.append(user_id)
                
                coordinated_spikes.append({
                    'timestamp': hour,
                    'activity_count': count,
                    'baseline_mean': baseline_mean,
                    'spike_multiplier': count / baseline_mean,
                    'active_users': active_users,
                    'coordination_score': len(active_users) / count if count > 0 else 0
                })
        
        # Analyze user coordination patterns
        user_coordination = defaultdict(int)
        for spike in coordinated_spikes:
            for user_id in spike['active_users']:
                user_coordination[user_id] += 1
        
        coordinated_users = [
            {
                'user_id': user_id,
                'coordinated_events': count,
                'coordination_frequency': count / len(coordinated_spikes),
                'bot_probability': min(0.9, count / len(coordinated_spikes) * 2)
            }
            for user_id, count in user_coordination.items()
            if count > len(coordinated_spikes) * 0.3  # Active in 30%+ of spikes
        ]
        
        return {
            'coordinated_spikes': coordinated_spikes,
            'coordinated_users': coordinated_users,
            'baseline_activity': {
                'mean': baseline_mean,
                'std': baseline_std,
                'total_hours_analyzed': len(activity_hours)
            },
            'network_coordination_score': len(coordinated_users) / len(user_hourly_activity) if user_hourly_activity else 0
        }
    
    def detect_geographic_anomalies(self, stream_events: List[StreamEvent]) -> Dict:
        """Detect impossible geographic travel patterns"""
        user_locations = defaultdict(list)
        
        for event in stream_events:
            user_locations[event.user_id].append({
                'timestamp': event.timestamp,
                'location': event.geographic_location,
                'ip_address': event.ip_address
            })
        
        suspicious_users = []
        
        for user_id, locations in user_locations.items():
            if len(locations) < 2:
                continue
            
            # Sort by timestamp
            locations.sort(key=lambda x: x['timestamp'])
            
            # Check for impossible travel
            for i in range(1, len(locations)):
                prev_loc = locations[i-1]
                curr_loc = locations[i]
                
                time_diff = (curr_loc['timestamp'] - prev_loc['timestamp']).total_seconds()
                
                if time_diff <= 0:
                    continue
                
                # Simple distance calculation (would need proper geo coordinates in real implementation)
                # For now, use location string changes as proxy
                if prev_loc['location'] != curr_loc['location']:
                    # Rapid location changes are suspicious
                    if time_diff < 300:  # 5 minutes
                        suspicious_users.append({
                            'user_id': user_id,
                            'anomaly_type': 'RAPID_LOCATION_CHANGE',
                            'time_diff_seconds': time_diff,
                            'locations': [prev_loc['location'], curr_loc['location']],
                            'confidence': 0.8
                        })
        
        return {
            'suspicious_users': suspicious_users,
            'total_users_analyzed': len(user_locations),
            'anomaly_rate': len(suspicious_users) / len(user_locations) if user_locations else 0
        }
    
    def analyze_device_fingerprinting(self, stream_events: List[StreamEvent]) -> Dict:
        """Detect device fingerprint manipulation and bot farms"""
        user_agents = defaultdict(list)
        ip_addresses = defaultdict(list)
        
        for event in stream_events:
            user_agents[event.user_id].append(event.user_agent)
            ip_addresses[event.user_id].append(event.ip_address)
        
        suspicious_patterns = []
        
        # Check for rotating user agents
        for user_id, agents in user_agents.items():
            unique_agents = set(agents)
            if len(unique_agents) > 5 and len(agents) > 20:
                suspicious_patterns.append({
                    'user_id': user_id,
                    'pattern_type': 'ROTATING_USER_AGENTS',
                    'unique_agents': len(unique_agents),
                    'total_requests': len(agents),
                    'rotation_frequency': len(unique_agents) / len(agents),
                    'confidence': min(0.9, len(unique_agents) / 10)
                })
        
        # Check for IP rotation
        for user_id, ips in ip_addresses.items():
            unique_ips = set(ips)
            if len(unique_ips) > 3 and len(ips) > 10:
                suspicious_patterns.append({
                    'user_id': user_id,
                    'pattern_type': 'IP_ROTATION',
                    'unique_ips': len(unique_ips),
                    'total_requests': len(ips),
                    'rotation_frequency': len(unique_ips) / len(ips),
                    'confidence': min(0.8, len(unique_ips) / 5)
                })
        
        return {
            'suspicious_patterns': suspicious_patterns,
            'total_users_analyzed': len(user_agents),
            'pattern_detection_rate': len(suspicious_patterns) / len(user_agents) if user_agents else 0
        }
    
    def detect_playlist_manipulation(self, stream_events: List[StreamEvent]) -> Dict:
        """Detect coordinated playlist manipulation"""
        playlist_streams = defaultdict(lambda: defaultdict(int))
        
        for event in stream_events:
            if event.source.startswith('playlist'):
                playlist_streams[event.source][event.user_id] += 1
        
        manipulated_playlists = []
        
        for playlist_id, user_streams in playlist_streams.items():
            if len(user_streams) < 10:
                continue
            
            # Check for unusual concentration
            total_streams = sum(user_streams.values())
            max_user_streams = max(user_streams.values())
            
            concentration_ratio = max_user_streams / total_streams
            
            if concentration_ratio > 0.5:  # One user accounts for 50%+ of streams
                suspicious_user = max(user_streams.items(), key=lambda x: x[1])
                manipulated_playlists.append({
                    'playlist_id': playlist_id,
                    'total_streams': total_streams,
                    'suspicious_user': suspicious_user[0],
                    'user_stream_count': suspicious_user[1],
                    'concentration_ratio': concentration_ratio,
                    'manipulation_confidence': min(0.9, concentration_ratio * 1.5)
                })
        
        return {
            'manipulated_playlists': manipulated_playlists,
            'total_playlists_analyzed': len(playlist_streams),
            'manipulation_rate': len(manipulated_playlists) / len(playlist_streams) if playlist_streams else 0
        }
    
    def comprehensive_stream_analysis(self, stream_events: List[StreamEvent]) -> Dict:
        """Perform comprehensive stream manipulation analysis"""
        
        # Run all detection methods
        completion_analysis = self.detect_perfect_completion_bots(stream_events)
        temporal_analysis = self.analyze_temporal_patterns(stream_events)
        geographic_analysis = self.detect_geographic_anomalies(stream_events)
        device_analysis = self.analyze_device_fingerprinting(stream_events)
        playlist_analysis = self.detect_playlist_manipulation(stream_events)
        
        # Aggregate suspicious users
        all_suspicious_users = set()
        user_confidence_scores = defaultdict(float)
        
        # Collect suspicious users from all analyses
        for analysis in [completion_analysis, temporal_analysis, geographic_analysis, device_analysis]:
            if 'suspicious_users' in analysis:
                for user in analysis['suspicious_users']:
                    all_suspicious_users.add(user['user_id'])
                    user_confidence_scores[user['user_id']] += user.get('confidence', 0.5)
        
        if 'coordinated_users' in temporal_analysis:
            for user in temporal_analysis['coordinated_users']:
                all_suspicious_users.add(user['user_id'])
                user_confidence_scores[user['user_id']] += user.get('bot_probability', 0.5)
        
        # Normalize confidence scores
        max_confidence = max(user_confidence_scores.values()) if user_confidence_scores else 1
        normalized_scores = {
            user_id: confidence / max_confidence 
            for user_id, confidence in user_confidence_scores.items()
        }
        
        # Classify users
        high_confidence_bots = [
            user_id for user_id, confidence in normalized_scores.items() 
            if confidence >= 0.8
        ]
        
        medium_confidence_bots = [
            user_id for user_id, confidence in normalized_scores.items() 
            if 0.6 <= confidence < 0.8
        ]
        
        return {
            'summary': {
                'total_streams_analyzed': len(stream_events),
                'total_users': len(set(event.user_id for event in stream_events)),
                'high_confidence_bots': len(high_confidence_bots),
                'medium_confidence_bots': len(medium_confidence_bots),
                'overall_bot_rate': len(all_suspicious_users) / len(set(event.user_id for event in stream_events)) if stream_events else 0
            },
            'detection_results': {
                'completion_analysis': completion_analysis,
                'temporal_analysis': temporal_analysis,
                'geographic_analysis': geographic_analysis,
                'device_analysis': device_analysis,
                'playlist_analysis': playlist_analysis
            },
            'bot_classifications': {
                'high_confidence': high_confidence_bots,
                'medium_confidence': medium_confidence_bots,
                'all_suspicious': list(all_suspicious_users),
                'confidence_scores': normalized_scores
            },
            'recommendations': self._generate_stream_recommendations(normalized_scores)
        }
    
    def _generate_stream_recommendations(self, confidence_scores: Dict[str, float]) -> List[str]:
        """Generate recommendations based on stream analysis"""
        recommendations = []
        
        high_confidence_count = sum(1 for score in confidence_scores.values() if score >= 0.8)
        total_suspicious = len(confidence_scores)
        
        if high_confidence_count > 100:
            recommendations.extend([
                "CRITICAL: Large-scale bot network detected",
                "IMMEDIATE platform-wide investigation required",
                "Coordinate with cybersecurity teams",
                "Implement emergency bot detection measures"
            ])
        elif high_confidence_count > 50:
            recommendations.extend([
                "Significant bot activity detected",
                "Enhanced monitoring recommended",
                "Review authentication systems"
            ])
        elif total_suspicious > 0:
            recommendations.extend([
                "Suspicious patterns identified",
                "Implement targeted monitoring",
                "Review high-confidence accounts"
            ])
        
        return recommendations

class BotNetworkCoordinator:
    """Advanced bot network coordination detection"""
    
    def __init__(self):
        self.coordination_patterns = {
            'temporal_sync': 0.8,      # 80% temporal synchronization
            'target_amplification': 5,  # 5x normal amplification
            'network_density': 0.3,     # 30% network density threshold
        }
    
    def detect_coordinated_amplification(self, stream_events: List[StreamEvent], 
                                       target_artists: List[str]) -> Dict:
        """Detect coordinated amplification of specific artists"""
        artist_streams = defaultdict(list)
        
        for event in stream_events:
            if event.artist_id in target_artists:
                artist_streams[event.artist_id].append(event)
        
        coordinated_campaigns = []
        
        for artist_id, events in artist_streams.items():
            if len(events) < 50:  # Insufficient data
                continue
            
            # Analyze temporal patterns for this artist
            hourly_counts = defaultdict(int)
            for event in events:
                hour = event.timestamp.replace(minute=0, second=0, microsecond=0)
                hourly_counts[hour] += 1
            
            # Detect amplification spikes
            if len(hourly_counts) > 24:
                counts = list(hourly_counts.values())
                mean_count = np.mean(counts)
                std_count = np.std(counts)
                
                threshold = mean_count + 2 * std_count
                
                amplification_periods = [
                    {
                        'timestamp': hour,
                        'stream_count': count,
                        'amplification_factor': count / mean_count
                    }
                    for hour, count in hourly_counts.items()
                    if count > threshold
                ]
                
                if amplification_periods:
                    coordinated_campaigns.append({
                        'artist_id': artist_id,
                        'amplification_periods': amplification_periods,
                        'max_amplification': max(ap['amplification_factor'] for ap in amplification_periods),
                        'campaign_confidence': min(0.9, len(amplification_periods) / 10)
                    })
        
        return {
            'coordinated_campaigns': coordinated_campaigns,
            'target_artists_analyzed': len(target_artists),
            'campaigns_detected': len(coordinated_campaigns)
        }

# Example usage
if __name__ == "__main__":
    # Initialize detector
    detector = StreamBotDetector()
    coordinator = BotNetworkCoordinator()
    
    # Generate sample data for testing
    sample_events = []
    base_time = datetime.now()
    
    # Simulate bot activity
    for i in range(1000):
        event = StreamEvent(
            timestamp=base_time + timedelta(minutes=i),
            user_id=f"bot_user_{i % 10}",
            artist_id="target_artist",
            track_id=f"track_{i % 5}",
            duration_seconds=180,
            completion_rate=0.99,  # Perfect completion
            source="playlist_bot",
            ip_address=f"192.168.1.{i % 255}",
            user_agent="BotAgent/1.0",
            geographic_location="BotLocation"
        )
        sample_events.append(event)
    
    # Run analysis
    results = detector.comprehensive_stream_analysis(sample_events)
    print("Stream Bot Detection Results:")
    print(json.dumps(results['summary'], indent=2))
