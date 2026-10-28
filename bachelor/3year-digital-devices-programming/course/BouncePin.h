#ifndef BOUNCE_PIN_H
#define BOUNCE_PIN_H

class BouncePin {
private:
    int pin;
    unsigned long debounceDelay;

    bool lastState = LOW;
    unsigned long lastMillis = 0;
    bool blocked = false;

public:
    ~BouncePin() {}
    BouncePin(const int pin, const unsigned long debounceDelay): 
        pin(pin), debounceDelay(debounceDelay) {}
    
    int state() { return lastState; }

    bool read() {
      bool currentState = digitalRead(pin);

      if (!blocked) {
        if (currentState != lastState) blocked = true;
        return lastState;
      } else {
        // wait enough time to handle bounce
        if (millis() - lastMillis < debounceDelay) return lastState;
        
        if (currentState != lastState) {
          // state still not the same even after timeout
          // so its not accidental contact bounce
          lastState = currentState;
        } else {
          // state now the same so it was accidental contact bounce
          // so do nothing
        }
        
        lastMillis = 0;
        blocked = false;
        return lastState;
      }
    }
};

#endif BOUNCE_PIN_H