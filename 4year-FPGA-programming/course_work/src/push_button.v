module push_button
 (
    input clk,             // clock pin
    input rst,             // reset pin
    input btn,             // input button pin

    output reg btn_pushed       // 1: pushed; 0: not pushed
                                // if button is pushed sets "1" on one tact and then goes back to "0"
 );

// ================================================================================

// debug values (for simulation)
//localparam DEBOUNCE_DELAY = 1000; // 1 ms

// release values
localparam DEBOUNCE_DELAY = 1_000_000;

reg [31:0]  deb_cnt;
reg         push_detected;

// ================================================================================

always @(posedge clk or negedge rst) begin
    if (~rst) begin
        deb_cnt         <= 32'b0;
        btn_pushed      <= 1'b0;
        push_detected   <= 1'b0;
    end else begin
        if (btn) begin
            // button not pressed
            deb_cnt         <= 32'b0;
            btn_pushed      <= 1'b0;
            push_detected   <= 1'b0;
        end else begin
            // button pressed
            if (deb_cnt < DEBOUNCE_DELAY) begin
                deb_cnt <= deb_cnt + 1'b1;
            end else begin
                if (~push_detected) begin
                    push_detected   <= 1'b1;
                    btn_pushed      <= 1'b1;
                end else begin
                    btn_pushed      <= 1'b0;
                end
            end
        end
    end
end

// ================================================================================

endmodule