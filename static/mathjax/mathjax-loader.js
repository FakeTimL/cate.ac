// Use this loader in order to ensure execution order
window.MathJax = {
	loader: {
		load: ['input/asciimath']
	},
	tex: {
		inlineMath: [['$', '$'], ['\\(', '\\)']],
		macros: {
			arc: ["{\\stackrel{\\Large\\frown}{#1}}", 1]
		}
	},
	asciimath: {
		delimiters: [['`', '`']]
	},
	svg: {
		fontCache: 'global'
	},
};

(function () {
	var script = document.createElement('script');
	script.src = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js';
	// script.async = true;
	document.getElementById('__head__').appendChild(script);
})();
