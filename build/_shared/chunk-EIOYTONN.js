import{c as v,i as u,j as d,k as c,m,p as f}from"/SequentialEGM/build/_shared/chunk-RMYRWJKG.js";var w=v((k,g)=>{u();d();c();f();m();g.exports=p;p.displayName="naniscript";p.aliases=[];function p(h){(function(r){var i=/\{[^\r\n\[\]{}]*\}/,l={"quoted-string":{pattern:/"(?:[^"\\]|\\.)*"/,alias:"operator"},"command-param-id":{pattern:/(\s)\w+:/,lookbehind:!0,alias:"property"},"command-param-value":[{pattern:i,alias:"selector"},{pattern:/([\t ])\S+/,lookbehind:!0,greedy:!0,alias:"operator"},{pattern:/\S(?:.*\S)?/,alias:"operator"}]};r.languages.naniscript={comment:{pattern:/^([\t ]*);.*/m,lookbehind:!0},define:{pattern:/^>.+/m,alias:"tag",inside:{value:{pattern:/(^>\w+[\t ]+)(?!\s)[^{}\r\n]+/,lookbehind:!0,alias:"operator"},key:{pattern:/(^>)\w+/,lookbehind:!0}}},label:{pattern:/^([\t ]*)#[\t ]*\w+[\t ]*$/m,lookbehind:!0,alias:"regex"},command:{pattern:/^([\t ]*)@\w+(?=[\t ]|$).*/m,lookbehind:!0,alias:"function",inside:{"command-name":/^@\w+/,expression:{pattern:i,greedy:!0,alias:"selector"},"command-params":{pattern:/\s*\S[\s\S]*/,inside:l}}},"generic-text":{pattern:/(^[ \t]*)[^#@>;\s].*/m,lookbehind:!0,alias:"punctuation",inside:{"escaped-char":/\\[{}\[\]"]/,expression:{pattern:i,greedy:!0,alias:"selector"},"inline-command":{pattern:/\[[\t ]*\w[^\r\n\[\]]*\]/,greedy:!0,alias:"function",inside:{"command-params":{pattern:/(^\[[\t ]*\w+\b)[\s\S]+(?=\]$)/,lookbehind:!0,inside:l},"command-param-name":{pattern:/^(\[[\t ]*)\w+/,lookbehind:!0,alias:"name"},"start-stop-char":/[\[\]]/}}}}},r.languages.nani=r.languages.naniscript,r.hooks.add("after-tokenize",function(e){var o=e.tokens;o.forEach(function(a){if(typeof a!="string"&&a.type==="generic-text"){var t=s(a);y(t)||(a.type="bad-line",a.content=t)}})});function y(e){for(var o="[]{}",a=[],t=0;t<e.length;t++){var b=e[t],n=o.indexOf(b);if(n!==-1){if(n%2===0)a.push(n+1);else if(a.pop()!==n)return!1}}return a.length===0}function s(e){return typeof e=="string"?e:Array.isArray(e)?e.map(s).join(""):s(e.content)}})(h)}});export{w as a};
