module test_bram_reader
(
    input        clk,
    output [7:0] segments,
    output [3:0] digits
);

// ================================================================================

localparam ADDRESS_SHIFT_TIKS = 27_000_000; // 1 гц

reg [24:0] counter = 0;
reg [3:0]  addr = 4'd0;
reg        rd_en = 1'b0;
wire [7:0] rd_data;

// ================================================================================
// address swicthing
always @(posedge clk) begin
    counter <= counter + 1'b1;
    
    if (counter == ADDRESS_SHIFT_TIKS)
    begin
        counter <= 0;
        addr    <= (addr == 4'd15) ? (4'd0) : (addr + 1'd1);
        rd_en   <= 1'b1;
    end else begin
        rd_en <= 1'b0;
    end
end

// ================================================================================
// BRAM instance (только чтение)
bram_rw_controller bram_inst (
    .clk(clk),
    .wr_en(1'b0),           // запись отключена
    .wr_addr(4'd0),
    .wr_data(8'd0),
    .rd_en(rd_en),
    .rd_addr(addr),
    .rd_data(rd_data)
);

// ================================================================================
// Disaply read data
seven_segment_indicator_binary disp_inst (
    .clk(clk),
    .value(rd_data[3:0]),
    .segments(segments),
    .digits(digits)
);

// ================================================================================

endmodule