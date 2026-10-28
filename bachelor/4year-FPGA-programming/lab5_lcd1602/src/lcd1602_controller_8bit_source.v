module lcd1602_controller_8bit_source
(
    input wire clk,         // Тактовый сигнал (27 МГц)
    input wire reset,       // Сигнал сброса
    output reg lcd_rs,      // RS: выбор регистра (0 - команды, 1 - данные)
    output reg lcd_en,      // Enable: активный строб для передачи данных
    output [7:0] lcd_data   // Шина данных (8-битный интерфейс)
);

// Тайминги и параметры
parameter CLK_FREQ = 27_000_000; // Частота тактового сигнала
parameter DELAY_MS = 50;         // Задержка в миллисекундах
parameter CMD_DELAY = (CLK_FREQ / 1000) * DELAY_MS; // Задержка в тактах

reg [31:0] delay_counter;  // Счётчик задержки
reg delay_done;            // Флаг завершения задержки

reg [3:0] state;           // Текущее состояние машины состояний
reg [3:0] cmd_index;    // Индекс текущей команды в инициализации
reg [3:0] char_index;      // Индекс текущего символа. 2^4 = 16 доступных символов

reg [7:0] current_char;    // Текущий символ для передачи
assign lcd_data = current_char;

// Строка "hello", заданная как массив ASCII-кодов
reg [7:0] hello [0:11];
initial
begin
    hello[0] = 8'h49; // 'I'
    hello[1] = 8'h20; // ' '
    hello[2] = 8'h6C; // 'l'
    hello[3] = 8'h6F; // 'o'
    hello[4] = 8'h76; // 'v'
    hello[5] = 8'h65; // 'e'
    hello[6] = 8'h20; // ' '
    hello[7] = 8'h4C; // 'L'
    hello[8] = 8'h45; // 'E'
    hello[9] = 8'h54; // 'T'
    hello[10] = 8'h49; // 'I'
    hello[11] = 8'h21; // '!'
end

// Состояния машины состояний
localparam INIT_1   = 0;
localparam INIT_2   = 1;
localparam INIT_3   = 2;
localparam CONFIG   = 3;
localparam PRINT    = 4;
localparam FINISH   = 5;
localparam EN_ON    = 6;
localparam EN_OFF   = 7;

reg [7:0] command_buffer [0:3]; // Буфер команд для инициализации
initial 
begin
    command_buffer[0] = 8'b0011_1000; // Function set: 8-bit mode, 2 lines, 5x8 dots
    command_buffer[1] = 8'b0000_1100; // Display ON, Cursor OFF
    command_buffer[2] = 8'b0000_0001; // Clear Display
    command_buffer[3] = 8'b0000_1100; // Display ON, Cursor OFF
end

// Логика создания задержки между операциями
always @(posedge clk or negedge reset)
begin
    if (~reset) begin
        delay_counter <= 0;
        delay_done <= 0;
    end else begin
        if (delay_counter < CMD_DELAY) begin
            delay_counter <= delay_counter + 1;
            delay_done <= 0;
        end else begin
            delay_counter <= 0;
            delay_done <= 1;
        end
    end
end

// Основная машина состояний
always @(posedge clk or negedge reset)
begin
    if (~reset)
    begin
        state <= INIT_1;
        lcd_rs <= 0;
        lcd_en <= 0;
        current_char <= 8'b0;
        char_index <= 0;
        cmd_index <= 0;
    end else begin
        if (delay_done) begin
            case (state)
            
            INIT_1, INIT_2, INIT_3, CONFIG:
            begin
                lcd_rs <= 0;
                current_char <= command_buffer[cmd_index];
                state <= EN_ON;
            end

            EN_ON:
            begin
                lcd_en <= 1;
                state <= EN_OFF;
            end
                
            EN_OFF:
            begin
                lcd_en <= 0;
                if (cmd_index == CONFIG) begin
                    state <= PRINT;
                end else begin
                    cmd_index <= cmd_index + 1;
                    state <= (cmd_index == 2) ? CONFIG : (cmd_index);
                end
            end

            PRINT:
            begin
                if (char_index < 12) begin
                    lcd_rs <= 1;
                    current_char <= hello[char_index];
                    char_index <= char_index + 1;
                    state <= EN_ON;
                end else begin
                    state <= FINISH;
                end
            end
            
            FINISH:
            begin
                lcd_rs <= 0;
                lcd_en <= 0;
            end

            endcase
        end
    end
end

endmodule
