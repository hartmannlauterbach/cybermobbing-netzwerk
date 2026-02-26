#!/usr/bin/env python3
"""
Experimental Bot Network Analysis Framework
Advanced methodologies for detecting and analyzing sophisticated bot networks
"""

import numpy as np
import pandas as pd
import networkx as nx
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from datetime import datetime, timedelta
import json
import re
from collections import defaultdict, Counter
import math
import random
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

@dataclass
class NetworkNode:
    """Node representing a potential bot or coordinated entity"""
    node_id: str
    node_type: str  # artist, user, playlist, social_account
    activity_patterns: Dict
    connections: Set[str]
    behavioral_score: float
    temporal_signature: Dict
    geographic_distribution: Dict

@dataclass
class NetworkEdge:
    """Edge representing relationships between nodes"""
    source: str
    target: str
    edge_type: str  # collaboration, follow, stream, mention
    weight: float
    temporal_pattern: Dict
    coordination_score: float

class ExperimentalNetworkAnalyzer:
    """Experimental analysis methods for advanced bot network detection"""
    
    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self.clustering_algorithms = {
            'dbscan': DBSCAN(eps=0.5, min_samples=3),
            'spectral': None,  # Would implement spectral clustering
            'hierarchical': None  # Would implement hierarchical clustering
        }
        
        self.experimental_thresholds = {
            'coordination_threshold': 0.85,
            'temporal_consistency': 0.9,
            'behavioral_similarity': 0.8,
            'network_density': 0.4,
            'amplification_factor': 15
        }
    
    def build_multilayer_network(self, artists_data: List[Dict], stream_data: List[Dict], 
                                social_data: List[Dict]) -> nx.MultiDiGraph:
        """Build multi-layer network representation"""
        
        # Layer 1: Artist Collaboration Network
        for artist in artists_data:
            self.graph.add_node(
                artist['spotify_id'],
                node_type='artist',
                name=artist['name'],
                monthly_listeners=artist['monthly_listeners'],
                genre=artist['genre'],
                layer='collaboration'
            )
            
            for collaborator in artist.get('collaborations', []):
                self.graph.add_edge(
                    artist['spotify_id'],
                    collaborator,
                    edge_type='collaboration',
                    layer='collaboration',
                    weight=1.0
                )
        
        # Layer 2: Stream Activity Network
        for stream in stream_data:
            user_id = stream['user_id']
            artist_id = stream['artist_id']
            
            if not self.graph.has_node(user_id):
                self.graph.add_node(
                    user_id,
                    node_type='user',
                    layer='stream'
                )
            
            if self.graph.has_edge(user_id, artist_id):
                self.graph[user_id][artist_id][0]['weight'] += stream['duration_seconds']
            else:
                self.graph.add_edge(
                    user_id,
                    artist_id,
                    edge_type='stream',
                    layer='stream',
                    weight=stream['duration_seconds'],
                    timestamp=stream['timestamp']
                )
        
        # Layer 3: Social Media Network
        for social in social_data:
            user_id = social['user_id']
            platform = social['platform']
            
            if not self.graph.has_node(user_id):
                self.graph.add_node(
                    user_id,
                    node_type='social_user',
                    platform=platform,
                    layer='social'
                )
            
            for connection in social.get('connections', []):
                if not self.graph.has_node(connection):
                    self.graph.add_node(
                        connection,
                        node_type='social_user',
                        platform=platform,
                        layer='social'
                    )
                
                self.graph.add_edge(
                    user_id,
                    connection,
                    edge_type='social_connection',
                    layer='social',
                    platform=platform,
                    weight=1.0
                )
        
        return self.graph
    
    def detect_coordination_patterns(self) -> Dict:
        """Detect sophisticated coordination patterns across network layers"""
        
        coordination_patterns = {
            'temporal_coordination': self._analyze_temporal_coordination(),
            'cross_layer_coordination': self._analyze_cross_layer_coordination(),
            'behavioral_coordination': self._analyze_behavioral_coordination(),
            'amplification_coordination': self._analyze_amplification_coordination()
        }
        
        # Calculate overall coordination scores
        overall_scores = {}
        
        for node in self.graph.nodes():
            node_scores = []
            for pattern_type, pattern_data in coordination_patterns.items():
                if node in pattern_data.get('node_scores', {}):
                    node_scores.append(pattern_data['node_scores'][node])
            
            if node_scores:
                overall_scores[node] = np.mean(node_scores)
        
        return {
            'coordination_patterns': coordination_patterns,
            'overall_coordination_scores': overall_scores,
            'highly_coordinated_nodes': [
                node for node, score in overall_scores.items() 
                if score > self.experimental_thresholds['coordination_threshold']
            ]
        }
    
    def _analyze_temporal_coordination(self) -> Dict:
        """Analyze temporal coordination patterns"""
        temporal_patterns = defaultdict(list)
        
        for edge_data in self.graph.edges(data=True):
            if 'timestamp' in edge_data[2]:
                source, target, data = edge_data
                timestamp = data['timestamp']
                hour_bucket = timestamp.replace(minute=0, second=0, microsecond=0)
                
                temporal_patterns[hour_bucket].append({
                    'source': source,
                    'target': target,
                    'edge_type': data['edge_type']
                })
        
        # Detect coordinated activity bursts
        coordination_scores = defaultdict(float)
        
        for timestamp, activities in temporal_patterns.items():
            if len(activities) > 10:  # Significant activity
                # Analyze participant overlap
                participants = set()
                for activity in activities:
                    participants.add(activity['source'])
                    participants.add(activity['target'])
                
                # High participation in short time suggests coordination
                coordination_strength = len(activities) / len(participants)
                
                for participant in participants:
                    coordination_scores[participant] += coordination_strength
        
        # Normalize scores
        max_score = max(coordination_scores.values()) if coordination_scores else 1
        normalized_scores = {
            node: score / max_score 
            for node, score in coordination_scores.items()
        }
        
        return {
            'temporal_bursts': len([t for t, a in temporal_patterns.items() if len(a) > 10]),
            'node_scores': normalized_scores,
            'coordination_events': temporal_patterns
        }
    
    def _analyze_cross_layer_coordination(self) -> Dict:
        """Analyze coordination across different network layers"""
        cross_layer_scores = defaultdict(float)
        
        # Find nodes that appear in multiple layers
        node_layers = defaultdict(set)
        for node, data in self.graph.nodes(data=True):
            layer = data.get('layer', 'unknown')
            node_layers[node].add(layer)
        
        # Multi-layer participation is suspicious
        for node, layers in node_layers.items():
            if len(layers) > 1:
                cross_layer_scores[node] = len(layers) / 3  # Normalize by max possible layers
        
        # Analyze cross-layer connectivity patterns
        for node in self.graph.nodes():
            layer_connections = defaultdict(set)
            
            for neighbor in self.graph.neighbors(node):
                neighbor_layer = self.graph.nodes[neighbor].get('layer', 'unknown')
                layer_connections[neighbor_layer].add(neighbor)
            
            # Suspicious if connected to similar nodes across layers
            for layer, connections in layer_connections.items():
                if len(connections) > 5:
                    cross_layer_scores[node] += 0.3
        
        return {
            'multi_layer_nodes': len([n for n, l in node_layers.items() if len(l) > 1]),
            'node_scores': cross_layer_scores,
            'layer_distribution': node_layers
        }
    
    def _analyze_behavioral_coordination(self) -> Dict:
        """Analyze behavioral similarity and coordination"""
        behavioral_scores = defaultdict(float)
        
        # Group nodes by type
        nodes_by_type = defaultdict(list)
        for node, data in self.graph.nodes(data=True):
            node_type = data.get('node_type', 'unknown')
            nodes_by_type[node_type].append(node)
        
        # Analyze behavioral similarity within each type
        for node_type, nodes in nodes_by_type.items():
            if len(nodes) < 3:
                continue
            
            # Extract behavioral features
            behavioral_features = {}
            for node in nodes:
                features = self._extract_behavioral_features(node)
                behavioral_features[node] = features
            
            # Calculate similarity scores
            for i, node1 in enumerate(nodes):
                similarities = []
                for j, node2 in enumerate(nodes):
                    if i != j:
                        similarity = self._calculate_behavioral_similarity(
                            behavioral_features[node1],
                            behavioral_features[node2]
                        )
                        similarities.append(similarity)
                
                if similarities:
                    avg_similarity = np.mean(similarities)
                    if avg_similarity > self.experimental_thresholds['behavioral_similarity']:
                        behavioral_scores[node1] = avg_similarity
        
        return {
            'behavioral_clusters': len(nodes_by_type),
            'node_scores': behavioral_scores,
            'similarity_threshold': self.experimental_thresholds['behavioral_similarity']
        }
    
    def _analyze_amplification_coordination(self) -> Dict:
        """Analyze coordinated amplification patterns"""
        amplification_scores = defaultdict(float)
        
        # Find potential amplification targets
        artist_nodes = [
            node for node, data in self.graph.nodes(data=True)
            if data.get('node_type') == 'artist'
        ]
        
        for artist in artist_nodes:
            # Analyze incoming stream patterns
            incoming_streams = []
            for predecessor in self.graph.predecessors(artist):
                edge_data = self.graph.get_edge_data(predecessor, artist)
                if edge_data and edge_data[0].get('edge_type') == 'stream':
                    incoming_streams.append({
                        'source': predecessor,
                        'weight': edge_data[0]['weight']
                    })
            
            if len(incoming_streams) > 5:
                # Check for coordinated amplification
                weights = [s['weight'] for s in incoming_streams]
                mean_weight = np.mean(weights)
                std_weight = np.std(weights)
                
                # Find outliers (potential amplification)
                for stream in incoming_streams:
                    if stream['weight'] > mean_weight + 2 * std_weight:
                        amplification_scores[stream['source']] += 0.5
                        amplification_scores[artist] += 0.3
        
        return {
            'amplification_targets': len(artist_nodes),
            'node_scores': amplification_scores,
            'amplification_threshold': self.experimental_thresholds['amplification_factor']
        }
    
    def _extract_behavioral_features(self, node: str) -> Dict:
        """Extract behavioral features for a node"""
        features = {
            'degree': self.graph.degree(node),
            'in_degree': self.graph.in_degree(node),
            'out_degree': self.graph.out_degree(node),
            'clustering_coefficient': nx.clustering(self.graph.to_undirected(), node),
            'betweenness_centrality': nx.betweenness_centrality(self.graph).get(node, 0),
            'edge_types': defaultdict(int)
        }
        
        # Count edge types
        for _, _, edge_data in self.graph.edges(node, data=True):
            edge_type = edge_data.get('edge_type', 'unknown')
            features['edge_types'][edge_type] += 1
        
        return features
    
    def _calculate_behavioral_similarity(self, features1: Dict, features2: Dict) -> float:
        """Calculate behavioral similarity between two nodes"""
        similarity = 0.0
        total_weight = 0.0
        
        # Compare numerical features
        numerical_features = ['degree', 'in_degree', 'out_degree', 'clustering_coefficient', 'betweenness_centrality']
        for feature in numerical_features:
            val1 = features1.get(feature, 0)
            val2 = features2.get(feature, 0)
            
            if val1 + val2 > 0:
                similarity += min(val1, val2) / max(val1, val2)
                total_weight += 1
        
        # Compare edge type distributions
        edge_types1 = features1.get('edge_types', {})
        edge_types2 = features2.get('edge_types', {})
        
        all_edge_types = set(edge_types1.keys()) | set(edge_types2.keys())
        for edge_type in all_edge_types:
            count1 = edge_types1.get(edge_type, 0)
            count2 = edge_types2.get(edge_type, 0)
            
            if count1 + count2 > 0:
                similarity += min(count1, count2) / max(count1, count2)
                total_weight += 1
        
        return similarity / total_weight if total_weight > 0 else 0.0
    
    def detect_sophisticated_bot_clusters(self) -> Dict:
        """Detect sophisticated bot clusters using advanced clustering algorithms"""
        
        # Extract node features for clustering
        node_features = {}
        for node in self.graph.nodes():
            features = self._extract_behavioral_features(node)
            # Flatten features for clustering
            feature_vector = [
                features['degree'],
                features['in_degree'],
                features['out_degree'],
                features['clustering_coefficient'],
                features['betweenness_centrality']
            ]
            
            # Add edge type features
            edge_type_features = [0] * 5  # Placeholder for different edge types
            for i, edge_type in enumerate(['collaboration', 'stream', 'social_connection', 'follow', 'mention']):
                edge_type_features[i] = features['edge_types'].get(edge_type, 0)
            
            feature_vector.extend(edge_type_features)
            node_features[node] = feature_vector
        
        if len(node_features) < 3:
            return {'status': 'insufficient_data_for_clustering'}
        
        # Prepare data for clustering
        feature_matrix = np.array(list(node_features.values()))
        node_list = list(node_features.keys())
        
        # Standardize features
        scaler = StandardScaler()
        standardized_features = scaler.fit_transform(feature_matrix)
        
        # Apply DBSCAN clustering
        dbscan = DBSCAN(eps=0.5, min_samples=3)
        cluster_labels = dbscan.fit_predict(standardized_features)
        
        # Analyze clusters
        clusters = defaultdict(list)
        for i, label in enumerate(cluster_labels):
            if label != -1:  # Ignore noise points
                clusters[label].append(node_list[i])
        
        # Analyze cluster properties
        suspicious_clusters = []
        for cluster_id, cluster_nodes in clusters.items():
            if len(cluster_nodes) < 3:
                continue
            
            # Calculate cluster metrics
            cluster_subgraph = self.graph.subgraph(cluster_nodes)
            cluster_density = nx.density(cluster_subgraph)
            
            # Check for bot-like properties
            avg_degree = np.mean([self.graph.degree(node) for node in cluster_nodes])
            avg_clustering = nx.average_clustering(cluster_subgraph.to_undirected())
            
            suspicious_score = 0.0
            
            # High density suggests coordination
            if cluster_density > 0.5:
                suspicious_score += 0.3
            
            # Similar connectivity patterns
            if avg_clustering > 0.7:
                suspicious_score += 0.3
            
            # High average degree
            if avg_degree > 10:
                suspicious_score += 0.2
            
            # Check for temporal coordination
            temporal_coordination = self._check_cluster_temporal_coordination(cluster_nodes)
            if temporal_coordination > 0.8:
                suspicious_score += 0.2
            
            if suspicious_score > 0.6:
                suspicious_clusters.append({
                    'cluster_id': cluster_id,
                    'nodes': cluster_nodes,
                    'size': len(cluster_nodes),
                    'density': cluster_density,
                    'avg_degree': avg_degree,
                    'avg_clustering': avg_clustering,
                    'suspicious_score': suspicious_score,
                    'temporal_coordination': temporal_coordination
                })
        
        return {
            'total_clusters': len(clusters),
            'suspicious_clusters': suspicious_clusters,
            'clustering_algorithm': 'DBSCAN',
            'feature_dimensions': feature_matrix.shape[1],
            'noise_points': list(cluster_labels).count(-1)
        }
    
    def _check_cluster_temporal_coordination(self, cluster_nodes: List[str]) -> float:
        """Check temporal coordination within a cluster"""
        temporal_data = []
        
        for node in cluster_nodes:
            for _, _, edge_data in self.graph.edges(node, data=True):
                if 'timestamp' in edge_data:
                    temporal_data.append(edge_data['timestamp'])
        
        if len(temporal_data) < 10:
            return 0.0
        
        # Analyze temporal clustering
        temporal_data.sort()
        time_diffs = []
        
        for i in range(1, len(temporal_data)):
            diff = (temporal_data[i] - temporal_data[i-1]).total_seconds()
            time_diffs.append(diff)
        
        # Calculate coordination score based on time difference consistency
        if time_diffs:
            mean_diff = np.mean(time_diffs)
            std_diff = np.std(time_diffs)
            
            if mean_diff > 0:
                consistency_score = 1.0 - (std_diff / mean_diff)
                return max(0.0, consistency_score)
        
        return 0.0
    
    def generate_network_intelligence_report(self) -> Dict:
        """Generate comprehensive network intelligence report"""
        
        # Run all analyses
        coordination_analysis = self.detect_coordination_patterns()
        cluster_analysis = self.detect_sophisticated_bot_clusters()
        
        # Calculate network-wide metrics
        network_metrics = {
            'total_nodes': self.graph.number_of_nodes(),
            'total_edges': self.graph.number_of_edges(),
            'network_density': nx.density(self.graph),
            'connected_components': nx.number_connected_components(self.graph.to_undirected()),
            'average_clustering': nx.average_clustering(self.graph.to_undirected()),
            'assortativity': nx.degree_assortativity_coefficient(self.graph)
        }
        
        # Identify high-value targets for investigation
        high_value_targets = []
        
        # Highly coordinated nodes
        for node in coordination_analysis['highly_coordinated_nodes']:
            node_data = self.graph.nodes[node]
            high_value_targets.append({
                'node_id': node,
                'node_type': node_data.get('node_type', 'unknown'),
                'coordination_score': coordination_analysis['overall_coordination_scores'][node],
                'investigation_priority': 'HIGH'
            })
        
        # Nodes in suspicious clusters
        for cluster in cluster_analysis['suspicious_clusters']:
            for node in cluster['nodes']:
                high_value_targets.append({
                    'node_id': node,
                    'node_type': self.graph.nodes[node].get('node_type', 'unknown'),
                    'cluster_id': cluster['cluster_id'],
                    'suspicious_score': cluster['suspicious_score'],
                    'investigation_priority': 'MEDIUM'
                })
        
        # Remove duplicates and sort by priority
        unique_targets = {}
        for target in high_value_targets:
            node_id = target['node_id']
            if node_id not in unique_targets or target['investigation_priority'] == 'HIGH':
                unique_targets[node_id] = target
        
        sorted_targets = sorted(
            unique_targets.values(),
            key=lambda x: (x['investigation_priority'], x.get('coordination_score', 0)),
            reverse=True
        )
        
        return {
            'executive_summary': {
                'network_size': network_metrics['total_nodes'],
                'highly_coordinated_nodes': len(coordination_analysis['highly_coordinated_nodes']),
                'suspicious_clusters': len(cluster_analysis['suspicious_clusters']),
                'investigation_priorities': len(sorted_targets)
            },
            'network_metrics': network_metrics,
            'coordination_analysis': coordination_analysis,
            'cluster_analysis': cluster_analysis,
            'high_value_targets': sorted_targets[:50],  # Top 50 targets
            'recommendations': self._generate_intelligence_recommendations(
                coordination_analysis, cluster_analysis, network_metrics
            )
        }
    
    def _generate_intelligence_recommendations(self, coordination_analysis: Dict, 
                                              cluster_analysis: Dict, 
                                              network_metrics: Dict) -> List[str]:
        """Generate intelligence recommendations based on analysis"""
        recommendations = []
        
        # Network-level recommendations
        if network_metrics['network_density'] > 0.3:
            recommendations.append("HIGH_DENSITY_NETWORK: Investigate potential widespread coordination")
        
        if len(coordination_analysis['highly_coordinated_nodes']) > network_metrics['total_nodes'] * 0.1:
            recommendations.append("MASSIVE_COORDINATION: Large-scale bot network detected")
        
        # Cluster-level recommendations
        if len(cluster_analysis['suspicious_clusters']) > 5:
            recommendations.append("MULTIPLE_CLUSTERS: Multiple coordinated bot networks identified")
        
        for cluster in cluster_analysis['suspicious_clusters']:
            if cluster['suspicious_score'] > 0.8:
                recommendations.append(f"CRITICAL_CLUSTER_{cluster['cluster_id']}: Immediate investigation required")
        
        # General recommendations
        recommendations.extend([
            "Implement real-time coordination detection",
            "Establish cross-platform monitoring",
            "Develop automated disruption capabilities",
            "Coordinate with platform security teams"
        ])
        
        return recommendations

# Example usage
if __name__ == "__main__":
    # Initialize analyzer
    analyzer = ExperimentalNetworkAnalyzer()
    
    # Generate sample data for testing
    sample_artists = [
        {
            'spotify_id': 'artist_1',
            'name': 'Test Artist 1',
            'monthly_listeners': 1000,
            'genre': 'Test',
            'collaborations': ['artist_2', 'artist_3']
        }
    ]
    
    sample_streams = [
        {
            'user_id': 'user_1',
            'artist_id': 'artist_1',
            'duration_seconds': 180,
            'timestamp': datetime.now()
        }
    ]
    
    sample_social = [
        {
            'user_id': 'user_1',
            'platform': 'instagram',
            'connections': ['user_2', 'user_3']
        }
    ]
    
    # Build network and analyze
    network = analyzer.build_multilayer_network(sample_artists, sample_streams, sample_social)
    report = analyzer.generate_network_intelligence_report()
    
    print("Experimental Network Analysis Report:")
    print(json.dumps(report['executive_summary'], indent=2))
