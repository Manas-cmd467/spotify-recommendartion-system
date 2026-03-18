import pandas as pd
import numpy as np
from scipy.sparse import load_npz
from sklearn.metrics.pairwise import cosine_similarity


class HybridRecommenderSystem:
    def __init__(self, number_of_recommendations=5, weight_content_based=0.5):
        """
        Initialize the Hybrid Recommender System
        
        Args:
            number_of_recommendations: Number of recommendations to return
            weight_content_based: Weight for content-based filtering (0-1)
        """
        self.number_of_recommendations = number_of_recommendations
        self.weight_content_based = weight_content_based
        self.weight_collaborative = 1 - weight_content_based
    
    def give_recommendations(self, song_name, artist_name, songs_data, 
                            transformed_matrix, track_ids, interaction_matrix, k=None):
        """
        Get hybrid recommendations combining content-based and collaborative filtering
        
        Args:
            song_name: Name of the input song
            artist_name: Name of the artist
            songs_data: DataFrame with song information
            transformed_matrix: Transformed feature matrix for content-based filtering
            track_ids: Array of track IDs
            interaction_matrix: Sparse matrix for collaborative filtering
            k: Number of recommendations (uses self.number_of_recommendations if None)
            
        Returns:
            DataFrame with top k recommendations
        """
        if k is None:
            k = self.number_of_recommendations
        
        # Find the input song
        song_row = songs_data.loc[(songs_data["name"] == song_name) and 
                                  (songs_data["artist"] == artist_name)]
        
        if song_row.empty:
            return pd.DataFrame()
        
        input_track_id = song_row['track_id'].values[0]
        track_idx = np.where(track_ids == input_track_id)[0][0]
        
        # Content-based filtering scores
        input_vector = transformed_matrix[track_idx].reshape(1, -1)
        content_scores = cosine_similarity(input_vector, transformed_matrix).ravel()
        
        # Collaborative filtering scores
        collab_vector = interaction_matrix[track_idx].reshape(1, -1)
        collab_scores = cosine_similarity(collab_vector, interaction_matrix).ravel()
        
        # Normalize scores to [0, 1]
        content_scores = (content_scores - content_scores.min()) / (content_scores.max() - content_scores.min() + 1e-10)
        collab_scores = (collab_scores - collab_scores.min()) / (collab_scores.max() - collab_scores.min() + 1e-10)
        
        # Hybrid score
        hybrid_scores = (self.weight_content_based * content_scores + 
                        self.weight_collaborative * collab_scores)
        
        # Get top k+1 recommendations (including the input song)
        top_indices = np.argsort(hybrid_scores)[-k-1:][::-1]
        
        # Get track IDs and filter
        recommendation_track_ids = track_ids[top_indices]
        recommendations = songs_data[songs_data["track_id"].isin(recommendation_track_ids)]
        
        return recommendations.reset_index(drop=True)