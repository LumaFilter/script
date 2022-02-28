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
    output               [DW-1:0] DataOut   ,
    input                         DataOutVld
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



module tr1 #(parameter
    DW = 10,//()()
    CW = 10,//()()
    FW = (DW/2+CW/2)//()()
)//()()
( inout [7:0]  a,//);
 input                           bbbbbbbbbbbbbbbbbbbbbbbb,zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz,//);
              output [DW/2-1:0]  c//);
);
 
  // Design content        
endmodule

module tr2 #(parameter
    DW = 10,//()()
    CW = 10,//()()
    FW = (DW/2+CW/2))//123
( inout [7:0]  a,//();
 input                           bbbbbbbbbbbbbbbbbbbbbbbb,zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz,//);
              output [DW/2-1:0]  c);//);

  // Design content        
endmodule




