// ================================================================================
 module top
 (
    input clk,
    input rst_n,
    input [1:0] btn, // Up, Down
    
    output reg buzzer;
 );
// ================================================================================

reg         _buzzer     = 1'b0;
reg [19:0]  _deb_cnt [1:0];

reg [15:0]  _freq           = 16'd1000;
reg [15:0]  _freq_max       = 16'd5000;
reg [15:0]  _freq_min       = 16'd100;
reg [15:0]  _freq_step      = 16'd500;
reg [19:0]  _freq_counter   = 20'b0;

assign buzzer = ~_buzzer;

// ================================================================================

// ================================================================================
integer i;
always @(posedge clk or negedge rst_n) begin
    
    if (!rst_n)
    begin
        _freq           <= 16'd0;
        _max_freq       <= 16'd5000;
        _min_freq       <= 16'd0;
        _freq_step      <= 16'd500;
        _freq_counter   <= 20'b0;
    end
    else begin
        
        // handle buttons
        for (i = 0; i < 2; i = i + 1)
        begin
            if (!btn[i] && _deb_cnt[i] < 1_000_000)
            begin
                _deb_cnt[i] <= _deb_cnt[i] + 20'b1;
                 
                if (_deb_cnt[i] == 999_999) begin
                    // btn on

                    if (i == 0) begin
                        _freq <= ((_freq + _freq_step) > _freq_max) ? (_freq) : (_freq + _freq_step);
                    end else if (i == 1) begin
                        _freq <= (_freq >= (_freq_min + _freq_step)) ? (_freq - _freq_step) : (_freq);
                    end
                end
            end

            if (btn[i])
            begin
                // btn off
                
                _deb_cnt[i]     <= 20'b0;
                _freq_counter   <= 20'b0;
                _buzzer         <= 0'b0;
            end
        end

        // handle buzzer
        if (_freq_counter == (1 / _freq) * 27_000_000 / 2) begin
            // play sound
            _buzzer <= 1'b1;
        end

        if (_freq_counter == (1 / _freq) * 27_000_000) begin
            // not play sound
            _buzzer <= 1'b0;

            // reset counter
            _freq_counter <= 20'b0;
        end
    end


    end
end
// ================================================================================

endmodule