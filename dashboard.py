import cv2
import numpy as np
from collections import Counter

def draw_dashboard(height, unique_people, person_time, zone_time, last_zone):
    panel = np.zeros((height, 350, 3), dtype=np.uint8)

    cv2.putText(panel, "RETAIL DASHBOARD", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.putText(panel, f"Unique People: {len(unique_people)}", (20, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    total_time = sum(person_time.values())
    cv2.putText(panel, f"Total Time: {total_time:.1f}s", (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # 🔥 حساب عدد الأشخاص في كل zone
    zone_counts = Counter(last_zone.values())

    y = 150
    cv2.putText(panel, "People per Zone:", (20, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    y += 25
    for zone, count in zone_counts.items():
        cv2.putText(panel, f"{zone}: {count}",
                    (20, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        y += 20

    y += 10

    # ⏱️ time per zone
    cv2.putText(panel, "Time per Zone:", (20, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    y += 25
    for pid, zones in zone_time.items():
        for z, t in zones.items():
            cv2.putText(panel, f"ID {pid} - {z}: {t:.1f}s",
                        (20, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
            y += 18

    y += 10

    # 📍 current position
    cv2.putText(panel, "Current Position:", (20, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    y += 25
    for pid, zone in last_zone.items():
        cv2.putText(panel, f"ID {pid} -> {zone}",
                    (20, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        y += 20

    return panel