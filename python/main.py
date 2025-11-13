# SPDX-FileCopyrightText: Copyright (C) 2025 ARDUINO SA
#
# SPDX-License-Identifier: MPL-2.0

from arduino.app_utils import *
from arduino.app_utils import App
from arduino.app_bricks.web_ui import WebUI
from arduino.app_bricks.video_objectdetection import VideoObjectDetection
from datetime import datetime, UTC
import time
import json
import os

ui = WebUI()
detection_stream = VideoObjectDetection(confidence=0.5, debounce_sec=0.0)
ui.on_message("override_th", lambda sid, threshold: detection_stream.override_threshold(threshold))

paused = False
pick_mode = False
last_detection_time = {}
DETECTION_COOLDOWN = 2.0  # seconds between same detections

label_map_path = os.path.join(os.path.dirname(__file__), "..", "assets", "label_map.json")
with open(label_map_path, "r") as f:
    label_map = json.load(f)

def save_label_map():
    with open(label_map_path, "w") as f:
        json.dump(label_map, f, indent=2)

def handle_find(label):
    print(f"Find triggered for label: {label}")
    if label in label_map:
        print("sending ", label_map[label][0])
        Bridge.notify("stepper", label_map[label][0])

ui.on_message("find", lambda sid, data: handle_find(data["label"]))

def toggle_pick_mode(sid, data):
    global pick_mode, paused
    pick_mode = not pick_mode
    paused = False  # resume detections when switching
    mode_msg = "Pick" if pick_mode else "Normal"
    print(f"Switched to {mode_msg} mode")
    ui.send_message("mode_status", {"mode": mode_msg})

ui.on_message("toggle_pick", toggle_pick_mode)

# Send current mode (so frontend stays in sync on page load)
def send_current_mode(sid, data):
    mode_msg = "Pick" if pick_mode else "Normal"
    ui.send_message("mode_status", {"mode": mode_msg})

ui.on_message("get_mode", send_current_mode)

def send_detections_to_ui(detections: dict):
    global paused, pick_mode
    current_time = time.time()

    if paused:
        return

    for key, value in detections.items():
        conf = value.get("confidence", 0)
        if conf * 100 < 85 or key not in label_map:
            continue

        last_time = last_detection_time.get(key, 0)
        if current_time - last_time < DETECTION_COOLDOWN:
            continue

        last_detection_time[key] = current_time

        if pick_mode:
            label_map[key][1] = max(0, label_map[key][1] - 1)
        else:
            label_map[key][1] += 1
            Bridge.notify("stepper", label_map[key][0])
            paused = True  # <-- pause until other device sends ack
            print("sending ", label_map[key][0], "using bridge")

        save_label_map()
        ui.send_message("count_update", {"label": key, "count": label_map[key][1]})
        print(f"{'Picked' if pick_mode else 'Added'} {key}: {label_map[key][1]}")



detection_stream.on_detect_all(send_detections_to_ui)

def resume(val: int):
    global paused
    if val == 0:
        paused = False

Bridge.provide("ack", resume)

def handle_get_count(sid, data):
    label = data["label"]
    if label in label_map:
        count = label_map[label][1]
        ui.send_message("count_response", {"label": label, "count": count})

ui.on_message("get_count", handle_get_count)

App.run()
