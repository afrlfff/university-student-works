// ================================================================================
 module top
 (
    input clk,
    
    output [7:0] segments, // A, B, C, D, E, F, G, DP
                           // i.e. segments[0] = DP, ..., segments[7] = A
    output [3:0] digits    // D1, D2, D3, D4
                           // i.e. digits[0] = D4, ..., digits[3] = D1
 );
// ================================================================================

reg [7:0]   _segments           = 8'b0;
reg [3:0]   _digits             = 4'b1000;
reg [31:0]  _total_segments     = 32'b0;
reg [14:0]  _time               = 15'b0; // 0 - 9_999
reg [25:0]  _timer_counter      = 26'b0; // 0 - 27_000_000
reg [31:0]  _switch_counter     = 32'b0; // 0 - 54_000

assign segments = ~_segments;   // segment pins are cathods so pass negative values
assign digits   = _digits;      // digit pins are anods so pass positive values

// ================================================================================
function [7:0] digit_to_segments;
    input [3:0] digit;
    begin
        case (digit)
            4'd0: digit_to_segments = 8'b11111100;
            4'd1: digit_to_segments = 8'b01100000;
            4'd2: digit_to_segments = 8'b11011010;
            4'd3: digit_to_segments = 8'b11110010;
            4'd4: digit_to_segments = 8'b01100110;
            4'd5: digit_to_segments = 8'b10110110;
            4'd6: digit_to_segments = 8'b10111110;
            4'd7: digit_to_segments = 8'b11100000;
            4'd8: digit_to_segments = 8'b11111110;
            4'd9: digit_to_segments = 8'b11110110;
            default:
                  digit_to_segments = 8'b00000000;
        endcase
    end
endfunction
// ================================================================================
function [31:0] time_to_total_segments;
    input [14:0] time_seconds;
    begin
        time_to_total_segments = {
            digit_to_segments(time_seconds / 1000),         // thousands
            digit_to_segments((time_seconds % 1000) / 100), // hundreds
            digit_to_segments((time_seconds % 100) / 10),   // tens
            digit_to_segments(time_seconds % 10)            // units
        };
    end
endfunction
// ================================================================================

// ================================================================================
always @(posedge clk)
begin    
    // increment counters
    _timer_counter  <= _timer_counter + 1'b1;
    _switch_counter <= _switch_counter + 1'b1;
    
    // update time every second
    if (_timer_counter >= 27_000_000) begin
        _total_segments = time_to_total_segments(_time);

        _timer_counter  <= 26'b0;
        _time           <= (_time < 9999) ? (_time + 1'b1) : (15'b0);
    end

    // update each digit every 2 ms
    if (_switch_counter >= 54_000) begin

        _segments   <= (_digits == 4'b1000) ? (_total_segments[23:16])  : 
                       (_digits == 4'b0100) ? (_total_segments[15:8])   : 
                       (_digits == 4'b0010) ? (_total_segments[7:0])    :
                       (_digits == 4'b0001) ? (_total_segments[31:24])  :
                                              (8'b0);
        _digits     <= (_digits == 4'b0001) ? (4'b1000) : (_digits >> 1);

        _switch_counter <= 32'b0;
    end
end
// ================================================================================

endmodule