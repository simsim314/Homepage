import { getCollection, type CollectionEntry } from 'astro:content';
export type Article = CollectionEntry<'articles'>;
export const href = (path = '') =>
  `${import.meta.env.BASE_URL.replace(/\/$/, '')}/${path.replace(/^\//, '')}`;
export const articleHref = (article: Article) => href(`articles/${article.id}/`);
export const previewHref = (article: Article) =>
  href(article.id === 'simkin-glider-gun' ? '#glider-gun' : `#preview-${article.id}`);
export const formatDate = (date: Date) =>
  new Intl.DateTimeFormat('en', { dateStyle: 'medium', timeZone: 'UTC' }).format(date);
export const statusLabels = {
  demonstrated: 'Demonstrated result',
  implemented: 'Implemented',
  experimental: 'Experiment',
  candidate: 'Candidate claim',
  ongoing: 'Work in progress',
};
export async function getContent() {
  const [raw, categories] = await Promise.all([
    getCollection('articles'),
    getCollection('interests'),
  ]);
  const interests = categories.sort((a, b) => a.data.order - b.data.order);
  const ids = new Set(interests.map((i) => i.id));
  const articles = raw
    .filter((a) => !a.data.draft)
    .sort(
      (a, b) =>
        b.data.date.getTime() - a.data.date.getTime() ||
        a.data.presentationOrder - b.data.presentationOrder ||
        a.data.title.localeCompare(b.data.title),
    );
  for (const a of articles) {
    if (new Set(a.data.topics).size !== a.data.topics.length)
      throw new Error(`Duplicate topics in ${a.id}`);
    for (const topic of a.data.topics)
      if (!ids.has(topic)) throw new Error(`Unknown interest '${topic}' in ${a.id}`);
    if (a.data.updated && a.data.updated < a.data.date)
      throw new Error(`Update precedes publication in ${a.id}`);
  }
  return { articles, interests };
}
export function relatedArticles(article: Article, all: Article[]) {
  return all
    .filter((a) => a.id !== article.id)
    .map((a) => ({
      article: a,
      score:
        a.data.topics.filter((t) => article.data.topics.includes(t)).length * 3 +
        a.data.tags.filter((t) => article.data.tags.includes(t)).length,
    }))
    .filter((a) => a.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, 3)
    .map((a) => a.article);
}
