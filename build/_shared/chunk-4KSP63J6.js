import{c as m,i,j as l,k as c,m as p,p as u}from"/SequentialEGM/build/_shared/chunk-RMYRWJKG.js";var b=m((f,o)=>{i();l();c();u();p();o.exports=r;r.displayName="t4Templating";r.aliases=[];function r(g){(function(s){function n(e,t,a){return{pattern:RegExp("<#"+e+"[\\s\\S]*?#>"),alias:"block",inside:{delimiter:{pattern:RegExp("^<#"+e+"|#>$"),alias:"important"},content:{pattern:/[\s\S]+/,inside:t,alias:a}}}}function d(e){var t=s.languages[e],a="language-"+e;return{block:{pattern:/<#[\s\S]+?#>/,inside:{directive:n("@",{"attr-value":{pattern:/=(?:("|')(?:\\[\s\S]|(?!\1)[^\\])*\1|[^\s'">=]+)/,inside:{punctuation:/^=|^["']|["']$/}},keyword:/\b\w+(?=\s)/,"attr-name":/\b\w+/}),expression:n("=",t,a),"class-feature":n("\\+",t,a),standard:n("",t,a)}}}}s.languages["t4-templating"]=Object.defineProperty({},"createT4",{value:d})})(g)}});export{b as a};
