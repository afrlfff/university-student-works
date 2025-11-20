 module top
 (
    input clk,
    input [5:0] btn,
    output [5:0] led
 );

reg [19:0]  deb_cnt [5:0];
reg [5:0]   selected_led;

assign led[0] = ~selected_led[0];
assign led[1] = ~selected_led[1];
assign led[2] = ~selected_led[2];
assign led[3] = ~selected_led[3];
assign led[4] = ~selected_led[4];
assign led[5] = ~selected_led[5];

integer i;
always @(posedge clk) begin
    for (i = 0; i < 6; i = i + 1) begin
    
        if (!btn[i] && deb_cnt[i] < 1_000_000)
        begin
            deb_cnt[i] <= deb_cnt[i] + 1'b1;
             
            if (deb_cnt[i] == 999_999)
            begin
                selected_led[i] = 'b1;
            end
        end

        if (btn[i])
        begin
            deb_cnt[i] <= 0;
            selected_led[i] = 'b0;
        end

    end
end

endmodule