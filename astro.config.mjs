import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import { unified } from '@astrojs/markdown-remark';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import basePaths from './scripts/remark-base-paths.mjs';

const plugins = { remarkPlugins: [remarkMath, basePaths], rehypePlugins: [rehypeKatex] };
export default defineConfig({
  site: 'https://simsim314.github.io',
  base: '/Homepage',
  trailingSlash: 'always',
  output: 'static',
  integrations: [mdx()],
  markdown: { processor: unified(plugins) },
});
