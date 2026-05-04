import cv2

def init_video():
    cap = cv2.VideoCapture("input.mp4")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps is None or fps == 0:
        fps = 25  # حل مشكلة الفيديو اللي ما يعطيش FPS

    out = cv2.VideoWriter(
        "output.mp4",
        cv2.VideoWriter_fourcc(*'mp4v'),
        fps,
        (width, height)
    )

    return cap, out, width, height, fps