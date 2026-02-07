// bram_reader.v
module bram_reader (
    input        clk,
    input        start,
    output reg   done
);

reg [2:0]  addr;
reg        ce;
reg        oce;

assign ce  = 1'b1;
assign oce = 1'b1;

wire [7:0] dout;
Gowin_SP u_bram (
    .dout(dout),
    .clk(clk),
    .oce(oce),
    .ce(ce),
    .reset(1'b0),
    .wre(1'b0),        // Только чтение
    .ad(addr),
    .din(8'h00)
);

// Простой счётчик адресов (0 → 7)
reg [3:0] state; // 0..8
always @(posedge clk) begin
    if (start) begin
        state <= 4'd0;
        addr  <= 3'd0;
        done  <= 1'b0;
    end else if (state < 8) begin
        if (state != 0) begin
            // Вывод предыдущего значения (т.к. чтение с задержкой 1 такт)
            $display("Addr %0d: 0x%h", state - 1, dout);
        end
        addr <= addr + 1;
        state <= state + 1;
    end else if (state == 8) begin
        $display("Addr 7: 0x%h", dout); // Последнее значение
        done <= 1'b1;
        state <= state;
    end
end

endmodule