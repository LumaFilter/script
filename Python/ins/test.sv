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

module test11( clk, reset_n,sclk,/*123*/
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

