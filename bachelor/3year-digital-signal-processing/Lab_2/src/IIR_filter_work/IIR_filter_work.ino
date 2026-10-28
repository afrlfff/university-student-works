
// Main constants
const int Fs = 1000;
unsigned long timestamp_curr = 0;
unsigned long timestamp_prev = 0;
int new_point;
double new_point_filtered;

// Filter constants
const int N = 6; // number of b coefficients
int buffer_x[N+1]; // store last N points we read + 1 cell for new point (for buffer shifting)
const double filter_coeffs_a[N] = {
  -0.0173, 0.0323, -0.0208, -0.0185, 0.0308, -0.0168
};
const int M = 6; // number of a coefficients
double buffer_y[M+1]; // store last M points we filtered + 1 cell for new point (for buffer shifting)
const double filter_coeffs_b[M] = {
  1, -3.9894, 6.6997, -5.8625, 2.6639, -0.5026
};

// Computed constants
const double T = 1 / Fs;
const double T_microseconds = T * 1000000;


void setup() {
  // ==== Initialization
  for (int i = 0; i < N; ++i) { buffer_x[i] = 0; }
  for (int i = 0; i < M; ++i) { buffer_y[i] = 0; }
  Serial.begin(500000);

  // ==== Start program
  // program will work for 10 seconds
  while (timestamp_curr < 10000000)
  {
    // read point every [T_microseconds] microseconds
    timestamp_curr = micros();
    if ((timestamp_curr - timestamp_prev) >= 1000)
    {
      new_point = analogRead(1);
      new_point_filtered = 0;



      // add new value to buffer
      buffer_x[N] = new_point;

      for (int i = 0; i < N; i++){
        buffer_x[i] = buffer_x[i + 1];
        buffer_y[i] = buffer_y[i + 1];
      }

      // ===== filtering and update buffers in parallel

      // for (int i = M - 1; i >= 0; --i)
      // {
      //   // buffer_x[i] = buffer_x[i + 1];
      //   // buffer_y[i] = buffer_y[i + 1];
      //   new_point_filtered += filter_coeffs_b[M - 1 - i] * buffer_x[i];
      //   new_point_filtered -= filter_coeffs_a[M - 1 - i] * buffer_y[i];
      // }
      for (int i = 0; i < N; i++){
        new_point_filtered += filter_coeffs_a[i] * buffer_x[N - i];
      }
      for (int i = 1; i < N; i++){
        new_point_filtered -= filter_coeffs_b[i] * buffer_y[N - i];
      }

      // add new value to buffer
      buffer_y[M] = new_point_filtered;

      // print filtered point
      Serial.println(- new_point_filtered);

      // update timestamps
      timestamp_prev = timestamp_curr;
    }
  }
}

void loop()
{
  // not using in the current program
}