module lcd1602_controller_8bit_with_delays
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

// ================================================================================

// debug values (for simulation)
//localparam DELAY_TURN_ON        = 2000;  // 2 ms
//localparam DELAY_CLEAR          = 2000;  // 2 ms
//localparam DELAY_SET_ADDR       = 50;     // 50 ns
//localparam DELAY_PRINT          = 50;     // 50 ns
//localparam DELAY_FUNCTION_SET   = 50;     // 50 ns
//localparam DELAY_DISPLAY_SWITCH = 50;     // 50 ns

// release values
localparam DELAY_TURN_ON        = 1_350_000;  // 50 ms
localparam DELAY_CLEAR          = 1_350_000;  // 50 ms
localparam DELAY_SET_ADDR       = 2_700;     // 100 mcs
localparam DELAY_PRINT          = 2_700;     // 100 mcs
localparam DELAY_FUNCTION_SET   = 2_700;     // 100 mcs
localparam DELAY_DISPLAY_SWITCH = 2_700;     // 100 mcs

localparam STATE_UNKNOWN          = 0;
localparam STATE_TURN_ON          = 1;
localparam STATE_INIT_1           = 2;
localparam STATE_INIT_2           = 3;
localparam STATE_INIT_3           = 4;
localparam STATE_CONFIG           = 5;
localparam STATE_IDLE             = 6;
localparam STATE_SET_ADDR         = 7;
localparam STATE_PRINT            = 8;
localparam STATE_CLEAR            = 9;
localparam STATE_EN_ON            = 10;

reg [31:0]  requested_delay;
reg         request_delay_signal;

reg [31:0] delay_counter;
reg delay_done;

reg [3:0] state;
reg [3:0] state_prev;
reg state_first_entry;

reg [7:0] command_buffer [0:3]; // Буфер команд для инициализации

reg [7:0] current_char;    // Текущий символ для передачи
assign lcd_data = current_char;

// ================================================================================

initial 
begin
    command_buffer[0] = 8'b0011_1000; // Function set: 8-bit mode, 2 lines, 5x8 dots
    command_buffer[1] = 8'b0000_1100; // Display ON, Cursor OFF
    command_buffer[2] = 8'b0000_0001; // Clear Display
    command_buffer[3] = 8'b0000_1100; // Display ON, Cursor OFF
end

// ================================================================================
// Making delays between lcd operations
always @(posedge clk or negedge reset)
begin
    if (~reset) begin
        delay_counter   <= 32'd0;
        delay_done      <= 1'b1;
    end else begin

        if (~delay_done) begin
            if (delay_counter < requested_delay) begin
                delay_counter   <= delay_counter + 1'b1;
            end else begin
                delay_counter   <= 32'd0;
                delay_done      <= 1'b1;
            end
        end
        else if (request_delay_signal) begin
            delay_done <= 1'b0;
            delay_counter <= 32'd0;
        end
    end
end

// ================================================================================
// Main FSM
always @(posedge clk or negedge reset)
begin
    if (~reset) begin
        state                   <= STATE_TURN_ON;
        state_prev              <= STATE_UNKNOWN;
        state_first_entry       <= 1'b1;
        lcd_en                  <= 1'b0;
        lcd_rs                  <= 1'b0;
        current_char            <= 8'b0;
    end else begin  
        request_delay_signal <= 1'b0; // to ensure that signal "1" will be only on a single tact

        // handle states
        case (state)
        // ========================================================================
        STATE_TURN_ON:
        begin
            state               <= STATE_EN_ON;
            state_prev          <= state;
            state_first_entry   <= 1'b1;
        end
        // ========================================================================
        STATE_INIT_1, STATE_INIT_2, STATE_INIT_3, STATE_CONFIG:
        begin
            case (state)
            STATE_INIT_1:     current_char <= command_buffer[0];
            STATE_INIT_2:     current_char <= command_buffer[1];
            STATE_INIT_3:     current_char <= command_buffer[2];
            STATE_CONFIG:     current_char <= command_buffer[3];
            endcase

            lcd_rs              <= 0;
            state               <= STATE_EN_ON;
            state_prev          <= state;
            state_first_entry   <= 1'b1;
        end
        // ========================================================================
        STATE_EN_ON:
        begin
            lcd_en                  <= 1'b1;

            if (state_first_entry) begin
                request_delay_signal    <= 1'b1;
                state_first_entry       <= 1'b0;

                case (state_prev)
                STATE_TURN_ON:      requested_delay     <= DELAY_TURN_ON;
                STATE_CLEAR:        requested_delay     <= DELAY_CLEAR;
                STATE_PRINT:        requested_delay     <= DELAY_PRINT;
                STATE_SET_ADDR:     requested_delay     <= DELAY_SET_ADDR;
                STATE_INIT_1:       requested_delay     <= DELAY_FUNCTION_SET;   
                STATE_INIT_2:       requested_delay     <= DELAY_DISPLAY_SWITCH;
                STATE_INIT_3:       requested_delay     <= DELAY_CLEAR;
                STATE_CONFIG:       requested_delay     <= DELAY_DISPLAY_SWITCH;
                default:            requested_delay     <= 1_350; // just in case; 50 mcs
                endcase
            end else begin
                if (~request_delay_signal && delay_done) begin
                    lcd_en              <= 1'b0;
                    state_prev          <= state;
                    state_first_entry   <= 1'b1;

                    case (state_prev)
                    STATE_TURN_ON:      state <= STATE_INIT_1;
                    STATE_INIT_1:       state <= STATE_INIT_2;
                    STATE_INIT_2:       state <= STATE_INIT_3;
                    STATE_INIT_3:       state <= STATE_CONFIG;
                    STATE_CONFIG:       state <= STATE_IDLE;
                    STATE_SET_ADDR:     state <= STATE_PRINT;
                    default:            state <= STATE_IDLE;
                    endcase
                end
            end
        end
        // ========================================================================
        STATE_IDLE:
        begin
            if (clear) begin
                state           <= STATE_CLEAR;
                state_prev      <= state;
            end
            else if (print) begin
                state           <= STATE_SET_ADDR;
                state_prev      <= state;
            end

            state_first_entry   <= 1'b1;
        end
        // ========================================================================
        STATE_SET_ADDR:
        begin
            lcd_rs                  <= 0;
            current_char            <= { 1'b1, ((row == 1'b0) ? (7'h00) : (7'h40)) + col };

            state                   <= STATE_EN_ON;
            state_prev              <= state;
            state_first_entry       <= 1'b1;
        end
        // ========================================================================
        STATE_PRINT:
        begin
            lcd_rs                  <= 1;
            current_char            <= character;

            state                   <= STATE_EN_ON;
            state_prev              <= state;
            state_first_entry       <= 1'b1;
        end
        // ========================================================================
        STATE_CLEAR:
        begin
            lcd_rs                  <= 0;
            current_char            <= command_buffer[2];

            state                   <= STATE_EN_ON;
            state_prev              <= state;
            state_first_entry       <= 1'b1;
        end
        // ========================================================================
        endcase
    end
end

// ================================================================================

endmodule
