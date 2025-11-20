module top
(
    input        clk,

    output [7:0] segments,
    output [3:0] digits
);

// ===== ТЕСТ СЕМИСЕГМЕНТНОГО ИНДИКАТОРА ===== //

//seven_segment_timer timer
//(
//    .clk(clk),
//    .segments(segments),
//    .digits(digits)
//);

// =========================================== //

// ===== ТЕСТ ЧТЕНИЯ ПАМЯТИ BRAM ===== //

test_bram_reader test_reader
(
    .clk(clk),
    .segments(segments),
    .digits(digits)
);

// =================================== //

// ===== ТЕСТ ЗАПИСИ В BRAM ===== //
// also replace bram module in bram_rw_controller.v (to bram_sp)
//test_bram_writer test_writer
//(
//    .clk(clk),
//    .segments(segments),
//    .digits(digits)
//);

// =================================== //

endmodule