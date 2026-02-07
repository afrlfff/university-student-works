module bram_reader (
    input        clk,
    input        en,
    input  [2:0] addr,
    output [7:0] data
);

wire [7:0] mem_dout;

Gowin_SP_Init bram_inst (
    .dout(mem_dout),
    .clk(clk),
    .oce(en),        // oce управляет загрузкой выходного регистра
    .ce(en),
    .reset(1'b0),
    .wre(1'b0),
    .ad(addr),
    .din(8'd0)
);

assign data = mem_dout; // registered inside BRAM

endmodule