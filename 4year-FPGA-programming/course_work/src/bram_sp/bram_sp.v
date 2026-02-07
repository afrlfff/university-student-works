//Copyright (C)2014-2024 Gowin Semiconductor Corporation.
//All rights reserved.
//File Title: IP file
//Tool Version: V1.9.9.03 Education (64-bit)
//Part Number: GW1NR-LV9QN88PC6/I5
//Device: GW1NR-9
//Device Version: C
//Created Time: Wed Dec 17 12:30:47 2025

// BRAM SP (single-port) generated module
// Address width: 8
// Data width: 16
// Initialized with: {16'd932, 16'd830, 16'd145, 16'b0, ..., 16'b0}

module bram_sp (dout, clk, oce, ce, reset, wre, ad, din);

output [15:0] dout;
input clk;
input oce;
input ce;
input reset;
input wre;
input [2:0] ad;
input [15:0] din;

wire [15:0] sp_inst_0_dout_w;
wire gw_vcc;
wire gw_gnd;

assign gw_vcc = 1'b1;
assign gw_gnd = 1'b0;

SP sp_inst_0 (
    .DO({sp_inst_0_dout_w[15:0],dout[15:0]}),
    .CLK(clk),
    .OCE(oce),
    .CE(ce),
    .RESET(reset),
    .WRE(wre),
    .BLKSEL({gw_gnd,gw_gnd,gw_gnd}),
    .AD({gw_gnd,gw_gnd,gw_gnd,gw_gnd,gw_gnd,gw_gnd,gw_gnd,ad[2:0],gw_gnd,gw_gnd,gw_vcc,gw_vcc}),
    .DI({gw_gnd,gw_gnd,gw_gnd,gw_gnd,gw_gnd,gw_gnd,gw_gnd,gw_gnd,gw_gnd,gw_gnd,gw_gnd,gw_gnd,gw_gnd,gw_gnd,gw_gnd,gw_gnd,din[15:0]})
);

defparam sp_inst_0.READ_MODE = 1'b0;
defparam sp_inst_0.WRITE_MODE = 2'b00;
defparam sp_inst_0.BIT_WIDTH = 16;
defparam sp_inst_0.BLK_SEL = 3'b000;
defparam sp_inst_0.RESET_MODE = "SYNC";
defparam sp_inst_0.INIT_RAM_00 = 256'h00000000000000000000000000000000000000000000000000000091033E03A4;

endmodule //bram_sp
