"""
Module for dynamic phase planning using semantic analysis and clustering.
"""

from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def plan_phases(phase_texts: List[str], num_phases: int = 4) -> List[Dict[str, str]]:
    """
    Cluster phase texts into num_phases clusters and generate high-level phase titles and descriptions.
    """
    if not phase_texts:
        return []

    # Vectorize texts
    vectorizer = TfidfVectorizer(stop_words='english')
    # Concatenate title and description for clustering
    combined_texts = [text for text in phase_texts]
    X = vectorizer.fit_transform(combined_texts)

    # Cluster
    n_clusters = min(num_phases, len(phase_texts))
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(X)

    clusters = {i: [] for i in range(n_clusters)}
    for idx, label in enumerate(kmeans.labels_):
        clusters[label].append(phase_texts[idx])

    # Generate phase summaries (simple concatenation or first item)
    phases = []
    for i in range(n_clusters):
        title = f"Phase {i+1}"
        description = " ".join(clusters[i])[:200]  # limit description length
        phases.append({"title": title, "description": description})

    return phases
