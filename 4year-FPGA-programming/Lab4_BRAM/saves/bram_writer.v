// bram_writer.v
module bram_writer (
    input        clk,
    input        start,
    output reg   done
);

reg [2:0]  addr;
reg [7:0]  data;
reg        wre;
reg        ce;
reg        oce;

// Сигналы управления
assign ce  = 1'b1;
assign oce = 1'b1;

// Инстанциация BSRAM (ваш сгенерированный модуль)
wire [7:0] dout_unused;
Gowin_SP u_bram (
    .dout(dout_unused),
    .clk(clk),
    .oce(oce),
    .ce(ce),
    .reset(1'b0),   // Сброс не нужен
    .wre(wre),
    .ad(addr),
    .din(data)
);

// Простая FSM: запись одного значения
always @(posedge clk) begin
    if (start) begin
        addr <= 3'd2;      // Адрес для записи
        data <= 8'hAA;     // Новое значение
        wre  <= 1'b1;
        done <= 1'b0;
    end else if (wre) begin
        wre  <= 1'b0;      // Запись длится 1 такт
        done <= 1'b1;
    end else begin
        done <= done;
    end
end

endmodule