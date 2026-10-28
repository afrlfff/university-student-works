`timescale 1ns/1ns

module tb_top;
    reg clk;
    reg rst;
    reg [4:0] input_btns;
    wire [7:0] indicator_segments;
    wire [3:0] indicator_digits;
    wire buz;
    wire lcd_rs;
    wire lcd_en;
    wire [7:0] lcd_data;

    // Instantiate LCD
    top top_inst
    (
        .clk(clk),
        .rst(rst),
        .input_btns(input_btns),
        .indicator_segments(indicator_segments),
        .indicator_digits(indicator_digits),
        .buz(buz),
        .lcd_rs(lcd_rs),
        .lcd_en(lcd_en),
        .lcd_data(lcd_data)
    );

    // Clock generator
    always #1 clk = ~clk;  // 2 ns period = 500 MHz

    // Test
    initial begin
        // Dump signals to VCD file for GTKWave
        $dumpfile("top.vcd");
        $dumpvars(0, tb_top);

        // Initialize
        clk = 0;
        rst = 0;
        input_btns = 5'b11111;
        #10 rst = 1;

        #20_000; // turn on + init menu

       //input_btns[1] = 1'b0; // go to game

        // Run simulation
        #10_000 $finish;
    end
endmodule