// ================================================================================
module seven_segment_indicator
(
    input           clk,
    input [13:0]    value,      // 0-9999

    output [7:0] segments,      // A, B, C, D, E, F, G, DP
                                // i.e. segments[0] = DP, ..., segments[7] = A
    output [3:0] digits         // D1, D2, D3, D4
                                // i.e. digits[0] = D4, ..., digits[3] = D1
);
// ================================================================================

localparam DIGIT_UPDATE_TICKS = 54_000; // 2 milliseconds

reg [7:0]  _segments            = 8'b0;
reg [3:0]  _digits              = 4'b1000;
reg [31:0] _total_segments      = 32'b0;
reg [31:0] _counter             = 32'b0;

assign segments = ~_segments;   // segment pins are cathods so pass negative values
assign digits = _digits;        // digit pins are anods so pass positive values

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

function [31:0] number_to_4_segments;
    input [13:0] number;
    begin
        number_to_4_segments = {
            digit_to_segments(number / 1000),         // thousands
            digit_to_segments((number % 1000) / 100), // hundreds
            digit_to_segments((number % 100) / 10),   // tens
            digit_to_segments(number % 10)            // units
        };
    end
endfunction

// ================================================================================
// update _total_segments
//always @(*) begin
//    reg [13:0] v = (value > 9999) ? 14'd9999 : value[13:0];
//    _total_segments = number_to_4_segments(
//        (value > 9999) ? 14'd9999 : value[13:0]
//    );
//end

// ================================================================================
// update digit
always @(posedge clk) begin
    _counter <= _counter + 1'b1;

    if (_counter >= DIGIT_UPDATE_TICKS) begin
        _counter <= 32'b0;

        _total_segments = number_to_4_segments(
            (value > 9999) ? 14'd9999 : value[13:0]
        );

        // update segments
        case (_digits)
            4'b1000: _segments <= _total_segments[23:16];   // after cyclic shift digits == 4'b0100'
            4'b0100: _segments <= _total_segments[15:8];    // after cyclic shift digits == 4'b0010'
            4'b0010: _segments <= _total_segments[7:0];     // after cyclic shift digits == 4'b0001'
            4'b0001: _segments <= _total_segments[31:24];   // after cyclic shift digits == 4'b1000'
            default: _segments <= 8'b0;
        endcase

        // update digit (using cyclic shift)
        _digits <= (_digits == 4'b0001) ? 4'b1000 : (_digits >> 1);
    end
end

// ================================================================================

endmodule