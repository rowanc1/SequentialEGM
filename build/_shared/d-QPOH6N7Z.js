import{c as R,i as r,j as i,k as o,m as l,p as d}from"/SequentialEGM/build/_shared/chunk-RMYRWJKG.js";var y=R((x,E)=>{r();i();o();d();l();function w(e){let u={$pattern:e.UNDERSCORE_IDENT_RE,keyword:"abstract alias align asm assert auto body break byte case cast catch class const continue debug default delete deprecated do else enum export extern final finally for foreach foreach_reverse|10 goto if immutable import in inout int interface invariant is lazy macro mixin module new nothrow out override package pragma private protected public pure ref return scope shared static struct super switch synchronized template this throw try typedef typeid typeof union unittest version void volatile while with __FILE__ __LINE__ __gshared|10 __thread __traits __DATE__ __EOF__ __TIME__ __TIMESTAMP__ __VENDOR__ __VERSION__",built_in:"bool cdouble cent cfloat char creal dchar delegate double dstring float function idouble ifloat ireal long real short string ubyte ucent uint ulong ushort wchar wstring",literal:"false null true"},_="(0|[1-9][\\d_]*)",n="(0|[1-9][\\d_]*|\\d[\\d_]*|[\\d_]+?\\d)",g="0[bB][01_]+",t="([\\da-fA-F][\\da-fA-F_]*|_[\\da-fA-F][\\da-fA-F_]*)",D="0[xX]"+t,a="([eE][+-]?"+n+")",N="("+n+"(\\.\\d*|"+a+")|\\d+\\."+n+"|\\."+_+a+"?)",f="(0[xX]("+t+"\\."+t+"|\\.?"+t+")[pP][+-]?"+n+")",s="("+_+"|"+g+"|"+D+")",m="("+f+"|"+N+")",c=`\\\\(['"\\?\\\\abfnrtv]|u[\\dA-Fa-f]{4}|[0-7]{1,3}|x[\\dA-Fa-f]{2}|U[\\dA-Fa-f]{8})|&[a-zA-Z\\d]{2,};`,b={className:"number",begin:"\\b"+s+"(L|u|U|Lu|LU|uL|UL)?",relevance:0},O={className:"number",begin:"\\b("+m+"([fF]|L|i|[fF]i|Li)?|"+s+"(i|[fF]i|Li))",relevance:0},M={className:"string",begin:"'("+c+"|.)",end:"'",illegal:"."},T={className:"string",begin:'"',contains:[{begin:c,relevance:0}],end:'"[cwd]?'},A={className:"string",begin:'[rq]"',end:'"[cwd]?',relevance:5},p={className:"string",begin:"`",end:"`[cwd]?"},I={className:"string",begin:'x"[\\da-fA-F\\s\\n\\r]*"[cwd]?',relevance:10},S={className:"string",begin:'q"\\{',end:'\\}"'},h={className:"meta",begin:"^#!",end:"$",relevance:5},v={className:"meta",begin:"#(line)",end:"$",relevance:5},C={className:"keyword",begin:"@[a-zA-Z_][a-zA-Z_\\d]*"},L=e.COMMENT("\\/\\+","\\+\\/",{contains:["self"],relevance:10});return{name:"D",keywords:u,contains:[e.C_LINE_COMMENT_MODE,e.C_BLOCK_COMMENT_MODE,L,I,T,A,p,S,O,b,M,h,v,C]}}E.exports=w});export default y();
