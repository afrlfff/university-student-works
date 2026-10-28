module top
(
    input wire clk,         // Тактовый сигнал (27 МГц)
    input wire reset,       // Сигнал сброса
    output wire lcd_rs,      // RS: выбор регистра (0 - команды, 1 - данные)
    output wire lcd_en,      // Enable: активный строб для передачи данных
    output [7:0] lcd_data   // Шина данных (8-битный интерфейс)
);

reg [7:0] characters [0:31];

initial
begin
    characters[0] = 8'h49; // 'I'
    characters[1] = 8'h20; // ' '
    characters[2] = 8'h6C; // 'l'
    characters[3] = 8'h6F; // 'o'
    characters[4] = 8'h76; // 'v'
    characters[5] = 8'h65; // 'e'
    characters[6] = 8'h20; // ' '
    characters[7] = 8'h4C; // 'L'
    characters[8] = 8'h45; // 'E'
    characters[9] = 8'h54; // 'T'
    characters[10] = 8'h49; // 'I'
    characters[11] = 8'h21; // '!'
    characters[12] = 8'h4C; // ' '
    characters[13] = 8'h45; // ' '
    characters[14] = 8'h54; // ' '
    characters[15] = 8'h49; // ' '
    characters[16] = 8'h49; // 'I'
    characters[17] = 8'h20; // ' '
    characters[18] = 8'h6C; // 'l'
    characters[19] = 8'h6F; // 'o'
    characters[20] = 8'h76; // 'v'
    characters[21] = 8'h65; // 'e'
    characters[22] = 8'h20; // ' '
    characters[23] = 8'h4C; // 'L'
    characters[24] = 8'h45; // 'E'
    characters[25] = 8'h54; // 'T'
    characters[26] = 8'h49; // 'I'
    characters[27] = 8'h21; // '!'
    characters[28] = 8'h4C; // ' '
    characters[29] = 8'h45; // ' '
    characters[30] = 8'h54; // ' '
    characters[31] = 8'h49; // ' '   
end

//lcd1602_controller_8bit_second_line lcd1602 (
//    .clk(clk),
//    .reset(reset),

//    .characters(characters),

//    .lcd_rs(lcd_rs),
//    .lcd_en(lcd_en),
//    .lcd_data(lcd_data)
//);




lcd1602_controller_8bit lcd1602
(
    .clk(clk),         // Тактовый сигнал (27 МГц)
    .reset(reset),       // Сигнал сброса

    .character(characters[0]),  // ASCII-код символа
    .row(row),                  // Строка для записи символа
    .col(col),                  // Столбец для записи символа

    .lcd_rs(lcd_rs),      // RS: выбор регистра (0 - команды, 1 - данные)
    .lcd_en(lcd_en),      // Enable: активный строб для передачи данных
    .lcd_data(lcd_data)
);





endmodule
