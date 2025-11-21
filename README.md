# Smart Inventory Robot (Edeg Impulse + UNO Q)

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

## 4. Hardware Design

Instructions or images about assembling the hardware.

---

## 5. Dataset Preparation

Follow these steps to prepare your dataset:

* Select 5 different objects for training.
* For each object, capture around **240 images** (200 for training, 40 for testing).

<p align="left">
  <img src="assets/docs_assets/object_list.jpg" width="300" />
</p>

### Create your project

<p align="left">
  <img src="assets/docs_assets/edge_1.png" width="300" />
</p>

### Collect images

Use the same camera you plan to use in the robot. Connect it to your PC and capture all the images.

<p align="left">
  <img src="assets/docs_assets/edge_2.png" width="500" />
  <img src="assets/docs_assets/edge_4.png" width="500" />
</p>

### Select “Collecting images”

Allow camera permissions if requested.

<p align="left">
  <img src="assets/docs_assets/edge_3.png" width="300" />
</p>

### Capture images one by one

* Edit the label to help you identify categories later.
* Capture in different orientations and lighting conditions.
* Choose **Training** dataset first (200 images), then **Testing** dataset (40 images).

<p align="left">
  <img src="assets/docs_assets/edge_7.gif" width="400" height="500"/>
  <img src="assets/docs_assets/edge_6.gif" width="400" />
</p>

### Label your images with bounding boxes

* Go to **Labeling Queue**.
* Draw a bounding box around the object.
* Click **Save label** to move to the next image.
* Edge Impulse intelligently estimates bounding boxes for consecutive images.

<p align="left">
  <img src="assets/docs_assets/edge_8.gif" width="600" />
</p>

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

Trying **MobileNetV2 SSD FPN-Lite 320x320** required resizing inputs to **320×320**.

<p align="left">
  <img src="assets/docs_assets/train_2.png" />
</p>

Added processing and learning blocks:

<p align="left">
  <img src="assets/docs_assets/train_3.png" width="600" />
  <img src="assets/docs_assets/train_4.png" width="600" />
</p>

### Generate features:
- Navigate to the "Image" section to save parameters and generate feastures.

<p align="left">
  <img src="assets/docs_assets/train_6_feat.png" width="500"/>
  <img src="assets/docs_assets/train_7_feat.png" width="500"/>
</p>

### Train the model
Selected the **MobileNetV2 SSD FPN-Lite 320x320** model in the **Object Detection** section, hit **Save & Train**:

<p align="left">
  <img src="assets/docs_assets/train_8_mn.png" width="500"/>
</p>

Training time is limited by Edge Impulse (1 hour), so around 25–30 epochs are possible.

Results:

<p align="left">
  <img src="assets/docs_assets/train_mn_score.png" width="500"/>
</p>

### Testing

Using **Live Classification** or **Model Testing → Classify all**:

<p align="left">
  <img src="assets/docs_assets/class_all_mn.png" width="400"/>
  <img src="assets/docs_assets/accu_mn.png"/>
</p>

Accuracy was around **87%**. Good, but we can improve this.

### Deployment summary

After selecting **Arduino UNO Q** as the target:

<p align="left">
  <img src="assets/docs_assets/choose_targ.png" width="400"/>
  <br>
  <img src="assets/docs_assets/choose_unoq.png" width="500" />
</p>

On deploying:

<p align="left">
  <img src="assets/docs_assets/unoq_11.png" width="600"/>
</p>

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

<p align="left">
  <img src="assets/docs_assets/fomo_1.png" width="500"/>
</p>

Training setup (no augmentation enabled):

<p align="left">
  <img src="assets/docs_assets/fomo_train_setup.png" width="600"/>
</p>

F1 score:

<p align="left">
  <img src="assets/docs_assets/fomo_f1_score.png" width="600"/>
</p>

Model accuracy:

<p align="left">
  <img src="assets/docs_assets/fomo_accu.png" width="300"/>
</p>

---

## 7. Optimized Model

### Experiment 3 (Final)

Everything remained the same except enabling **Data Augmentation**:

<p align="left">
  <img src="assets/docs_assets/fomo_mod_aug.png" width="600"/>
</p>

Precision:

<p align="left">
  <img src="assets/docs_assets/fomo_aug_f1.png" width="600"/>
</p>

Accuracy:

<p align="left">
  <img src="assets/docs_assets/fomo_aug_accu.png" width="300"/>
</p>

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

### Once your UNO Q is setup and ready, login to your **Edge Impulse Account**
You’ll need the **.eim** file from Edge Impulse.
Go to **Deployment → Build**
The `.eim` file downloads automatically once the build completes.
<p align="left">
  <img src="assets/docs_assets/edge_last.png" width="500"/>
</p>

### Download this repository on your UNO Q, and store the Unzipped Folder inside the **Arduino Apps** Folder.

---

## 9. Arduino App Explanation

File Structure:
<br>
<img src="assets/docs_assets/file_struct.png" height="500"/>
<br>
File description:
1. Accelstepper Library
2. Servo Library
3. Python Code
4. Arduino Sketch

You can add libraries just like how you do, by pressing the button next to "Library"

Under assets, you can view the **index.html** and **app.js** which you can modify for your use case too:
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


Explain how your Arduino App works.

---

## 10. Usage and UI

Explain how to use the robot and describe the UI.

---

## 11. Conclusion

Summarize the project and end notes.

