module bram_rw_controller (
    input        clk,
    input        rst_n,

    // Порт записи
    input        wr_en,
    input  [2:0] wr_addr,
    input  [7:0] wr_data,

    // Порт чтения
    input        rd_en,
    input  [2:0] rd_addr,
    output [7:0] rd_data
);

// Общий BRAM
wire [7:0] mem_dout;

bram_sp_init bram_inst (
    .dout(mem_dout),
    .clk(clk),
    .oce(rd_en),                   // только при чтении
    .ce(rd_en | wr_en),            // разрешить доступ
    .reset(~rst_n),                // если нужен сброс выхода
    .wre(wr_en),
    .ad(wr_en ? wr_addr : rd_addr), // приоритет записи, если оба en=1
    .din(wr_data)
);

assign rd_data = mem_dout;

endmodule