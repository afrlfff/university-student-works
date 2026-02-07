// ================================================================================
 module seven_segment_timer
 (
    input clk,
    
    output [7:0] segments, // A, B, C, D, E, F, G, DP
                           // i.e. segments[0] = DP, ..., segments[7] = A
    output [3:0] digits    // D1, D2, D3, D4
                           // i.e. digits[0] = D4, ..., digits[3] = D1
 );
// ================================================================================

reg [13:0] _time =       14'b0;
reg [31:0] _counter =    32'b0;

// ================================================================================

seven_segment_indicator indicator
(
    .clk(clk),
    .value(_time),
    .segments(segments),
    .digits(digits)
);

// ================================================================================
always @(posedge clk)
begin
    _counter <= _counter + 1'b1;
    
    // update time every second
    if (_counter >= 27_000_000)
    begin
        _counter <= 32'b0;
        _time    <= (_time < 9999) ? (_time + 1'b1) : (14'b0);
    end
end
// ================================================================================

endmodule