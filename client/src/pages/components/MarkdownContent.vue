<script lang="ts">
import MarkdownIt from 'markdown-it';
import katex from '@traptitech/markdown-it-katex';
import hljs, { type HLJSApi } from 'highlight.js';
import 'katex/dist/katex.min.css';
import 'highlight.js/styles/github.css';

function hljsLean(hljs: HLJSApi) {
  /*
  Language: Lean
  Author: Patrick Massot
  Category: scientific
  Description: Language definition for Lean theorem prover
  */
  const LEAN_KEYWORDS = {
    keyword:
      'theorem|10 lemma|10 definition def class structure instance ' +
      'example inductive coinductive ' +
      'axiom axioms hypothesis constant constants ' +
      'universe universes variable variables parameter parameters ' +
      'begin end ' +
      'import open theory prelude renaming hiding exposing ' +
      'calc match do by let in extends ' +
      'fun assume ' +
      '#check #eval #reduce #print',
    built_in:
      'Type Prop|10 Sort rw|10 rewrite rwa erw subst substs ' +
      'simp dsimp simpa simp_intros finish ' +
      'unfold unfold1 dunfold unfold_projs unfold_coes ' +
      'delta cc ac_reflexivity ac_refl ' +
      'existsi|10 cases rcases with intro intros introv by_cases ' +
      'refl rfl funext propext exact exacts ' +
      'refine apply eapply fapply apply_with apply_instance ' +
      'induction rename assumption revert generalize specialize clear ' +
      'contradiction by_contradiction by_contra trivial exfalso ' +
      'symmetry transitivity destruct constructor econstructor ' +
      'left right split injection injections ' +
      'repeat try continue skip swap solve1 abstract all_goals any_goals done ' +
      'fail_if_success success_if_fail guard_target guard_hyp ' +
      'have replace at suffices show from ' +
      'congr congr_n congr_arg norm_num ring ',
    literal: 'tt ff',
    meta: 'noncomputable|10 private protected meta mutual',
    section: 'section namespace end',
    strong: 'sorry admit',
  };
  const LEAN_IDENT_RE = /[A-Za-z_][\\w\u207F-\u209C\u1D62-\u1D6A\u2079']*/;
  const DASH_COMMENT = hljs.COMMENT('--', '$');
  const MULTI_LINE_COMMENT = hljs.COMMENT('/-[^-]', '-/');
  const DOC_COMMENT = {
    className: 'doctag',
    begin: '/-[-!]',
    end: '-/',
  };
  const ATTRIBUTE_DECORATOR = {
    className: 'meta',
    begin: '@\\[',
    end: '\\]',
  };
  const ATTRIBUTE_LINE = {
    className: 'meta',
    begin: '^attribute',
    end: '$',
  };
  const LEAN_DEFINITION = {
    className: 'theorem',
    beginKeywords: 'def theorem lemma class instance structure',
    end: ':=',
    excludeEnd: true,
    contains: [
      {
        className: 'keyword',
        begin: /extends/,
      },
      hljs.inherit(hljs.TITLE_MODE, {
        begin: LEAN_IDENT_RE,
      }),
      {
        className: 'params',
        begin: /[([{]/,
        end: /[)\]}]/,
        endsParent: false,
        keywords: LEAN_KEYWORDS,
      },
      {
        className: 'symbol',
        begin: /:/,
        endsParent: true,
      },
    ],
    keywords: LEAN_KEYWORDS,
  };
  return {
    keywords: LEAN_KEYWORDS,
    contains: [
      hljs.QUOTE_STRING_MODE,
      hljs.NUMBER_MODE,
      DASH_COMMENT,
      MULTI_LINE_COMMENT,
      DOC_COMMENT,
      LEAN_DEFINITION,
      ATTRIBUTE_DECORATOR,
      ATTRIBUTE_LINE,
      { begin: /⟨/ },
    ],
  };
}

// Register once on import.
hljs.registerLanguage('lean', hljsLean);

// See: https://github.com/markdown-it/markdown-it
// See: https://github.com/waylonflinn/markdown-it-katex

export default {
  props: {
    markdown: { type: String, required: true },
    display: { type: Boolean, default: false },
  },
  data() {
    return { converted: '' };
  },
  created() {
    const big = this.display;
    const md = new MarkdownIt({
      html: true,
      highlight(str, lang) {
        if (lang && hljs.getLanguage(lang)) {
          try {
            const inner = hljs.highlight(str, { language: lang }).value;
            return `<pre class="${big ? '' : 'tight'}"><code class="${big ? 'hljs' : ''}">${inner}</code></pre>`;
          } catch (_) {
            return '';
          }
        } else {
          return '';
        }
      },
    });
    md.use(katex, { errorColor: '#9f3a38' });
    this.converted = md.render(this.markdown);
  },
};

/*
function addStyling(el: HTMLElement, selector: string, classes: string) {
  const elems = el.querySelectorAll(selector);
  for (let i = 0; i < elems.length; i++) {
    elems[i].className += ' ' + classes;
  }
}

function render(el: HTMLElement) {
  // Add styling classes to markdown content.
  addStyling(el, 'h1', 'ui header');
  addStyling(el, 'h2', 'ui header');
  addStyling(el, 'h3', 'ui header');
  addStyling(el, 'h4', 'ui header');
  addStyling(el, 'h5', 'ui header');
  addStyling(el, 'h6', 'ui header');
  addStyling(el, 'ul', 'ui bulleted list');
  addStyling(el, 'ul li', 'item');
  addStyling(el, 'ol', 'ui list');
  addStyling(el, 'ol li', 'item');
  addStyling(el, 'table', 'ui celled table');
  addStyling(el, 'img', 'ui centered medium rounded image');
  addStyling(el, 'hr', 'ui divider');
}
*/
</script>

<template>
  <div v-html="converted"></div>
</template>

<style scoped>
:deep(pre.tight) {
  margin: 0;
  white-space: pre-wrap;
}
</style>
