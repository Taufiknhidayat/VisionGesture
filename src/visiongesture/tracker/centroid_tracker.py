import numpy as np
from collections import OrderedDict
from scipy.spatial import distance as dist
from scipy.optimize import linear_sum_assignment
from typing import Dict, Tuple, List

from configs.settings import TRACKER_MAX_DISAPPEARED, TRACKER_MAX_DISTANCE

class CentroidTracker:
    def __init__(self):
        self.next_object_id = 0
        self.objects: Dict[int, Tuple[int, int]] = OrderedDict()
        self.disappeared: Dict[int, int] = OrderedDict()
        
        self.max_disappeared = TRACKER_MAX_DISAPPEARED
        self.max_distance = TRACKER_MAX_DISTANCE

    def _register(self, centroid: Tuple[int, int]) -> int:
        """Registers a new hand object with a unique ID."""
        self.objects[self.next_object_id] = centroid
        self.disappeared[self.next_object_id] = 0
        self.next_object_id += 1
        return self.next_object_id - 1

    def _deregister(self, object_id: int) -> None:
        """Removes a hand object tracking due to prolonged disappearance."""
        del self.objects[object_id]
        del self.disappeared[object_id]

    def update(self, input_centroids: List[Tuple[int, int]]) -> Dict[int, Tuple[int, int]]:
        """
        Updates the tracker with new centroids. 
        Uses Hungarian Algorithm to strictly assign stable IDs.
        """
        if len(input_centroids) == 0:
            for object_id in list(self.disappeared.keys()):
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > self.max_disappeared:
                    self._deregister(object_id)
            return self.objects

        input_arr = np.array(input_centroids, dtype="int")

        # If no objects are currently tracked, register all input centroids
        if len(self.objects) == 0:
            for i in range(len(input_arr)):
                self._register(tuple(input_arr[i]))
            return self.objects

        object_ids = list(self.objects.keys())
        object_centroids = list(self.objects.values())

        # Compute Euclidean distance between existing objects and new input centroids
        distance_matrix = dist.cdist(np.array(object_centroids), input_arr)
        
        # Apply Hungarian Algorithm for optimal bipartite matching
        row_ind, col_ind = linear_sum_assignment(distance_matrix)

        used_rows = set()
        used_cols = set()

        for row, col in zip(row_ind, col_ind):
            if distance_matrix[row, col] > self.max_distance:
                continue

            object_id = object_ids[row]
            self.objects[object_id] = tuple(input_arr[col])
            self.disappeared[object_id] = 0

            used_rows.add(row)
            used_cols.add(col)

        unused_rows = set(range(distance_matrix.shape[0])).difference(used_rows)
        unused_cols = set(range(distance_matrix.shape[1])).difference(used_cols)

        # Handle disappeared objects
        for row in unused_rows:
            object_id = object_ids[row]
            self.disappeared[object_id] += 1
            if self.disappeared[object_id] > self.max_disappeared:
                self._deregister(object_id)

        # Register new objects
        for col in unused_cols:
            self._register(tuple(input_arr[col]))

        return self.objects