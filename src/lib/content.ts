import { getCollection, type CollectionEntry } from 'astro:content';
export type Article = CollectionEntry<'articles'>;
export const href = (path = '') =>
  `${import.meta.env.BASE_URL.replace(/\/$/, '')}/${path.replace(/^\//, '')}`;
export const articleHref = (article: Article) => href(`articles/${article.id}/`);
export const previewHref = (article: Article) =>
  article.id === 'simkin-glider-gun' ? `${articleHref(article)}#glider-gun` : articleHref(article);
export const formatDate = (date: Date) =>
  new Intl.DateTimeFormat('en', { dateStyle: 'medium', timeZone: 'UTC' }).format(date);
export const statusLabels = {
  demonstrated: 'Demonstrated result',
  implemented: 'Implemented',
  experimental: 'Experiment',
  candidate: 'Candidate claim',
  ongoing: 'Work in progress',
  preprint: 'Research preprint',
  note: 'Research note',
};
export async function getContent() {
  const [raw, categories] = await Promise.all([
    getCollection('articles'),
    getCollection('interests'),
  ]);
  const interests = categories.sort((a, b) => a.data.order - b.data.order);
  const ids = new Set(interests.map((i) => i.id));
  const ancestors = new Map<string, string[]>();
  for (const interest of interests) {
    const chain: string[] = [];
    let parent = interest.data.parent;
    while (parent) {
      if (!ids.has(parent)) throw new Error(`Unknown parent '${parent}' in ${interest.id}`);
      if (parent === interest.id || chain.includes(parent))
        throw new Error(`Interest hierarchy cycle in ${interest.id}`);
      chain.push(parent);
      parent = interests.find((i) => i.id === parent)!.data.parent;
    }
    ancestors.set(interest.id, chain);
  }
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
  if (articles.filter((a) => a.data.homepageHero).length > 1)
    throw new Error('Only one article can be the homepage hero.');
  const connectedArticles = articles.map((article) => ({
    ...article,
    data: {
      ...article.data,
      topics: [
        ...new Set(article.data.topics.flatMap((topic) => [topic, ...ancestors.get(topic)!])),
      ],
    },
  }));
  for (const interest of interests) {
    if (new Set(interest.data.articleOrder).size !== interest.data.articleOrder.length)
      throw new Error(`Duplicate article in reading order for ${interest.id}`);
    for (const id of interest.data.articleOrder) {
      const article = connectedArticles.find((a) => a.id === id);
      if (!article?.data.topics.includes(interest.id))
        throw new Error(`Reading order for ${interest.id} includes unrelated article: ${id}`);
    }
    if (!interest.data.representative) continue;
    const representative = connectedArticles.find(
      (article) => article.id === interest.data.representative,
    );
    if (!representative?.data.showPreview || !representative.data.topics.includes(interest.id))
      throw new Error(
        `Interest ${interest.id} must feature an illustrated article from its own topic.`,
      );
  }
  return { articles: connectedArticles, interests };
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
