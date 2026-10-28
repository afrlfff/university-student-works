`timescale 1ns/1ns

module tb_lcd1602;
    reg clk;
    reg rst;
    reg lcd_print_signal;
    reg lcd_clear_signal;
    reg lcd_write_row;
    reg [3:0] lcd_write_col;
    reg [7:0] lcd_write_char;
    wire lcd_rs;
    wire lcd_en;
    wire [7:0] lcd_data;

    // Instantiate LCD
    lcd1602_controller_8bit_with_delays lcd_inst
    (
        .clk(clk),
        .reset(rst),

        .row(lcd_write_row),
        .col(lcd_write_col),
        .character(lcd_write_char),
        .print(lcd_print_signal),
        .clear(lcd_clear_signal),

        .lcd_rs(lcd_rs),
        .lcd_en(lcd_en),
        .lcd_data(lcd_data)
    );

    // Clock generator
    always #1 clk = ~clk;  // 2 ns period = 500 MHz

    // Test
    initial begin
        // Dump signals to VCD file for GTKWave
        $dumpfile("lcd1602.vcd");
        $dumpvars(0, tb_lcd1602);

        // Initialize
        clk = 0;
        rst = 0;
        lcd_print_signal = 1'b0;
        lcd_clear_signal = 1'b0;
        lcd_write_row = 1'b0;
        lcd_write_col = 4'd0;
        lcd_write_char = 8'd0;
        #10 rst = 1;

        #15000; // turn on delay (turn on + initialization)

        lcd_write_char = 8'hCC;
        lcd_clear_signal = 1'b1;
        #4 lcd_clear_signal = 1'b0;
        #5000; // clear delay

        lcd_write_row = 1'b0;
        lcd_write_col = 4'd0;
        lcd_write_char = 8'hAA;
        lcd_print_signal = 1'b1;
        #4 lcd_print_signal = 1'b0;
        #500; // print delay

        lcd_write_row = 1'b0;
        lcd_write_col = 4'd1;
        lcd_write_char = 8'hBB;
        lcd_print_signal = 1'b1;
        #4 lcd_print_signal = 1'b0;
        #500; // print delay

        lcd_write_char = 8'hCC;
        lcd_clear_signal = 1'b1;
        #4 lcd_clear_signal = 1'b0;
        #5000; // clear delay

        lcd_write_row = 1'b0;
        lcd_write_col = 4'd0;
        lcd_write_char = 8'hAA;
        lcd_print_signal = 1'b1;
        #4 lcd_print_signal = 1'b0;
        #500; // print delay

        lcd_write_row = 1'b0;
        lcd_write_col = 4'd1;
        lcd_write_char = 8'hBB;
        lcd_print_signal = 1'b1;
        #4 lcd_print_signal = 1'b0;
        #500; // print delay

        // Run simulation
        #1000 $finish;
    end
endmodule