# Smart Inventory Robot (Edge Impulse + UNO Q)

## Introduction

This project walks you through building your own **Inventory Robot** that can automatically identify, organize, and track the components you use in your workspace. After finishing a prototype, placing every part back in the right spot can become time-consuming and difficult. This robot solves that by intelligently sorting and maintaining a clear inventory of your items.

Whether you are a beginner or a hobbyist, this guide makes it simple to understand how the robot works, how to train your machine learning model on **Edge Impulse**, and how to integrate everything with the **Arduino UNO Q**.

---

## Table of Contents

1. [Problem Understanding](#1-problem-understanding)
2. [Solution](#2-solution)
3. [What You Will Learn](#3-what-you-will-learn)
4. [Hardware Design](#4-hardware-design)
5. [Dataset Preparation](#5-dataset-preparation)
6. [Train on Edge Impulse Studio](#6-train-on-edge-impulse-studio)
7. [Optimized Model](#7-optimized-model)
8. [Integrate with UNO Q](#8-integrate-with-uno-q)
9. [Arduino App Explanation](#9-arduino-app-explanation)
10. [Usage and UI](#10-usage-and-ui)
11. [Conclusion](#11-conclusion)

---

## 1. Problem Understanding

When working on electronics projects, components often get scattered all over the workspace. After finishing your work, identifying and sorting them back into their correct locations becomes tiring. This leads to misplaced parts, wasted time searching, and reduced productivity.

Manual sorting is repetitive and error-prone. As your component collection grows, keeping track of everything becomes even harder.

This project focuses on creating an automated system that can:

* Quickly identify items
* Count them accurately
* Sort and position them correctly
* Maintain a consistent, updated inventory

With the Arduino UNO Q and Edge Impulse, this project eliminates the repetitive steps and builds a smart, reliable solution.

---

## 2. Solution

Explain your overall solution approach.

---

## 3. What You Will Learn

Here are the key concepts you’ll learn while building this project:

1. How to train an ML model in **Edge Impulse**, optimize it, and integrate it into your **Arduino UNO Q** application.
2. How to utilize the UNO Q’s core ability—seamless software-to-hardware communication through the **Bridge API**.
3. How to adapt this software workflow to your own hardware setup.

**To make the process easier, I have also built the entire hardware and included all the STL files you need.**
The robot has a simple design focused on showcasing how the Arduino UNO Q and Edge Impulse can work together for smart inventory management.

---

## 4. System / Hardware Design

### Concept
This hardware setup is built as a **Proof of Concept** to demonstrate the Edge AI application.  
A **radial motion mechanism** is used for its simplicity, stability, and ease of construction.

### CAD / STL Files  
All CAD and STL files are provided below.

### Hardware Used
- Arduino Uno Q  
- Logitech C270  
- Arduino CNC Shield  
- NEMA 17 Stepper Motor (with long cable)  
- Limit Switch  
- 20×20 Aluminum Extrusion (≥15 cm)  
- MG995 Servo Motor  
- 1 m wires (×4)  
- T-nuts for 20×20 extrusion  
- M3 screws

### Circuit Diagram
<img src="assets/docs_assets/hardware/circ_diag.png" width="400" />

---

### 1. Construct the Base  
<img src="assets/docs_assets/hardware/base_build.png" width="400" />

---

### 2. Mount the Stepper Motor
Attach the aluminum extrusion to the base using a T-nut, as shown.  
<img src="assets/docs_assets/hardware/stepper_mounter.png" width="400" />

---

### 3. Install the Limit Switch  
<img src="assets/docs_assets/hardware/attach_base.png" width="400" />

---

### 4. Mount the Servo and Detection Platform  
Secure the servo to the platform using the screw provided with the servo.  
<img src="assets/docs_assets/hardware/servo_mount.png" width="400" />

---

### 5. Attach and Align the Camera
Before mounting, adjust the camera focus relative to the platform.  
<img src="assets/docs_assets/hardware/set_focus.gif" width="400" />  
<br>
* Use another T nut here to secure the camera holder.
<img src="assets/docs_assets/hardware/cam_mount.png" width="400" />

Use hot glue to fix the camera to the holder — and the hardware assembly is complete.  
<img src="assets/docs_assets/hardware/full_done.png" width="400" />


---

## 5. Dataset Preparation

Follow these steps to prepare your dataset:

* Select 5 different objects for training.
* For each object, capture around **240 images** (200 for training, 40 for testing).

<br>
<img src="assets/docs_assets/object_list.jpg" width="400" />

### Create your project

  <img src="assets/docs_assets/edge_1.png" width="400" />


### Collect images

Use the same camera you plan to use in the robot. Connect it to your PC and capture all the images.<br>
  <img src="assets/docs_assets/edge_2.png" width="400" />
  <img src="assets/docs_assets/edge_4.png" width="400" />

### Select “Collecting images”

Allow camera permissions if requested.<br>
  <img src="assets/docs_assets/edge_3.png" width="400" />


### Capture images one by one

* Edit the label to help you identify categories later.
* Capture in different orientations and lighting conditions.
* Choose **Training** dataset first (200 images), then **Testing** dataset (40 images).

  <img src="assets/docs_assets/edge_7.gif" width="400" />
  <img src="assets/docs_assets/edge_6.gif" width="400" />


### Label your images with bounding boxes

* Go to **Labeling Queue**.
* Draw a bounding box around the object.
* Click **Save label** to move to the next image.
* Edge Impulse intelligently estimates bounding boxes for consecutive images.<br><br>
  <img src="assets/docs_assets/edge_8.gif" width="600" />


You can also use AI-based auto-labeling using OpenAI or Gemini API keys.

Repeat this process for all objects.

---

## 6. Train on Edge Impulse Studio

### How do you know what to choose?

Training is an experimental process—try models, adjust parameters, and iterate until you get the performance you need.

Before we dive in, here is a summary of my experiments,.

| Experiment               | Model Used                       | Input Size | Data Augmentation | Accuracy / F1 Score              | Model Size |
| ------------------------ | -------------------------------- | ---------- | ----------------- | -------------------------------- | ---------- |
| **Experiment 1**         | MobileNetV2 SSD FPN-Lite 320x320 | 320×320    | ❌ No              | ~87% accuracy                    | **11 MB**  |
| **Experiment 2**         | FOMO MobileNetV2 0.35            | 90×90      | ❌ No              | Good F1 score but lower accuracy | **106 KB**  |
| **Experiment 3 (Final)** | **FOMO MobileNetV2 0.35**        | **90×90**  | **✔️ Yes**        | **High accuracy & precision**    | **106 KB** |

### **Training Steps (Overview)**

1. [Create an Impulse](#creating-an-impulse)
2. [Generate Features](#generate-features)
3. [Train the Model](#train-the-model)
4. [Model Testing (Classify All)](#testing)
5. [Select Arduino UNO Q as Target](#deployment-summary)
6. [Deploy the Model (.eim File)](#integrate-with-uno-q)

---


### Creating an Impulse

* Go to **Create Impulse**.
* An impulse processes raw data into features and uses a learning block for classification.

### Experiment 1

Trying **MobileNetV2 SSD FPN-Lite 320x320** required resizing inputs to **320×320**.<br>
  <img src="assets/docs_assets/train_2.png" />


Added processing and learning blocks: <br>


  <img src="assets/docs_assets/train_3.png" width="400" />
  <img src="assets/docs_assets/train_4.png" width="400" />


### Generate features:
- Navigate to the "Image" section to save parameters and generate feastures.<br>

  <img src="assets/docs_assets/train_6_feat.png" width="400"/>
  <img src="assets/docs_assets/train_7_feat.png" width="400"/>


### Train the model
Selected the **MobileNetV2 SSD FPN-Lite 320x320** model in the **Object Detection** section, hit **Save & Train**:<br>
  <img src="assets/docs_assets/train_8_mn.png" width="400"/>


Training time is limited by Edge Impulse (1 hour), so around 25–30 epochs are possible.<br>

Results:<br>
  <img src="assets/docs_assets/train_mn_score.png" width="400"/>


### Testing

Using **Live Classification** or **Model Testing → Classify all**:<br>
  <img src="assets/docs_assets/class_all_mn.png" width="400"/>
  <img src="assets/docs_assets/accu_mn.png"/>


Accuracy was around **87%**. Good, but we can improve this.

### Deployment summary

After selecting **Arduino UNO Q** as the target:<br>

  <img src="assets/docs_assets/choose_targ.png" width="400"/>
  <br>
  <img src="assets/docs_assets/choose_unoq.png" width="400" />

On deploying:<br>

  <img src="assets/docs_assets/unoq_11.png" width="400"/>

### Learnings from Experiment 1

* Model size was large (**11 MB**)
* Accuracy and precision can be improved
* Input size (320×320) is unnecessarily big

---

## Experiment 2

Same pipeline, but now:

* Input size changed to **90×90**
* Model switched to **FOMO MobileNetV2 0.35** (supports arbitrary image sizes)

### Impulse

  <img src="assets/docs_assets/fomo_1.png" width="400"/>


Training setup (no augmentation enabled):<br>

  <img src="assets/docs_assets/fomo_train_setup.png" width="400"/>


F1 score:<br>
  <img src="assets/docs_assets/fomo_f1_score.png" width="400"/>


Model accuracy:<br>

  <img src="assets/docs_assets/fomo_accu.png" width="400"/>

---

## 7. Optimized Model

### Experiment 3 (Final)

Everything remained the same except enabling **Data Augmentation**:<br>

  <img src="assets/docs_assets/fomo_mod_aug.png" width="400"/>


Precision:<br>

  <img src="assets/docs_assets/fomo_aug_f1.png" width="400"/>


Accuracy:<br>

  <img src="assets/docs_assets/fomo_aug_accu.png" width="400"/>


### Why this worked better

* Data augmentation prevents overfitting
* Model becomes more robust to variations
* Model size reduced from **11 MB → 106 KB**
* Training speed significantly improved

### Summary of Experiments



---

If you'd like, I can also add a short one-line takeaway below the table.


---

## 8. Integrate with UNO Q

### Setup the Arduino UNO Q as a Single Board Computer:
[Arduino Uno Q Single-Board Computer Set](https://docs.arduino.cc/tutorials/uno-q/single-board-computer/)

If you face issues with App Lab on your board, consider reflashing it with a new image:
<br>
[Flash a new Image](https://docs.arduino.cc/tutorials/uno-q/update-image/)

### Once your UNO Q is setup and ready, login to your **Edge Impulse Account** in UNO Q
You’ll need the **.eim** file from Edge Impulse.
Go to **Deployment → Build**
The `.eim` file downloads automatically once the build completes.<br>

  <img src="assets/docs_assets/edge_last.png" width="400"/>

### Adding the app
You can access folders and files on UNO Q using **Thunar**, which is like file explorer on Windows.
#### Download this repository on your UNO Q, and store the Unzipped Folder inside the **Arduino Apps** Folder.
  <img src="assets/docs_assets/ardapp_fold.png" width="300"/>
  <img src="assets/docs_assets/pasted_app.png" width="300"/>

### Adding the .eim model file
* Enable "Show hidden Files" in Thunar
* Navigate to **.arduino-bricks → ei-models** and paste the downloaded .eim file here
<img src="assets/docs_assets/bricks_fold.png" width="300"/>
<img src="assets/docs_assets/pasted_eim.png" width="300"/>

### The app.yaml file.
* Navigate to **Arduino App → Inventory-Robot-UNO-Q → app.yaml**

```yaml
name: Inventory-Robot-UNO-Q
description: This example showcases object detection within a live feed from a USB camera.
ports: []
bricks:
- arduino:video_object_detection: {variables: {
      EI_OBJ_DETECTION_MODEL: /home/arduino/.arduino-bricks/ei-models/inventory-robot-linux-aarch64-gpu-v10.eim
    }}
- arduino:web_ui: {}
icon: 📽️

```
* Replace the .eim file name with your downloaded file name
* You can replace the **name** with your own app name, if needed.
   


---

## 9. Arduino App Explanation

File Structure:
<br>
<img src="assets/docs_assets/file_struct.png" height="400"/>
<br>
File description:
1. Accelstepper Library
2. Servo Library
3. Python Code
4. Arduino Sketch

You can add libraries just like how you do in Arduino IDE, by pressing the button next to "Library"

Under assets, you can view the **index.html** and **app.js** which you can modify for your use case too:<br>
<img src="assets/docs_assets/assets_more.png" height="400"/>


### The label_map.json is an important file:
This is where you can add
- A new object
- Its position
- Its total count
<br>
Here's an example of its representation in the file:

| object | position | total count |
|--------|----------|--------------|
| esp32  | 2        | 15           |


### I have initialized all the count values as 0 because the robot will update its count automatically as it places them in their respective positions

```json
{
  "esp32": [2,0],
  "servo": [3,0],
  "motor": [3,0],
  "wheel": [4,0],
  "sensor": [5,0]
}
```


## Interaction Between Python and Arduino

### **Python Logic**

```python
def send_detections_to_ui(detections: dict):
    global paused, pick_mode

    if paused:
        return

    now = time.time()

    for key, value in detections.items():
        conf = value.get("confidence", 0)

        if conf * 100 < 85 or key not in label_map:
            continue
        if now - last_detection_time.get(key, 0) < DETECTION_COOLDOWN:
            continue

        last_detection_time[key] = now

        if pick_mode:
            label_map[key][1] = max(0, label_map[key][1] - 1)
        else:
            label_map[key][1] += 1
            Bridge.notify("stepper", label_map[key][0])   # send position to UNO Q
            paused = True

        save_label_map()
        ui.send_message("count_update", {"label": key, "count": label_map[key][1]})

detection_stream.on_detect_all(send_detections_to_ui)
```

**Summary:**

* Only detections above **85% confidence** are considered.
* For each valid detection, Python sends the object’s **position index** to the UNO Q using `Bridge.notify("stepper", position)`.
* Python enters a **paused** state until the microcontroller confirms that the item has been placed.

---

### **Arduino Logic**

* Below is a minimal skeleton showing how the UNO Q receives commands and sends back acknowledgements:
* You can use this code structure for your own project.

```cpp
#include <Arduino_RouterBridge.h>

long positions[6] = {0, 33, 66, 99, 132, 165};
// my stepper motor takes 200steps for one revolution, so these values are the respective positions for the 6 containers

void movePos(int n) {
    // your hardware logic here (stepper, servo, etc.)

    int var = 0;
    Bridge.notify("ack", var);   // send ack back to Python
}

void setup() {
    Bridge.begin();
    Monitor.begin(115200);
    // initialization logic
}

void loop() {
    Bridge.provide("stepper", movePos);  // listen for "stepper" events from Python
}
```

**Summary:**

* `Bridge.provide("stepper", movePos)` waits for Python to send a position.
* The received integer `n` tells the motor which container to move to.
* Once the object is dropped, Arduino sends back `Bridge.notify("ack", 0)`.

---

### **Python Resumes Detection After Ack**

```python
def resume(val: int):
    global paused
    if val == 0:
        paused = False

Bridge.provide("ack", resume)
```

**Summary:**

* Arduino’s acknowledgment (`ack = 0`) triggers the Python code to **unpause**.
* The detection loop continues only after the robot finishes placing the object.
* Other parts of the code handle the features of the UI

---

## 10. Usage and UI

Explain how to use the robot and describe the UI.

---

## 11. Conclusion

Summarize the project and end notes.

