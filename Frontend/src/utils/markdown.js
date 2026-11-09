import DOMPurify from "dompurify";
// webpack 4 cannot parse markdown-it's modern ESM dependency graph;
// the package's official browser UMD build is self-contained.
import MarkdownIt from "markdown-it/dist/browser/markdown-it.umd.min.js";

const markdown = new MarkdownIt({
  html: true,
  breaks: true,
  linkify: true,
  typographer: false
});

export function renderMarkdown (source) {
  return DOMPurify.sanitize(markdown.render(source || ""));
}
