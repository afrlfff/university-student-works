module lcd1602_controller_8bit
(
    input wire clk,             // Тактовый сигнал (27 МГц)
    input wire reset,           // Сигнал сброса

    input reg [7:0] characters [0:31], // Символы
    
    output reg lcd_rs,          // RS: выбор регистра (0 - команды, 1 - данные)
    output reg lcd_en,          // Enable: активный строб для передачи данных
    output [7:0] lcd_data       // Шина данных (8-битный интерфейс)
);

// Тайминги и параметры
parameter CLK_FREQ = 27_000_000; // Частота тактового сигнала

parameter CMD_DELAY = (CLK_FREQ / 1000) * 50; // Задержка в тактах (50 мс; с запасом)
parameter EN_DELAY = 15; // Задержка в тактах (>= 14 нс; с запасом)
parameter CLEAR_DELAY = 45_000; // Задержка в тактах (>= 1.52 мс; с запасом)
//parameter BASIC_CMD_DELAY = 1_500;  // Задержка в тактах (>= 37 мкс; с запасом)
parameter INIT_DELAY = 450_000; // Задержка в тактах (>= 15 мс; с запасом)

reg [31:0] cmd_delay_counter;           // Счётчик задержки
reg [31:0] en_delay_counter;            // Счётчик задержки
reg [31;0] clear_delay_counter;         // Счётчик задержки
reg [31;0] init_delay_counter;          // Счётчик задержки
reg cmd_delay_done;             // Флаг завершения задержки
reg clear_delay_done;           // Флаг завершения задержки
reg init_delay_done;            // Флаг завершения задержки

reg [3:0] state;           // Текущее состояние машины состояний
reg [3:0] init_cmd_index;       // Индекс текущей команды в инициализации

reg [7:0] current_char;    // Текущий символ для передачи
assign lcd_data = current_char;


// Состояния машины состояний
localparam INIT_1       = 0;
localparam INIT_2       = 1;
localparam INIT_3       = 2;
localparam CONFIG       = 3;
localparam IDLE         = 4;
localparam PRINT        = 6;
localparam CLEAR        = 7;
localparam EN_ON        = 8;
localparam EN_OFF       = 9;

reg [7:0] command_buffer [0:3]; // Буфер команд для инициализации
initial 
begin
    command_buffer[0] = 8'b0011_1000; // Function set: 8-bit mode, 2 lines, 5x8 dots
    command_buffer[1] = 8'b0000_1100; // Display ON, Cursor OFF
    command_buffer[2] = 8'b0000_0001; // Clear Display
    command_buffer[3] = 8'b0000_1100; // Display ON, Cursor OFF

    clear_delay_done <= 1'b1;
    init_delay_done <= 1'b0;
end

// Логика создания задержки перед запуском (INIT)
always @(posedge clk)
begin
    if (~init_delay_done) begin
        if (init_delay_counter < INIT_DELAY) begin
            init_delay_counter <= init_delay_counter + 1'b1;
        end else begin
            init_delay_done <= 1'b1;
        end
    end
end

// Логика создания задержки между операциями (командами)
always @(posedge clk or negedge reset)
begin
    if (~reset)
    begin
        cmd_delay_counter <= 1'b0;
        cmd_delay_done <= 1'b0;
    end else begin
        if (cmd_delay_counter < CMD_DELAY)
        begin
            cmd_delay_counter <= cmd_delay_counter + 1'b1;
            cmd_delay_done <= 1'b0;
        end else begin
            cmd_delay_counter <= 1'b0;
            cmd_delay_done <= 1'b1;
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
        init_cmd_index <= 0;
    end else begin
        if (init_delay_done && cmd_delay_done)
        begin
            case (state)
            INIT_1, INIT_2, INIT_3, CONFIG:
            begin
                lcd_rs <= 0;
                current_char <= command_buffer[init_cmd_index];
                state <= EN_ON;
            end
            EN_ON:
            begin
                if (lcd_en == 1'b0)
                begin
                    lcd_en <= 1;
                    en_delay_counter <= 0;
                end else begin
                    if (en_delay_counter < EN_DELAY) begin
                        en_delay_counter <= en_delay_counter + 1;
                    end else begin
                        state <= EN_OFF;
                    end
                end
            end
            EN_OFF:
            begin
                lcd_en <= 0;
                if (init_cmd_index == CONFIG) begin
                    state <= IDLE;
                end else begin
                    init_cmd_index <= init_cmd_index + 1;
                    state <= (init_cmd_index == 2) ? CONFIG : (init_cmd_index);
                end
            end
            IDLE:
            begin
                lcd_rs <= 0;
                lcd_en <= 0;

                // handle delays
                if (clear_delay_done == 1'b0') begin
                    if (clear_delay_counter < CLEAR_DELAY) begin
                        clear_delay_counter <= clear_delay_counter + 1'b1;
                    end else begin
                        clear_delay_done <= 1'b1;
                    end
                end

                
                
                // main processing
                // ...
                if (char_changed) begin
                    char_changed <= 1'b0;
                    state <= SET_ADDR;
                end
            end
            CLEAR:
            begin
                lcd_rs <= 0;
                current_char <= command_buffer[2];
                state <= EN_ON;
            end
            SET_ADDR:
            begin
                // ...
                lcd_rs <= 1'b0;
                current_char <= ((row == 0) ? (8'h00') : (8'h40)) + col;
                state <= EN_ON;
            end
            PRINT:
            begin
                lcd_rs <= 1;
                current_char = character;
                state <= EN_ON;
            end
            endcase
        end

        state_prev = state;
    end
end

endmodule