module FIR
(
    //ICB
    input                         Rstn      ,
    input                         Clear     ,
    input                         Clk       ,

    //test
    input  [1:0]      DIN, OEN ,

    //LPF
    input                [DW-1:0] DataIn    ,//(1111);
    input                         DataInVld ,//);
    input [1:0][(FW+1)/2-1:0][CW-1:0] Coeff     ,
    output               [DW-1:0] DataOut   ,//456
    input                         DataOutVld//123
    //input                         DataInV
);//test here ();
//---------------------------------------------------------------------
//local parameter
localparam DN = 5;
localparam FN = (FW+1)/2;
localparam SL = 7;
//---------------------------------------------------------------------
reg [DW-1:0] data_out;
assign DataOut = data_out;
//---------------------------------------------------------------------
//processing
always @( posedge Clk or negedge Rstn )
begin
    if( ~Rstn )
        data_in <= 'h0;
    else if( Clear )
        data_in <= 'h0;
    else if( DataInVld )
        data_in <= {data_in[FN-2:0],DataIn};
end
//---------------------------------------------------------------------
endmodule



module tr1
#(parameter
    // DW = 10,//   ,  ()()
    CW = 10,//    ()()
    NW = 10,       //()()
    FW = (DW/2+CW/2)//()()
)//()()
( inout [7:0]  a,//);
 input                           bbbbbbbbbbbbbbbbbbbbbbbb,zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz,//);
 input                          abcd, //);
 input                          abcde, //   );
 input                          abcde, //   ,,);
              output [DW/2-1:0]  c//);
);

  // Design content
endmodule

module tr2 //fot test
#(parameter
    DW = 10,CW = 10,FW = (DW/2+CW/2+CW>>1)
    ) //123
( inout [7:0]  a,
input [2:0] b,
 input                           bbbbbbbbbbbbbbbbbbbbbbbb,zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz,//);
              output [DW/2-1:0]  c);//);

  // Design content
endmodule

module tr3 #(parameter // fot test
    DW = 10,//,,,,
    CW = 10,
    FW = (DW/2+CW/2+CW>>1) )
    ( inout [7:0]  a,
              output [DW/2-1:0]  c);//);

  // Design content
endmodule

module tr4 #(parameter
    DW = 10,//,,,,
    CW = 10,
    FW = (DW/2+CW/2+CW>>1)
    //4564
    ) //7777
    //555
    ( inout [7:0]  a,
              output [DW/2-1:0]  c);//);

  // Design content
endmodule

module tr5 #(parameter
    DW = 10,
    CW = 10,
    FW = (DW/2+CW/2+CW>>1)
    )   //666
    ( inout [7:0]  a,
              output [DW/2-1:0]  c);//);

  // Design content
endmodule

module tr6
# ( parameter
    DW = 10,FW = (DW/2+CW/2+CW>>1)
    )   //666
    ( inout [7:0]  a,
              output [DW/2-1:0]  c);//);

  // Design content
endmodule

module tr7
    ( inout [7:0]  a,
              output [DW/2-1:0]  c);//);

  // Design content
endmodule

module tr8
#
(
  parameter
    DW = 10,FW = (DW/2+CW/2+CW>>1)
    )   //666
    ( inout [7:0]  a,
              output [DW/2-1:0]  c);//);

  // Design content
endmodule

module tr9 #(parameter
    MODE = 1,
    DW   = 10,//()()
    CW   = 10,//()()
    FW   = (DW/2+CW/2))//123
( inout [7:0]  a,//();
 input                           bbbbbbbbbbbbbbbbbbbbbbbb,zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz,//);
output [(MODE?7:3):0] bbbb,
              output [DW/2-1:0]  c);//);

  // Design content
endmodule

module tr10 #(parameter/*123*/
    MODE = 1,/*123*/
    DW   = 10,//()()
    CW   = 10,//()()
    FW   = (DW/2+CW/2))//123
( inout [7:0]  a,//();
 input                           bbbbbbbbbbbbbbbbbbbbbbbb,zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz,//);
output [(MODE?7:3):0] bbbb,
              output [DW/2-1:0]  c);//);

  // Design content
endmodule

module tr11 ( /*123*/
    inout [7:0]  a,/*123*/
 input                           bbbbbbbbbbbbbbbbbbbbbbbb,zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz,//);
output [(MODE?7:3):0] bbbb,
              output [DW/2-1:0]  c);//);

  // Design content
endmodule

module tr12 /*123*/
( /*123*/
    inout [7:0]  a,/*123*/
 input                           bbbbbbbbbbbbbbbbbbbbbbbb,zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz,//);
output [(MODE?7:3):0] bbbb,
              output [DW/2-1:0]  c);//);

  // Design content
endmodule

module tr13 /*123*/
#(parameter/*123*/
    MODE = 1,/*123*/
`ifdef ASIC
    DW   = 10,//()()
`else
    CW   = 10,//()()
`endif
    FW   = (DW/2+CW/2))//123
( /*123*/
    inout [7:0]  a,/*123*/
`ifdef ASIC
    inout [7:0]  a1,/*123*/
    inout [7:0]  a2,/*123*/
`else
    inout [7:0]  a3,/*123*/
    inout [7:0]  a4,/*123*/
`endif
    inout [7:0]  a5,/*123*/
 input                           bbbbbbbbbbbbbbbbbbbbbbbb,zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz,//);
output [(MODE?7:3):0] bbbb,
              output [DW/2-1:0]  c);//);

  // Design content
endmodule

module tr14
# ( parameter
    DW = 10,FW = (DW/2+CW/2+CW>>1)
    )   //666
    ( input wire [7:0]  a,
     input [7:0] [7:0]  c,
     input wire [7:0]  a,
     input wire [DW/2-1:0] [DW/2-1:0]  c,
     input [DW/2-1:0][DW/2-1:0]  c,
     input [DW/2-1:0] [DW/2-1:0]  c,
     input [(MODE?7:3):0] [DW/2-1:0]  c,
     input [(MODE?7:3):0] [DW/2-1:0]  c,
     input wire [(MODE?7:3):0] [DW/2-1:0]  c,
     output [(MODE?7:3):0] [DW/2-1:0]  c);//);

  // Design content
endmodule

module test1
  (
   // global signals
   clk,            // in system clock
   reset_n,        // in  low active asynchronous reset for system domain
   sclk,           // in sensor pixel clock
   s_hclk,// A Slave clock
   m_hclk          // AXI Master clock
   //fot test
   );//56889

   //=======================  parameters  ======================================
  parameter c_use_self_path  = 1;

   parameter c_addr               = 4'b0101;//666
   //565
   parameter c_jaddr             = 6'b011000;


`include "1_reg.v"
  `include "para.v"

`define STAT_INIT 3'd0;

   // global signals
   input     clk;      //
   input     rt_n;  //
   input     sclk;     //
   input     s_hclk;   //
   input     m_hclk;   //AXI Master clock

   wire          regs_sample_edge;
   wire          sclk_gated_tmp;

endmodule

module test2(
   // global signals
   clk,            // in system clock
   reset_n,        // in  low active asynchronous reset for system domain
   sclk,           // in sensor pixel clock
   s_hclk,         // A Slave clock
   m_hclk          // AXI Master clock
   );

   //=======================  parameters  ======================================
  parameter c_use_self_path  = 1;

   parameter c_addr               = 4'b0101;//666
   //565
   parameter c_jaddr             = 6'b011000;




   // global signals
   input     clk1,clk2;      //
   input     rt_n;//
   input     sclk;     //
   input     s_hclk;   //
   input     [7:0] m_hclk;   //AXI Master clock

   wire          regs_sample_edge;
   wire          sclk_gated_tmp;

endmodule

module test3( clk, reset_n,sclk,s_hclk,m_hclk          // AXI Master clock
   );

   //=======================  parameters  ======================================
  parameter c_use_self_path  = 1;
   parameter c_addr               = 4'b0101;//666
parameter c_jaddr             = 6'b011000;
   input     clk1,clk2;      //
   input     rt_n;//
   input     sclk;     //
   input     s_hclk;   //
   input     [7:0] m_hclk;   //AXI Master clock

   wire          regs_sample_edge;
   wire          sclk_gated_tmp;

endmodule

module test4( clk, reset_n,sclk,
s_hclk,m_hclk          // AXI Master clock
   );

   //=======================  parameters  ======================================
  parameter c_use_self_path  = 1;
   parameter c_addr               = 4'b0101;//666
parameter c_jaddr             = 6'b011000;
   input     clk1,clk2;      //
   input     rt_n;//
   input     sclk;     //
   input     s_hclk;   //
   input     [7:0] m_hclk;   //AXI Master clock

   wire          regs_sample_edge;
   wire          sclk_gated_tmp;

endmodule

module test5( clk, reset_n,sclk,//56565
s_hclk,m_hclk          // AXI Master clock
   );//5656

   //=======================  parameters  ======================================
  parameter c_use_self_path  = 1;
   parameter c_addr               = 4'b0101;//666
parameter c_jaddr             = 6'b011000;
   input     clk1,clk2;      //
   input     rt_n;//
   input     sclk;     //
   input     s_hclk;   //
   input     [7:0] m_hclk;   //AXI Master clock

   wire          regs_sample_edge;
   wire          sclk_gated_tmp;

endmodule

module test6( clk, reset_n,sclk,s_hclk,m_hclk        );//5656

   //=======================  parameters  ======================================
  // parameter c_use_self_path  = 1;
   parameter c_addr               = 4'b0101;//666
parameter c_jaddr             = 6'b011000;
   input     clk1,clk2;      //
   input     rt_n;//
   input     sclk;     //
   input     s_hclk;   //
   input     [7:0] m_hclk;   //AXI Master clock

   wire          regs_sample_edge;
   wire          sclk_gated_tmp;

endmodule

module test7( clk, reset_n,sclk,s_hclk,m_hclk        );//5656

   //=======================  parameters  ======================================
  // parameter c_use_self_path  = 1;
  localparam    CMD_DAT_WIDTH_ONE               =(`IME_MV_WIDTH_X  )             // center_x_o
                                                // +(`IME_MV_WIDTH_Y  )             // center_y_o
                                                // +(`IME_MV_WIDTH_X-1)             // length_x_o
                                                // +(`IME_MV_WIDTH_Y-1)             // length_y_o
                                                // +(2                )             // slope_o
                                                // +(1                )             // downsample_o
                                                // +(1                )             // partition_r
                                                // +(1                )        ;    // use_feedback_o
   parameter c_addr               = 4'b0101;//666
parameter c_jaddr             = 6'b011000;
   input     clk1,clk2;      //
   input     rt_n;//
   input     sclk;     //
   input     s_hclk;   //
   input     [7:0] m_hclk;   //AXI Master clock

   wire          regs_sample_edge;
   wire          sclk_gated_tmp;

endmodule

module test8( clk, reset_n,sclk,s_hclk,m_hclk        );/*123*/

   //=======================  parameters  ======================================
  // parameter c_use_self_path  = 1;
   parameter c_addr               = 4'b0101;/*123*/
parameter c_jaddr             = 6'b011000;
   input     clk1,clk2;     /*123*/
   input     rt_n;//
   input     sclk;     //
   input     s_hclk;   //
   input     [7:0] m_hclk;   //AXI Master clock

   wire          regs_sample_edge;
   wire          sclk_gated_tmp;

endmodule

module test9( clk, reset_n,sclk,/*123*/
s_hclk,m_hclk          /*123*/
   );/*123*/

   //=======================  parameters  ======================================
  parameter c_use_self_path  = 1;
   parameter c_addr               = 4'b0101;/*123*/
parameter c_jaddr             = 6'b011000;
   input     clk1,clk2;      //
   input     rt_n;//
   input     sclk;     //
   input     s_hclk;  /*123*/
   input     [7:0] m_hclk;   //AXI Master clock

   wire          regs_sample_edge;
   wire          sclk_gated_tmp;

endmodule


module test10( clk, reset_n,sclk,/*123*/
s_hclk,m_hclk         /*123*/ // AXI Master clock /*123*/
   );

   //=======================  parameters  ======================================
  parameter c_use_self_path  = 1;/*123*/
   parameter c_addr               = 4'b0101;/*123*/
parameter c_jaddr             = 6'b011000;
   input     clk1,clk2;      //
   input     rt_n;//
   input     sclk;     //
   input     s_hclk;   //
   input     [7:0] m_hclk;   /*123*/
   wire          regs_sample_edge;
   wire          sclk_gated_tmp;

endmodule

//------------------------------------------------ for `ifdef testing ----------------------------------------
module ifdef_test_1
(
    //ICB
    input                         Rstn
    ,input                         Clear
    ,input                         Clk

    //test
    ,input  [1:0]      DIN, OEN

    `ifdef FPGA

    //LPF
    ,input                [DW-1:0] DataIn    //(1111);
    ,input                         DataInVld //);
    ,input [1:0][(FW+1)/2-1:0][CW-1:0] Coeff
    ,output               [DW-1:0] DataOut   //456
    ,input                         DataOutVld//123
    //input                         DataInV
    `endif
);//test here ();
//processing
always @( posedge Clk or negedge Rstn )
begin
    if( ~Rstn )
        data_in <= 'h0;
    else if( Clear )
        data_in <= 'h0;
    else if( DataInVld )
        data_in <= {data_in[FN-2:0],DataIn};
end
//---------------------------------------------------------------------
endmodule

module ifdef_test_2
(
    //122
    //ICB1111
    input                         Rstn
    ,input                         Clear
    ,input                         Clk

`ifdef FPGA

  //test
  ,input                         Clk

  //test
`endif FPGA
//test
    ,input                         Clk
    //test
    ,input  [1:0]      DIN, OEN

    //LPF
    ,input                [DW-1:0] DataIn    //(1111);
    ,input                         DataInVld //);
    ,input [1:0][(FW+1)/2-1:0][CW-1:0] Coeff
    ,output               [DW-1:0] DataOut   //456
    ,input                         DataOutVld//123
    //input                         DataInV
);//test here ();
//---------------------------------------------------------------------
//local parameter
localparam DN = 5;
localparam FN = (FW+1)/2;
localparam SL = 7;
//---------------------------------------------------------------------
reg [DW-1:0] data_out;
assign DataOut = data_out;
//---------------------------------------------------------------------
//processing
always @( posedge Clk or negedge Rstn )
begin
    if( ~Rstn )
        data_in <= 'h0;
    else if( Clear )
        data_in <= 'h0;
    else if( DataInVld )
        data_in <= {data_in[FN-2:0],DataIn};
end
//---------------------------------------------------------------------
endmodule



module ifdef_test_3
#(parameter
    // DW = 10,//   ,  ()()
    CW = 10,//    ()()

    `ifdef FPGA

  //test
  NW = 10,       //()()

  //test
`endif
//test

    NW = 10,       //()()
    FW = (DW/2+CW/2)//()()
)//()()
( inout [7:0]  a,//);
 input                           bbbbbbbbbbbbbbbbbbbbbbbb,zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz,//);
 input                          abcd, //);
 input                          abcde, //   );
 input                          abcde, //   ,,);
              output [DW/2-1:0]  c//);
);

  // Design content
endmodule

module ifdef_test_4
#(parameter
    // DW = 10,//   ,  ()()
    CW = 10//    ()()

    `ifdef FPGA

  //test
  ,NW = 10       //()()

  //test

//test

    ,NW = 10       //()()
    ,FW = (DW/2+CW/2)//()()
    `endif
)//()()
( inout [7:0]  a,//);
 input                           bbbbbbbbbbbbbbbbbbbbbbbb,zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz,//);
 input                          abcd, //);
 input                          abcde, //   );
 input                          abcde, //   ,,);
              output [DW/2-1:0]  c//);
);

  // Design content
endmodule




module ifdef_test_5( clk, reset_n,sclk,/*123*/
s_hclk,m_hclk         /*123*/ // AXI Master clock /*123*/
   );

   //=======================  parameters  ======================================
  parameter c_use_self_path  = 1;/*123*/
   parameter c_addr               = 4'b0101;/*123*/
parameter c_jaddr             = 6'b011000;
   input     clk1,clk2;      //
   input     rt_n;//
   `ifdef FPGA
   input     sclk;     //
   input     s_hclk;   //
   `endif
   input     [7:0] m_hclk;   /*123*/
   wire          regs_sample_edge;
   wire          sclk_gated_tmp;

endmodule

module ifdef_test_6(
   // global signals
   clk,            // in system clock
   reset_n,        // in  low active asynchronous reset for system domain
   sclk,           // in sensor pixel clock
   `ifdef FPGA
   s_hclk,         // A Slave clock
   `endif
   m_hclk          // AXI Master clock
   );

   //=======================  parameters  ======================================
  parameter c_use_self_path  = 1;
`ifdef FPGA
   parameter c_addr               = 4'b0101;//666
   //565
   parameter c_jaddr             = 6'b011000;
`endif



   // global signals
   input     clk1,clk2;      //
   `ifdef FPGA
   input     rt_n;//
   `endif
   input     sclk;     //
   input     s_hclk;   //
   input     [7:0] m_hclk;   //AXI Master clock

   wire          regs_sample_edge;
   wire          sclk_gated_tmp;

endmodule

module ifdef_test_7(
   // global signals
   clk            // in system clock
   ,reset_n        // in  low active asynchronous reset for system domain
   ,sclk           // in sensor pixel clock
   `ifdef FPGA
   ,s_hclk         // A Slave clock
   `endif
   ,m_hclk          // AXI Master clock
   );

   //=======================  parameters  ======================================
  parameter c_use_self_path  = 1;
`ifdef FPGA
   parameter c_addr               = 4'b0101;//666
   //565
   parameter c_jaddr             = 6'b011000;
`endif



   // global signals
   input     clk1,clk2;      //
   `ifdef FPGA
   input     rt_n;//
   `endif
   input     sclk;     //
   input     s_hclk;   //
   input     [7:0] m_hclk;   //AXI Master clock
   `endif

   wire          regs_sample_edge;
   wire          sclk_gated_tmp;

endmodule

module ifdef_test_8 (
                 clk
                ,rst_n
                `ifdef FPGA
                ,pwrite
                ,psel
                `endif
                ,penable
                ,paddr
                ,pwdata
                ,prdata
                ,fld_w1_sgl
                ,fld_w1_bus
                `ifdef FPGA
                ,fld_wo1_sgl
                ,fld_wo1_bus
                `endif
                );
input           clk;
input           rst_n;
`ifdef FPGA
input           pwrite;
input           psel;
`endif
input           penable;
input  [31:0]   paddr;
input  [31:0]   pwdata;
output [31:0]   prdata;
output          fld_w1_sgl;
output [2:0]    fld_w1_bus;
`ifdef FPGA
output          fld_wo1_sgl;
output [2:0]    fld_wo1_bus;
`endif
wire            clk;
wire            rst_n;
wire            pwrite;
wire            psel;
wire            penable;
wire [31:0]     paddr;
wire [31:0]     pwdata;
wire [31:0]     TMPLREG4;
wire            tmplreg1_wr;
wire            tmplreg1_rd;
wire            tmplreg2_wr;
wire            tmplreg2_rd;
wire            tmplreg3_wr;
wire            tmplreg3_rd;
wire            tmplreg4_wr;
wire            tmplreg4_rd;
wire            reg_wr;
wire            reg_rd;
assign reg_wr = psel & pwrite & penable;

always@(*) begin
    case(paddr)
        32'h40070030 + 8'h00 : prdata = TMPLREG1  ;
        32'h40070030 + 8'h04 : prdata = TMPLREG2  ;
        32'h40070030 + 8'h08 : prdata = TMPLREG3  ;
        32'h40070030 + 8'h0c : prdata = TMPLREG4  ;
        default:prdata = 32'b0;
    endcase
end
endmodule

module ifdef_test_9( clk, reset_n,sclk,/*123*/
s_hclk,m_hclk         /*123*/ // AXI Master clock /*123*/
   );

   //=======================  parameters  ======================================
`ifdef ASIC
  parameter c_use_self_path  = 1;/*123*/
`else
   parameter c_addr               = 4'b0101;/*123*/
`endif
parameter c_jaddr             = 6'b011000;
   input     clk1,clk2;      //
   input     rt_n;//
`ifdef ASIC
   input     sclk;     //
`else
   input     s_hclk;   //
`endif
   input     [7:0] m_hclk;   /*123*/
   wire          regs_sample_edge;
   wire          sclk_gated_tmp;

endmodule

module vivado #(parameter/*123*/
    MODE = 1,/*123*/
    DW   = 10,//()()
    CW   = 10,//()()
    FW   = (DW/2+CW/2))//123
( inout [7:0]  a,//();
 input                           bbbbbbbbbbbbbbbbbbbbbbbb,zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz,//);
output [(MODE?7:3):0] bbbb,
              output [DW/2-1:0]  c,
              (* mark_debug="true" *)output reg [17:0]  wr_addr,                       // Memory Write Address  
(* mark_debug="true" *)output reg [7:0]   wr_be,                         // Memory Write Byte Enable  
(* mark_debug="true" *)output reg [31:0]  wr_data,                       // Memory Write Data  
(* mark_debug="true" *)output reg         wr_en,                         // Memory Write Enable  
(* mark_debug="true" *)input              wr_busy                        // Memory Write Busy 
              );//);

  // Design content
endmodule


