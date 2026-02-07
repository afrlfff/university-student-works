module buzzer (
    input clk,
    input rst,
    
    input [13:0] freq,    // sound frequency
    input play,    // 1: play sound; 0: not play sound

    output reg buz      // output signal to buzzer
);

// ================================================================================

localparam CLK_FREQ = 27_000_000; // Частота тактового сигнала
reg [31:0] counter = 0;

// ================================================================================

always @(posedge clk or negedge rst) begin
    if (~rst) begin
        counter <= 32'b0;
        buz    <= 1'b0;
    end else begin
        if (play) begin
            counter <= counter + 1'b1;

            if (counter >= CLK_FREQ/2/freq) begin
                counter <= 32'b0;
                buz    <= ~buz;
            end
        end else begin
            counter <= 32'b0;
            buz    <= 1'b0;
        end
    end
end

// ================================================================================

endmodule
