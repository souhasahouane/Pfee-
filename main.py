import cv2
import numpy as np
from collections import defaultdict

from detector import PersonDetector
from tracker import create_tracker
from kalman import KalmanBox
from video_utils import init_video
from zones import get_zone
from dashboard import draw_dashboard

def main():
    detector = PersonDetector()
    tracker = create_tracker()

    cap, out, width, height, fps = init_video()

    kalman_dict = {}
    person_time = {}
    unique_people = set()

    zone_history = defaultdict(set)

    heatmap = np.zeros((height, width), dtype=np.float32)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # توحيد الحجم
        frame = cv2.resize(frame, (width, height))

        detections = detector.detect(frame)
        tracks = tracker.update_tracks(detections, frame=frame)

        for track in tracks:
            if not track.is_confirmed():
                continue

            track_id = track.track_id
            x1, y1, x2, y2 = map(int, track.to_ltrb())

            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            if track_id not in kalman_dict:
                kalman_dict[track_id] = KalmanBox()

            cx, cy = kalman_dict[track_id].update(cx, cy)

            # الوقت
            person_time[track_id] = person_time.get(track_id, 0) + 1 / fps

            if person_time[track_id] > 1:
                unique_people.add(track_id)

            # zones
            zone = get_zone(cx, width)
            zone_history[track_id].add(zone)

            # heatmap
            heatmap[y1:y2, x1:x2] += 1

            # رسم bbox
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(frame, f"ID:{track_id}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # 📊 dashboard
        dashboard = draw_dashboard(height, unique_people, person_time, zone_history)

        # 👁️ عرض كل واحد في نافذة
        cv2.imshow("Main Video", frame)
        cv2.imshow("Dashboard", dashboard)

        # 💾 حفظ الفيديو (بدون dashboard)
        out.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    print("TOTAL UNIQUE PEOPLE:", len(unique_people))


if __name__ == "__main__":
    main()