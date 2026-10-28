module lcd1602_controller_8bit
(
    input clk,         // Тактовый сигнал (27 МГц)
    input reset,       // Сигнал сброса

    input       row,
    input [3:0] col,
    input [7:0] character,
    input       print,
    input       clear,

    output reg lcd_rs,      // RS: выбор регистра (0 - команды, 1 - данные)
    output reg lcd_en,      // Enable: активный строб для передачи данных
    output [7:0] lcd_data   // Шина данных (8-битный интерфейс)
);

// Тайминги и параметры
localparam CLK_FREQ = 27_000_000;                // Частота тактового сигнала
localparam CMD_DELAY = (CLK_FREQ / 1000) * 50;   // 50 ms

reg [31:0] delay_counter;  // Счётчик задержки
reg delay_done;            // Флаг завершения задержки

reg [3:0] state;           // Текущее состояние машины состояний
reg [3:0] cmd_index;       // Индекс текущей команды в инициализации

reg need_clear;
reg need_print;
reg clear_finished;
reg print_finished;

reg print_address_is_set;

reg [7:0] current_char;    // Текущий символ для передачи
assign lcd_data = current_char;

// Состояния машины состояний
localparam INIT_1           = 0;
localparam INIT_2           = 1;
localparam INIT_3           = 2;
localparam CONFIG           = 3;
localparam SET_ADDR         = 4;
localparam PRINT            = 5;
localparam IDLE             = 6;
localparam EN_ON            = 7;
localparam EN_OFF           = 8;
localparam CLEAR            = 9;

reg [7:0] command_buffer [0:3]; // Буфер команд для инициализации
initial 
begin
    command_buffer[0] = 8'b0011_1000; // Function set: 8-bit mode, 2 lines, 5x8 dots
    command_buffer[1] = 8'b0000_1100; // Display ON, Cursor OFF
    command_buffer[2] = 8'b0000_0001; // Clear Display
    command_buffer[3] = 8'b0000_1100; // Display ON, Cursor OFF
end

// Логика отслеживания необходимости записи
always @(posedge clk or negedge reset)
begin
    if (~reset) begin
        need_print <= 1'b0;
        need_clear <= 1'b0;
    end else begin
        if (print) need_print <= 1'b1;
        if (clear) need_clear <= 1'b1;
        
        if (print_finished) need_print <= 1'b0;
        if (clear_finished) need_clear <= 1'b0;
    end
end

// Логика создания задержки между операциями
always @(posedge clk or negedge reset)
begin
    if (~reset) begin
        delay_counter <= 0;
        delay_done <= 0;
    end else begin
        if (delay_counter < CMD_DELAY)
        begin
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
    if (~reset) begin
        state                   <= INIT_1;
        lcd_rs                  <= 0;
        lcd_en                  <= 0;
        current_char            <= 8'b0;
        cmd_index               <= 0;
        print_address_is_set    <= 1'b0;
        print_finished          <= 1'b0;
        clear_finished          <= 1'b0;
    end else begin
        // to ensure that these signals will be on "1" only for a single tact
        print_finished          <= 1'b0;
        clear_finished          <= 1'b0;

        if (delay_done)
        begin
            case (state)

            INIT_1, INIT_2, INIT_3, CONFIG:
            begin
                lcd_rs          <= 0;
                current_char    <= command_buffer[cmd_index];
                state           <= EN_ON;
            end

            EN_ON:
            begin
                lcd_en  <= 1;
                state   <= EN_OFF;
            end

            EN_OFF:
            begin
                lcd_en  <= 0;
                state   <= IDLE;
            end

            IDLE:
            begin
                if (cmd_index == CONFIG) begin

                    if (need_clear)
                    begin
                        state <= CLEAR;
                    end
                    else if (need_print)
                    begin
                        if (print_address_is_set) begin
                            state <= PRINT;
                        end else begin
                            state <= SET_ADDR;
                        end
                    end
                    
                end else begin
                    cmd_index <= cmd_index + 1;
                    state <= (cmd_index == 2) ? CONFIG : (cmd_index);
                end
            end

            SET_ADDR:
            begin
                lcd_rs                  <= 1'b0;
                current_char            <= { 1'b1, ((row == 1'b0) ? (7'h00) : (7'h40)) + col }; 
                state                   <= EN_ON;
                print_address_is_set    <= 1'b1;
            end
            
            PRINT:
            begin
                lcd_rs                  <= 1;
                current_char            <= character;
                state                   <= EN_ON;
                print_address_is_set    <= 1'b0;
                print_finished          <= 1'b1;
            end

            CLEAR:
            begin
                lcd_rs                  <= 0;
                current_char            <= command_buffer[2];
                state                   <= EN_ON;
                clear_finished          <= 1'b1;
            end

            endcase
        end
    end
end

endmodule
