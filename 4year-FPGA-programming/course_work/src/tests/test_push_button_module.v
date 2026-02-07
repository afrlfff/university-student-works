`timescale 1ns/1ns

module tb_push_button;
    reg clk;
    reg rst;
    reg input_btn;
    wire _btn_pushed;

    // Instantiate button
    push_button push_btn_inst ( 
        .clk(clk), 
        .rst(rst), 
        .btn(input_btn), 
        .btn_pushed(_btn_pushed) 
    );

    // Clock generator
    always #1 clk = ~clk;  // 10 ns period = 100 MHz

    initial begin
        // Dump signals to VCD file for GTKWave
        $dumpfile("push_button.vcd");
        $dumpvars(0, tb_push_button);

        // Initialize
        clk = 0;
        rst = 0;
        input_btn = 1;
        #10 rst = 1;

        #100 input_btn = 0;
        #1000 input_btn = 1;

        // Run simulation
        #200 $finish;
    end
endmodule