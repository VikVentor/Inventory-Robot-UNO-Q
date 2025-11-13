#include <Arduino_RouterBridge.h>
#include <AccelStepper.h>

#define STEP_PIN 2
#define DIR_PIN 5
#define ENABLE_PIN 8
#define LIMIT_PIN 9
#define SERVO_PIN 11

AccelStepper stepper(AccelStepper::DRIVER, STEP_PIN, DIR_PIN);

bool homed = false;
long positions[6] = {0, 33, 66, 99, 132, 165};

void pwmServo(int deg) {
    int pulse = map(deg, 0, 180, 1000, 2000);
    digitalWrite(SERVO_PIN, HIGH);
    delayMicroseconds(pulse);
    digitalWrite(SERVO_PIN, LOW);
    delayMicroseconds(20000 - pulse);
}

void moveServo(int deg) {
    for (int i = 0; i < 50; i++)
        pwmServo(deg);
}

void servoDrop() {
    moveServo(35);
    delay(2000);
    moveServo(75);
}

void movePos(int n) {
    if (n < 1 || n > 6) return;
    delay(2000);

    long target = positions[n - 1];
    Monitor.println("moving stepper");
    stepper.moveTo(target);

    while (stepper.distanceToGo() != 0)
        stepper.run();

    servoDrop();

    int var = 0;
    Monitor.println("sending ack");

    stepper.moveTo(10);
    while (stepper.distanceToGo() != 0)
        stepper.run();

    Bridge.notify("ack", var);
}

void setup() {
    pinMode(ENABLE_PIN, OUTPUT);
    digitalWrite(ENABLE_PIN, LOW);
    pinMode(LIMIT_PIN, INPUT_PULLUP);
    pinMode(SERVO_PIN, OUTPUT);

    Bridge.begin();
    Monitor.begin(115200);

    stepper.setMaxSpeed(1000);
    stepper.setAcceleration(1000);

    while (!homed) {
        if (digitalRead(LIMIT_PIN) == HIGH) {
            stepper.stop();
            stepper.setCurrentPosition(0);
            homed = true;
        } else {
            stepper.setSpeed(-50);
            stepper.runSpeed();
        }
    }

    servoDrop();
}

void loop() {
    Bridge.provide("stepper", movePos);
}
