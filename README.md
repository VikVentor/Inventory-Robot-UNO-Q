# Smart Inventory Robot (Edeg Impulse + UNO Q)

## Introduction
This project will guide you on how to build your own **Inventory Robot** that can manage and track any item you want to store. It provides a simple and straightforward solution to automate, organize, and segregate your objects.
As a hobbyist, once you're done prototyping, it often becomes difficult to place every component back in its correct location. This robot solves that by automating the process of tracking and arranging items efficiently.

---

## Table of Contents

1. [Problem Understanding](#1-problem-understanding)  
2. [Solution](#2-solution)  
3. [What You Will Learn](#3-what-you-will-learn)  
4. [Build Your Hardware](#4-build-your-hardware)  
5. [Dataset Preparation](#5-dataset-preparation)  
6. [Train on Edge Impulse Studio](#6-train-on-edge-impulse-studio)  
7. [Optimized Model](#7-optimized-model)  
8. [Integrate with UNO Q](#8-integrate-with-uno-q)
9. [Arduino App Explanation](#9-arduino-app-explanation)
10. [Usage and UI](#10-usage-and-ui)
11. [Conclusion](#11-conclusion)

---
## 1. Problem Understanding

When working on prototypes or hobby projects, components often end up scattered across the workspace. After completing a project, it becomes difficult to identify, sort, and return each item to its correct place. This leads to misplaced components, wasted time searching for parts, and an overall inefficient workflow.

Manual sorting and tracking of items is repetitive and prone to human error. As the number of components grows, maintaining a proper inventory becomes even harder.

The core problem is the lack of an easy, automated system that can:
- Identify items quickly  
- Count them accurately  
- Sort and place them in the right location  
- Keep a consistent record of what’s stored  

This project aims to eliminate these manual tasks by providing an automated, intelligent inventory robot powered by the Arduino UNO Q and Edge Impulse.

## 2. Solution
Explain your overall solution approach.

---

## 3. What You Will Learn
List the key learning points.
1. How to train an ML model int **Edge Impulse**, optimize it in and integrate it into your **Arduino UNO Q app**.
3. Use the core feature of Arduino UNO Q, that is seamless communication from your software to hardware using the Bridge API.
4. Use this software solution for your own hardware setup.

**To help you build your complete solution I have also built the hardware for you with all the necessary hardware and STL files** <br>
**The Robot comprises of a very simple design and has been designed to demonstrate the capabilities of Arduino UNO Q and Edge Impulse for this Application**

---

## 4. Build Your Hardware
Instructions or images about assembling the hardware.

---

## 5. Dataset Preparation
- To prepare your dataset, follow these steps (images below show the process):
- I will be choosing 5 different objects for this project
- So a total of 5 labels, with approximately 240 images per label is required (200 for training, 40 for testing);
<p align="left">
  <img src="assets/docs_assets/object_list.jpg" width="300" />
</p>

### Create your project
<p align="left">
  <img src="assets/docs_assets/edge_1.png" width="300" />
</p>

### Collect images
- Use the camera that you will be using in your actual robot, connect it to your PC and take photos.
<p align="left">
  <img src="assets/docs_assets/edge_2.png" width="500" />
  <img src="assets/docs_assets/edge_4.png" width="500" />
</p>

### Select on "collecting images" 
- Provide the permission, if prompted by your browser.
<p align="left">
  <img src="assets/docs_assets/edge_3.png" width="300" />
</p>

### Capture your images one by one (Label is not the actual labelling in this case, it is to let you identify your captured images easily)
- Make sure to edit the label, it lets you identify what images you have captured for sorting them later.
- Capture images in various lighting conditions/orientations as shown in the gif.
- Choose Training Dataset first (Capture approximately 200 images)
- Then choose Testing dataset for around 40 images.
<p align="left">
  <img src="assets/docs_assets/edge_7.gif" width="400" height = "500"/>
  <img src="assets/docs_assets/edge_6.gif" width="400" />
</p>

- You may ask, why 200 images and not more? To our advantage, the background of the camera feed stays constant, i.e. the white platform in this case.

### Label your images with a bounbding box:
- Navigate to the Labeling Queue present at the top menu, draw a bounding box which approximately borders your object.
- Click on save label, you will get the next image and so on.
- Edge Impulse  provides a great feature here, which automatically tracks the next image and draws aa bounding box by estimating the approximate position
<p align="left">
  <img src="assets/docs_assets/edge_8.gif" width="600" />
</p>
- You can also use the AI labelling feature using OpenAI or Gemini API keys.

### Repeat this process for other objects as well.



---

## 6. Train on Edge Impulse Studio

### Ok, so how do I know what to choose? 
- It's all about experimenting with various models, options and even your dataset itself.
- To make it clear for you, I have experimented with various options myself, before arriving at the final optimised solution.
  <br>
  <br>
  
### I Created an Impulse 
- Naviagte to the Create Impulse section:
- An impulse takes raw data, uses signal processing to extract features, and then uses a learning block to classify new data.
### Experiment 1
- I wanted to try the MobileNetV2 SSD FPN-Lite 320x320 available in the model options (will be clear in the next step)
- So for this model, the constraint was to have a 320x320 size input for the images.
<img src="assets/docs_assets/train_2.png" />

- I added a processing block and a learning block
<p align="left">
  <img src="assets/docs_assets/train_3.png" width="600" />
  <img src="assets/docs_assets/train_4.png" width="600" />
</p>

- Then I saved the impulse:

- The next section is the "Image" section that lets you generate features
<p align="left">
  <img src="assets/docs_assets/train_6_feat.png" width="500"/>
  <img src="assets/docs_assets/train_7_feat.png" width="500"/>
</p>

- The next section is the "Object Detection".
- Here is where i chose the MobileNetV2 SSD FPN-Lite 320x320 model:
- Hit save & train
<p align="left">
  <img src="assets/docs_assets/train_8_mn.png" width="500"/>
</p>
- So, I could only choose upto 25 - 30 epochs as Edge Impulse provides a job limit of only an Hour
- Anything above 30 Epochs would exceed training time.
<br>
- Results:
<p align="left">
  <img src="assets/docs_assets/train_mn_score.png" width="500"/>
</p>

- So then I proceeded to the "Live Classification" Section
- You can choose live classififcation using your connected webcam.
- I used load sample. It takes a random image from your **Test dataset** and compares whther the prediction has matched the label that you set for your test data.

<br>
- But how do I test all of them to check the over all performance?
- Navigate to the next Section: " Model Testing"
- Select classify all
<p align="left">
  <img src="assets/docs_assets/class_all_mn.png" width="400"/>
  <img src="assets/docs_assets/accu_mn.png"  />
</p>
<br>
- 87% is not bad, but could it be better? let's find out.

- Select the Target option on the top right, choose Arduino UNO Q and save
<p align="left">
  <img src="assets/docs_assets/choose_targ.png" width="400"/>
  <br>
  <img src="assets/docs_assets/choose_unoq.png" width="500" />
</p>

- The final Section "Deployment"
- Select Build
- Here you will see a summary of details for the model for UNO Q:
<p align="left">
  <img src="assets/docs_assets/unoq_11.png" width="600"/>
</p>

### Learnings from Experiment 1:
- Model size too Large (11MB)
- We can improve the model's accuarcy and precision score further
- We can lower the input size for training i.e. make it 90x90 instead of 320x320

### Experiment 2
All the steps are the same except now:
- I chose 90x90 as input size for the impulse
- Choosing a different model that accepts any image size, i.e. **FOMO (Faster Objects, More Objects) MobileNetV2 0.35**

#### Impulse 
- So I create my impulse with the below change
- Learning & Processing block remain the same.
<p align="left">
  <img src="assets/docs_assets/fomo_1.png" width="500"/>
</p>

- "Image" section step generates the features

- Training using the **FOMO (Faster Objects, More Objects) MobileNetV2 0.35** model, with the below parameters.
- **Note that data augmentation is not selected**
<p align="left">
  <img src="assets/docs_assets/fomo_train_setup.png" width="600"/>
</p>

- I get the following F1 Score
<p align="left">
  <img src="assets/docs_assets/fomo_f1_score.png" width="600"/>
</p>

- Amazing! so its going to be accurate! Well maybe not
<p align="left">
  <img src="assets/docs_assets/fomo_accu.png" width="300"/>
</p>

---

## 7. Optimized Model
### Experiment 3, Final
- Everything is the same except,
- I have enabled **data augementation**
<p align="left">
  <img src="assets/docs_assets/fomo_mod_aug.png" width="600"/>
</p>

- Precision Score:
<p align="left">
  <img src="assets/docs_assets/fomo_aug_f1.png" width="600"/>
</p>

- Accuracy:
<p align="left">
  <img src="assets/docs_assets/fomo_aug_accu.png" width="300"/>
</p>

- So, what made the drastic difference?
- **Use Data Augmentation: Data augmentation helps prevent overfitting by artificially increasing the variety and size of your dataset. It makes models more robust and better at handling real-world variations**
- Reduced model size from 11MB to 106KB
- Faster training time.

---

## 8. Integrate with UNO Q
### Setup the Arduino UNO Q as a Single Board Computer:
<br>
[Arduino Uno Q Single-Board Computer Setup](https://docs.arduino.cc/tutorials/uno-q/single-board-computer/)

- We need the .eim file from Edge Impulse:
- Navigate to the deployement section of Edge impulse adn Select Build.
- It will automatically start a download for a .eim file after the build is successfully.
<p align="left">
  <img src="assets/docs_assets/edge_last.png" width="500"/>
</p>



---

## 9. Arduino App Explanation
Explain how your Arduino App works.

---

## 10. Usage and UI
Explain how to use the robot and describe the UI.

---

## 11. Conclusion
Summarize the project and end notes.



