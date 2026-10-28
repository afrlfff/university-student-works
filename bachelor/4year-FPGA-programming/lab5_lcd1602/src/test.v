module top
(
    input wire clk,         // Тактовый сигнал (27 МГц)
    output led
);

reg a = 0;

always @(posedge clk)
begin 
    a = !a;
end

assign led = a;

endmodule