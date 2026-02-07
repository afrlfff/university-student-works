module test_bram_writer
(
    input        clk,
    output [7:0] segments,
    output [3:0] digits
);

// ================================================================================
reg [1:0] state = 0;
reg [3:0] addr = 3'd0;
reg [7:0] write_data = 8'b00001010;

reg        wr_en = 1'b0;
reg        rd_en = 1'b0;
wire [7:0] rd_data;

// ================================================================================
// Конечный автомат
always @(posedge clk) begin
    wr_en <= 1'b0;
    rd_en <= 1'b0;
    
    case (state)
        2'd0: begin // Запись
            wr_en <= 1'b1;
            rd_en <= 1'b0;
            state <= 2'd1;
        end
        2'd1: begin // Чтение (на следующем такте)
            wr_en <= 1'b0;
            rd_en <= 1'b1;
            state <= 2'd2;
        end
        2'd2: begin // Отображение (ждём, пока индикатор покажет)
            // остаёмся здесь
        end
    endcase
end

// ================================================================================
// BRAM isntance
bram_rw_controller bram_inst (
    .clk(clk),
    .wr_en(wr_en),
    .wr_addr(addr),          // пишем в адрес 0
    .wr_data(write_data),
    .rd_en(rd_en),
    .rd_addr(addr),          // читаем тот же адрес
    .rd_data(rd_data)
);

// ================================================================================
// display read value
seven_segment_indicator_binary disp_init (
    .clk(clk),
    .value(rd_data[3:0]),
    .segments(segments),
    .digits(digits)
);

endmodule