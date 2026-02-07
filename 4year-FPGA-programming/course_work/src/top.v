module top (
    input clk,
    input rst,

    input [4:0] input_btns,

    output [7:0] indicator_segments,
    output [3:0] indicator_digits,

    output buz,

    output wire  lcd_rs,
    output wire  lcd_en,
    output [7:0] lcd_data
);

// input_btns[0]: go to MainMenu
// input_btns[1]: go to Game / restart the game
// input_btns[2]: go to ShowBest
// input_btns[3]: player jump
// input_btns[4]: game pause

// ================================================================================

// debug values (for simulation)
//localparam SCORE_TONE_DURATION      = 50;     // 50 ns
//localparam DEATH_TONE_DURATION      = 50;     // 50 ns

//localparam PLAYER_JUMP_DURATION     = 1000;   // 1 ms
//localparam WALL_MOVE_SPEED          = 500;    // 500 ns
//localparam SCORE_INCREASING_SPEED   = 1000;   // 1 ms

//localparam TURN_ON_LCD_DELAY        = 5000;   // 5 ms
//localparam PRINT_LCD_DELAY          = 200;    // 200 ns
//localparam CLEAR_LCD_DELAY          = 2500;   // 2.5 ms

// release values
localparam SCORE_TONE_DURATION      = 10_800_000;   // 400 ms
localparam DEATH_TONE_DURATION      = 8_100_000;    // 300 ms

localparam PLAYER_JUMP_DURATION     = 13_500_000;   // 500 ms
localparam WALL_MOVE_SPEED          = 4_050_000;    // 150 ms for each cell
localparam SCORE_INCREASING_SPEED   = 2_700_000;    // 100 ms

localparam TURN_ON_LCD_DELAY        = 40_500_000;   // 1.5 s
localparam PRINT_LCD_DELAY          = 10_000;       // > 200 mcs (PRINT + SET_ADDR + reserve)
localparam CLEAR_LCD_DELAY          = 1_500_000;    // > 50 ms   (CLEAR + reserve)



localparam NUM_SCORE_TO_PLAY_SOUND  = 50; // if change => code of score value trimming also should be changed

localparam STATE_UNKNOWN            = 0;
localparam STATE_MENU_INIT_1        = 1;
localparam STATE_MENU_INIT_2        = 2;
localparam STATE_MENU               = 3;
localparam STATE_SHOW_BEST_INIT_1   = 4;
localparam STATE_SHOW_BEST_INIT_2   = 4;
localparam STATE_SHOW_BEST          = 5;
localparam STATE_GAME_INIT          = 6;
localparam STATE_GAME               = 7;
localparam STATE_TURN_ON            = 8;

localparam STATE_LCD_UNKNOWN    = 0;
localparam STATE_LCD_IDLE       = 1;
localparam STATE_LCD_CLEAR      = 2;
localparam STATE_LCD_PRINT      = 3;

localparam STATE_BUZZER_UNKNOWN         = 0;
localparam STATE_BUZZER_IDLE            = 1;
localparam STATE_BUZZER_SCORE_SOUND     = 2;
localparam STATE_BUZZER_DEATH_SOUND     = 3;

localparam PLAYER_CHAR_CODE     = 105; // "i"
localparam WALL_CHAR_CODE       = 65;  // "A"

localparam OBJECT_UNKNOWN       = 0;
localparam OBJECT_PLAYER        = 1;
localparam OBJECT_WALL          = 2;
localparam OBJECT_CLEAR         = 3;

wire input_btns_clicked [0:5];

reg [3:0] state;
reg [3:0] state_prev;
reg [3:0] lcd_state;
reg [3:0] buzzer_state;
reg state_first_entry;

reg [13:0] score;
reg [13:0] best_score;

reg         buzzer_play_signal;
reg [13:0]  buzzer_current_tone;

reg buzzer_request_score_sound_signal;
reg buzzer_request_death_sound_signal;

reg [13:0] tone_buffer [0:2];

reg  [7:0] lcd_write_char;
reg        lcd_write_row;
reg  [3:0] lcd_write_col;
reg        lcd_print_signal;
reg        lcd_clear_signal;
reg  [4:0] lcd_char_idx;
reg        lcd_request_state_signal;
reg [3:0]  lcd_requested_state;

reg [3:0]   current_print_object;
reg         current_player_row;
reg [3:0]   current_wall_col;

reg is_game_paused;
reg is_game_finished;
reg player_jumped;

reg [31:0] turn_on_counter;

reg [31:0]  buzzer_counter;
reg [31:0] lcd_counter;
reg [31:0] jump_counter;
reg [31:0] wall_move_counter;
reg [31:0] score_increase_counter;

reg [7:0] main_menu_message [0:7];
reg [4:0] main_menu_addresses [0:7]; 

reg [7:0] show_best_message [0:9];
reg [4:0] show_best_addresses [0:9]; 

// ================================================================================

initial begin
//    main_menu_addresses[0] = 6; main_menu_message[0] = 8'h6D; // 'm'
//    main_menu_addresses[1] = 7; main_menu_message[1] = 8'h61; // 'a'
//    main_menu_addresses[2] = 8; main_menu_message[2] = 8'h69; // 'i'
//    main_menu_addresses[3] = 9; main_menu_message[3] = 8'h6E; // 'n'
    main_menu_addresses[0] = 6; main_menu_message[0] = 8'h6D; // 'm'
    main_menu_addresses[1] = 7; main_menu_message[1] = 8'h65; // 'e'
    main_menu_addresses[2] = 8; main_menu_message[2] = 8'h6E; // 'n'
    main_menu_addresses[3] = 9; main_menu_message[3] = 8'h75; // 'u'

    show_best_addresses[0] = 6; show_best_message[0] = 8'h62; // 'b'
    show_best_addresses[1] = 7; show_best_message[1] = 8'h65; // 'e'
    show_best_addresses[2] = 8; show_best_message[2] = 8'h73; // 's'
    show_best_addresses[3] = 9; show_best_message[3] = 8'h74; // 't'
//    show_best_addresses[4] = 21; show_best_message[4] = 8'h72; // 'r'
//    show_best_addresses[5] = 22; show_best_message[5] = 8'h65; // 'e'
//    show_best_addresses[6] = 23; show_best_message[6] = 8'h73; // 's'
//    show_best_addresses[7] = 24; show_best_message[7] = 8'h75; // 'u'
//    show_best_addresses[8] = 25; show_best_message[8] = 8'h6C; // 'l'
//    show_best_addresses[9] = 26; show_best_message[9] = 8'h74; // 't'

    tone_buffer[0]  = 14'd932; // score #1
    tone_buffer[1]  = 14'd830; // score #2
    tone_buffer[2]  = 14'd145; // death

    best_score      = 14'd0;
end

// ================================================================================
// Handle buzzer
always @(posedge clk or negedge rst)
begin
    if (~rst) begin
        buzzer_counter      <= 32'd0;
        buzzer_play_signal  <= 1'b0;
        buzzer_state        <= STATE_BUZZER_IDLE;
        buzzer_current_tone <= 14'd0;
    end else begin
        if (buzzer_request_score_sound_signal)
            buzzer_state <= STATE_BUZZER_SCORE_SOUND;
        if (buzzer_request_death_sound_signal)
            buzzer_state <= STATE_BUZZER_DEATH_SOUND;

        case (buzzer_state)
        // ========================================================================
        STATE_BUZZER_IDLE:
        begin
            buzzer_counter      <= 32'd0;
            buzzer_play_signal  <= 1'b0;
        end
        // ========================================================================
        STATE_BUZZER_SCORE_SOUND:
        begin
            if (buzzer_counter == 0) begin
                buzzer_current_tone     <= tone_buffer[0];
            end else if (buzzer_counter == SCORE_TONE_DURATION / 2) begin
                buzzer_current_tone     <= tone_buffer[1];
            end else if (buzzer_counter == SCORE_TONE_DURATION) begin
                buzzer_state            <= STATE_BUZZER_IDLE;
            end

            buzzer_play_signal  <= 1'b1;
            buzzer_counter      <= buzzer_counter + 1'b1;
        end
        // ========================================================================
        STATE_BUZZER_DEATH_SOUND:
        begin
            if (buzzer_counter == 0) begin
                buzzer_current_tone     <= tone_buffer[2];
            end else if (buzzer_counter == DEATH_TONE_DURATION) begin
                buzzer_state            <= STATE_BUZZER_IDLE;
            end

            buzzer_play_signal  <= 1'b1;
            buzzer_counter      <= buzzer_counter + 1'b1;
        end
        // ========================================================================
        endcase
    end
end

// ================================================================================
// Handle display printing and clearing
always @(posedge clk or negedge rst)
begin
    if (~rst) begin
        lcd_counter         <= 32'd0;
        lcd_state           <= STATE_LCD_IDLE;
        lcd_clear_signal    <= 1'b0;
        lcd_print_signal    <= 1'b0;
    end else begin
        // reset variables to ensure that they will be on state "1" just for a single tact
        lcd_clear_signal    <= 1'b0;
        lcd_print_signal    <= 1'b0;

        // update state
        if (lcd_request_state_signal) begin
            lcd_state <= lcd_requested_state;
            lcd_counter <= 32'd0;
        end

        // handle states
        case (lcd_state)
        // ========================================================================
        STATE_LCD_CLEAR:
        begin
            if (lcd_counter > 0) begin
                if (lcd_counter < CLEAR_LCD_DELAY) begin
                    lcd_counter     <= lcd_counter + 1'b1;
                end else begin
                    lcd_state       <= STATE_LCD_IDLE;
                end
            end else begin
                lcd_clear_signal    <= 1'b1;
                lcd_counter         <= lcd_counter + 1'b1;
            end
        end
        // ========================================================================
        STATE_LCD_PRINT:
        begin
            if (lcd_counter > 0) begin
                if (lcd_counter < PRINT_LCD_DELAY) begin
                    lcd_counter     <= lcd_counter + 1'b1;
                end else begin
                    lcd_state       <= STATE_LCD_IDLE;
                end
            end else begin
                lcd_print_signal    <= 1'b1;
                lcd_counter         <= lcd_counter + 1'b1;
            end
        end
        // ========================================================================
        STATE_LCD_IDLE:
        begin
            lcd_counter <= 32'd0;
        end
        // ========================================================================
        endcase
    end
end

// ================================================================================
// Main FSM
always @(posedge clk or negedge rst)
begin
    if (~rst) begin
        state                   <= STATE_TURN_ON;
        state_prev              <= STATE_UNKNOWN;  
        score                   <= 14'd0;
        best_score              <= 14'd0;
        state_first_entry       <= 1'b1;
        lcd_char_idx            <= 5'b0;
        current_print_object    <= OBJECT_PLAYER;
        player_jumped           <= 1'b0;
        jump_counter            <= 32'd0;
        wall_move_counter       <= 32'd0;
        score_increase_counter  <= 32'd0;
        is_game_paused          <= 1'b0;
        is_game_finished        <= 1'b0;
        
        turn_on_counter         <= 32'd0;

        lcd_write_char              <= 8'h00;
        lcd_write_row               <= 1'b0;
        lcd_write_col               <= 8'd0;
        lcd_requested_state         <= STATE_LCD_UNKNOWN;
        lcd_request_state_signal    <= 1'b0;

        current_player_row      <= 1'b1;
        current_wall_col        <= 4'd15;

        buzzer_request_score_sound_signal   <= 1'b0;
        buzzer_request_death_sound_signal   <= 1'b0;

    end else begin
        // to ensure that state "1" will be only on a signle tact
        lcd_request_state_signal            <= 1'b0;
        buzzer_request_score_sound_signal   <= 1'b0;
        buzzer_request_death_sound_signal   <= 1'b0;  

        case (state)
        // ========================================================================
        STATE_TURN_ON:
        begin
            if (turn_on_counter < TURN_ON_LCD_DELAY) begin
                turn_on_counter <= turn_on_counter + 1'b1;
            end else begin
                turn_on_counter     <= 32'd0;
                state_prev          <= state;
                state               <= STATE_GAME_INIT;
                state_first_entry   <= 1'b1;
            end
        end
        // ========================================================================
        STATE_MENU_INIT_1:
        begin
            // handle first entry => init display clearing
            if (state_first_entry) begin
                lcd_requested_state         <= STATE_LCD_CLEAR;
                lcd_request_state_signal    <= 1'b1;
                state_first_entry           <= 1'b0;
            end else begin
                // wait for display finish clearing
                if (~lcd_request_state_signal && lcd_state == STATE_LCD_IDLE) begin
                    state_prev          <= state;
                    state               <= STATE_MENU_INIT_2;
                    state_first_entry   <= 1'b1;
                end
            end
        end
        // ========================================================================
        STATE_MENU_INIT_2:
        begin
            // handle first entry => reset char_index
            if (state_first_entry) begin
                lcd_char_idx        <= 5'd0;
                state_first_entry   <= 1'b0;
            end else begin
                // wait for display to finish previous commands
                if (~lcd_request_state_signal && lcd_state == STATE_LCD_IDLE) begin
                    // print "main menu" text on the display
                    if (lcd_char_idx < 4) begin
                        lcd_requested_state         <= STATE_LCD_PRINT;
                        lcd_request_state_signal    <= 1'b1;

                        lcd_write_char  <= main_menu_message[lcd_char_idx];
                        lcd_write_row   <= main_menu_addresses[lcd_char_idx][4];
                        lcd_write_col   <= main_menu_addresses[lcd_char_idx][3:0];

                        lcd_char_idx    <= lcd_char_idx + 1'b1;
                    end else begin
                        state_prev          <= state;
                        state               <= STATE_MENU;
                        state_first_entry   <= 1'b1;
                    end
                end
            end
        end
        // ========================================================================
        STATE_MENU:
        begin
            // handle user actions
            if (input_btns_clicked[1]) begin
                state_prev          <= state;
                state               <= STATE_GAME_INIT;
                state_first_entry   <= 1'b1;
            end else
            if (input_btns_clicked[2]) begin
                state_prev          <= state;
                state               <= STATE_SHOW_BEST_INIT_1;
                state_first_entry   <= 1'b1;
            end
        end
        // ========================================================================
        STATE_SHOW_BEST_INIT_1:
        begin
            // handle first entry => init display clearing
            if (state_first_entry) begin
                lcd_requested_state         <= STATE_LCD_CLEAR;
                lcd_request_state_signal    <= 1'b1;
                state_first_entry           <= 1'b0;
            end else begin
                // wait for display finish clearing
                if (~lcd_request_state_signal && lcd_state == STATE_LCD_IDLE) begin
                    state_prev          <= state;
                    state               <= STATE_SHOW_BEST_INIT_2;
                    state_first_entry   <= 1'b1;
                end
            end
        end
        // ========================================================================
        STATE_SHOW_BEST_INIT_2:
        begin
            // handle first entry => reset char_index
            if (state_first_entry) begin
                lcd_char_idx        <= 5'd0;
                state_first_entry   <= 1'b0;
            end else begin
                // wait for display to finish previous commands
                if (~lcd_request_state_signal && lcd_state == STATE_LCD_IDLE) begin
                    // print "best result" text on the display
                    if (lcd_char_idx < 4) begin
                        lcd_requested_state         <= STATE_LCD_PRINT;
                        lcd_request_state_signal    <= 1'b1;

                        lcd_write_char  <= show_best_message[lcd_char_idx];
                        lcd_write_row   <= show_best_addresses[lcd_char_idx][4];
                        lcd_write_col   <= show_best_addresses[lcd_char_idx][3:0];

                        lcd_char_idx    <= lcd_char_idx + 1'b1;
                    end else begin
                        state_prev          <= state;
                        state               <= STATE_SHOW_BEST;
                        state_first_entry   <= 1'b1;
                    end
                end 
            end
        end
        // ========================================================================
        STATE_SHOW_BEST:
        begin
            // handle first entry
            if (state_first_entry) begin
                score               <= best_score;
                state_first_entry   <= 1'b0;
            end else begin
                // handle user actions
                if (input_btns_clicked[0]) begin
                    state_prev          <= state;
                    state               <= STATE_MENU_INIT_1;
                    state_first_entry   <= 1'b1;
                end else
                if (input_btns_clicked[1]) begin
                    state_prev          <= state;
                    state               <= STATE_GAME_INIT;
                    state_first_entry   <= 1'b1;
                end
            end
        end
        // ========================================================================
        STATE_GAME_INIT:
        begin
            // handle first entry => init display clearing
            if (state_first_entry) begin
                lcd_requested_state         <= STATE_LCD_CLEAR;
                lcd_request_state_signal    <= 1'b1;
                state_first_entry           <= 1'b0;
            end else begin
                // wait for display finish clearing
                if (~lcd_request_state_signal && lcd_state == STATE_LCD_IDLE) begin
                    state_prev          <= state;
                    state               <= STATE_GAME;
                    state_first_entry   <= 1'b1;
                end
            end
        end
        // ========================================================================
        STATE_GAME:
        begin
            // handle first entry
            if (state_first_entry) begin
                score                       <= 14'd0;
                state_first_entry           <= 1'b0;
                current_wall_col            <= 4'd15;
                current_player_row          <= 1'b1;
                wall_move_counter           <= 32'd0;
                is_game_paused              <= 1'b0;
                is_game_finished            <= 1'b0;
                score_increase_counter      <= 32'd0;
            end else begin
                // main_handler
                if (~is_game_paused && ~is_game_finished)
                begin
                    // increase score
                    if (score_increase_counter < SCORE_INCREASING_SPEED) begin
                        score_increase_counter  <= score_increase_counter + 1'b1;
                    end else begin
                        score_increase_counter  <= 32'd0;
                        score                   <= (score < 14'd9999) ? (score + 1'b1) : (14'd9999);
                        best_score              <= (score > best_score) ? (score) : (best_score);
                    end

                    // handle score sound
                    if (score[5:0] == NUM_SCORE_TO_PLAY_SOUND) begin
                        buzzer_request_score_sound_signal <= 1'b1;
                    end

                    // handle wall moving
                    if (wall_move_counter < WALL_MOVE_SPEED) begin
                        wall_move_counter <= wall_move_counter + 1'b1;
                    end else begin
                        wall_move_counter <= 32'd0;
                        current_wall_col  <= (current_wall_col > 0) ? (current_wall_col - 1'b1) : (4'd15);
                    end

                    // handle player jump
                    if (player_jumped) begin
                        if (jump_counter < PLAYER_JUMP_DURATION) begin
                            jump_counter        <= jump_counter + 1'b1;
                            current_player_row  <= 1'b0;
                        end else begin
                            player_jumped       <= 1'b0;
                            jump_counter        <= 32'd0; 
                            current_player_row  <= 1'b1;
                        end
                    end

                    // handle game end (player-wall collision)
                    if (current_player_row == 1 && current_wall_col == 0) begin
                        // end the game
                        buzzer_request_death_sound_signal   <= 1'b1;
                        is_game_finished                    <= 1'b1;
                    end
                end

                // print game (player - wall - player - wall - ...)
                if (~lcd_request_state_signal && lcd_state == STATE_LCD_IDLE && ~is_game_finished) begin
                    case (current_print_object)
                    OBJECT_PLAYER:
                    begin
                        lcd_write_char          <= PLAYER_CHAR_CODE;
                        lcd_write_row           <= current_player_row;
                        lcd_write_col           <= 4'd0;
                        current_print_object    <= OBJECT_WALL;
                        lcd_requested_state     <= STATE_LCD_PRINT;
                    end
                    OBJECT_WALL:
                    begin
                        lcd_write_char          <= WALL_CHAR_CODE;
                        lcd_write_row           <= 1'b1;
                        lcd_write_col           <= current_wall_col;
                        current_print_object    <= OBJECT_CLEAR;
                        lcd_requested_state     <= STATE_LCD_PRINT;
                    end
                    OBJECT_CLEAR:
                    begin
                        lcd_write_char          <= WALL_CHAR_CODE;
                        current_print_object    <= OBJECT_PLAYER;
                        lcd_requested_state     <= STATE_LCD_CLEAR;
                    end
                    endcase

                    lcd_request_state_signal    <= 1'b1;
                end

                // handle user actions
                if (input_btns_clicked[0]) begin
                    state_prev          <= state;
                    state               <= STATE_MENU_INIT_1;
                    state_first_entry   <= 1'b1;
                end else 
                if (input_btns_clicked[1]) begin
                    state_prev          <= state;
                    state               <= STATE_GAME_INIT;
                    state_first_entry   <= 1'b1;
                end else
                if (input_btns_clicked[2]) begin
                    state_prev          <= state;
                    state               <= STATE_SHOW_BEST_INIT_1;
                    state_first_entry   <= 1'b1;
                end else
                if (input_btns_clicked[3] && ~player_jumped) begin
                    // player jump
                    player_jumped       <= 1'b1;
                    jump_counter        <= 32'd0;
                end else if (input_btns_clicked[4]) begin
                    // game pause
                    is_game_paused      <= ~is_game_paused;
                end
            end
        end
        // ========================================================================

        endcase
    end
end

// ================================================================================

push_button push_btn1_init ( .clk(clk), .rst(rst), .btn(input_btns[0]), .btn_pushed(input_btns_clicked[0]) );
push_button push_btn2_init ( .clk(clk), .rst(rst), .btn(input_btns[1]), .btn_pushed(input_btns_clicked[1]) );
push_button push_btn3_init ( .clk(clk), .rst(rst), .btn(input_btns[2]), .btn_pushed(input_btns_clicked[2]) );
push_button push_btn4_init ( .clk(clk), .rst(rst), .btn(input_btns[3]), .btn_pushed(input_btns_clicked[3]) );
push_button push_btn5_init ( .clk(clk), .rst(rst), .btn(input_btns[4]), .btn_pushed(input_btns_clicked[4]) );

buzzer buzzer_init ( .clk(clk), .rst(rst), .freq(buzzer_current_tone), .play(buzzer_play_signal), .buz(buz) );

seven_segment_indicator indicator_init (
    .clk(clk),
    .value(score),
    .segments(indicator_segments),
    .digits(indicator_digits)
);

lcd1602_controller_8bit_with_delays lcd_init
(
    .clk(clk),
    .reset(rst),

    .row(lcd_write_row),
    .col(lcd_write_col),
    .character(lcd_write_char),
    .print(lcd_print_signal),
    .clear(lcd_clear_signal),

    .lcd_rs(lcd_rs),
    .lcd_en(lcd_en),
    .lcd_data(lcd_data)
);

// ================================================================================

endmodule