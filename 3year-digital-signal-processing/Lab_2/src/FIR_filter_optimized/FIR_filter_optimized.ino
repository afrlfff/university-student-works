
// Main constants
const int Fs = 1000;
unsigned long timestamp_curr = 0;
unsigned long timestamp_prev = 0;
int new_point;
double new_point_filtered;

// Filter constants
const int N = 6; // number of filter coefficients
int buffer[N + 1] = {0, 0, 0, 0, 0, 0}; // store last N points we read + 1 cell for new point (for buffer shifting)
const double filter_coeffs[N] = {
  0.2579, 0.1231, 0.1345, 0.1345, 0.1231, 0.2579
};

// Computed constants
const double T = 1 / Fs;
const double T_microseconds = T * 1000000;


void setup() {
  // ==== Initialization
  for (int i = 0; i < N; ++i) { buffer[i] = 0; }
  Serial.begin(500000);

  // ==== Program start
  // program will work for 10 seconds
  while (timestamp_curr < 10000000)
  {
    // read point every [T_microseconds] microseconds
    timestamp_curr = micros();
    if ((timestamp_curr - timestamp_prev) >= 1000)
    {
      new_point = analogRead(1);
      new_point_filtered = 0;

      // add new point to buffer
      buffer[N] = new_point;
      
      //memcpy(buffer, buffer[1], N * sizeof(int));
      for (uint8_t i = 0; i < N; i++){
        buffer[i] = buffer[i+1];
      }

      // ==== Buffer shift and filtering in parallel
      // for (int i = N - 1; i >= 0; --i)
      // {
      //   buffer[i] = buffer[i + 1];
      //   new_point_filtered += filter_coeffs[N - 1 - i] * buffer[i];
      // }
      
      for (uint8_t i = 0; i < N; i++){
        new_point_filtered += filter_coeffs[i] * buffer[N - i - 1];
      }

      // print filtered point
      Serial.println(new_point_filtered);

      // update timestamps
      timestamp_prev = timestamp_curr;
    }
  }
}

void loop()
{
  // not using in the current program
}