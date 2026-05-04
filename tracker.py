from deep_sort_realtime.deepsort_tracker import DeepSort

def create_tracker():
    return DeepSort(
        max_age= 100,   
        n_init=6,
        nn_budget=150,
        max_cosine_distance=0.1
    )