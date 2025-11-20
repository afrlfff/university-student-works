// bram_writer.v
module bram_writer (
    input        clk,
    input        en,          // enable записи
    input  [2:0] addr,
    input  [7:0] data
);

// Чтение отключено: wre = 1, ce = en
// oce безразличен при записи (но подадим 0 или 1 — не важно)
Gowin_SP_Init bram_inst (
    .dout(),               // не используется
    .clk(clk),
    .oce(1'b0),            // можно и 1'b1 — не влияет при wre=1
    .ce(en),
    .reset(1'b0),
    .wre(1'b1),
    .ad(addr),
    .din(data)
);

endmodule