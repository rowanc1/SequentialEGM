import{c as p,i as d,j as g,k as _,m as u,p as m}from"/SequentialEGM/build/_shared/chunk-RMYRWJKG.js";var v=p((f,D)=>{d();g();_();m();u();var n="[0-9](_*[0-9])*",s=`\\.(${n})`,r="[0-9a-fA-F](_*[0-9a-fA-F])*",C={className:"number",variants:[{begin:`(\\b(${n})((${s})|\\.)?|(${s}))[eE][+-]?(${n})[fFdD]?\\b`},{begin:`\\b(${n})((${s})[fFdD]?\\b|\\.([fFdD]\\b)?)`},{begin:`(${s})[fFdD]?\\b`},{begin:`\\b(${n})[fFdD]\\b`},{begin:`\\b0[xX]((${r})\\.?|(${r})?\\.(${r}))[pP][+-]?(${n})[fFdD]?\\b`},{begin:"\\b(0|[1-9](_*[0-9])*)[lL]?\\b"},{begin:`\\b0[xX](${r})[lL]?\\b`},{begin:"\\b0(_*[0-7])*[lL]?\\b"},{begin:"\\b0[bB][01](_*[01])*[lL]?\\b"}],relevance:0};function M(e){let c={keyword:"abstract as val var vararg get set class object open private protected public noinline crossinline dynamic final enum if else do while for when throw try catch finally import package is in fun override companion reified inline lateinit init interface annotation data sealed internal infix operator out by constructor super tailrec where const inner suspend typealias external expect actual",built_in:"Byte Short Char Int Long Boolean Float Double Void Unit Nothing",literal:"true false null"},O={className:"keyword",begin:/\b(break|continue|return|this)\b/,starts:{contains:[{className:"symbol",begin:/@\w+/}]}},R={className:"symbol",begin:e.UNDERSCORE_IDENT_RE+"@"},o={className:"subst",begin:/\$\{/,end:/\}/,contains:[e.C_NUMBER_MODE]},b={className:"variable",begin:"\\$"+e.UNDERSCORE_IDENT_RE},a={className:"string",variants:[{begin:'"""',end:'"""(?=[^"])',contains:[b,o]},{begin:"'",end:"'",illegal:/\n/,contains:[e.BACKSLASH_ESCAPE]},{begin:'"',end:'"',illegal:/\n/,contains:[e.BACKSLASH_ESCAPE,b,o]}]};o.contains.push(a);let E={className:"meta",begin:"@(?:file|property|field|get|set|receiver|param|setparam|delegate)\\s*:(?:\\s*"+e.UNDERSCORE_IDENT_RE+")?"},l={className:"meta",begin:"@"+e.UNDERSCORE_IDENT_RE,contains:[{begin:/\(/,end:/\)/,contains:[e.inherit(a,{className:"meta-string"})]}]},T=C,t=e.COMMENT("/\\*","\\*/",{contains:[e.C_BLOCK_COMMENT_MODE]}),i={variants:[{className:"type",begin:e.UNDERSCORE_IDENT_RE},{begin:/\(/,end:/\)/,contains:[]}]},N=i;return N.variants[1].contains=[i],i.variants[1].contains=[N],{name:"Kotlin",aliases:["kt","kts"],keywords:c,contains:[e.COMMENT("/\\*\\*","\\*/",{relevance:0,contains:[{className:"doctag",begin:"@[A-Za-z]+"}]}),e.C_LINE_COMMENT_MODE,t,O,R,E,l,{className:"function",beginKeywords:"fun",end:"[(]|$",returnBegin:!0,excludeEnd:!0,keywords:c,relevance:5,contains:[{begin:e.UNDERSCORE_IDENT_RE+"\\s*\\(",returnBegin:!0,relevance:0,contains:[e.UNDERSCORE_TITLE_MODE]},{className:"type",begin:/</,end:/>/,keywords:"reified",relevance:0},{className:"params",begin:/\(/,end:/\)/,endsParent:!0,keywords:c,relevance:0,contains:[{begin:/:/,end:/[=,\/]/,endsWithParent:!0,contains:[i,e.C_LINE_COMMENT_MODE,t],relevance:0},e.C_LINE_COMMENT_MODE,t,E,l,a,e.C_NUMBER_MODE]},t]},{className:"class",beginKeywords:"class interface trait",end:/[:\{(]|$/,excludeEnd:!0,illegal:"extends implements",contains:[{beginKeywords:"public protected internal private constructor"},e.UNDERSCORE_TITLE_MODE,{className:"type",begin:/</,end:/>/,excludeBegin:!0,excludeEnd:!0,relevance:0},{className:"type",begin:/[,:]\s*/,end:/[<\(,]|$/,excludeBegin:!0,returnEnd:!0},E,l]},a,{className:"meta",begin:"^#!/usr/bin/env",end:"$",illegal:`
`},T]}}D.exports=M});export default v();
