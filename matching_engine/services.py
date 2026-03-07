from video_fingerprinting.models import VideoFingerprint
from video_fingerprinting.services import FingerprintService

class MatchingService:
    @staticmethod
    def _hamming_distance(hash1, hash2):
        """
        Calculate the Hamming distance between two hex strings.
        """
        if len(hash1) != len(hash2):
            return 999
        
        # Convert hex strings to integers and XOR them
        i1 = int(hash1, 16)
        i2 = int(hash2, 16)
        xor = i1 ^ i2
        
        # Count the set bits
        distance = bin(xor).count('1')
        return distance

    @classmethod
    def find_match(cls, query_video_path, threshold=10):
        """
        Generate fingerprints for the query video and find the best match in the database.
        """
        query_fingerprints = FingerprintService.generate_fingerprints(query_video_path)
        if not query_fingerprints:
            return None, 0.0
            
        best_match = None
        min_avg_distance = threshold
        
        # This is a brute-force search for demonstration.
        # In production, use a more efficient indexing strategy.
        all_fingerprints = VideoFingerprint.objects.all().select_related('movie')
        
        for record in all_fingerprints:
            db_hashes = record.fingerprint_data.get('hashes', [])
            if not db_hashes:
                continue
                
            # Compare query hashes with db hashes
            # We look for a sequence of matches
            total_distance = 0
            matches_found = 0
            
            for qf in query_fingerprints:
                q_hash = qf['hash']
                
                # Find the minimum distance for this query hash in the DB record
                min_dist_for_hash = 999
                for dbf in db_hashes:
                    dist = cls._hamming_distance(q_hash, dbf['hash'])
                    if dist < min_dist_for_hash:
                        min_dist_for_hash = dist
                
                if min_dist_for_hash < threshold:
                    total_distance += min_dist_for_hash
                    matches_found += 1
            
            if matches_found > 0:
                avg_distance = total_distance / matches_found
                # Confidence is inversely proportional to average distance
                # Adjust confidence calculation as needed
                confidence = max(0, 1 - (avg_distance / threshold)) * (matches_found / len(query_fingerprints))
                
                if best_match is None or confidence > (best_match.get('confidence', 0)):
                    best_match = {
                        'movie': record.movie,
                        'confidence': confidence,
                        'matches': matches_found
                    }
        
        return best_match
